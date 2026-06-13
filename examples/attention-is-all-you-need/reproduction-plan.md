# Reproduction Plan: Attention Is All You Need

## Reproduction Target

- Exact claim to reproduce: Transformer machine translation quality on WMT 2014 English-German or English-French.
- Practical first target: implement a minimal Transformer and validate it on a tiny synthetic or small translation task.
- Success metric for first target: model overfits a tiny dataset, masks behave correctly, loss decreases, and generated outputs are plausible.
- Success metric for faithful target: BLEU under a documented tokenization and evaluation pipeline.

## Scope Decision

Do not start by trying to reproduce the full headline BLEU. Start by reproducing the mechanism:

1. scaled dot-product attention
2. multi-head attention
3. encoder block
4. decoder block with causal mask
5. encoder-decoder attention
6. training loop with warmup schedule
7. BLEU evaluation path

## Dependencies

| Area | Needed | Source / uncertainty |
| --- | --- | --- |
| Data | WMT 2014 En-De or En-Fr for faithful run; small translation/copy task for sanity check. | Dataset preprocessing must match the paper or a documented reproduction. |
| Tokenization | BPE or modern subword tokenizer. | Exact vocabulary and preprocessing affect BLEU. |
| Model | Transformer encoder-decoder with multi-head attention and positional encoding. | Architecture is clear enough to implement from the paper. |
| Training | Adam-style optimizer, warmup schedule, dropout, label smoothing. | Hyperparameters need careful source matching. |
| Evaluation | BLEU implementation and decoding configuration. | BLEU can differ across tokenization and script versions. |
| Compute | Small educational run can use one GPU or CPU for toy data; faithful reproduction needs more. | Original setup used multiple GPUs for headline results. |

## Implementation Modules

| Module | Responsibility | Inputs | Outputs | Risk |
| --- | --- | --- | --- | --- |
| `tokenizer.py` | Train/load subword tokenizer and encode data. | Raw parallel text. | Token IDs and vocabulary. | High for faithful BLEU. |
| `data.py` | Batch, pad, create masks. | Tokenized source/target pairs. | Batches and masks. | Mask shape bugs are common. |
| `attention.py` | Scaled dot-product and multi-head attention. | Q/K/V tensors and mask. | Context tensors. | Softmax mask broadcasting. |
| `model.py` | Encoder, decoder, embeddings, positional encoding. | Source and target token IDs. | Logits. | Residual/norm order differences. |
| `train.py` | Loss, optimizer, schedule, checkpointing. | Batches and model. | Trained checkpoints. | Learning-rate schedule instability. |
| `decode.py` | Greedy or beam decoding. | Source sentence and checkpoint. | Generated target text. | Beam details change BLEU. |
| `eval.py` | BLEU and sanity metrics. | Predictions and references. | Scores. | Tokenization mismatch. |

## Build Order

1. Implement tensor-only attention and test shapes.
2. Add causal mask tests for decoder self-attention.
3. Build one encoder block and one decoder block.
4. Train on a copy task until it overfits.
5. Add a tiny translation dataset and verify end-to-end generation.
6. Add BLEU evaluation.
7. Add paper-like hyperparameters only after the minimal loop is stable.

## Sanity Checks

- Attention weights sum to 1 over non-masked positions.
- Causal mask prevents token `t` from attending to positions greater than `t`.
- Padding mask prevents attention to padded tokens.
- Tiny model overfits 32 examples.
- Loss decreases before trying beam search.
- Greedy decoding works before beam decoding.
- BLEU script is fixed and documented.

## Missing Details To Resolve

| Missing detail | Why it matters | How to resolve |
| --- | --- | --- |
| Exact preprocessing pipeline | Tokenization changes BLEU substantially. | Use a known WMT preprocessing recipe and document it. |
| Decoding parameters | Beam size and length penalty affect reported results. | Match paper details or state a modern baseline. |
| Model variant | Base vs big changes compute and results. | Reproduce base first. |
| Evaluation script | BLEU implementations differ. | Pin one script/version in the README. |
| Hardware budget | Full reproduction may be expensive. | Separate educational reproduction from faithful benchmark. |

## Reproduction Risks

- Hidden preprocessing differences can dominate final score.
- Exact BLEU may not match due to data version, tokenization, or evaluation script.
- Large batch schedule and warmup may not transfer to small-batch training.
- A correct architecture can still underperform if decoding is not matched.
- Modern libraries may use slightly different layer normalization ordering or initialization defaults.

## Minimal Repo Plan

```text
transformer-repro/
  README.md
  pyproject.toml
  src/
    transformer_repro/
      attention.py
      model.py
      data.py
      train.py
      decode.py
      eval.py
  tests/
    test_attention.py
    test_masks.py
    test_overfit.py
  configs/
    tiny-copy.yaml
    wmt14-base.yaml
```

## First Three Days

| Day | Goal | Done when |
| --- | --- | --- |
| 1 | Implement attention, masks, positional encoding, and shape tests. | Unit tests pass and a forward pass returns logits. |
| 2 | Train tiny encoder-decoder on copy/reversal data. | Model overfits a tiny dataset and greedy decode works. |
| 3 | Add small translation data path and BLEU evaluation. | End-to-end training/evaluation command is documented. |

## What I Would Build First

Build `attention.py` and `test_masks.py`. Most later failures become confusing if masking is wrong, so the first useful artifact is a reliable attention module with explicit shape and mask tests.
