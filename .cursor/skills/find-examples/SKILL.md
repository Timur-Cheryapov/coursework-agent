---
name: find-examples
description: Find real textbook examples matching a coursework problem type. Use when the user needs specific textbook references with worked examples, or asks "where can I find an example of..." Searches known textbooks, OpenLibrary, Google Books, Semantic Scholar, and arXiv.
---

# 🔍 Find Examples

Find real textbook examples that match the user's coursework problem type. This is the core research skill — designed to succeed where generic search tools fail.

## When to Use

- Use when the user needs **real textbook examples** matching their problem type
- Use when the user asks: "Find me an example of...", "Which textbook has..."
- This skill is helpful for finding specific chapters, sections, and worked examples

## Instructions

### Step 1 — Translate to Textbook Language

Convert the user's task description into standard academic terminology:

| User Says | Textbook Term |
|-----------|---------------|
| "find the force" | "static equilibrium force calculation" |
| "solve the spring thing" | "simple harmonic motion" |
| "do the beam problem" | "beam deflection / bending moment analysis" |
| "find the current" | "Kirchhoff's laws / circuit analysis" |
| "solve the differential equation" | "second-order linear ODE with constant coefficients" |

### Step 2 — Construct Search Queries

Build **multiple** search queries from different angles:

1. **Topic + "worked example"**: e.g., `"static equilibrium worked example"`
2. **Topic + "solved problem"**: e.g., `"moment of inertia solved problem"`
3. **Textbook name + topic**: e.g., `"Hibbeler statics moment equilibrium"`
4. **Topic + "tutorial" / "lecture notes"**: for supplementary sources

### Step 3 — Search Using Available Tools

Execute searches in priority order:

1. **Known textbook database** (`tools/book_finder.py` → `match_known_textbooks`)
   - Instant match against curated textbook-topic mapping
   - Returns specific textbook recommendations

2. **OpenLibrary** (`tools/book_finder.py` → `search_openlibrary_books`)
   - Finds actual textbook editions with ISBNs
   - Useful for verifying book existence

3. **Google Books** (`tools/book_finder.py` → `search_google_books`)
   - May have preview available for verification
   - Shows table of contents and chapter info

4. **Semantic Scholar** (`tools/web_search.py` → `search_semantic_scholar`)
   - Academic papers with worked derivations
   - Look for tutorial/review papers

5. **arXiv** (`tools/web_search.py` → `search_arxiv`)
   - Preprints with detailed derivations
   - Lecture note compilations

### Step 4 — Cross-Reference and Validate

For each candidate result:
- Does this source **actually exist**? (Verify via multiple APIs)
- Does it **actually contain worked examples** for this specific topic?
- Is the **difficulty level** appropriate? (introductory vs advanced)
- Can the student **realistically access** this source?

### Step 5 — Rank and Present

Sort results by:
1. **Specificity**: Does it solve the *exact same type* of problem?
2. **Accessibility**: Can the student find/access this?
3. **Quality**: Is it a well-known, reputable source?
4. **Worked examples**: Does it show full step-by-step solutions?

## Output Format

For each recommended source:

```
### [Rank]. Book/Paper Title
- **Author(s):** Full author names
- **Edition:** e.g., 14th Edition (2016)
- **Relevant Chapter:** Chapter 4 — Equilibrium of a Rigid Body
- **Specific Example:** Example 4.5 — Equilibrium of a Rigid Body with Distributed Load
- **Why it's relevant:** This example solves the exact same type of problem:
  calculating support reactions for a beam with a distributed load.
- **Difficulty match:** ⭐⭐⭐ (Intermediate — matches coursework level)
- **Access:** Available in most university libraries; OpenLibrary link: [URL]
```

## Important Rules
- **NEVER** recommend a book without specifying what makes it relevant
- **NEVER** fabricate chapter numbers or example numbers — if unsure, say so
- **ALWAYS** distinguish between "this book covers the topic" vs "this specific example solves this type of problem"
- Prefer **well-known textbooks** over obscure sources
- If you can't find an exact match, say so and recommend the closest alternatives
