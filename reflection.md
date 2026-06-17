# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

When I ran the game the first time, the game looked like any normal number guessing game. However, one thing that I noticed after playing my first round was that the hints were misleading. For example, if I guessed 5, I would be told to guess a number that is higher. However, upon ending the round, I would find out that the actual number was below 5. Another bug that I discovered was that when I tried to start a new game, nothing happened. This meant that I had to refresh the page to play another game. Out of curiosity, I also found out that you are allowed to guess numbers outside the range of 1 and 100, which I believe is unintentional. 

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |

|-------|-------------------|-----------------|------------------------|

|Guess: 50, Secret: 24|Hint: go lower | Hint: Go higher |none |

|New Game |Starts new game |nothing happens |none |

|Guess: -1 |Guess is rejected |Gues is accepted |none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

On this project I used Claude. One suggestion that was correct was making it so that a new game can be created. Previously, this was not the case, and the website had to be refreshed. I verified that the suggestion addressed this bug by playing a game and clicking "New Game" to see if a new game was created. Doing this, I found out that the AI's suggestion was correct. One AI suggestion that was incorrect was fixing the range of acceptable guesses. At first, I thought that the AI correctly addressed this issue. I tested by playing a game and giving numbers that were ridiculously small or large, to which the game accepted these values. This is how I knew that the bug persisted. So, I went back to the AI and mentioned this persistent bug, to which the AI addressed it once more. After testing once more, the bug was resolved! 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

To determine whether a bug was really fixed, I had to play the game for myself and ask myself, "Does this behavior make sense?". One manual test that I ran was that making sure that the hints were not misleading. Prior, I had the AI address this bug, so testing it was the first thing that I decided to do to make sure that the AI did not make the bug worse or make no significant change. When I played the game, I found that the hints were still misleading. Doing this manual test helped me to understand that there were still bugs in the code. Mentioning this to the AI, I mentioned the persistence of this bug, to which it addressed it again. Then, it was finally fixed after another round of manual testing. The AI helped me to design  automated tests in the test_game_logic.py file, tackling different edge cases. 

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit reruns work in that whenever you interact with something on the page that you are on, Streamlit reruns the entire script from top to bottom to reflect the change that was made. Because variables are reinitialized due to Streamlit reruns, session state allows certain variables to persist across reruns, such as the secret number that you are trying to guess in the game. 

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to reuse in future projects is going back and forth with Claude after edits are made to ensure that changes fixed bugs. One thing I would do differently is consult other AI models to see how different AI's tackle problems, and understand what AI's might be the best for my application. This project changed the way I think about AI generated code because it made me realize that even advanced AI models make mistakes and need our guidance to have the best possible effect on the code that we are working on. 