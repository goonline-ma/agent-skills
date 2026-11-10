#!/usr/bin/env python3
"""Deterministic Pitch Deck Structural Linter & Contact-Sheet Visual QA Builder.

Subcommands:
  check <deck.pptx>                 Audit slide bounds, placeholder leaks, title wrap risk, and notes.
  grid  <png_dir> <out_dir>         Tile rendered slide PNGs into 2x4 contact sheets for vision inspection.
"""
import argparse
import glob
import json
import os
import re
import sys

BANNED_PATTERNS = [
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
    re.compile(r"lorem ipsum", re.IGNORECASE),
    re.compile(r"\[(?:insert|placeholder|tbd|todo|draft)[^\]]*\]", re.IGNORECASE),
]


def iter_shapes(shapes):
    for sh in shapes:
        yield sh
        if sh.shape_type == 6 and hasattr(sh, "shapes"):  # GROUP
            yield from iter_shapes(sh.shapes)


def cmd_check(args: argparse.Namespace) -> int:
    try:
        from pptx import Presentation
    except ImportError:
        sys.exit("Error: python-pptx is required (`pip install python-pptx`).")

    prs = Presentation(args.pptx)
    slide_w = prs.slide_width / 914400.0
    slide_h = prs.slide_height / 914400.0

    issues = []
    warnings = []

    for idx, slide in enumerate(prs.slides, 1):
        has_notes = False
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
            has_notes = bool(slide.notes_slide.notes_text_frame.text.strip())
        if not has_notes and not args.allow_missing_notes:
            warnings.append(f"Slide {idx}: empty speaker notes.")

        for sh in iter_shapes(slide.shapes):
            left = (sh.left or 0) / 914400.0
            top = (sh.top or 0) / 914400.0
            width = (sh.width or 0) / 914400.0
            height = (sh.height or 0) / 914400.0

            # Allow intentional full-bleed background shapes (tolerance 0.08 in)
            if left + width > slide_w + 0.08:
                issues.append(
                    f"Slide {idx} shape '{sh.name}': overflows right edge ({left + width:.2f}in > {slide_w:.2f}in)."
                )
            if top + height > slide_h + 0.08:
                issues.append(
                    f"Slide {idx} shape '{sh.name}': overflows bottom edge ({top + height:.2f}in > {slide_h:.2f}in)."
                )

            texts = []
            if sh.has_text_frame:
                texts.append(sh.text_frame.text)
                for p in sh.text_frame.paragraphs:
                    for run in p.runs:
                        if run.font.size and run.font.size.pt >= 28 and len(p.text.strip()) > args.max_title_chars:
                            warnings.append(
                                f"Slide {idx}: >=28pt heading is {len(p.text.strip())} chars (> {args.max_title_chars}, wrap collision risk): '{p.text.strip()[:55]}...'"
                            )
                            break
            if sh.has_table:
                for row in sh.table.rows:
                    for cell in row.cells:
                        texts.append(cell.text)

            joined = "\n".join(texts)
            for pat in BANNED_PATTERNS:
                m = pat.search(joined)
                if m:
                    issues.append(f"Slide {idx} shape '{sh.name}': banned placeholder '{m.group(0)}' found.")

    report = {
        "file": os.path.abspath(args.pptx),
        "slides": len(prs.slides),
        "size_in": [round(slide_w, 3), round(slide_h, 3)],
        "issues": issues,
        "warnings": warnings,
        "ok": len(issues) == 0,
    }
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


def cmd_grid(args: argparse.Namespace) -> int:
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        sys.exit("Error: Pillow is required (`pip install Pillow`).")

    pngs = sorted(glob.glob(os.path.join(args.png_dir, "*.png")))
    if not pngs:
        sys.exit(f"Error: no PNG files found in {args.png_dir}")

    os.makedirs(args.out_dir, exist_ok=True)
    cols, rows = 2, 4
    per_sheet = cols * rows
    cell_w, cell_h = 1280, 720
    pad = 24
    out_files = []

    for sheet_idx in range(0, len(pngs), per_sheet):
        batch = pngs[sheet_idx : sheet_idx + per_sheet]
        canvas_w = cols * cell_w + (cols + 1) * pad
        canvas_h = rows * cell_h + (rows + 1) * pad
        canvas = Image.new("RGB", (canvas_w, canvas_h), (18, 18, 22))
        draw = ImageDraw.Draw(canvas)

        for i, p_path in enumerate(batch):
            r, c = divmod(i, cols)
            x = pad + c * (cell_w + pad)
            y = pad + r * (cell_h + pad)
            with Image.open(p_path) as im:
                resized = im.convert("RGB").resize((cell_w, cell_h), Image.Resampling.LANCZOS)
                canvas.paste(resized, (x, y))
            draw.rectangle([x - 2, y - 2, x + cell_w + 2, y + cell_h + 2], outline=(90, 95, 110), width=2)
            draw.rectangle([x + 8, y + 8, x + 130, y + 40], fill=(0, 0, 0))
            draw.text((x + 16, y + 15), f"Slide {sheet_idx + i + 1:02d}", fill=(255, 255, 255))

        out_path = os.path.join(args.out_dir, f"grid_{(sheet_idx // per_sheet) + 1:02d}.png")
        canvas.save(out_path, optimize=True)
        out_files.append(os.path.abspath(out_path))

    print(json.dumps({"slides_processed": len(pngs), "grids": out_files}, indent=2))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Pitch Deck Structural Linter & Contact-Sheet Builder")
    sub = p.add_subparsers(dest="cmd", required=True)

    pc = sub.add_parser("check", help="Check .pptx geometry, placeholders, title length, and notes")
    pc.add_argument("pptx", help="Path to .pptx file")
    pc.add_argument("--max-title-chars", type=int, default=52)
    pc.add_argument("--allow-missing-notes", action="store_true")
    pc.set_defaults(func=cmd_check)

    pg = sub.add_parser("grid", help="Build 2x4 contact-sheet PNGs from rendered slide PNGs")
    pg.add_argument("png_dir", help="Directory containing rendered slide PNGs (s01.png, ...)")
    pg.add_argument("out_dir", help="Output directory for grid_01.png, ...")
    pg.set_defaults(func=cmd_grid)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
