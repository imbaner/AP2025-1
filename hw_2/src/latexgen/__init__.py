from typing import Iterable, List, Optional, Sequence

_ESCAPE_MAP = {
    '&': r'\&',
    '%': r'\%',
    '$': r'\$',
    '#': r'\#',
    '_': r'\_',
    '{': r'\{',
    '}': r'\}',
    '~': r'\textasciitilde{}',
    '^': r'\textasciicircum{}',
    '\\': r'\textbackslash{}',
}

def escape_tex(s: object) -> str:
    text = str(s)
    # If there's an unmatched number of '$', escape them (treat as text)
    if text.count('$') % 2 == 1:
        text = text.replace('$', r'\$')

    out: List[str] = []
    in_math = False
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        # Preserve a literal "\$" outside math; do not escape the backslash further
        if not in_math and ch == '\\' and i + 1 < n and text[i + 1] == '$':
            out.append(r'\$')
            i += 2
            continue
        if ch == '$':
            in_math = not in_math
            out.append('$')
        else:
            out.append(ch if in_math else _ESCAPE_MAP.get(ch, ch))
        i += 1
    return ''.join(out)


def _normalize_table(data: Sequence[Sequence[object]]) -> List[List[str]]:
    rows = [list(map(escape_tex, row)) for row in data]
    if not rows:
        return []
    width = max(len(r) for r in rows)
    padded = [r + [''] * (width - len(r)) for r in rows]
    return padded

def render_table(
    data: Sequence[Sequence[object]],
    *, headers: Optional[Sequence[object]] = None,
    align: Optional[Sequence[str]] = None,
    caption: Optional[str] = None,
    label: Optional[str] = None,
    table_env: bool = True,
) -> str:
    body_rows = _normalize_table(data)
    ncols = max(len(r) for r in body_rows) if body_rows else (len(headers) if headers else 0)
    if headers:
        hdr = list(map(escape_tex, headers))
        if len(hdr) < ncols:
            hdr += [''] * (ncols - len(hdr))
    else:
        hdr = None

    if align is None:
        col_spec = 'l' * ncols
    else:
        if isinstance(align, str):
            col_spec = align
        else:
            col_spec = ''.join(align)
    if not col_spec:
        col_spec = 'l'

    lines = []
    lines.append(f"\\begin{{tabular}}{{{col_spec}}}")
    if hdr:
        lines.append(r' \\ '.join([' & '.join(hdr)]) + r' \\ \hline')
    for row in body_rows:
        lines.append(' & '.join(row) + r' \\')
    lines.append(r'\end{tabular}')
    tabular_code = '\n'.join(lines)

    if not table_env:
        return tabular_code

    outer = [r'\begin{table}[htbp]', r'\centering', tabular_code]
    if caption:
        outer.append(f"\\caption{{{escape_tex(caption)}}}")
    if label:
        outer.append(f"\\label{{{label}}}")
    outer.append(r'\end{table}')
    return '\n'.join(outer)

def render_image(
    path: str, *, width: str = '\\linewidth',
    caption: Optional[str] = None,
    label: Optional[str] = None,
    position: str = 'htbp'
) -> str:
    pieces = [f"\\begin{{figure}}[{position}]", r'\centering', f"\\includegraphics[width={width}]{{{path}}}"]
    if caption:
        pieces.append(f"\\caption{{{escape_tex(caption)}}}")
    if label:
        pieces.append(f"\\label{{{label}}}")
    pieces.append(r'\end{figure}')
    return '\n'.join(pieces)

def render_document(
    body: str, *, title: Optional[str] = None, author: Optional[str] = None,
    packages: Optional[Sequence[str]] = None, docclass: str = 'article',
    options: Optional[Sequence[str]] = None
) -> str:
    pkg_list = ['graphicx', 'booktabs']
    if packages:
        pkg_list.extend(packages)
    opts = '[' + ','.join(options) + ']' if options else ''
    head = [f"\\documentclass{opts}{{{docclass}}}"]
    for p in pkg_list:
        head.append(f"\\usepackage{{{p}}}")
    if title:
        head.append(f"\\title{{{escape_tex(title)}}}")
    if author:
        head.append(f"\\author{{{escape_tex(author)}}}")
    head.append(r'\begin{document}')
    if title:
        head.append(r'\maketitle')
    return '\n'.join(head) + '\n' + body + '\n\\end{document}\n'
