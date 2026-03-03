---
name: solve-problem
description: Step-by-step problem solving for physics, mechanics, and mathematics coursework. Use when the user provides a problem that requires a numerical or symbolic solution. Follows a 7-step protocol: Identify, Knowns/Unknowns, Principle, Setup, Solve, Check, Reference.
---

# 🔧 Solve Problem

Step-by-step problem solving for physics, mechanics, and mathematics coursework.

## When to Use

- Use this skill when the user provides a physics, mechanics, or mathematics problem that requires a numerical or symbolic solution.
- Use when the user says: "Solve this", "Help me with this problem", "What's the answer?"

## Instructions

When given a physics/mechanics/math problem, follow these **seven steps** exactly:

### Step 1 — IDENTIFY
- What **type** of problem is this? (e.g., static equilibrium, second-order ODE, projectile motion)
- Which **domain** does it belong to? (Mechanics / Physics / Mathematics)
- What **sub-topic** is this? (e.g., beam bending, Lagrangian mechanics, Fourier series)

### Step 2 — KNOWNS & UNKNOWNS
- List all **given values** with units
- List all **quantities to find** with their expected units
- Note any **implicit assumptions** (e.g., frictionless surface, ideal gas, small angle approximation)

### Step 3 — PRINCIPLE
- Which **law, theorem, or formula** applies?
- State it explicitly: e.g., *"Newton's Second Law: $\vec{F} = m\vec{a}$"*
- If multiple methods exist, briefly mention alternatives and justify your choice

### Step 4 — SETUP
- **Draw a free body diagram** (describe it textually if visual not possible)
- **Define coordinate system** (origin, positive directions)
- **Set up equations** — write the governing equations before substituting numbers
- For ODE/PDE problems: state the equation, boundary conditions, and initial conditions

### Step 5 — SOLVE
- Show **every algebraic step** in LaTeX
- Use `align*` environment for multi-step derivations
- **Do not skip steps** — the student needs to see the full chain of reasoning
- Simplify intermediate results and box/highlight the final answer

### Step 6 — CHECK
- **Dimensional analysis**: verify units are consistent
- **Sanity check**: does the magnitude make physical sense?
- **Limiting cases**: check behavior at extreme values (e.g., $m \to 0$, $t \to \infty$)
- **Alternative method**: if feasible, verify with a second approach

### Step 7 — REFERENCE
- Name the **textbook chapter/section** this problem type maps to
- Suggest **similar examples** from known textbooks
- Use `tools/book_finder.py` to find additional references
- Cite as: *Author, Title, Edition, Chapter X, Example Y*

## Output Format

Structure every solution as:

```
## Problem
[Original problem statement]

## Solution

### Given
[List of known values]

### Find
[What to determine]

### Approach
[Principle and method]

### Working
[Full step-by-step solution in LaTeX]

### Answer
$$\boxed{[Final answer with units]}$$

### Verification
[Dimensional analysis + sanity check]

### References
[Textbook citations]
```

## Quality Checklist
- Every step has a clear justification
- All units are consistent and explicitly stated
- Final answer is boxed: `$\boxed{F = 49.05 \text{ N}}$`
- At least one verification method applied
- At least 2 textbook references provided
