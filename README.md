# ChatBench

A small agent benchmark covering five skills:

| Category | File | What it probes |
|---|---|---|
| **Factual recall** | `tasks/factual_recall.jsonl` | Basic facts answered directly. |
| **Deep research** | `tasks/deep_research.jsonl` | Multi-hop questions requiring an intermediate inference before the answer. |
| **Instruction following** | `tasks/instruction_following.jsonl` | Strict output-format constraints (exact text, JSON, character bans). |
| **Inflection** | `tasks/inflection.jsonl` | Multi-turn conversations where instructions or state change mid-stream; the model must track the *latest* state. |
| **In-context learning** | `tasks/in_context_learning.jsonl` | Inferring a novel rule/operator from examples and applying it. |

37 tasks total. Grading is deterministic (regex / substring / JSON checks), so runs are reproducible and need no judge model.
