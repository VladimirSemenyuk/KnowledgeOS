#!/usr/bin/env python3
"""Выгрузка медиа недели в Cloudflare R2: Buffer принимает картинки и видео только по публичной ссылке.

Запуск из корня KnowledgeOS через окружение `.venv`:

    R=Posts/render
    $R/.venv/bin/python $R/upload.py Posts/weeks/2026-11-30-week-2/instagram/img/r-kurs-cover.png
    $R/.venv/bin/python $R/upload.py Posts/weeks/2026-11-30-week-2          # вся папка недели
    $R/.venv/bin/python $R/upload.py ~/Movies/reels-1-final.mp4 --week 2026-11-30-week-2

Ключ в бакете повторяет путь от `Posts/weeks/`: `2026-11-30-week-2/instagram/img/r-kurs-cover.png`.
Файл вне `Posts/weeks/` (готовый Reels из ~/Movies) требует `--week`, ключ — `<week>/<имя файла>`.
Для каждого файла печатается публичная ссылка — её и передают в Buffer.
Файл с тем же размером в бакете уже есть — не перезаливается.

Из папки берутся только медиа (png, jpg, mp4, mov, pdf, gif); служебные файлы
(`frames/`, `_*.png`, `.qrcheck.png`) пропускаются.

Настройки — в `Posts/render/.env.r2` (в git не попадает), образец — `.env.r2.example`.
"""
import argparse
import mimetypes
import os
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", module="boto3")  # окружение на Python 3.9: предупреждение об устаревании
import boto3
from botocore.exceptions import ClientError

HERE = Path(__file__).resolve().parent
WEEKS = HERE.parent / "weeks"
ENV_FILE = HERE / ".env.r2"
MEDIA = {".png", ".jpg", ".jpeg", ".gif", ".mp4", ".mov", ".pdf"}
SKIP_DIRS = {"frames"}
REQUIRED = ["R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_BUCKET", "R2_PUBLIC_URL"]


def load_env():
    if not ENV_FILE.exists():
        sys.exit(f"Нет {ENV_FILE}: скопируйте .env.r2.example и заполните.")
    env = {}
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"')
    missing = [k for k in REQUIRED if not env.get(k)]
    if missing:
        sys.exit(f"В {ENV_FILE.name} не заполнено: {', '.join(missing)}")
    return env


def is_media(p: Path) -> bool:
    return (
        p.suffix.lower() in MEDIA
        and not p.name.startswith(("_", "."))
        and not SKIP_DIRS & set(p.parts)
    )


def collect(paths):
    files = []
    for raw in paths:
        p = Path(raw).expanduser().resolve()
        if p.is_dir():
            files += sorted(f for f in p.rglob("*") if f.is_file() and is_media(f))
        elif p.is_file():
            files.append(p)
        else:
            sys.exit(f"Не найден: {raw}")
    return files


def key_for(p: Path, week) -> str:
    try:
        return p.relative_to(WEEKS).as_posix()
    except ValueError:
        if not week:
            sys.exit(f"{p} вне Posts/weeks/ — укажите --week <папка недели>")
        return f"{week}/{p.name}"


def main():
    ap = argparse.ArgumentParser(description="Выгрузить медиа в R2 и напечатать публичные ссылки")
    ap.add_argument("paths", nargs="+", help="файлы или папки")
    ap.add_argument("--week", help="папка недели для файлов вне Posts/weeks/, например 2026-11-30-week-2")
    ap.add_argument("--force", action="store_true", help="перезалить, даже если файл уже есть")
    args = ap.parse_args()

    env = load_env()
    s3 = boto3.client(
        "s3",
        endpoint_url=f"https://{env['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=env["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=env["R2_SECRET_ACCESS_KEY"],
        region_name="auto",
    )
    bucket, base = env["R2_BUCKET"], env["R2_PUBLIC_URL"].rstrip("/")

    files = collect(args.paths)
    if not files:
        sys.exit("Медиафайлов не найдено.")

    for f in files:
        key = key_for(f, args.week)
        size = f.stat().st_size
        url = f"{base}/{key}"
        if not args.force:
            try:
                if s3.head_object(Bucket=bucket, Key=key)["ContentLength"] == size:
                    print(f"есть     {url}")
                    continue
            except ClientError as e:
                if e.response["Error"]["Code"] not in ("404", "NoSuchKey", "NotFound"):
                    raise
        ctype = mimetypes.guess_type(f.name)[0] or "application/octet-stream"
        s3.upload_file(str(f), bucket, key, ExtraArgs={"ContentType": ctype})
        print(f"залито   {url}  ({size / 1e6:.1f} МБ)")


if __name__ == "__main__":
    main()
