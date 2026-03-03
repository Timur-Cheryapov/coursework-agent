---
name: task-templates
description: Pre-built prompt templates for common coursework requests. Use when the user needs help structuring their request, or invoke directly to see available templates for finding examples, solving problems, explaining concepts, running research workflows, verifying solutions, formatting LaTeX, and comparing methods.
disable-model-invocation: true
---

# 📋 Task Templates

Pre-built prompt templates for common student requests. Use these as starting points — customize based on the specific problem.

## When to Use

- Use when the user wants to see available template formats
- Use when the user needs help structuring a request
- Invoke directly with `/task-templates` to browse templates

## Templates

### Template 1: "Find Example of X"

**Trigger Phrases:** "Find me an example of...", "Where can I find a worked example of...", "Which textbook has examples of..."

```
I need to find textbook examples that match this problem type:

**Problem type:** [describe the type of problem]
**Specific topic:** [e.g., moment of inertia of composite bodies]
**Course level:** [e.g., 2nd year engineering]

Please:
1. Search for matching textbook examples using /find-examples
2. Rank results by how closely they match my exact problem type
3. For each result, tell me which textbook/chapter/section and what the example covers
4. Suggest the top 3 most relevant sources
```

---

### Template 2: "Solve Problem Y"

**Trigger Phrases:** "Solve this problem...", "Help me with this question...", "Can you work through this..."

```
Please solve this problem step by step:

**Problem:** [paste the problem statement]

Follow the full problem-solving protocol:
1. Classify the problem type
2. List knowns and unknowns
3. State the governing principle
4. Show complete setup (FBD / coordinate system)
5. Solve with full algebraic working in LaTeX
6. Verify with dimensional analysis and sanity check
7. Reference relevant textbook examples
```

---

### Template 3: "Explain Concept Z"

**Trigger Phrases:** "Explain...", "What is...", "How does... work?", "Why do we use..."

```
I need a clear explanation of:

**Concept:** [name the concept]
**Context:** [what course/topic this comes up in]
**My current understanding:** [what I already know / what confuses me]

Please:
1. Define the concept clearly
2. Show the key equation(s) and explain every symbol
3. Derive it from first principles
4. Give a concrete numerical example
5. List common mistakes students make
6. Suggest textbook sections for further reading
```

---

### Template 4: "Run Research Workflow"

**Trigger Phrases:** "Research this problem", "Run research workflow on this", "Full analysis of this task"

```
Run the full research workflow on this coursework task:

**Task:** [paste the full coursework brief / problem statement]

I need:
1. Complete worked solution with full LaTeX formatting
2. Wolfram Alpha verification of the answer
3. 3-5 specific textbook references with matching examples
4. Assessment of difficulty and topic classification
5. Any additional sources (papers, lecture notes) that have similar problems
```

---

### Template 5: "Verify My Solution"

**Trigger Phrases:** "Check my answer...", "Is this correct?", "Verify my solution..."

```
Please verify my solution to this problem:

**Problem:** [paste problem]
**My solution:** [paste your working/answer]

Please:
1. Check if my approach is correct
2. Verify each algebraic step
3. Confirm the final answer using Wolfram Alpha
4. Point out any errors and show the correction
5. Suggest improvements to my method if applicable
```

---

### Template 6: "Format in LaTeX"

**Trigger Phrases:** "Format this in LaTeX", "Convert to LaTeX", "Make this report-ready"

```
Please format the following solution in clean LaTeX, ready for my coursework report:

**Content:** [paste your solution/working]

Requirements:
- Use proper LaTeX math environments (align*, equation, etc.)
- Include all units with \text{} formatting
- Box the final answer
- Structure with sections: Given, Find, Approach, Working, Answer
- Add proper references in bibliography format
```

---

### Template 7: "Compare Methods"

**Trigger Phrases:** "What's the difference between...", "Should I use X or Y method?", "Compare approaches for..."

```
Compare different solution methods for this type of problem:

**Problem type:** [describe]
**Method 1:** [e.g., energy method]
**Method 2:** [e.g., Newton's second law]

Please:
1. Solve using both methods (full working)
2. Show that both give the same answer
3. Explain when each method is preferable
4. Note which method is typically expected at my course level
```
