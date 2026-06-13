# Reproduction And Implementation Checklist

Use this when the user asks to reproduce, implement, train, evaluate, or turn a paper into code.

## Reproduction Target

- Exact claim/result to reproduce:
- Minimal version worth building first:
- Success metric:
- Acceptable approximation:

## Dependencies

| Area | Needed | Source / uncertainty |
| --- | --- | --- |
| Data |  |  |
| Model / method |  |  |
| Training code |  |  |
| Evaluation code |  |  |
| Hardware / compute |  |  |
| Pretrained weights |  |  |

## Implementation Modules

| Module | Responsibility | Inputs | Outputs | Risk |
| --- | --- | --- | --- | --- |
| Data loader |  |  |  |  |
| Preprocessing |  |  |  |  |
| Model / algorithm |  |  |  |  |
| Training or optimization loop |  |  |  |  |
| Evaluation |  |  |  |  |
| Experiment config |  |  |  |  |

## Build Order

1. Recreate the smallest data path.
2. Implement the core method without optimization tricks.
3. Add evaluation metrics.
4. Match one baseline or sanity check.
5. Add ablations and scaling details only after the minimal loop works.

## Sanity Checks

- Can the data loader read a tiny sample?
- Do tensor shapes / schemas match the method description?
- Does a random or trivial baseline run?
- Does the metric implementation match the paper?
- Does the model overfit a tiny subset when expected?
- Are seeds, splits, preprocessing, and evaluation protocols controlled?

## Missing Details To Resolve

| Missing detail | Why it matters | How to resolve |
| --- | --- | --- |
|  |  |  |

## Reproduction Risks

- Hidden preprocessing:
- Ambiguous hyperparameters:
- Unreleased data or weights:
- Compute mismatch:
- Evaluation mismatch:
- Non-determinism:

## Final Plan

Summarize the reproduction as:

- Day 1:
- Day 2:
- Day 3:
- Stretch goals:
