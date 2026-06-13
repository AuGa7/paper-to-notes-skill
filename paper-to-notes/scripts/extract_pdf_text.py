#!/usr/bin/env python3
"""Extract text from a PDF with page markers.

The script intentionally supports several backends because Codex environments
vary. It tries Python libraries first, then the external `pdftotext` binary.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable, Iterable


PageText = list[tuple[int, str]]


def clean_text(text: str) -> str:
    lines = []
    for line in text.replace("\x00", "").splitlines():
        lines.append(line.rstrip())
    return "\n".join(lines).strip()


def format_pages(source: Path, method: str, pages: PageText) -> str:
    chunks = [
        "# Extracted PDF Text",
        "",
        f"Source: {source}",
        f"Method: {method}",
        f"Pages extracted: {len(pages)}",
        "",
    ]
    for page_num, text in pages:
        chunks.append(f"--- Page {page_num} ---")
        chunks.append(text.strip() or "[No extractable text on this page]")
        chunks.append("")
    return "\n".join(chunks).rstrip() + "\n"


def limit_pages(items: Iterable[tuple[int, str]], max_pages: int | None) -> PageText:
    pages: PageText = []
    for page_num, text in items:
        if max_pages is not None and len(pages) >= max_pages:
            break
        pages.append((page_num, clean_text(text)))
    return pages


def extract_with_pypdf(path: Path, max_pages: int | None) -> PageText:
    from pypdf import PdfReader  # type: ignore

    reader = PdfReader(str(path))
    return limit_pages(
        ((idx + 1, page.extract_text() or "") for idx, page in enumerate(reader.pages)),
        max_pages,
    )


def extract_with_pypdf2(path: Path, max_pages: int | None) -> PageText:
    from PyPDF2 import PdfReader  # type: ignore

    reader = PdfReader(str(path))
    return limit_pages(
        ((idx + 1, page.extract_text() or "") for idx, page in enumerate(reader.pages)),
        max_pages,
    )


def extract_with_pdfplumber(path: Path, max_pages: int | None) -> PageText:
    import pdfplumber  # type: ignore

    with pdfplumber.open(str(path)) as pdf:
        return limit_pages(
            ((idx + 1, page.extract_text() or "") for idx, page in enumerate(pdf.pages)),
            max_pages,
        )


def extract_with_pymupdf(path: Path, max_pages: int | None) -> PageText:
    import fitz  # type: ignore

    doc = fitz.open(str(path))
    try:
        return limit_pages(
            ((idx + 1, page.get_text("text") or "") for idx, page in enumerate(doc)),
            max_pages,
        )
    finally:
        doc.close()


def extract_with_pdftotext(path: Path, max_pages: int | None) -> PageText:
    if not shutil.which("pdftotext"):
        raise RuntimeError("pdftotext binary is not available")

    cmd = ["pdftotext", "-layout"]
    if max_pages is not None:
        cmd.extend(["-f", "1", "-l", str(max_pages)])
    cmd.extend([str(path), "-"])
    result = subprocess.run(cmd, check=True, text=True, capture_output=True)
    text = clean_text(result.stdout)
    if not text:
        return []
    # pdftotext does not reliably preserve page boundaries in stdout, so mark
    # the result as one extracted block.
    return [(1, text)]


METHODS: list[tuple[str, Callable[[Path, int | None], PageText]]] = [
    ("pypdf", extract_with_pypdf),
    ("PyPDF2", extract_with_pypdf2),
    ("pdfplumber", extract_with_pdfplumber),
    ("PyMuPDF", extract_with_pymupdf),
    ("pdftotext", extract_with_pdftotext),
]


def usable_text_length(pages: PageText) -> int:
    return sum(len(text.strip()) for _, text in pages)


def run_self_test() -> int:
    sample = [(1, "  Title  \n\nA method."), (2, "Result table\n  value  ")]
    rendered = format_pages(Path("sample.pdf"), "self-test", sample)
    assert "Source: sample.pdf" in rendered
    assert "--- Page 1 ---" in rendered
    assert "Title" in rendered
    print("self-test ok")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract text from a PDF with page markers.")
    parser.add_argument("pdf", nargs="?", type=Path, help="Path to the PDF file.")
    parser.add_argument("--out", type=Path, help="Write extracted text to this file.")
    parser.add_argument("--max-pages", type=int, help="Only extract the first N pages.")
    parser.add_argument(
        "--min-chars",
        type=int,
        default=200,
        help="Minimum extracted character count before accepting a backend. Default: 200.",
    )
    parser.add_argument("--self-test", action="store_true", help="Run a small internal test.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        return run_self_test()
    if args.pdf is None:
        print("error: provide a PDF path or use --self-test", file=sys.stderr)
        return 2
    path = args.pdf.expanduser().resolve()
    if not path.exists():
        print(f"error: PDF not found: {path}", file=sys.stderr)
        return 2
    if path.suffix.lower() != ".pdf":
        print(f"warning: file does not end in .pdf: {path}", file=sys.stderr)

    failures: list[str] = []
    best: tuple[str, PageText] | None = None
    for name, extractor in METHODS:
        try:
            pages = extractor(path, args.max_pages)
            if usable_text_length(pages) >= args.min_chars:
                best = (name, pages)
                break
            if pages and best is None:
                best = (name, pages)
            failures.append(f"{name}: extracted too little text")
        except Exception as exc:  # pragma: no cover - backend availability varies.
            failures.append(f"{name}: {exc}")

    if best is None:
        print("error: no PDF text extractor succeeded.", file=sys.stderr)
        print("Install one backend, for example: python -m pip install pypdf", file=sys.stderr)
        print("Backend attempts:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 3

    method, pages = best
    output = format_pages(path, method, pages)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
        print(f"wrote {args.out} using {method} ({usable_text_length(pages)} chars)")
    else:
        sys.stdout.write(output)

    if usable_text_length(pages) < args.min_chars:
        print(
            "warning: extracted text is short; the PDF may be scanned, figure-heavy, or protected.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
