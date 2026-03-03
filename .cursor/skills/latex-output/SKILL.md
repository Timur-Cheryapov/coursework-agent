---
name: latex-output
description: Format mathematical output in clean, professional LaTeX. Applied automatically as the final step of every solution and explanation. Use when the user asks to format something in LaTeX or needs report-ready output.
---

# 📝 LaTeX Output

Format any mathematical output in clean, professional LaTeX. This skill is applied automatically as the final step of every solution and explanation.

## When to Use

- Use to format **any mathematical output** in clean LaTeX
- Use when the user says: "Format in LaTeX", "Convert to LaTeX", "Make this report-ready"
- This skill is also applied automatically by other skills as a final formatting step

## Instructions

### Inline vs Display Math
- **Inline**: Use `$...$` for short expressions within text: *"The force is $F = ma$."*
- **Display**: Use `$$...$$` or `\[...\]` for important standalone equations

### Multi-step Solutions
Use `align*` for sequential derivation steps:
```latex
\begin{align*}
  F &= ma \\
    &= 5 \times 9.81 \\
    &= 49.05 \text{ N}
\end{align*}
```

### Boxed Final Answers
Always box the final answer:
```latex
$$\boxed{F = 49.05 \text{ N}}$$
```

### Units
Always use `\text{}` for units, with a thin space:
```latex
$F = 49.05 \text{ N}$
$v = 3.0 \text{ m/s}$
$\rho = 1000 \text{ kg/m}^3$
```

### Fractions
- Simple: `\frac{a}{b}`
- Display: `\dfrac{a}{b}` for larger fractions in display mode

### Vectors
- Bold: `\mathbf{F}`
- Arrow: `\vec{F}`
- Unit vectors: `\hat{i}, \hat{j}, \hat{k}`

### Matrices
```latex
\begin{pmatrix}
  a & b \\
  c & d
\end{pmatrix}
```

### Derivatives
- Ordinary: `\frac{dy}{dx}` or `\frac{d^2y}{dx^2}`
- Partial: `\frac{\partial f}{\partial x}`
- Dot notation (time): `\dot{x}, \ddot{x}`

### Integrals
```latex
\int_a^b f(x) \, dx
\oint \mathbf{F} \cdot d\mathbf{l}
\iint_S \mathbf{F} \cdot d\mathbf{A}
```

### Common Operators
| Symbol | LaTeX | Use |
|--------|-------|-----|
| ∇ | `\nabla` | Gradient, divergence, curl |
| × | `\times` | Cross product, multiplication |
| · | `\cdot` | Dot product |
| ≈ | `\approx` | Approximation |
| ≡ | `\equiv` | Definition / identity |
| ∑ | `\sum_{i=1}^{n}` | Summation |
| ∏ | `\prod_{i=1}^{n}` | Product |
| lim | `\lim_{x \to a}` | Limit |

### Environments

#### Numbered equations (for referencing)
```latex
\begin{equation} \label{eq:newton}
  F = ma
\end{equation}
```

#### Cases (piecewise functions)
```latex
f(x) = \begin{cases}
  x^2 & \text{if } x \geq 0 \\
  -x^2 & \text{if } x < 0
\end{cases}
```

#### Systems of equations
```latex
\begin{cases}
  2x + 3y &= 7 \\
  x - y &= 1
\end{cases}
```

### Full Document Generation

When the user needs a complete LaTeX document (for copying into their report), use `tools/latex_renderer.py`:

```python
from tools.latex_renderer import build_solution, build_document

solution = build_solution(
    problem_statement="...",
    given="...",
    find="...",
    approach="...",
    working="...",
    answer="...",
    verification="...",
    references=[{"author": "...", "title": "...", "edition": "...", "details": "..."}]
)

document = build_document(solution, title="Problem X Solution")
```

## Quality Checklist
- All math expressions properly delimited (`$...$` or `$$...$$`)
- Units in `\text{}` with proper spacing
- Final answer boxed with `\boxed{}`
- Multi-step derivations in `align*`
- All symbols defined where first used
- No raw ASCII math — everything in LaTeX notation
