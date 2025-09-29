import shutil
import subprocess
from pathlib import Path
from latexgen import render_table, render_image, render_document

def pdflatex_path():
    p = shutil.which("pdflatex")
    if p:
        return p
    candidates = [
        "/Library/TeX/texbin/pdflatex",
        "/usr/local/texlive/2025basic/bin/universal-darwin/pdflatex",
        "/usr/local/texlive/2024basic/bin/universal-darwin/pdflatex",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    return None

def main(compile_pdf: bool = False):
    root = Path(__file__).resolve().parents[1]
    assets = root / "assets"
    artifacts = root / "artifacts"
    artifacts.mkdir(exist_ok=True)

    rows = [
        ["Item", "Qty", "Price"],
        ["Apples", 3, "$2.50"],
        ["Bananas", 5, "$1.70"],
        ["Kiwi_#", 2, "$4.20"],
    ]
    tab = render_table(rows[1:], headers=rows[0], align="lcr",
                       caption="Groceries", label="tab:grocery")

    fig = render_image(str(assets / "sample.png"), width="0.6\\linewidth",
                       caption="Sample PNG inserted via \\includegraphics", label="fig:sample")

    body = tab + "\n\n" + fig
    doc = render_document(body, title="HW02 — Table + Image", author="Your Name")

    tex_path = artifacts / "hw02_full.tex"
    tex_path.write_text(doc, encoding="utf-8")
    print(f"Wrote {tex_path}")

    if compile_pdf:
        pdflatex = pdflatex_path()
        if not pdflatex:
            raise SystemExit(
                "pdflatex not found.\n"
                "Try one of:\n"
                "  /Library/TeX/texbin/pdflatex\n"
                "  /usr/local/texlive/2025basic/bin/universal-darwin/pdflatex\n"
            )
        for i in range(2):
            print(f"Running pdflatex pass {i+1}...")
            subprocess.run([
                pdflatex,
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-output-directory", str(artifacts),
                str(tex_path)
            ], check=True)
        print(f"PDF is at {artifacts / 'hw02_full.pdf'}")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--compile", action="store_true",
                    help="Compile the generated .tex to PDF using pdflatex")
    args = ap.parse_args()
    main(compile_pdf=args.compile)