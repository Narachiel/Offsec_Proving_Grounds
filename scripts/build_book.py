#!/usr/bin/env python3
"""Build a single A4 PDF book from repository PDFs, adding a cover and TOC.

Produces: Offsec_Proving_Grounds_Book.pdf at repo root.
"""
import os
from pathlib import Path
from datetime import datetime

try:
    from PyPDF2 import PdfReader, PdfMerger, PdfWriter
except Exception:
    raise

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm
    from reportlab.lib import colors
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


def make_header_overlay(title: str, out_path: Path):
    c = canvas.Canvas(str(out_path), pagesize=A4)
    w, h = A4
    c.setFillColor(colors.red)
    c.setFont('Helvetica-Bold', 16)
    c.drawCentredString(w / 2, h - 20 * mm, title)
    c.showPage()
    c.save()


def build_book():
    pdfs = collect_pdfs()
    if not pdfs:
        print('No PDFs found to merge.')
        return 1

    print(f'Found {len(pdfs)} PDFs to include')

    # First, create modified versions of each PDF with header overlay (or prepended header fallback).
    modified_files = []  # list of (orig_path, modified_path, page_count)
    for idx, p in enumerate(pdfs):
        r = PdfReader(str(p))
        title = p.stem
        header_path = TEMP_DIR / f'header_{idx}.pdf'
        tmp_modified = TEMP_DIR / f'mod_{idx}.pdf'
        make_header_overlay(title, header_path)

        writer = PdfWriter()
        overlay_reader = PdfReader(str(header_path))
        overlay_page = overlay_reader.pages[0]
        try:
            # attempt to merge overlay onto first page
            first = r.pages[0]
            try:
                first.merge_page(overlay_page)
                writer.add_page(first)
                for i in range(1, len(r.pages)):
                    writer.add_page(r.pages[i])
            except Exception:
                # fallback: prepend overlay as its own page
                writer.add_page(overlay_page)
                for pg in r.pages:
                    writer.add_page(pg)
        except Exception:
            # if anything unexpected, just copy original
            for pg in r.pages:
                writer.add_page(pg)

        with open(tmp_modified, 'wb') as fh:
            writer.write(fh)

        # read back to get page count
        mod_reader = PdfReader(str(tmp_modified))
        modified_files.append((p, tmp_modified, len(mod_reader.pages)))

    # compute page offsets from modified files
    total = 0
    offsets = []
    for orig, mod, count in modified_files:
        offsets.append(total + 1)
        total += count

    # Create cover
    cover_path = TEMP_DIR / 'cover.pdf'
    make_cover('Offsec Proving Grounds — Compendium', 'Narachiel', cover_path)

    # TOC entries map file names (relative) to start pages after cover and toc placeholders
    # We'll assume cover is 1 page; TOC may be multiple pages; compute TOC after we know its length.
    # To get TOC length we construct a preliminary TOC and measure pages.

    # Build preliminary TOC based on modified_files and iterate until TOC page count stabilizes.
    toc_path = TEMP_DIR / 'toc.pdf'
    toc_pages = 1
    while True:
        merged_offset = 1 + toc_pages  # cover=1
        entries = []
        for idx, (orig, mod, count) in enumerate(modified_files):
            display = orig.relative_to(REPO_ROOT).as_posix()
            start_page = merged_offset + offsets[idx] - 1
            entries.append((display, start_page))

        make_toc(entries, toc_path)
        toc_reader = PdfReader(str(toc_path))
        new_toc_pages = len(toc_reader.pages)
        if new_toc_pages == toc_pages:
            break
        toc_pages = new_toc_pages

    # Now merge: cover, toc, then for each pdf overlay header onto its first page
    merger = PdfMerger()
    merger.append(str(cover_path))
    merger.append(str(toc_path))
    # Append modified PDFs in order
    for orig, mod, count in modified_files:
        merger.append(str(mod))

    # write merged to a temp merged file first
    merged_tmp = TEMP_DIR / 'merged_tmp.pdf'
    merger.write(str(merged_tmp))
    merger.close()

    # Add page numbers as footer on every page
    merged_reader = PdfReader(str(merged_tmp))
    writer = PdfWriter()
    for i, page in enumerate(merged_reader.pages, start=1):
        # create footer overlay
        footer_path = TEMP_DIR / f'footer_{i}.pdf'
        c = canvas.Canvas(str(footer_path), pagesize=A4)
        w, h = A4
        c.setFont('Helvetica', 9)
        c.setFillColor(colors.grey)
        c.drawCentredString(w / 2, 10 * mm, str(i))
        c.showPage()
        c.save()

        footer_reader = PdfReader(str(footer_path))
        try:
            page.merge_page(footer_reader.pages[0])
        except Exception:
            pass
        writer.add_page(page)

    # ensure output directory exists
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_FILE, 'wb') as fh:
        writer.write(fh)

    print(f'Created book: {OUT_FILE}')
    return 0


if __name__ == '__main__':
    raise SystemExit(build_book())
