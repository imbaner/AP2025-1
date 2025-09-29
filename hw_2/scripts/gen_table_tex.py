from pathlib import Path
from latexgen import render_table, render_document

def main():
    data = [
        ["Name", "Language", "Stars"],
        ["uv", "Rust",  "★ ★ ★ ★ ★"],
        ["CPython", "C", "★ ★ ★ ★"],
        ["LaTeX", "TeX", "∞"],
    ]
    headers = ["Project", "Tech", "Rating"]
    table_code = render_table(data[1:], headers=headers, align=['l','l','c'], caption="Sample table", label="tab:sample")
    doc = render_document(table_code, title="HW02 — Table Example", author="Your Name")
    out_dir = Path(__file__).resolve().parents[1] / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "hw02_table.tex"
    out_path.write_text(doc, encoding="utf-8")
    print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()