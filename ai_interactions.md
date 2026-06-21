# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|

|negative numbers |ok, lets go after some edge cases such as negative numbers, decimals, or extreme values. what are two other edge cases? now with all of these edge cases, create new tests for them in the test_game_logic.py file
 |test_negative_number_parses_but_is_out_of_range() & test_negative_secret_comparison_is_numeric() |yes |this edge case was chosen to see if negative numbers are rejected by the game, which they should be since they would be out of range|

|decimals |(same prompt as first) |test_positive_decimal_is_rejected() & test_negative_decimal_is_rejected() & test_whole_valued_decimal_is_rejected() |yes |this edge case was chosen to see if decimal numbers are rejected by the game, which they should be since decimal values indicate an infinite number of possible guesses|

|extreme values |(same prompt as first) |test_extremely_large_value_parses_but_is_out_of_range() & test_scientific_overflow_is_rejected_gracefully() & test_is_in_range_handles_extremes() |yes |this edge case was chosen to see if extreme values like unnecessarily large numbers are rejected, which they should be considering they would be out of range |

|strange formatting |(same prompt as first) |test_whitespace_padded_number_is_accepted() & test_plus_sign_and_leading_zeros_accepted() |yes |this edge case was chosen to see if cases with plus signs or whitespace are accepted, to which guesses with these should pass since they do not affect the actual guess|

|junk values| (same prompt as first)|test_scientific_notation_with_dot_is_rejected() & test_scientific_notation_without_dot_is_rejected() & test_whitespace_only_is_rejected() & test_thousands_separator_is_rejected() & test_nan_text_is_rejected() |yes |this edge case was chosen to see if random "junk" values rejected by the game, which they normally should be |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
