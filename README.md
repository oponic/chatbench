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

## Running

```sh
# Offline smoke test (echoes the prompt; fails everything by design):
python run.py --model echo --verbose

# Against the Claude API (needs ANTHROPIC_API_KEY and `pip install anthropic`):
python run.py --model anthropic                       # default: claude-opus-4-8
python run.py --model anthropic:claude-sonnet-4-6 --verbose
python run.py --model anthropic --categories inflection in_context_learning
python run.py --model anthropic --json results.json   # dump full per-task output
```

Output is a per-category and overall pass rate.

## Task format

Each line of a `.jsonl` file is one task:

```json
{"id": "fr-001", "category": "factual_recall",
 "prompt": "What is the chemical symbol for gold? Answer with only the symbol.",
 "grader": [{"check": "regex", "pattern": "^\\s*Au\\s*$"}]}
```

Multi-turn tasks use `turns` (a list of user messages) instead of `prompt`; the
final assistant reply is graded:

```json
{"id": "in-001", "category": "inflection",
 "turns": ["My favorite number is 7.", "Change it to 12.", "What is it? Just the number."],
 "grader": [{"check": "regex", "pattern": "^\\s*12\\s*$"}]}
```

A task **passes only if every check in its `grader` list passes.**

### Check types

| `check` | Fields | Passes when |
|---|---|---|
| `exact` | `value` | normalized (trim+lowercase) answer equals value |
| `regex` | `pattern` | pattern found in answer (`re.search`) |
| `contains_all` | `values` | all strings present (case-insensitive) |
| `contains_any` | `values` | at least one string present |
| `not_contains` | `values`, optional `case_sensitive` | none of the strings present |
| `json_valid` | — | answer parses as JSON |
| `json_keys` | `values` | answer is a JSON object containing all named keys |

## Adding a model

Implement the `Model` protocol in `chatbench/models.py` (a `reply(messages)`
method returning a string) and wire it into `load_model`. Adapters take standard
chat messages: `[{"role": "user"|"assistant", "content": str}, ...]`.

## Layout

```
run.py                  CLI entry point
chatbench/models.py     model adapters (echo, anthropic)
chatbench/runner.py     task loading + conversation driving
chatbench/scorer.py     deterministic graders
tasks/*.jsonl           the benchmark tasks
```
