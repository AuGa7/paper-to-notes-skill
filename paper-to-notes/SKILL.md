---
name: paper-to-notes
description: Transform research papers, arXiv PDFs, academic articles, technical reports, or pasted paper text into structured study notes, method breakdowns, experiment summaries, reproduction plans, implementation roadmaps, literature review matrices, and follow-up question lists. Use when the user asks to read, analyze, explain, summarize, compare, reproduce, implement, or review a research paper or technical paper.
---

# Paper To Notes

## Goal

Turn a paper into useful research work products, not a shallow abstract rewrite. Extract what the paper claims, how the method works, what evidence supports it, what is missing, and what a reader would need to reproduce or implement it.

## Source Handling

1. Identify the input type.
   - For a local PDF, run `scripts/extract_pdf_text.py` when text is not already available.
   - For pasted text, use the supplied text directly and ask for the PDF only if figures, equations, or tables are essential.
   - For a URL, DOI, or arXiv link, retrieve the paper when browsing is available or ask the user for the PDF/text when it is not.
   - For multiple papers, switch to comparison mode and build a matrix before writing narrative notes.
2. Preserve evidence.
   - Keep section names, page numbers, table numbers, figure numbers, and equation numbers when available.
   - Distinguish paper-stated facts from your interpretation.
   - Mark unknowns explicitly instead of inventing missing implementation details or results.
3. Detect extraction problems.
   - If the PDF appears scanned or text extraction is poor, report that OCR is needed.
   - If important figures/tables are not readable from text, say which ones need visual inspection.

## Workflow

1. Build a paper map.
   - Extract title, authors, venue/year if available, paper type, keywords, and section outline.
   - Identify the problem, motivation, assumptions, target users or research community, and claimed contributions.

2. Read for mechanism.
   - Explain the method as inputs, transformations, outputs, training or inference loop, and dependencies.
   - Rewrite important formulas in words and define symbols.
   - Convert algorithms, architectures, or pipelines into numbered steps.

3. Read for evidence.
   - Extract datasets, baselines, metrics, experimental setup, ablations, and headline results.
   - Separate quantitative results from qualitative claims.
   - Note missing baselines, weak metrics, limited datasets, compute constraints, and possible threats to validity.

4. Choose the output mode.
   - Use **study notes** by default for one paper.
   - Use **reproduction plan** when the user asks to reproduce, implement, code, train, evaluate, or verify the paper.
   - Use **review memo** when the user asks for strengths, weaknesses, novelty, or whether the paper is convincing.
   - Use **comparison matrix** when the user provides multiple papers or asks for related work.

5. Write the final artifact.
   - Use `references/note-template.md` for single-paper notes.
   - Use `references/reproduction-checklist.md` for reproduction or implementation requests.
   - Use `references/comparison-matrix.md` for multiple papers.
   - Keep the answer structured enough that the user can save it as Markdown.

## Output Rules

- Start with a short TL;DR, then provide the deeper structure.
- Prefer tables for experiments, datasets, baselines, limitations, and implementation tasks.
- Include "What I would verify next" for research judgment and "What I would build first" for implementation work.
- Keep equations and technical terms, but explain them in plain language.
- Do not overclaim. Use phrases like "the paper reports", "the authors argue", and "this suggests" to separate evidence from interpretation.
- If the user wants a beginner-friendly explanation, add analogies only after the exact technical description.

## Bundled Resources

### PDF text extraction

Use the script when a local PDF needs text extraction:

```bash
python paper-to-notes/scripts/extract_pdf_text.py paper.pdf --out paper.txt
```

Useful options:

```bash
python paper-to-notes/scripts/extract_pdf_text.py paper.pdf --max-pages 8
python paper-to-notes/scripts/extract_pdf_text.py paper.pdf --out paper.txt --min-chars 500
python paper-to-notes/scripts/extract_pdf_text.py --self-test
```

The script tries common Python PDF libraries and `pdftotext` if available. If none are installed, tell the user to install one extractor such as `pypdf` or provide copied paper text.

### Templates

- Read `references/note-template.md` when producing full notes for a single paper.
- Read `references/reproduction-checklist.md` when planning implementation, replication, training, evaluation, or code.
- Read `references/comparison-matrix.md` when analyzing two or more papers.

## Quality Checklist

Before finishing, verify that the response includes:

- the paper's actual problem and contribution, not only a generic summary
- method steps detailed enough for another reader to explain or implement
- experiments and results separated from author claims
- limitations and open questions
- reproduction or implementation tasks when relevant
- clear uncertainty notes for anything not supported by the paper text
