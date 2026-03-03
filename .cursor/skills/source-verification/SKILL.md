---
name: source-verification
description: Verify that cited sources are real, accessible, and relevant before presenting them. Use after finding potential sources via search tools, before citing any textbook or paper, or when the user asks "Is this source real?" or "Where can I find this?"
---

# ✅ Source Verification

Ensure that **all cited sources are real, accessible, and relevant**. Used as a quality check before presenting references to the user.

## When to Use

- Use after finding potential sources via `tools/web_search.py` or `tools/book_finder.py`
- Use before citing any textbook, paper, or resource in a solution
- Use when the user asks: "Is this source real?" or "Where can I find this?"

## Instructions

### STEP 1 — Existence Check
For each candidate source, verify it exists:

| Source Type | Verification Method |
|------------|-------------------|
| **Textbook** | Search OpenLibrary + Google Books for exact title/author match |
| **Paper** | Search Semantic Scholar for DOI or exact title |
| **Preprint** | Search arXiv for arXiv ID or exact title |
| **Lecture notes** | URL check (if available) |

### STEP 2 — Metadata Verification
Confirm these details are accurate:
- **Title** matches exactly (no paraphrasing)
- **Author(s)** are correct
- **Year/Edition** is accurate
- **ISBN** (for books) is valid
- **DOI** (for papers) resolves correctly

### STEP 3 — Relevance Assessment
For each verified source, assess:

1. **Topic coverage**: Does this source actually cover the specific topic?
   - ✅ Confirmed: "Chapter 4 is titled 'Equilibrium of Rigid Bodies'"
   - ⚠️ Likely: "This textbook covers statics, which includes equilibrium"
   - ❌ Uncertain: "This textbook covers mechanics, which may include this topic"

2. **Example presence**: Does it contain worked examples?
   - ✅ Confirmed: Known to contain numbered worked examples
   - ⚠️ Likely: Textbook format suggests examples present
   - ❌ Unknown: Can't verify without access to the book

3. **Difficulty match**: Appropriate for the student's level?
   - Introductory (1st/2nd year) vs Advanced (3rd/4th year) vs Graduate

### STEP 4 — Confidence Rating

Assign each source a confidence level:

| Rating | Meaning | When to Use |
|--------|---------|-------------|
| 🟢 **High** | Verified existence + confirmed relevant content | Well-known textbook on exact topic |
| 🟡 **Medium** | Verified existence + likely relevant | Known textbook, but can't confirm specific chapter |
| 🔴 **Low** | Unverified or uncertain relevance | Can't confirm existence or relevance |

### STEP 5 — Presentation Rules

Based on confidence:

- 🟢 **High confidence**: Cite normally with full details
  > *R.C. Hibbeler, "Engineering Mechanics: Statics", 14th ed., Chapter 4 covers equilibrium of rigid bodies with multiple worked examples.*

- 🟡 **Medium confidence**: Cite with caveat
  > *Meriam & Kraige, "Engineering Mechanics" likely covers this topic in their statics section. Verify chapter details against your specific edition.*

- 🔴 **Low confidence**: Don't cite; instead suggest
  > *You may want to search your university library catalog for textbooks on [topic].*

## Common Verification Scenarios

### Scenario 1: Well-known textbook
- **Hibbeler Statics** → 🟢 Automatically high confidence for statics problems
- Can specify general chapter topics without claiming exact example numbers

### Scenario 2: Paper found via Semantic Scholar
- Verify DOI resolves → Check abstract matches topic → Rate relevance
- If abstract mentions "worked example" or "tutorial" → higher confidence

### Scenario 3: Can't find the source
- **DO NOT** fabricate or guess details
- Say: *"I was unable to verify this specific reference. Here are confirmed alternatives: ..."*

## Red Flags (Never Cite)
- Source doesn't appear in any search engine or database
- Author name doesn't match the title in any database
- Edition number seems implausible
- The source appears to be AI-generated or from a content farm
