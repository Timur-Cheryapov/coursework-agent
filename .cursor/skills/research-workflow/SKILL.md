---
name: research-workflow
description: Full end-to-end research pipeline for coursework problems. Use when the user pastes a coursework task and says "Run research workflow" or "Research this problem". Orchestrates problem solving, textbook search, Wolfram verification, and LaTeX formatting into a complete report.
---

# 🔬 Research Workflow

Full end-to-end research pipeline for coursework problems. This is the **master workflow** that orchestrates all other skills and tools.

## When to Use

- Use when the user pastes a coursework task and says "Run research workflow" or "Research this problem"
- Use for "Full analysis of this task"
- This skill is helpful when the user needs a complete report: solution + sources + verification

## Instructions

### STEP 1 — Classify the Problem

1. Read the problem carefully and identify:
   - **Domain**: Mechanics / Physics / Mathematics
   - **Sub-topic**: e.g., static equilibrium, second-order ODE
   - **Problem type**: calculation, derivation, proof, conceptual
   - **Difficulty level**: introductory / intermediate / advanced
2. State the classification clearly to the user
3. List the key concepts involved

### STEP 2 — Solve the Problem

Use the `/solve-problem` skill protocol:
1. Follow the 7-step problem-solving protocol exactly
2. Show full working in LaTeX (use `align*` for derivations)
3. Include all intermediate steps — skip nothing
4. Box the final answer: `$\boxed{...}$`
5. Perform dimensional analysis and sanity checks

### STEP 3 — Search for Matching Textbook Examples

Use `tools/web_search.py` → `search_all()` + the `/find-examples` skill:
1. Translate the problem into textbook search terms
2. Run `search_all()` with example-optimized queries:
   - `"[topic] worked example"`
   - `"[topic] solved problem"`
   - `"[textbook name] [topic]"`
3. Filter for results likely to contain **actual worked examples**
4. Present the top 5 results with relevance notes

### STEP 4 — Find Relevant Textbooks

Use `tools/book_finder.py` → `find_books()`:
1. Search for textbooks covering this exact problem type
2. Cross-reference with the known textbook database
3. For each match, specify:
   - Which chapter/section covers this topic
   - Whether the book has worked examples of this type
   - How the student can access it (library, online, etc.)

### STEP 5 — Verify the Answer

Use `tools/wolfram_query.py`:
1. Formulate the problem as a Wolfram Alpha query
2. Compare Wolfram's answer with our solution
3. If they differ, investigate and reconcile
4. Report the verification result to the user

### STEP 6 — Format Final Output

Use the `/latex-output` skill + `tools/latex_renderer.py`:
1. Compile everything into a clean, structured output
2. Format in LaTeX using the solution template
3. Include the academic integrity reminder

## Output Template

```markdown
# 📋 Research Report: [Problem Title]

## Problem Classification
- **Domain:** [Mechanics/Physics/Mathematics]
- **Sub-topic:** [Specific topic]
- **Type:** [Calculation/Derivation/Proof/Conceptual]

## Full Worked Solution
[Complete step-by-step solution in LaTeX]

## Answer
$$\boxed{[Final answer with units]}$$

## Verification
- **Wolfram Alpha:** [Confirmed / Discrepancy noted]
- **Dimensional analysis:** [Check result]
- **Sanity check:** [Reasonableness assessment]

## Textbook References
1. [Author], *[Title]*, [Edition], Chapter [X], Example [Y]
   - **Relevance:** [Why this example matches]
2. [Author], *[Title]*, [Edition], Chapter [X]
   - **Relevance:** [Why this chapter is useful]
3. ...

## Additional Sources
- [Paper/preprint references from Semantic Scholar / arXiv]

## Academic Integrity Note
> This worked solution is for your learning and understanding.
> Your coursework submission should reflect your own work.
> Use this as a guide to develop your own solution approach.
```

## Error Handling

- **If the problem is ambiguous:** Ask the user to clarify before solving
- **If no textbook matches found:** Explain what was searched and suggest broader search terms
- **If Wolfram verification fails:** Report the discrepancy and show both solutions
- **If APIs are down:** Use the known textbook database as fallback and note which searches couldn't be performed
