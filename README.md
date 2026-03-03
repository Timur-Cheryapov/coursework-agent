# 🧠 Coursework Research Agent

A local AI agent specialized in **mechanics, physics, and mathematics** coursework research. Built for Cursor IDE — uses the [Agent Skills standard](https://cursor.com/docs/context/skills) with structured rules, skills, tools, and workflows to search for real academic sources, solve problems step-by-step, and find relevant textbook examples.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Wolfram Alpha (Optional but Recommended)

Get a free API key at [developer.wolframalpha.com](https://developer.wolframalpha.com), then:

```bash
export WOLFRAM_APP_ID="your-api-key-here"
```

On Windows:
```powershell
set WOLFRAM_APP_ID=your-api-key-here
```

### 3. Use in Cursor

- The `.cursor/rules/*.mdc` files **auto-load** as always-applied agent context.
- The `.cursor/skills/*/SKILL.md` files are **auto-discovered** by the Agent and appear under **Cursor Settings → Rules → Agent Decides**.
- Open any file and use **Ctrl+L** (Windows) or **Cmd+L** (Mac) to chat.
- Type `/` in Agent chat to see and invoke available skills.

### 4. Try It

Paste your coursework task and say:

> **"Run research workflow on this problem"**

Or invoke skills directly:
- `/solve-problem` — step-by-step solution
- `/find-examples` — find matching textbook examples
- `/research-workflow` — full pipeline with verification
- `/task-templates` — browse all available prompt templates

---

## Project Structure

```
.cursor/
├── rules/                         ← Always-applied agent rules
│   ├── agent.mdc                  ← Core agent identity & behavior
│   ├── domain.mdc                 ← Physics/math/mechanics expertise
│   ├── safety.mdc                 ← Academic integrity guardrails
│   └── tools.mdc                  ← How to execute Python tools
└── skills/                        ← Agent Skills (auto-discovered)
    ├── solve-problem/SKILL.md     ← 7-step problem solving protocol
    ├── find-examples/SKILL.md     ← Find matching textbook examples
    ├── explain-concept/SKILL.md   ← Conceptual explanations
    ├── latex-output/SKILL.md      ← LaTeX formatting conventions
    ├── research-workflow/SKILL.md ← Full research pipeline
    ├── problem-solving/SKILL.md   ← Quick focused problem solving
    ├── source-verification/SKILL.md ← Verify sources before citing
    └── task-templates/SKILL.md    ← Pre-built prompt templates

tools/                             ← Python tools (shared scripts)
├── __init__.py                    ← Package exports
├── web_search.py                  ← Semantic Scholar + arXiv + OpenLibrary
├── wolfram_query.py               ← Wolfram Alpha symbolic math
├── book_finder.py                 ← OpenLibrary + Google Books lookup
└── latex_renderer.py              ← LaTeX formatting & doc generation

.tmp/                              ← Agent scratch space (gitignored)
├── *.tex                          ← Generated LaTeX documents
├── *.md                           ← Search results, verifications
└── *.py                           ← Temporary helper scripts

memory/
└── context_store.json             ← Persistent context across sessions

prompts/
└── system_prompt.md               ← Master system prompt reference
```

---

## Skills

Skills follow the [Cursor Agent Skills standard](https://cursor.com/docs/context/skills). Each skill is a folder under `.cursor/skills/` containing a `SKILL.md` file with YAML frontmatter.

| Skill | Invocation | Auto-invoked? | Description |
|-------|-----------|---------------|-------------|
| **solve-problem** | `/solve-problem` | ✅ Yes | 7-step protocol: Identify → Knowns → Principle → Setup → Solve → Check → Reference |
| **find-examples** | `/find-examples` | ✅ Yes | Search known textbooks, OpenLibrary, Google Books, Semantic Scholar, arXiv |
| **explain-concept** | `/explain-concept` | ✅ Yes | Definition → Equations → Intuition → Derivation → Example → Pitfalls |
| **latex-output** | `/latex-output` | ✅ Yes | LaTeX conventions, templates, document generation |
| **research-workflow** | `/research-workflow` | ✅ Yes | Full pipeline: classify → solve → search → verify → format |
| **problem-solving** | `/problem-solving` | ✅ Yes | Quick solving without full research pipeline |
| **source-verification** | `/source-verification` | ✅ Yes | Verify sources exist and are relevant before citing |
| **task-templates** | `/task-templates` | ❌ Manual only | Browse 7 pre-built prompt templates |

---

## Tools & APIs

| Tool | Cost | What It Does |
|------|------|-------------|
| **Semantic Scholar API** | Free | Find academic papers & books |
| **arXiv API** | Free | Physics/math preprints |
| **OpenLibrary API** | Free | Textbook lookup |
| **Google Books API** | Free | Textbook search with previews |
| **Wolfram Alpha API** | Free tier | Symbolic math solving & verification |

### Testing Tools from CLI

```bash
# Search for academic sources
python tools/web_search.py "moment of inertia composite body worked example"

# Find textbooks
python tools/book_finder.py "engineering mechanics statics moment"

# Query Wolfram Alpha (requires WOLFRAM_APP_ID)
python tools/wolfram_query.py "integrate x^2 sin(x) dx"

# Demo LaTeX renderer
python tools/latex_renderer.py
```

---

## Supported Domains

### Mechanics
Statics, dynamics, rigid body motion, Lagrangian/Hamiltonian mechanics, vibrations, fluid mechanics, structural mechanics

### Physics
Classical mechanics, thermodynamics, electromagnetism, wave mechanics, quantum basics, special relativity

### Mathematics
Calculus, ODEs, PDEs, linear algebra, vector calculus, Fourier series, numerical methods
