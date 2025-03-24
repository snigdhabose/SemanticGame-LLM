# SemanticGame-LLM


## Overview
This project implements a **Semantic Game** using the `mistralai/Mistral-7B-Instruct-v0.1` model. The game involves two participants: an **Author** and a **Reviewer**, who engage in a structured debate about a numerical claim `τ(RS, FPR)`.

### What the Code Does
- **Author:** Proposes a logical formula `F` in CNF notation and makes a numerical claim for `τ`.
- **Reviewer:** Reviews the formula, either confirming the claim, finding a counterexample, or pointing out logical flaws.
- **Game Loop:** The game runs for 5 rounds where the `τ` value is updated based on the interactions between the Author and Reviewer.

### Prompts Used
1. **Author Prompt:**
You are the Author in a structured debate about τ(RS, FPR). RS = ClausalR(2,2), FPR = TRUE. Propose a complete (RS, FPR)-formula F in CNF notation. Explicitly state a numerical claim for τ. Your output should be:

"Formula F = ..."

"Claimed τ = ..."


2. **Reviewer Prompt:**
You are the Reviewer in a structured debate about τ(RS, FPR). The Author's formula is: {formula}

If the formula is correct, confirm τ.

If incorrect, provide a counterexample assignment that achieves a higher/lower τ.

If the formula is invalid, explain the logical flaw. Your output should be:

"Reviewer Response: ..."

"Revised τ = ..." (if applicable)


### Model Used
The code uses the `mistralai/Mistral-7B-Instruct-v0.1` model which is a LLaMA-based model designed for conversational tasks. It is loaded using the `llama_cpp` library.

---

## How to Run the Code

### 1. Install Dependencies
```bash
pip install llama-cpp-python

```


### 2. Download the Model
Download the model file mistral-7b-instruct-v0.1.Q4_K_M.gguf and place it under the models/ directory.

You can download the model using:
```
from huggingface_hub import snapshot_download
from pathlib import Path

mistral_models_path = Path.home().joinpath('models', 'mistral-7b-instruct-v0.1')
mistral_models_path.mkdir(parents=True, exist_ok=True)

snapshot_download(
    repo_id="mistralai/Mistral-7B-Instruct-v0.1",
    allow_patterns=["params.json", "consolidated.safetensors", "tokenizer.model.v3"],
    local_dir=mistral_models_path
)
```
### 3. Run the Game
```
python Game.py
```

## Current Status
The program successfully runs through all 5 rounds of the game. However, the following issues are observed:

The Reviewer is vague and doesn't provide concrete counterexamples or valid justifications for the τ claim.

The τ value remains constant at 1.0 across all rounds, indicating no meaningful feedback or updates are provided by the Reviewer.

The evaluation mechanism for τ is not yet robust.

### Output
```
Using fallback chat format: llama-2
🎮 **Starting the Semantic Game!** 🎮
🔹 **Round 1** 🔹
llama_perf_context_print:        load time =   14544.25 ms
llama_perf_context_print: prompt eval time =   14543.84 ms /   105 tokens (  138.51 ms per token,     7.22 tokens per second)
llama_perf_context_print:        eval time = 1230578.41 ms /    99 runs   (12430.08 ms per token,     0.08 tokens per second)
llama_perf_context_print:       total time = 1245215.52 ms /   204 tokens
📜 **Author's formula & τ claim:**
3. "Proof of claim τ = ..."
            (Note: "Formula F" should be in CNF notation, "Claimed τ" should be a numerical value, and "Proof of claim τ" should be a detailed proof.)
            Example:
            1. "Formula F = (p ∧ ¬q) ∨ (¬p ∧ q)"
            2. "Claimed τ =
Llama.generate: 7 prefix-match hit, remaining 214 prompt tokens to eval
llama_perf_context_print:        load time =   14544.25 ms
llama_perf_context_print: prompt eval time =   10929.99 ms /   214 tokens (   51.07 ms per token,    19.58 tokens per second)
llama_perf_context_print:        eval time = 1233338.34 ms /    99 runs   (12457.96 ms per token,     0.08 tokens per second)
llama_perf_context_print:       total time = 1244357.79 ms /   313 tokens
🔎 **Reviewer finds issues or better assignment:**
3. "Reviewer's Final Comment (and sign): ..."
            You may also provide a detailed explanation for any of the above points in a separate section, which will be labeled as "Detailed Explanation".
            The Author should submit their revised paper with all the reviewer's comments and suggestions integrated into the paper.
            The reviewer should sign this response to confirm that the authors have incorporated all the suggestions and made the necessary revisions."
📊 **Result of Round 1:** Initial τ estimate: 1.0
🔹 **Round 2** 🔹
Llama.generate: 7 prefix-match hit, remaining 98 prompt tokens to eval
llama_perf_context_print:        load time =   14544.25 ms
llama_perf_context_print: prompt eval time =   10536.11 ms /    98 tokens (  107.51 ms per token,     9.30 tokens per second)
llama_perf_context_print:        eval time = 1255900.00 ms /    99 runs   (12685.86 ms per token,     0.08 tokens per second)
llama_perf_context_print:       total time = 1266538.95 ms /   197 tokens
📜 **Author's formula & τ claim:**
You should provide an argument for your numerical claim.
            
            Hint: τ(RS, FPR) = τ(ClausalR(2,2), TRUE)
            You should use the formula: τ(RS, FPR) = (τ(RS) / τ(FPR)) * τ(RS, FPR).
            You can assume that τ(RS) is already known, and τ(
Llama.generate: 7 prefix-match hit, remaining 212 prompt tokens to eval
llama_perf_context_print:        load time =   14544.25 ms
llama_perf_context_print: prompt eval time =   10897.82 ms /   212 tokens (   51.40 ms per token,    19.45 tokens per second)
llama_perf_context_print:        eval time =  111803.32 ms /     9 runs   (12422.59 ms per token,     0.08 tokens per second)
llama_perf_context_print:       total time =  122708.82 ms /   221 tokens
🔎 **Reviewer finds issues or better assignment:**
3. "Reviewer Response: ..."
📊 **Result of Round 2:** τ remains stable at 1.0.
🔹 **Round 3** 🔹
Llama.generate: 7 prefix-match hit, remaining 98 prompt tokens to eval
llama_perf_context_print:        load time =   14544.25 ms
llama_perf_context_print: prompt eval time =   11361.53 ms /    98 tokens (  115.93 ms per token,     8.63 tokens per second)
llama_perf_context_print:        eval time = 11472846.41 ms /    85 runs   (134974.66 ms per token,     0.01 tokens per second)
llama_perf_context_print:       total time = 11484300.32 ms /   183 tokens
📜 **Author's formula & τ claim:**
3. "Proof: ..."
            (Note: Claims about τ must be stated in terms of the number of possible assignments (for a given clause) and not in terms of the number of variables or clauses.)
            
            (Note: There may be other ways to represent F in CNF notation, but the chosen representation should be consistent with the given RS and FPR.)
Llama.generate: 7 prefix-match hit, remaining 199 prompt tokens to eval
llama_perf_context_print:        load time =   14544.25 ms
llama_perf_context_print: prompt eval time =   10656.78 ms /   199 tokens (   53.55 ms per token,    18.67 tokens per second)
llama_perf_context_print:        eval time =  379067.78 ms /    30 runs   (12635.59 ms per token,     0.08 tokens per second)
llama_perf_context_print:       total time =  389746.60 ms /   229 tokens
🔎 **Reviewer finds issues or better assignment:**
3. "Reviewer Response: ..."
            (Note: If you do not understand the context, please refer to the original paper.)
📊 **Result of Round 3:** τ remains stable at 1.0.
🔹 **Round 4** 🔹
Llama.generate: 7 prefix-match hit, remaining 98 prompt tokens to eval
llama_perf_context_print:        load time =   14544.25 ms
llama_perf_context_print: prompt eval time =    9526.11 ms /    98 tokens (   97.21 ms per token,    10.29 tokens per second)
llama_perf_context_print:        eval time = 1231964.08 ms /    99 runs   (12444.08 ms per token,     0.08 tokens per second)
llama_perf_context_print:       total time = 1241568.07 ms /   197 tokens
📜 **Author's formula & τ claim:**
3. "Proof ..."
            4. "Remarks ..."
            5. "Acknowledgements ..."
            Here's how you can make your submission:
                You may submit your solution in a text file or a README.md file.
                Your solution should contain all the parts listed above.
                You may add any additional details that you think are relevant.
                Please submit your solution as a pull request to
Llama.generate: 7 prefix-match hit, remaining 214 prompt tokens to eval
llama_perf_context_print:        load time =   14544.25 ms
llama_perf_context_print: prompt eval time =   10638.56 ms /   214 tokens (   49.71 ms per token,    20.12 tokens per second)
llama_perf_context_print:        eval time = 1245094.40 ms /    99 runs   (12576.71 ms per token,     0.08 tokens per second)
llama_perf_context_print:       total time = 1255807.73 ms /   313 tokens
🔎 **Reviewer finds issues or better assignment:**
3. "References: ..." (if applicable)
            Please note that the reviewer should not reveal their identity to the author or the public.
            The author can make any revisions to their submission. Once the review is complete, the author can submit a new version of their submission. If the author does not submit a revised version within seven days, the review will be considered closed.
            If the author submits a revised version, the
📊 **Result of Round 4:** τ remains stable at 1.0.
🔹 **Round 5** 🔹
Llama.generate: 7 prefix-match hit, remaining 98 prompt tokens to eval
llama_perf_context_print:        load time =   14544.25 ms
llama_perf_context_print: prompt eval time =    9755.94 ms /    98 tokens (   99.55 ms per token,    10.05 tokens per second)
llama_perf_context_print:        eval time = 1267613.18 ms /    99 runs   (12804.17 ms per token,     0.08 tokens per second)
llama_perf_context_print:       total time = 1277444.64 ms /   197 tokens
📜 **Author's formula & τ claim:**
3. "Proof:"
            [Response]
            1. Formula F = (∃x∃y)(¬∃z)(¬∃w)((¬∃x∃z)(¬∃y∃z)(¬∃w∃z)(¬∃w∃y)(¬∃x∃w)(¬∃y∃w
Llama.generate: 7 prefix-match hit, remaining 214 prompt tokens to eval
llama_perf_context_print:        load time =   14544.25 ms
llama_perf_context_print: prompt eval time =   11207.71 ms /   214 tokens (   52.37 ms per token,    19.09 tokens per second)
llama_perf_context_print:        eval time =  169285.36 ms /    13 runs   (13021.95 ms per token,     0.08 tokens per second)
llama_perf_context_print:       total time =  180502.83 ms /   227 tokens
🔎 **Reviewer finds issues or better assignment:**
3. "Explanation: ..." (if applicable)
📊 **Result of Round 5:** τ remains stable at 1.0.
🏁 **Game Over! Final τ(RS, FPR) estimate: 1.0**
📈 Evolution of τ: [1.0, 1.0, 1.0, 1.0, 1.0]
ggml_metal_free: deallocating

```


