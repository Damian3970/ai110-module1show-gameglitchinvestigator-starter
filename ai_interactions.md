# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I prompted Claude to "implement a feature such that it tracks guess history from previous games, showing the guesses for that game and the secret number". 

**What did the agent do?**

1. Added function in logic_utils.py to create game record
2. Added another function in the same file to display game status for past games (win vs. loss)
3. Edited app.py to allow append previous match data in order when a new game is created

**What did you have to verify or fix manually?**

I had to manually verify that the feature was successfully implemented. I played a few games and found a drop-down feature in the game that showed me previous games that I played, my guesses, and whether or not I guessed the secret number. 
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
now, review the code for PEP 8 style compliance and apply its suggestions to resolve any formatting or naming issues it identifies

```

**Linting output before:**

(Tool used: `pycodestyle`, run with
`python -m pycodestyle app.py logic_utils.py tests/test_game_logic.py`)

```
app.py:43:34: E261 at least two spaces before inline comment
app.py:43:35: E262 inline comment should start with '# '
app.py:60:49: E261 at least two spaces before inline comment
app.py:60:50: E262 inline comment should start with '# '
app.py:89:56: E261 at least two spaces before inline comment
app.py:89:57: E262 inline comment should start with '# '
app.py:90:31: E261 at least two spaces before inline comment
app.py:90:32: E262 inline comment should start with '# '
app.py:109:48: E261 at least two spaces before inline comment
app.py:109:49: E262 inline comment should start with '# '
app.py:115:75: E261 at least two spaces before inline comment
app.py:115:76: E262 inline comment should start with '# '
app.py:115:101: E501 line too long (115 > 100 characters)
app.py:142:42: E261 at least two spaces before inline comment
app.py:142:43: E262 inline comment should start with '# '
logic_utils.py:1:1: E265 block comment should start with '# '
tests/test_game_logic.py:14:1: E402 module level import not at top of file
tests/test_game_logic.py:29:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:132:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:135:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:141:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:191:72: W292 no newline at end of file

(A second pass at PEP 8's strict 79-char limit also flagged 6 more
E501 "line too long" warnings, all 80-85 characters.)
```

**Linting output after:**

```
$ python -m pycodestyle app.py logic_utils.py tests/test_game_logic.py
(no output — 0 violations)
```

**Changes applied:**

- **E261 / E262 (inline comments):** reformatted the `#FIX:` notes to the
  PEP 8 style `  # FIX:` (two spaces before the `#`, one space after).
- **E265 (block comment):** fixed the top-of-file `#FIX:` comment to `# FIX:`.
- **E501 (line too long):** moved long inline `# FIX:` comments onto their own
  line above the code, and wrapped two long test `assert` statements.
- **E302 (blank lines):** restored two blank lines between test functions.
- **E402 (import not at top):** the `logic_utils` import must come after the
  `sys.path` setup, so I added `# noqa: E402` with an explanatory note rather
  than reordering (which would break the import).
- **W292 (newline at EOF):** added the missing trailing newline.
- **Naming:** no changes needed — all names already use `snake_case`.

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
