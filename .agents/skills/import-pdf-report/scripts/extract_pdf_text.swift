import Foundation
import PDFKit

guard CommandLine.arguments.count == 3 else {
    FileHandle.standardError.write(Data("Usage: extract_pdf_text.swift input.pdf output.txt\n".utf8))
    exit(2)
}

let inputURL = URL(fileURLWithPath: CommandLine.arguments[1])
let outputURL = URL(fileURLWithPath: CommandLine.arguments[2])

guard FileManager.default.fileExists(atPath: inputURL.path) else {
    FileHandle.standardError.write(Data("PDF not found: \(inputURL.path)\n".utf8))
    exit(1)
}

guard let document = PDFDocument(url: inputURL) else {
    FileHandle.standardError.write(Data("Could not open PDF: \(inputURL.path)\n".utf8))
    exit(1)
}

var chunks: [String] = []
for index in 0..<document.pageCount {
    guard let page = document.page(at: index) else { continue }
    let text = page.string ?? ""
    chunks.append("\n\n--- PAGE \(index + 1) ---\n\n\(text)")
}

let extracted = chunks.joined(separator: "\n")
try extracted.write(to: outputURL, atomically: true, encoding: .utf8)

let nonWhitespaceCount = extracted.filter { !$0.isWhitespace }.count
FileHandle.standardError.write(Data("Extracted \(document.pageCount) pages, \(nonWhitespaceCount) non-whitespace characters.\n".utf8))

if nonWhitespaceCount < 500 {
    FileHandle.standardError.write(Data("Warning: very little text extracted. This PDF may need OCR.\n".utf8))
}
