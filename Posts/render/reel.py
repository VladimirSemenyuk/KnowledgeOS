#!/usr/bin/env python3
"""Монтаж Reels: вырезать паузы, выровнять звук, вжечь субтитры по визуальной системе.

Два шага, запуск из корня KnowledgeOS через окружение `.venv` (установка — в `reels.md`):

    R=Posts/render
    $R/.venv/bin/python $R/reel.py prep   ~/Movies/take.mov
    $R/.venv/bin/python $R/reel.py render ~/Movies/take.mov ~/Movies/reels-2-final.mp4

`prep` распознаёт речь и кладёт рабочие файлы в папку `take.reel/` рядом с видео:
    words.json   — слова с таймкодами (распознавание, не править);
    speech.json  — участки речи по громкости, по ним режутся паузы;
    captions.txt — субтитры, их правят перед `render`.

Формат captions.txt — одна строка на экран:
    12 | В 2017 году
Число — номер первого слова этого экрана в words.json: по нему берётся время показа.
Экран длится до начала следующего. Текст справа свободный: исправить ошибку
распознавания, разбить или склеить экраны, убрать точку. Слово в *звёздочках* —
красное, одно-два на ролик. Строки с # игнорируются.

Настройки `render`:
    --pre 0.16 --post 0.26  запас до и после фразы на склейке, секунды;
    --tail 0.45             хвост после последней фразы;
    --keep 59.5-82.5,91.8-110.6  взять только эти участки исходника, секунды —
                            когда в записи несколько дублей. Слова нужного дубля,
                            которых нет в words.json, дописываются в его конец;
    --grade "..."           цветокоррекция, фильтры ffmpeg. По умолчанию — GRADE:
                            снять голубую дымку с чёрного, чуть контраста и резкости.
                            "none" — без коррекции.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "fonts", "Onest.ttf")
DARK, LIGHT, RED = (0x16, 0x18, 0x1A, 235), (0xF3, 0xF4, 0xF1, 255), (0xD2, 0x30, 0x2C, 255)
FONT_SIZE, MAX_TEXT_W, CAPTION_Y = 76, 900, 1270
# Камера iPhone/Continuity в комнатном свете: чёрное приподнято и уходит в синий, картинка мыльная.
GRADE = "colorlevels=gimin=0.03:bimin=0.075,eq=contrast=1.05,unsharp=5:5:0.7:5:5:0"
SHORT = {"в", "на", "у", "а", "и", "что", "до", "от", "без", "про", "с", "я", "это", "где", "мою", "свою"}


def ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def run(cmd):
    subprocess.run([ffmpeg(), "-hide_banner", "-loglevel", "error", "-y", *cmd], check=True)


def workdir(video, given):
    d = given or os.path.splitext(video)[0] + ".reel"
    os.makedirs(d, exist_ok=True)
    return d


# ---------- prep

def speech_regions(wav):
    w = wave.open(wav)
    a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
    hop = w.getframerate() // 100
    n = len(a) // hop
    db = 20 * np.log10(np.sqrt((a[: n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    floor = np.percentile(db[db > -150], 20)  # петличка глушит тишину в ноль — её не считаем
    thr = floor + 0.30 * (np.percentile(db, 95) - floor)
    regs, i = [], 0
    while i < n:
        if db[i] > thr:
            j = i
            while j < n and db[j] > thr:
                j += 1
            if regs and i * 0.01 - regs[-1][1] < 0.3:
                regs[-1][1] = j * 0.01
            else:
                regs.append([i * 0.01, j * 0.01])
            i = j
        else:
            i += 1
    return [r for r in regs if r[1] - r[0] > 0.08]


def auto_captions(words):
    """Черновая разбивка: 2–4 слова, разрыв на знаках препинания, без висячих предлогов."""
    caps, cur = [], []
    length = lambda ws: sum(len(w["w"].strip()) + 1 for _, w in ws)
    for i, w in enumerate(words):
        if cur and (len(cur) >= 4 or length(cur) + len(w["w"].strip()) > 20):
            carry = []
            while len(cur) > 1 and cur[-1][1]["w"].strip().lower() in SHORT:
                carry.insert(0, cur.pop())
            caps.append(cur)
            cur = carry
        cur.append((i, w))
        if w["w"].strip()[-1:] in ".,?!":
            caps.append(cur)
            cur = []
    if cur:
        caps.append(cur)
    lines = []
    for c in caps:
        text = " ".join(w["w"].strip() for _, w in c).rstrip(".,")
        lines.append(f"{c[0][0]} | {text}")
    return lines


def prep(a):
    d = workdir(a.video, a.work)
    wav = os.path.join(d, "audio.wav")
    run(["-i", a.video, "-vn", "-ac", "1", "-ar", "16000", wav])
    json.dump(speech_regions(wav), open(os.path.join(d, "speech.json"), "w"))
    from faster_whisper import WhisperModel
    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    segs, _ = model.transcribe(wav, language="ru", word_timestamps=True, beam_size=5)
    words = []
    for s in segs:
        print(f"[{s.start:6.2f}] {s.text.strip()}")
        words += [{"w": w.word, "s": round(w.start, 3), "e": round(w.end, 3)} for w in s.words]
    json.dump(words, open(os.path.join(d, "words.json"), "w"), ensure_ascii=False, indent=0)
    cap = os.path.join(d, "captions.txt")
    if os.path.exists(cap) and not a.force:
        print(f"{cap} уже есть — не перезаписываю (--force, чтобы перезаписать)")
    else:
        head = "# номер первого слова | текст экрана. *слово* — красным. Правьте текст и разбивку.\n"
        open(cap, "w").write(head + "\n".join(auto_captions(words)) + "\n")
    print(f"\nГотово: {d}\nПроверьте captions.txt и запустите render.")


# ---------- render

def keep_segments(speech, pre, post, tail):
    segs = []
    for s, e in speech:
        s, e = max(0, s - pre), e + post
        if segs and s - segs[-1][1] < 0.22:
            segs[-1][1] = max(segs[-1][1], e)
        else:
            segs.append([s, e])
    segs[-1][1] += tail
    return segs


def remap(t, segs):
    off = 0
    for s, e in segs:
        if t < s:
            return off
        if t <= e:
            return off + t - s
        off += e - s
    return off


def black_bars(video):
    """Чёрные полосы сверху и снизу кадра (бывают у записей с iPhone) — сколько строк срезать."""
    raw = subprocess.run([ffmpeg(), "-v", "error", "-ss", "1", "-i", video, "-frames:v", "1",
                          "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
    probe = subprocess.run([ffmpeg(), "-hide_banner", "-i", video], capture_output=True, text=True).stderr
    w, h = map(int, re.search(r"Video:.*?(\d{3,5})x(\d{3,5})", probe).groups())
    rows = np.frombuffer(raw, np.uint8)[: w * h].reshape(h, w).mean(1)
    top = next(i for i in range(h) if rows[i] > 8)
    bot = next(i for i in range(h) if rows[h - 1 - i] > 8)
    return w, h, top, bot


def caption_png(text, path):
    font = ImageFont.truetype(FONT, FONT_SIZE)
    font.set_variation_by_axes([700])
    parts = re.split(r"(\*[^*]+\*)", text)
    plain = "".join(p.strip("*") for p in parts)
    if font.getlength(plain) > MAX_TEXT_W:  # длинный экран — уменьшаем шрифт, а не вылезаем за край
        font = ImageFont.truetype(FONT, int(FONT_SIZE * MAX_TEXT_W / font.getlength(plain)))
        font.set_variation_by_axes([700])
        print(f"  мелкий шрифт: «{plain}» — лучше разбить экран")
    asc, desc = font.getmetrics()
    px, py = 30, 18
    im = Image.new("RGBA", (int(font.getlength(plain) + 2 * px), asc + desc + 2 * py - 6), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=16, fill=DARK)
    x = px
    for p in parts:
        if not p:
            continue
        red = p.startswith("*") and p.endswith("*")
        p = p.strip("*")
        d.text((x, py - 4), p, font=font, fill=RED if red else LIGHT)
        x += font.getlength(p)
    im.save(path)


def render(a):
    d = workdir(a.video, a.work)
    words = json.load(open(os.path.join(d, "words.json")))
    speech = json.load(open(os.path.join(d, "speech.json")))
    if a.keep:
        ranges = [tuple(map(float, r.split("-"))) for r in a.keep.split(",")]
        speech = [[max(s, lo), min(e, hi)] for s, e in speech for lo, hi in ranges if s < hi and e > lo]
    segs = keep_segments(speech, a.pre, a.post, a.tail)
    total = sum(e - s for s, e in segs)
    caps = []
    for line in open(os.path.join(d, "captions.txt")):
        if line.strip() and not line.startswith("#"):
            i, text = line.split("|", 1)
            caps.append([int(i), text.strip()])
    caps.sort()
    pngdir = os.path.join(d, "png")
    os.makedirs(pngdir, exist_ok=True)
    items = []
    for k, (i, text) in enumerate(caps):
        st = max(0, remap(words[i]["s"], segs) - 0.05)
        if k + 1 < len(caps):
            nxt = max(0, remap(words[caps[k + 1][0]]["s"], segs) - 0.05)
            last = words[caps[k + 1][0] - 1]["e"]
            en = nxt if nxt - remap(last, segs) < 0.8 else remap(last, segs) + 0.25
        else:
            en = total
        path = os.path.join(pngdir, f"c{k:03d}.png")
        caption_png(text, path)
        items.append((st, en, path, text))
    print(f"Склеек: {len(segs)}, длительность {total:.1f} с, экранов субтитров: {len(items)}")

    fc, n = [], len(segs)
    for i, (s, e) in enumerate(segs):
        fc.append(f"[0:v]trim={s:.3f}:{e:.3f},setpts=PTS-STARTPTS[v{i}]")
        fc.append(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,"
                  f"afade=t=in:d=0.015,afade=t=out:st={e - s - 0.03:.3f}:d=0.03[a{i}]")
    fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac]")
    w, h, top, bot = black_bars(a.video)
    if top or bot:
        print(f"Чёрные полосы: сверху {top} px, снизу {bot} px — срезаю")
    fc.append(f"[vc]crop={w}:{h - top - bot}:0:{top},"
              "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,fps=30,"
              + ("" if a.grade == "none" else a.grade + ",") + "format=yuv420p[b0]")
    last = "b0"
    for k, (st, en, _, _) in enumerate(items):
        fc.append(f"[{last}][{k + 1}:v]overlay=x=(W-w)/2:y={CAPTION_Y}:enable='gte(t,{st:.3f})*lt(t,{en:.3f})'[b{k + 1}]")
        last = f"b{k + 1}"
    fc.append("[ac]highpass=f=80,loudnorm=I=-12:TP=-1.5:LRA=11,aresample=48000[ao]")
    cmd = ["-i", a.video]
    for it in items:
        cmd += ["-i", it[2]]
    cmd += ["-filter_complex", ";".join(fc), "-map", f"[{last}]", "-map", "[ao]",
            "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p",
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", a.out]
    run(cmd)
    print(f"Готово: {a.out}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    pp = sub.add_parser("prep")
    pp.add_argument("video")
    pp.add_argument("--work")
    pp.add_argument("--model", default="medium")
    pp.add_argument("--force", action="store_true")
    pr = sub.add_parser("render")
    pr.add_argument("video")
    pr.add_argument("out")
    pr.add_argument("--work")
    pr.add_argument("--pre", type=float, default=0.16)
    pr.add_argument("--post", type=float, default=0.26)
    pr.add_argument("--tail", type=float, default=0.45)
    pr.add_argument("--keep")
    pr.add_argument("--grade", default=GRADE)
    a = p.parse_args()
    prep(a) if a.cmd == "prep" else render(a)


if __name__ == "__main__":
    sys.exit(main())
