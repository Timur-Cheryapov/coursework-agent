---
name: explain-concept
description: Provide deep conceptual explanations for physics, mechanics, and mathematics topics. Use when the user asks "What is...", "How does... work?", "Why do we use...", or "Explain the difference between X and Y".
---

# 💡 Explain Concept

Provide deep, structured conceptual explanations for physics, mechanics, and mathematics topics.

## When to Use

- Use when the user needs to **understand a concept** rather than solve a specific problem
- Use when the user asks: "What is [concept]?", "How does [phenomenon] work?", "Why do we use [method]?", "Explain the difference between X and Y"
- This skill is helpful for building intuition before tackling problems

## Instructions

### Step 1 — Assess Current Understanding
Before diving deep, gauge what the student likely knows:
- Is this an introductory or advanced course?
- What prerequisites should they already have?
- Are they asking about fundamentals or a subtle nuance?
- Use the ask questions tool if you need to clarify the student's level.

### Step 2 — Core Explanation (The "What")
- **Define** the concept in one clear sentence
- **State** the key equation(s) in LaTeX
- **Identify** the physical/mathematical intuition behind it

### Step 3 — Deep Dive (The "Why")
- **Derive** the key result from first principles when appropriate
- **Connect** to concepts the student already knows
- **Explain** each term in the equation — what does each symbol represent physically?

### Step 4 — Concrete Example (The "How")
- Provide a **simple, concrete example** that illustrates the concept
- Walk through it with numbers to make it tangible
- Show how the concept applies in practice

### Step 5 — Common Pitfalls
- List **common mistakes** students make with this concept
- Explain **why** the mistake is wrong (not just that it is)
- Provide **corrected** reasoning

### Step 6 — Connections & Context
- How does this relate to **adjacent topics**?
- When does this concept **break down** or need modification?
- What are the **assumptions** underlying this concept?
- Where does this fit in the **bigger picture** of the course?

## Explanation Levels

Adapt depth based on the topic:

| Level | Audience | Style |
|-------|----------|-------|
| **Foundational** | First-year | Intuitive analogies, minimal math, lots of diagrams |
| **Intermediate** | Second/third-year | Full derivations, moderate rigor, worked examples |
| **Advanced** | Final-year/postgrad | Rigorous proofs, edge cases, research connections |

## Output Format

```
## [Concept Name]

### Definition
[One-sentence definition]

### Key Equation
$$[Main equation in LaTeX]$$

where:
- $X$ = [description with units]
- $Y$ = [description with units]

### Intuition
[Physical or mathematical intuition — what does this MEAN?]

### Derivation
[Step-by-step derivation from first principles]

### Example
[Concrete worked example with numbers]

### Common Mistakes
1. [Mistake] → [Correction]
2. [Mistake] → [Correction]

### Related Topics
- [Topic 1] — [How it connects]
- [Topic 2] — [How it connects]

### Further Reading
- [Textbook reference 1]
- [Textbook reference 2]
```

## Quality Standards
- Explanations should be **self-contained** — don't assume the student has the textbook open
- Use **analogies** where helpful, but always follow with the rigorous version
- Every equation should have **all symbols defined** with units
- Include **dimensional analysis** for physical quantities
