<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:020617,45:4338ca,100:0f766e&height=190&section=header&text=Paper%20to%20Notes&fontSize=44&fontColor=ffffff&fontAlignY=38&desc=Turn%20research%20papers%20into%20notes%2C%20method%20maps%2C%20and%20reproduction%20plans.&descSize=15&descAlignY=60&animation=fadeIn" alt="Paper to Notes" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Codex-Skill-0f172a?style=for-the-badge&logo=openai&logoColor=white" alt="Codex Skill" />
  <img src="https://img.shields.io/badge/Use%20Case-Research%20Reading-4338ca?style=for-the-badge" alt="Research Reading" />
  <img src="https://img.shields.io/badge/Output-Reproduction%20Plan-0f766e?style=for-the-badge" alt="Reproduction Plan" />
  <img src="https://img.shields.io/badge/License-MIT-111827?style=for-the-badge" alt="MIT License" />
</p>

`paper-to-notes` is a Codex skill for turning research papers into useful working notes: method breakdowns, experiment summaries, limitations, reproduction plans, implementation roadmaps, and follow-up questions.

## Why This Exists

很多论文摘要都太浅：读完只知道“这篇文章大概讲什么”，但不知道方法怎么跑、实验怎么设计、能不能复现、下一步该问什么。

这个 skill 的目标是让 Codex 像一个认真读 paper 的研究助理：

- 先识别论文的问题、贡献和方法机制
- 再拆实验、数据集、指标、baseline 和局限
- 最后产出可以继续行动的笔记或复现计划

It is useful for students, researchers, engineers, and anyone trying to move from "I skimmed the paper" to "I understand what to build or verify next."

## What It Produces

| Need | Output |
| --- | --- |
| Understand one paper | Structured notes with TL;DR, contribution, method, experiments, limitations, and questions |
| Implement a paper | Module breakdown, build order, sanity checks, missing details, and reproduction risks |
| Compare papers | Problem/method/result matrix and recommendation |
| Study a method | Plain-language explanation plus exact technical structure |
| Review a paper | Strengths, weaknesses, evidence quality, and threats to validity |

## Install

Copy the skill folder into your Codex skills directory:

```bash
cp -R paper-to-notes ~/.codex/skills/paper-to-notes
```

Then invoke it in Codex:

```text
Use $paper-to-notes to analyze this research paper into structured notes, a method breakdown, and a reproduction plan.
```

## Example Prompts

```text
Use $paper-to-notes on this PDF. I want study notes plus a reproduction checklist.
```

```text
Use $paper-to-notes to compare these three papers and tell me which one is best to implement first.
```

```text
Use $paper-to-notes. Explain the method section like I need to code it, but keep the exact technical details.
```

中文也可以：

```text
使用 $paper-to-notes 阅读这篇论文，输出中文笔记、方法流程、实验表格和复现计划。
```

## Included Resources

```text
paper-to-notes/
  SKILL.md
  agents/openai.yaml
  references/
    note-template.md
    reproduction-checklist.md
    comparison-matrix.md
  scripts/
    extract_pdf_text.py
```

The PDF script tries common extraction backends and keeps page markers:

```bash
python paper-to-notes/scripts/extract_pdf_text.py paper.pdf --out paper.txt
```

## Design Principles

- Stay grounded in the paper text.
- Separate author claims from interpretation.
- Keep enough technical detail for implementation.
- Treat missing details as explicit unknowns.
- Produce notes that can become code, review, or study material.

## License

MIT
