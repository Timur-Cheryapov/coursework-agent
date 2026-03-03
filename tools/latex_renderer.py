"""
LaTeX Renderer Tool — Format & Render LaTeX Output
Provides utilities for formatting mathematical solutions in LaTeX,
generating complete document templates, and rendering to readable output.
"""

import re
from typing import Optional


# ---------------------------------------------------------------------------
# LaTeX templates
# ---------------------------------------------------------------------------

DOCUMENT_TEMPLATE = r"""\documentclass[12pt,a4paper]{{article}}
\usepackage{{amsmath, amssymb, amsthm}}
\usepackage{{physics}}
\usepackage{{graphicx}}
\usepackage{{geometry}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}
\geometry{{margin=2.5cm}}

\title{{{title}}}
\author{{{author}}}
\date{{{date}}}

\begin{{document}}
\maketitle

{content}

\end{{document}}
"""

SOLUTION_TEMPLATE = r"""\section*{{Problem}}
{problem_statement}

\section*{{Solution}}

\subsection*{{Given}}
{given}

\subsection*{{Find}}
{find}

\subsection*{{Approach}}
{approach}

\subsection*{{Working}}
{working}

\subsection*{{Answer}}
{answer}

\subsection*{{Verification}}
{verification}

\subsection*{{References}}
{references}
"""

REFERENCE_TEMPLATE = r"""\bibitem{{{key}}} {author}, \textit{{{title}}}, {edition}, {details}."""


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def wrap_inline_math(text: str) -> str:
    """Ensure single $ delimiters for inline math expressions."""
    # Don't double-wrap
    if text.startswith("$") and text.endswith("$"):
        return text
    return f"${text}$"


def wrap_display_math(text: str) -> str:
    """Wrap expression in display math (equation) environment."""
    text = text.strip().strip("$")
    return f"\\[\n{text}\n\\]"


def wrap_aligned(steps: list[str]) -> str:
    """
    Wrap a list of aligned equation steps.

    Args:
        steps: List of equation strings, each with '=' for alignment.
               e.g. ["F &= ma", "&= 5 \\times 9.81", "&= 49.05 \\text{{ N}}"]
    """
    content = " \\\\\n".join(f"  {s}" for s in steps)
    return f"\\begin{{align*}}\n{content}\n\\end{{align*}}"


def wrap_cases(cases: list[tuple[str, str]]) -> str:
    """
    Wrap conditions in a cases environment.

    Args:
        cases: List of (expression, condition) tuples.
    """
    content = " \\\\\n".join(f"  {expr} & \\text{{if }} {cond}" for expr, cond in cases)
    return f"\\begin{{cases}}\n{content}\n\\end{{cases}}"


def format_matrix(rows: list[list[str]], style: str = "pmatrix") -> str:
    """
    Format a matrix in LaTeX.

    Args:
        rows:  List of rows, each row is a list of element strings.
        style: Matrix style: pmatrix, bmatrix, vmatrix, etc.
    """
    row_strs = [" & ".join(row) for row in rows]
    content = " \\\\\n".join(f"  {r}" for r in row_strs)
    return f"\\begin{{{style}}}\n{content}\n\\end{{{style}}}"


def format_fraction(numerator: str, denominator: str) -> str:
    """Format a fraction."""
    return f"\\frac{{{numerator}}}{{{denominator}}}"


def format_vector(components: list[str], style: str = "column") -> str:
    """Format a vector as column or row."""
    if style == "row":
        return f"\\begin{{pmatrix}} {' & '.join(components)} \\end{{pmatrix}}"
    rows = [[c] for c in components]
    return format_matrix(rows, "pmatrix")


# ---------------------------------------------------------------------------
# Solution builder
# ---------------------------------------------------------------------------

def build_solution(
    problem_statement: str,
    given: str,
    find: str,
    approach: str,
    working: str,
    answer: str,
    verification: str = "",
    references: Optional[list[dict]] = None,
) -> str:
    """
    Build a complete formatted solution.

    Args:
        problem_statement: The original problem text.
        given:            Known values and conditions.
        find:             What we need to determine.
        approach:         Which principle/law/method we'll use.
        working:          Full step-by-step working (LaTeX).
        answer:           Final answer with units.
        verification:     Dimensional analysis / sanity check.
        references:       List of dicts with keys: author, title, edition, details.

    Returns:
        Formatted LaTeX solution string.
    """
    ref_lines = []
    if references:
        ref_lines.append("\\begin{enumerate}")
        for ref in references:
            ref_lines.append(
                f"  \\item {ref.get('author', 'Unknown')}, "
                f"\\textit{{{ref.get('title', 'Untitled')}}}, "
                f"{ref.get('edition', '')}, "
                f"{ref.get('details', '')}"
            )
        ref_lines.append("\\end{enumerate}")

    return SOLUTION_TEMPLATE.format(
        problem_statement=problem_statement,
        given=given,
        find=find,
        approach=approach,
        working=working,
        answer=answer,
        verification=verification or "N/A",
        references="\n".join(ref_lines) if ref_lines else "N/A",
    )


def build_document(
    content: str,
    title: str = "Coursework Solution",
    author: str = "",
    date: str = "\\today",
) -> str:
    """
    Build a complete LaTeX document.

    Args:
        content: The body content (from build_solution or custom).
        title:   Document title.
        author:  Author name.
        date:    Date string.

    Returns:
        Complete .tex document string.
    """
    return DOCUMENT_TEMPLATE.format(
        title=title,
        author=author,
        date=date,
        content=content,
    )


# ---------------------------------------------------------------------------
# LaTeX → readable plaintext (for terminal display)
# ---------------------------------------------------------------------------

def latex_to_readable(latex: str) -> str:
    """
    Convert LaTeX math notation to a more readable plaintext form.
    This is a best-effort conversion for terminal display.
    """
    text = latex

    # Remove environments
    text = re.sub(r"\\begin\{.*?\}", "", text)
    text = re.sub(r"\\end\{.*?\}", "", text)

    # Common replacements
    replacements = {
        r"\frac": "/",
        r"\cdot": "·",
        r"\times": "×",
        r"\pm": "±",
        r"\mp": "∓",
        r"\leq": "≤",
        r"\geq": "≥",
        r"\neq": "≠",
        r"\approx": "≈",
        r"\infty": "∞",
        r"\partial": "∂",
        r"\nabla": "∇",
        r"\alpha": "α",
        r"\beta": "β",
        r"\gamma": "γ",
        r"\delta": "δ",
        r"\epsilon": "ε",
        r"\theta": "θ",
        r"\lambda": "λ",
        r"\mu": "μ",
        r"\pi": "π",
        r"\sigma": "σ",
        r"\omega": "ω",
        r"\Omega": "Ω",
        r"\phi": "φ",
        r"\psi": "ψ",
        r"\rightarrow": "→",
        r"\leftarrow": "←",
        r"\Rightarrow": "⇒",
        r"\sum": "Σ",
        r"\int": "∫",
        r"\prod": "∏",
        r"\sqrt": "√",
    }
    for cmd, symbol in replacements.items():
        text = text.replace(cmd, symbol)

    # Remove remaining LaTeX commands
    text = re.sub(r"\\text\{(.*?)\}", r"\1", text)
    text = re.sub(r"\\[a-zA-Z]+", "", text)

    # Remove braces
    text = re.sub(r"[{}]", "", text)

    # Clean up whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ---------------------------------------------------------------------------
# Common unit formatting
# ---------------------------------------------------------------------------

UNIT_MAP = {
    "N": r"\text{ N}",
    "m": r"\text{ m}",
    "kg": r"\text{ kg}",
    "s": r"\text{ s}",
    "J": r"\text{ J}",
    "W": r"\text{ W}",
    "Pa": r"\text{ Pa}",
    "rad": r"\text{ rad}",
    "deg": r"^\circ",
    "m/s": r"\text{ m/s}",
    "m/s^2": r"\text{ m/s}^2",
    "N·m": r"\text{ N·m}",
    "kg/m^3": r"\text{ kg/m}^3",
}


def format_with_unit(value: str, unit: str) -> str:
    """Format a value with its proper LaTeX unit."""
    latex_unit = UNIT_MAP.get(unit, rf"\text{{ {unit}}}")
    return f"{value}{latex_unit}"


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Demo: build a sample solution
    working = wrap_aligned([
        r"F &= ma",
        r"&= 5 \times 9.81",
        r"&= 49.05 \text{ N}",
    ])

    solution = build_solution(
        problem_statement="A block of mass $m = 5$ kg rests on a frictionless surface. Find the force required to accelerate it at $g = 9.81$ m/s².",
        given=r"$m = 5$ kg, $a = g = 9.81$ m/s$^2$",
        find="Force $F$",
        approach="Newton's Second Law: $F = ma$",
        working=working,
        answer=format_with_unit("49.05", "N"),
        verification=r"Dimensional check: $[kg][m/s^2] = [N]$ ✓",
        references=[
            {"author": "R.C. Hibbeler", "title": "Engineering Mechanics: Statics", "edition": "14th ed.", "details": "Chapter 3, Example 3.1"},
        ],
    )

    doc = build_document(solution, title="Sample Problem Solution")
    print(doc)
