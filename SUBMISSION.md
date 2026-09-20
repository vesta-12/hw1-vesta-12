# HW1 submission

**Name:** Serbina Sofiya  
**Student ID:** S23070210  
**Group:** CSS4007-ENG-10  
**Repository:** https://github.com/vesta-12/hw1-vesta-12

## AI tool disclosure

I used ChatGPT mainly for explaining parts of the assignment and for debugging when I had problems with APIs and model availability. All experiments were run by me locally in PyCharm, and the numbers and examples in this report come from my own outputs.

---

## Sublab Easy - the registration bot and its bill

**How I laid the catalogue out inside the system prompt, and why:**

> I used one line per course. Each line contains the course code, title, credits, prerequisites, meeting times, and remaining seats. I chose this format because it is compact and easy to read while still giving the model all the information needed to check eligibility. I also included the student's completed courses, the minimum and maximum credit limits, and explicit rules for prerequisites, full courses, schedule conflicts, and courses that are not in the catalogue.

**My turn 5 (Kazakh or Russian):**

> Мен үшінші курс студентімін. Қай курстарға әлі тіркеле аламын?

### Run 1 — OpenAI, `gpt-5.6-luna`

| Turn | Input tokens | Output tokens | Cost $ |
|---|---:|---:|---:|
| 1 | 513 | 494 | 0.000695 |
| 2 | 747 | 144 | 0.000322 |
| 3 | 834 | 63 | 0.000242 |
| 4 | 916 | 26 | 0.000214 |
| 5 | 970 | 437 | 0.000718 |
| **total** | **3980** | **1164** | **0.002193** |

### Run 2 — OpenRouter, `poolside/laguna-s-2.1:free`

The originally specified `google/gemma-4-26b-a4b-it:free` repeatedly returned HTTP 429 because the upstream Google AI Studio shared pool was rate-limited. I therefore used `poolside/laguna-s-2.1:free` to complete the OpenRouter run with the same client and conversation code.

| Turn | Input tokens | Output tokens | Cost $ |
|---|---:|---:|---:|
| 1 | 605 | 425 | 0.000000 |
| 2 | 1057 | 162 | 0.000000 |
| 3 | 1244 | 202 | 0.000000 |
| 4 | 1469 | 134 | 0.000000 |
| 5 | 1661 | 855 | 0.000000 |
| **total** | **6036** | **1778** | **0.000000** |

### Turn 4, verbatim

The turn where you asked for CSS-4090, which does not exist. Paste both replies exactly as they came back — do not tidy them.

**OpenAI:**

```
I cannot add **CSS-4090 — Quantum Machine Learning** because it is not listed in the course catalogue.
```

**OpenRouter:**

```
I cannot add CSS-4090 Quantum Machine Learning to your schedule because this course is not listed in the course catalogue provided. According to the registration rules, I must refuse requests for courses that are not in the catalogue, as I cannot verify prerequisites, availability, schedule, or credits for non-catalogued courses.

Would you like to consider one of the eligible courses that are actually in the catalogue instead? The options you're eligible for are:
- CSS-4007 Artificial Intelligence (6 credits)
- CSS-4102 Distributed Systems (5 credits)
- FIN-3300 Financial Modelling (5 credits)
```

### Written answers

**1. The two providers used almost identical code. What actually changed, and what did not?**

> Main changes were the API key, the base_url, and the model name. For OpenAI I used OPENAI_API_KEY and the default OpenAI endpoint. For OpenRouter I used OPENROUTER_API_KEY and https://openrouter.ai/api/v1.
> Client library itself did not change. Both used the same OpenAI class, the same message format, the same chat.completions.create() method, and the same way of reading the reply and token usage from the response. The conversation history code also stayed the same.

**2. Why did the input token count climb on every turn when your questions stayed roughly the same length? Use the numbers from your own table. What happens to the bill at fifty turns?**

> Input token count increased because the model does not remember previous API calls by itself. On every turn, the program sends the system prompt and the complete conversation history again, including all previous user messages and assistant replies.
> For Luna - increased from 513 tokens on turn 1 to 747, 834, 916, and finally 970 on turn 5. For Laguna it increased even more. 605, 1057, 1244, 1469, and 1661 tokens.
> If the conversation continued for fifty turns, every later request would contain a much longer history. The later calls would therefore become increasingly expensive. If each turn adds roughly the same amount of text, the total amount of input processed over the whole conversation grows much faster than the number of turns because earlier messages are sent repeatedly.

**3. Turn 4: did the bot refuse, or did it invent CSS-4090?** If it refused, what in your system prompt held the line? If it invented, what did it make up — credits, a room, an instructor?

> Both models refused the request and did not invent CSS-4090. Luna directly said that the course was not listed in the catalogue. Laguna also refused and said that it could not verify its prerequisites, availability, schedule, or credits.
> I think the explicit instruction in my system prompt was important here: the model was told to use only the provided catalogue, explicitly refuse a requested course if it was not present, and never invent a course or course information. Neither model invented credits, a room, an instructor, or a schedule for CSS-4090.

**4. Where else was either bot wrong?** Turn 2 asks for two courses that meet at the same hour; two courses in the catalogue are full. Did the bots notice?

> Luna handled the main constraints correctly. In turn 2 it noticed that CSS-4007 and CSS-4102 both meet on Tuesday from 09:00 to 10:50 and refused to register them together. In turn 1 it also identified CSS-4400 as full. CSS-3011 is also full, although Luna mainly excluded it because the student had already completed it rather than explicitly mentioning both reasons.
> Laguna also noticed the Tuesday collision in turn 2 and correctly refused to register both courses together. It identified CSS-4400 as having zero remaining seats, but did not explicitly point out that CSS-3011 was also full; it was already completed, so it was excluded anyway.
> Laguna made some additional mistakes. In turn 1 it said that CSS-4007 and CSS-4102 would “exceed the maximum credit limit,” even though together they are only 11 credits and the maximum is 30. It also mentioned courses being “not part of your programme,” although there is no such restriction in the catalogue. In turn 3 it suggested adding FIN-3300 to the two conflicting courses to reach 16 credits, even though the schedule conflict would still remain. Its Kazakh answer in turn 5 was also less reliable: it changed Tuesday to Wednesday for the conflicting courses and made another inconsistent credit calculation.

## Sublab Medium - one task, six models

The three original OpenRouter models were replaced because their endpoints were unavailable, paid, or repeatedly rate-limited during the experiment. I used Laguna S 2.1, Ling 3.0 Flash VL, and Dots3-Note Preview instead. The OpenAI models were kept unchanged.


| Model | Exact | Failed | Tokens | Cost $ |
|---|---:|---:|---:|---:|
| poolside/laguna-s-2.1:free | 1 | 0 | 14,136 | 0.00000 |
| inclusionai/ling-3.0-flash-vl:free | 1 | 0 | 18,429 | 0.00000 |
| dots-studio/dots-3-note-preview:free | 2 | 0 | 29,841 | 0.00000 |
| gpt-5.6-luna | 3 | 0 | 3,045 | 0.00269 |
| gpt-5.6-terra | 1 | 0 | 2,341 | 0.01848 |
| gpt-5.6-sol | 2 | 0 | 2,267 | 0.04398 |

`Exact` was quite a strict metric in this experiment. A model could repair the intended error correctly but still receive `exact = false` after adding punctuation or making another grammatically reasonable change.

### Which error types did each model repair?

Here, **Yes** means that the model correctly repaired this error type in all relevant examples. **Partial** means that it repaired some examples but failed to restore the correct form in others. **No** means that it did not repair the target error.

| Error type | Laguna S | Ling 3.0 | Dots3 | Luna | Terra | Sol |
|---|---|---|-----|---|---|---|
| kaz_to_rus | Partial | Partial | Partial | Yes | Yes | Yes |
| latin_homoglyph | Yes | Yes | Yes | Yes | Yes | Yes |
| drop_hyphen | No | No | Yes | Yes | Yes | Yes |
| join_words | Partial | Partial | Partial | Yes | Yes | Yes |
| double_letter | Partial | Partial | Partial | Yes | Yes | Yes |

For `kaz_to_rus`, I included KZ-04 (`kaz_to_rus_partial`) as part of the same general error family.

**The latin_homoglyph row: what happened?**

KZ-03 was easily detected. Laguna and Dots restored the original words precisely, and other models also correctly substituted them with Latin characters.

**Where a model returned good Kazakh that was not identical to original, say so**

Models would sometimes alter the punctuation, causing them to trigger an exact = false result. While they might have corrected the text, they would also add a punctuation mark. Consequently, the character-by-character evaluation method is far from perfect; the quantitative difference score appears significantly higher than the actual linguistic discrepancies. Additionally, OpenAI models would sometimes switch from singular to plural forms; although the result looked like natural Kazakh, I do not consider this an accurate correction.

**Cheapest model that was good enough, and why:**

Given the hassle I went through just trying to find endpoints for free models before I even started using them, they certainly wouldn't rank as the best. Free models are extremely inefficient with token usage, the difference compared to paid ones is massive. Plus, their performance quality is highly questionable. I’d choose Luna as the best model because it strikes an excellent balance between cost and quality.

## Sublab Harder - open the tokenizer

### A. What a language costs

**`cl100k_base`:**

| Language | Tokens | Chars | Tok/char | × English | $ per 1,000 sentences |
|---|---:|---:|---:|---:|---:|
| kk | 200 | 263 | 0.760 | 3.75 | 0.166667 |
| ru | 129 | 277 | 0.466 | 2.30 | 0.107500 |
| en | 59 | 291 | 0.203 | 1.00 | 0.049167 |

**`o200k_base`:**

| Language | Tokens | Chars | Tok/char | × English | $ per 1,000 sentences |
|---|---:|---:|---:|---:|---:|
| kk | 84 | 263 | 0.319 | 1.58 | 0.070000 |
| ru | 74 | 277 | 0.267 | 1.32 | 0.061667 |
| en | 59 | 291 | 0.203 | 1.00 | 0.049167 |

The cost calculation uses the average sentence length in each language and the `gpt-5.6-sol` input rate of $5 per million tokens.

### B. What a homoglyph does

| Sentence id | Foreign char (index, name) | Tokens correct | Tokens corrupted | Δ | Diverges at |
|---|---|---:|---:|---:|---:|
| KZ-03 | `(0, 'A', LATIN CAPITAL LETTER A)`, `(2, 'a', LATIN SMALL LETTER A)`, `(5, 't', LATIN SMALL LETTER T)` | 16 | 20 | +4 | 0 |
| KZ-08 | `(1, 'o', LATIN SMALL LETTER O)`, `(3, 'a', LATIN SMALL LETTER A)`, `(9, 'T', LATIN CAPITAL LETTER T)` | 21 | 24 | +3 | 1 |

**Token pieces around the divergence:**

KZ-03:

```text
correct  : ['А', 'лая', 'қ', 'тарға', ' ақша']
corrupted: ['A', 'л', 'a', 'я', 'қ']
```

KZ-08:

```text
correct  : ['Д', 'он', 'аль', 'д', ' Т', 'рамп']
corrupted: ['Д', 'o', 'н', 'a', 'л', 'ль']
```

### C. Did it get better?

| Language | cl100k_base | o200k_base | Change |
|---|---:|---:|---:|
| kk | 0.760 | 0.319 | −0.441 (−58.0%) |
| ru | 0.466 | 0.267 | −0.199 (−42.6%) |
| en | 0.203 | 0.203 | 0.000 (0%) |

### Written answers

**1. What is the Kazakh tax?**

In mathematical terms, the Kazakh language cost approximately 3.75 times more than English. With cl100k_base, Kazakh required 0.760 tokens per character, whereas English required only 0.203 tokens; this resulted in an estimated cost of $0.166667 for Kazakh and $0.049167 for English. The figures were significantly better with o200k_base, as the ratio dropped to 0.319 tokens per character. The cost per 1,000 sentences also decreased, coming in at $0.070000. The new tokenizer improved the situation regarding tokens per character by approximately 58%.

**2. Why did the models repair `kaz_to_rus` but struggle with `latin_homoglyph`?**

First, kaz_to_rus replaces one Cyrillic letter with another; while the resulting spelling is incorrect according to Kazakh language rules, the word remains written within the same script system. When dealing with homoglyphs, we must recognize that even if characters appear identical to the human eye, their underlying computer codes differ, which can cause the tokenizer to split the word differently. For instance, the correct text for KZ-03 began as ['А', 'лая', 'қ', 'тарға', ' ақша'], whereas the corrupted version was ['A', 'л', 'a', 'я', 'қ']. A divergence in token sequences occurred at index 0, and the total number of tokens in the sentence increased from 16 to 20. A similar issue arose with KZ-08: the sequences ['Д', 'он', 'аль', 'д', ' Т', 'рамп'] and ['Д', 'o', 'н', 'a', 'л', 'ль'] diverged at index 1, and the token count rose from 21 to 24. Consequently, the presence of homoglyphs results in the model receiving a different sequence of tokens. Such mixing of systems can lead to errors.

**3. Name one thing this measurement does not explain about your Sublab Medium results.**

I tested only cl100k_base and o200k_base. However, Laguna, Ling, and Dots were accessed via OpenRouter, and they may use entirely different tokenizers. Therefore, I cannot claim that they encountered the specific tokenization patterns presented in this subsection. For a proper comparison, I would have needed to use each model's "native" tokenizer and process the same sentences through it.
