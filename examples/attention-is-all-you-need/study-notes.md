# Study Notes: Attention Is All You Need

## Paper

- Title: Attention Is All You Need
- Authors: Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin
- Venue / year: NeurIPS 2017
- Sources: [arXiv:1706.03762](https://arxiv.org/abs/1706.03762), [NeurIPS proceedings](https://papers.nips.cc/paper/7181-attention-is-all-you-need)
- Paper type: architecture paper with machine translation experiments
- Main topic: sequence transduction without recurrence or convolution

## TL;DR

The paper introduces the Transformer, an encoder-decoder architecture built around attention rather than recurrent or convolutional sequence processing. Its central claim is that self-attention can model token relationships while enabling much more parallel training. The evidence comes mainly from WMT 2014 English-German and English-French machine translation experiments, plus a smaller parsing generalization check. The key caveat is that the paper proves the idea in translation-focused settings; later general-purpose language-model success is downstream of this work, not directly established by these experiments.

## One-Sentence Contribution

> This paper contributes a fully attention-based encoder-decoder architecture that replaces recurrent and convolutional sequence modeling with multi-head self-attention, positional encodings, residual paths, and position-wise feed-forward layers.

## Problem And Motivation

- Sequence-to-sequence models before this paper relied heavily on recurrence, convolution, or attention added on top of those structures.
- Recurrence makes training less parallel because later hidden states depend on earlier steps.
- Convolution improves parallelism but needs depth or large kernels to connect distant positions.
- The paper asks whether attention alone can handle sequence transduction efficiently and accurately.

## Core Ideas

| Idea | Explanation | Why it matters |
| --- | --- | --- |
| Scaled dot-product attention | Queries compare against keys, produce weights, then mix values. The score is scaled by key dimension. | Gives a simple differentiable routing mechanism between tokens. |
| Multi-head attention | Several attention projections run in parallel, then concatenate. | Lets the model attend to different relationship types or positions simultaneously. |
| Self-attention | Query, key, and value come from the same sequence. | Allows each token to aggregate information from other tokens in the sequence. |
| Encoder-decoder attention | Decoder queries attend over encoder outputs. | Lets generated target tokens condition on source sentence representations. |
| Positional encoding | Add position signals to token embeddings. | Attention alone is order-agnostic, so position must be injected. |
| Position-wise feed-forward layer | Same small MLP applied independently to every position. | Adds nonlinear transformation after attention mixing. |

## Method Breakdown

### Inputs

- Source token sequence, usually byte-pair encoded for translation.
- Target token sequence shifted during teacher-forced training.
- Token embeddings plus positional encodings.

### Process

1. Embed source tokens and add positional encodings.
2. Pass the source sequence through stacked encoder blocks.
3. Each encoder block applies multi-head self-attention, residual connection, layer normalization, feed-forward layer, another residual connection, and another normalization.
4. Embed previous target tokens and add positional encodings.
5. Pass target states through decoder blocks with masked self-attention, encoder-decoder attention, and feed-forward layers.
6. Project decoder states to vocabulary logits and train with cross-entropy-style objective plus label smoothing.

### Outputs

- Token probabilities for the next target token.
- A full translated sequence during decoding.
- Attention maps that can be inspected, though the paper does not make interpretability the main result.

## Key Equations / Algorithms

| Item | Plain-language meaning | Implementation hint |
| --- | --- | --- |
| Scaled dot-product attention | Convert query-key similarity into weights over values. | `softmax(Q @ K.T / sqrt(d_k)) @ V` |
| Multi-head attention | Run several attention projections, concatenate, project back. | Split hidden size across heads; keep shape checks strict. |
| Sinusoidal positional encoding | Use sine/cosine functions at different frequencies to encode position. | Precompute table or generate on the fly. |
| Masked decoder attention | Prevent target positions from seeing future target tokens. | Add causal mask before softmax. |

## Experiments

| Task | Dataset / setting | Baselines | Metric | Reported result |
| --- | --- | --- | --- | --- |
| Machine translation | WMT 2014 English-German | Prior recurrent/convolutional systems and ensembles | BLEU | arXiv abstract reports 28.4 BLEU for the model; NeurIPS abstract reports 27.5 BLEU for a single model. |
| Machine translation | WMT 2014 English-French | Prior state-of-the-art systems | BLEU | arXiv abstract reports 41.8 BLEU after 3.5 days on eight GPUs; NeurIPS abstract reports 41.1 BLEU. |
| Parsing | English constituency parsing | Task-specific comparison systems | Parsing score | Used as evidence that Transformer can generalize beyond translation. |

Source note: the arXiv page and NeurIPS proceedings present slightly different headline BLEU numbers, likely because they refer to different paper versions or reporting contexts. A careful reader should cite the exact source used.

## Strengths

- The architecture is conceptually clean and easier to parallelize than recurrent sequence models.
- The paper pairs architectural novelty with strong machine translation results.
- The method became modular: attention, feed-forward blocks, layer normalization, residuals, and positional encoding can be studied independently.
- The reproduction path is realistic at small scale because a minimal Transformer can be implemented without specialized sequence recurrence kernels.

## Limitations

- The headline evidence is concentrated on machine translation.
- Compute and data details matter; reproducing exact BLEU is much harder than reproducing the architecture.
- The paper does not settle how attention-only architectures behave under modern large-scale pretraining.
- Interpretability of attention patterns is shown suggestively, not established as a rigorous explanation method.

## Reproduction Notes

- Data needed: WMT 2014 translation data for faithful reproduction; a toy parallel corpus is enough for architecture validation.
- Code needed: tokenizer/BPE, dataset pipeline, Transformer model, optimizer schedule, masking, BLEU evaluation.
- Compute likely needed: exact headline reproduction requires substantial GPU resources; educational reproduction can run much smaller.
- Hardest missing detail: matching preprocessing, tokenization, batching, and evaluation protocol precisely.
- Minimal reproduction target: train a tiny Transformer on a small translation or copy/reversal task and verify the model overfits a tiny subset.

## Questions To Ask Next

1. Which result should be treated as the reproduction target: arXiv version, NeurIPS proceedings, or a modern implementation baseline?
2. How much of the performance comes from architecture versus preprocessing, schedule, label smoothing, and batch size?
3. What failure modes appear when sequence length grows?
4. How do learned positional embeddings compare to sinusoidal encoding in the same setup?
5. How stable is training when model size and warmup schedule are changed?

## Confidence Notes

- Well-supported by the paper: the architecture components, translation tasks, and reported headline BLEU claims.
- Inferred from context: practical implementation difficulty and modern educational reproduction strategy.
- Unclear without deeper source inspection: exact preprocessing details needed to match original BLEU.
