---
name: problem-solving
description: Quick focused problem solving without full research pipeline. Use when the user just wants a solution — "Solve this", "Help me with this problem", "What's the answer?" Faster than the full research workflow but still thorough with verification.
---

# 🧮 Problem Solving

A focused workflow for when the user **just wants a solution** (without the full research pipeline). Faster than `/research-workflow` but still thorough.

## When to Use

- Use when the user says: "Solve this", "Help me with this problem", "What's the answer?"
- Use when the user provides a specific problem but doesn't need textbook references
- This skill is helpful for quick homework help scenarios

## Instructions

### STEP 1 — Parse the Problem
1. Extract the problem statement
2. Identify domain and sub-topic (quick classification)
3. List knowns and unknowns

### STEP 2 — Choose Strategy
Based on problem type, select the solving approach:

| Problem Type | Strategy |
|-------------|----------|
| **Static equilibrium** | Free body diagram → sum of forces/moments = 0 |
| **Dynamics** | Newton's 2nd law or energy methods |
| **ODE** | Classify order/linearity → characteristic equation or variation of parameters |
| **PDE** | Separation of variables or transform methods |
| **Linear algebra** | Matrix formulation → row reduction or eigenvalue decomposition |
| **Calculus** | Direct integration, substitution, or by parts |
| **Lagrangian** | Define generalized coordinates → Euler-Lagrange equations |
| **Thermodynamics** | Identify system → first/second law analysis |
| **Circuits** | Kirchhoff's laws or mesh/nodal analysis |

### STEP 3 — Solve (Full Working)
Follow the `/solve-problem` skill Steps 3–5:
1. State the governing principle
2. Set up equations (with diagram/coordinate system description)
3. Show every algebraic step in LaTeX
4. Simplify and present the final answer

### STEP 4 — Verify
1. Dimensional analysis
2. Sanity check (order of magnitude, sign, limiting cases)
3. Optionally verify with `tools/wolfram_query.py`

### STEP 5 — Output
Format using the `/latex-output` skill:
- Clean LaTeX with boxed answer
- Brief mention of applicable textbook references
- Academic integrity note

## Quick Reference: Common Solution Patterns

### Mechanics — Force Equilibrium
$$\sum F_x = 0, \quad \sum F_y = 0, \quad \sum M_O = 0$$

### Mechanics — Newton's Second Law
$$\sum \vec{F} = m\vec{a}$$

### Energy Methods
$$T_1 + V_1 = T_2 + V_2 \quad \text{(conservative)}$$
$$T_1 + V_1 + U_{1 \to 2}^{nc} = T_2 + V_2 \quad \text{(non-conservative)}$$

### Second-Order ODE
$$ay'' + by' + cy = f(x)$$
Characteristic equation: $ar^2 + br + c = 0$

### Eigenvalue Problem
$$A\vec{x} = \lambda\vec{x} \implies \det(A - \lambda I) = 0$$
