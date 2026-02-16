#!/usr/bin/env python3
"""Build a single A4 PDF book from repository PDFs, adding a cover and TOC.

Produces: Offsec_Proving_Grounds_Book.pdf at repo root.
"""
import os
from pathlib import Path
from datetime import datetime

try:
    from PyPDF2 import PdfReader, PdfMerger
except Exception:
    raise

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm
except Exception:
    raise


REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_FILE = REPO_ROOT / "pdf" / "Offsec_Proving_Grounds_Book.pdf"
TEMP_DIR = REPO_ROOT / "scripts" / ".book_tmp"
TEMP_DIR.mkdir(parents=True, exist_ok=True)


def collect_pdfs():
    # Preferred ordering: README.pdf, PG_Play/*.pdf, PG_Practice/Linux/*.pdf, PG_Practice/Windows/*.pdf, others
    root = REPO_ROOT
    pdfs = []
    # README first
    r = root / 'README.pdf'
    if r.exists():
        pdfs.append(r)

    play_dir = root / 'PG_Play'
    if play_dir.exists():
        pdfs += sorted(play_dir.glob('*.pdf'))

    prat = root / 'PG_Practice'
    if prat.exists():
        linux = prat / 'Linux'
        windows = prat / 'Windows'
        if linux.exists():
            pdfs += sorted(linux.glob('*.pdf'))
        if windows.exists():
            pdfs += sorted(windows.glob('*.pdf'))

    # Add any other pdfs in the repo that are not already included
    for p in sorted(root.rglob('*.pdf')):
        # skip files in scripts, .git, and the combined book itself
        if 'scripts' in p.parts or '.git' in p.parts:
            continue
        if p.name == OUT_FILE.name:
            continue
        if p not in pdfs:
            pdfs.append(p)

    return pdfs


def make_cover(title: str, author: str, out_path: Path):
    c = canvas.Canvas(str(out_path), pagesize=A4)
    w, h = A4
    c.setFont('Helvetica-Bold', 28)
    c.drawCentredString(w / 2, h - 80 * mm, title)
    c.setFont('Helvetica', 14)
    c.drawCentredString(w / 2, h - 95 * mm, f'Compiled by {author}')
    c.drawCentredString(w / 2, h - 105 * mm, datetime.utcnow().strftime('%Y-%m-%d UTC'))
    c.showPage()
    c.save()


def make_toc(entries, out_path: Path):
    # entries: list of (display_name, start_page)
    c = canvas.Canvas(str(out_path), pagesize=A4)
    w, h = A4
    margin = 20 * mm
    y = h - margin
    c.setFont('Helvetica-Bold', 20)
    c.drawString(margin, y, 'Table of Contents')
    y -= 12 * mm
    c.setFont('Helvetica', 11)
    for name, page in entries:
        # wrap long names simply
        if y < margin:
            c.showPage()
            y = h - margin
            c.setFont('Helvetica', 11)
        text = (name if len(name) < 80 else name[:76] + '...')
        c.drawString(margin, y, text)
        c.drawRightString(w - margin, y, str(page))
        y -= 7 * mm
    c.showPage()
    c.save()


def make_title_page(title: str, out_path: Path):
    c = canvas.Canvas(str(out_path), pagesize=A4)
    w, h = A4
    # Use header-sized title (not oversized)
    c.setFont('Helvetica-Bold', 20)
    # position like a header
    c.drawCentredString(w / 2, h - 40 * mm, title)
    c.showPage()
    c.save()


def build_book():
    pdfs = collect_pdfs()
    if not pdfs:
        print('No PDFs found to merge.')
        return 1

    print(f'Found {len(pdfs)} PDFs to include')

    # compute page offsets (include one title page per document)
    readers = []
    offsets = []
    total = 0
    for p in pdfs:
        r = PdfReader(str(p))
        readers.append((p, r))
        offsets.append(total + 1)  # 1-based start page in merged document
        total += len(r.pages) + 1  # include title page for each document

    # Create cover
    cover_path = TEMP_DIR / 'cover.pdf'
    make_cover('Offsec Proving Grounds — Compendium', 'Narachiel', cover_path)

    # TOC entries map file names (relative) to start pages after cover and toc placeholders
    # We'll assume cover is 1 page; TOC may be multiple pages; compute TOC after we know its length.
    # To get TOC length we construct a preliminary TOC and measure pages.

    # Build preliminary merger to compute TOC start pages: cover (1) + toc (unknown) + content
    # For simplicity, we'll generate the TOC with page numbers offset by 1 + toc_pages (we'll iterate if needed).

    # First guess: TOC fits in 2 pages. We'll generate and then re-create if page counts shift.
    toc_path = TEMP_DIR / 'toc.pdf'

    # Compute initial start pages assuming cover=1 and toc_pages=1
    toc_pages = 1
    while True:
        merged_offset = 1 + toc_pages  # cover=1
        entries = []
        for idx, (p, r) in enumerate(readers):
            display = p.relative_to(REPO_ROOT).as_posix()
            start_page = merged_offset + offsets[idx] - 1
            entries.append((display, start_page))

        make_toc(entries, toc_path)
        # measure toc pages
        toc_reader = PdfReader(str(toc_path))
        new_toc_pages = len(toc_reader.pages)
        if new_toc_pages == toc_pages:
            break
        toc_pages = new_toc_pages

    # Now merge: cover, toc, then for each pdf add a title page then the content
    merger = PdfMerger()
    merger.append(str(cover_path))
    merger.append(str(toc_path))
    for idx, (p, _) in enumerate(readers):
        title = p.stem
        title_path = TEMP_DIR / f'title_{idx}.pdf'
        make_title_page(title, title_path)
        merger.append(str(title_path))
        merger.append(str(p))

    merger.write(str(OUT_FILE))
    merger.close()

    print(f'Created book: {OUT_FILE}')
    return 0


if __name__ == '__main__':
    raise SystemExit(build_book())
