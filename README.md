# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->


## What This Does

This system is a text classifier that sorts individual posts and comments
from r/Fitness into one of four categories based on their primary purpose:
`question` (seeking advice or an answer), `progress_update` (reporting
personal fitness results or a journey), `vent` (expressing frustration about
a gym-related experience), or `advice_analysis` (explaining, evaluating, or
recommending something using reasoning). It was fine-tuned on 165 hand-labeled
real posts using a small transformer model (DistilBERT).

---

## Label Taxonomy

### `question`

**Definition:** A post whose main purpose is to get an answer or recommendation from others, even if it includes personal context or a claim as background.

**Example 1:**
> "Cardio before weights...bad? ... I recently read on a 'gym gurus' instagram that doing cardio before lifting weights is bad for you... Is this true?"

The author describes their cardio routine, mentions advice they saw on Instagram, and asks, “Is this true?” 

Why it fits: The main purpose is to get an answer.

**Example 2:**
> “Was I the asshole or was he?”
A user recounts a gym incident involving equipment and asks whether they were in the wrong. 
Why it fits: The author explicitly seeks other people's judgment, so question is the best fit.

### `progress_update`

**Definition:** A post whose main purpose is to report personal fitness results, a change over time, or an ongoing journey, without the poster primarily asking for help or offering reasoning to others.

**Example 1:**
> “9.5 months into my journey: 6'1 27M 335 → 176”
The author describes their fitness journey, training routine, and progress over nine and a half months. 
Why it fits: The primary purpose is reporting a personal journey and its results.

**Example 2:**
> “Got into the gym finally as a 5’8 150lb dude”
The author shares starting to work out, changes in their weight, and excitement about learning new exercises. 
Why it fits: The main purpose is sharing personal progress and enthusiasm, rather than asking for advice

### `vent`

**Definition:** A post whose main purpose is to express frustration or recount an annoying/disappointing experience, without primarily asking for advice.

**Example 1:**
> Complaint about gym music
A user complains about their gym playing excessively loud music. 
Why it fits: The main purpose is expressing frustration, not seeking a solution.

**Example 2:**
> Complaint about unsolicited advice
A user describes someone approaching them during a workout to criticize their lifting technique without being asked. 
Why it fits: The author recounts an irritating experience to express frustration.

### `advice_analysis`

**Definition:** A post whose main purpose is to explain, evaluate, or recommend something about fitness using reasoning, evidence, or a specific checkable fact.

**Example 1:**
> “I made a guide to help you stop being lazy and consistently get in the gym”
The author draws on psychology concepts such as rewards, precommitment, and reducing barriers to explain how people can build consistent exercise habits. 
Why it fits: The post offers a structured explanation and actionable recommendations.

**Example 2:**
> Advice about workout progression
An experienced lifter explains how adjusting training intensity and focusing on heavier weights affected their performance. 
Why it fits: The comment explains a training approach and its results rather than primarily asking a question.

### The hardest boundary

**Which two labels:** `question` vs. `advice_analysis`

**The decision rule I used every time:** If a post ends with or is clearly building toward a direct question ("Is this true?", "should I...", "what do you think"), it's `question` - even if it contains personal backstory, a claim, or something that sounds like it could be analyzed. The question is still the post's actual purpose. `advice_analysis` is reserved for posts where the poster is the one doing the explaining or recommending, not the one asking.

**A note on post structure:** I excluded recurring structural/container posts (e.g., weekly megathreads like "Rant Wednesday" that exist to collect other users' replies, rather than express content themselves) during data collection. Individual replies within such threads were still eligible for collection and labeled normally based on their actual content, since those replies are genuine posts with real intent behind them.

---


## The Dataset

**Where the posts came from:** r/Fitness, a public subreddit with no login wall required to read. I excluded recurring structural/container posts (e.g., weekly "Rant Wednesday" megathreads) since they don't represent individual post intent — only genuine individual posts and genuine individual replies were collected.

**How I labelled them:** I developed four labels based on the primary purpose of each post: question, progress_update, vent, and advice_analysis. I used explicit decision rules to resolve ambiguous cases, focusing on what the author was primarily trying to accomplish rather than tone alone.

**Counts per label:**
| Label | Count | Share |
|---|---|---|
| vent | 43 | 26% |
| progress_update | 43 | 26% |
| question | 42 | 25% |
| advice_analysis | 37 | 22% |
| **Total** | 165 | 100% |

**Three hard cases**

**1.**
> *The post:* "Cardio before weights...bad?" — describes a personal cardio routine, cites a claim from an Instagram "gym guru," and asks whether it's true.
>
> *Could have been:* `question` or `advice_analysis`
>
> *I chose, because:* The post explicitly ends with "Is this true?" - the question is the post's actual purpose, even though it contains a claim that could be analyzed. My decision rule: if a post is building toward a direct question, it's `question` regardless of what claims or backstory it contains.

**2.**
> *The post:* "Rant Wednesday" weekly megathread invitation.
>
> Could have been: vent or excluded from the dataset.

> I chose exclusion because: The thread invites other users to share their frustrations; the invitation itself is not an individual's expression of frustration. Its primary function is structural: collecting contributions.

> Decision rule: Exclude recurring container posts. Individual replies within those threads remain eligible and are classified according to their own content and intent.

**3.**
> The post: “People keep taking the equipment I’m waiting for at the gym. It’s so annoying. Does anyone else deal with this?”

> Could have been: vent or question.

> I chose vent because: The main purpose is to express frustration about a recurring gym experience. The final question asks whether other people can relate, rather than primarily seeking advice or a solution.

> Decision rule: If the main purpose is to express frustration, label it vent, even if the author asks whether others experience the same thing. If the main purpose is to obtain information, advice, or a solution, label it question. The presence of a question mark alone does not determine the label.
---

## The Training Run

**Base model:** distilbert-base-uncased

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, seed 42

**Anything I changed from the defaults, and why:** Nothing — I used the starter's default hyperparameters for this first run.

**Split sizes:** train 115, val 25, test 25 (70/15/15 stratified split). Per-label counts in the test split: question 6, progress_update 7, vent 6, advice_analysis 6. All four labels have fewer than 8 examples in the test split, which the notebook itself flagged as a reason to expect F1 scores to move significantly between seeds.

---


## How I Used AI

**Moment 1**

I asked Claude to suggest labels for a batch of real r/Fitness posts I'd
collected, based on my 4-label taxonomy and decision rules. It correctly
labeled most of them, but flagged several posts as too short or ambiguous to
reliably label (e.g., single-sentence fragments with no real context). I
reviewed every suggestion myself, corrected a few labels that didn't match my
own decision rules on close reads, and dropped the flagged fragments entirely
rather than forcing them into a category.

**Moment 2**

While reviewing one of my labeled rows, Claude pointed out that one post
("Please don't laugh at the weights I'm talking about...") reported specific
numeric strength gains over time but I had initially labeled it `vent`
because of its self-deprecating opening line. I reread it against my own
`progress_update` definition and relabeled it, since the post's actual content
was reporting measurable gains, not expressing frustration as its main
purpose.

**Pre-labelling disclosure:** I labeled my first 20 posts entirely by hand,
with no AI involvement (marked `cold` in the note column). For the remaining
~145 posts, I had Claude suggest labels in batches based on my taxonomy, then
read and corrected every single suggestion myself before adding it to the
dataset (marked `ai-assisted`).

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained


| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.400 | 0.440 | +0.040 |
| Macro F1 | 0.293 | 0.351 | +0.058 |
| F1 — `advice_analysis` | 0.000 | 0.286 | +0.286 |
| F1 — `progress_update` | 0.727 | 0.545 | -0.182 |
| F1 — `question` | 0.444 | 0.000 | -0.444 |
| F1 — `vent` | 0.000 | 0.571 | +0.571 |


**What I predicted before I looked:**

I expect my trained model to perform somewhat better than the baseline in overall accuracy because it has been trained on actual examples from my specific four-label classification task. However, I am not highly confident about this prediction. My trained model achieved only 44% accuracy, and completely failed to identify the `question` class (F1 = 0.000). With only 165 examples, the training data may not have been sufficient to learn reliable patterns across all four categories. Therefore, I think the trained model may outperform the baseline, but I also consider it possible that the baseline will achieve comparable or better results.

**What the gap actually means:**

My prediction was partially right, but in a more interesting way than I expected. Overall accuracy is only slightly higher for the trained model (+0.040), which matches my low-confidence prediction. But the per-label breakdown tells a more specific story than a single accuracy number: the baseline and my trained model fail on completely different labels. The baseline (a general-purpose zero-shot classifier, not trained on my data) scores 0 F1 on both `advice_analysis` and `vent` — it has no exposure to how my specific labels are worded. My trained model fixed both of those (0.286 and 0.571 respectively), which is real evidence that fine-tuning taught it something the baseline couldn't get from label names alone. But my trained model introduced a new blind spot — `question` dropped to 0.000, down from the baseline's 0.444 — likely because `question` had the least distinct boundary in my taxonomy (it overlaps with `advice_analysis` and even `vent` in places, as I noted in my hardest-boundary writeup). Fine-tuning didn't uniformly improve the model; it reshaped which mistakes it makes.

---


## Run Log — Before

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy ≥ 60% | 60% | 0.440 | 0.240 | 0.440 | MISSED (all 3 seeds below target) |
| 2. F1 ≥ 0.40 per label | 0.40 | question: 0.000, progress_update: 0.545, vent: 0.571, advice_analysis: 0.286 | question: 0.000, progress_update: 0.387, vent: 0.000, advice_analysis: 0.000 | question: 0.444, progress_update: 0.545, vent: 0.500, advice_analysis: 0.000 | MISSED (no seed clears 0.40 on all 4 labels) |
| 3. Confidence gap ≥ 15 points | 62.5 pts | 75.0 pts | 12.5 pts | MISSED |
| 4. Balance ≥ 20% per label | 20% | 22-26% (unchanged by training) | 22-26% | 22-26% | MET (all 3 seeds — this is a property of the dataset itself, not the training run) |
| 5. Agreement ≥ 80% with staff labels | 100% (30/30) | same | same | MET |  scored under staff’s taxonomy, not my four labels|

### The spread table

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.440 | 0.240 | 0.440 | 0.200 |
| Macro F1 | 0.351 | 0.097 | 0.372 | 0.276 |
| F1 — `question` | 0.000 | 0.000 | 0.444 | 0.444 |
| F1 — `progress_update` | 0.545 | 0.387 | 0.545 | 0.158 |
| F1 — `vent` | 0.571 | 0.000 | 0.500 | 0.571 |
| F1 — `advice_analysis` | 0.286 | 0.000 | 0.000 | 0.286 |

**Stability note (from the notebook):** "Accuracy moved 0.200 across seeds — more than 10 points. Your dataset is too small or too lopsided for a stable measure." This is a genuine diagnosis, not a coding error — with only 165 labeled examples split 4 ways, test splits of 6-7 examples per label are small enough that one seed (seed 7) landed on an unusually hard or atypical split, cratering every label's F1 to near-zero except `progress_update`.

### Confusion matrix

### Confusion matrix

Seed 42 (25 test posts). Rows are true labels, columns are the model's guesses.

| true \ predicted | question | progress_update | vent | advice_analysis |
|---|---|---|---|---|
| **question** | 0 | 5 | 1 | 0 |
| **progress_update** | 0 | 6 | 1 | 0 |
| **vent** | 0 | 2 | 4 | 0 |
| **advice_analysis** | 1 | 2 | 2 | 1 |

**My biggest off-diagonal number, and what it means:** 5 real `question` posts were called `progress_update`, and 0 went the other way. The model did not learn the `question` boundary. It guessed `progress_update` for 15 of the 25 test posts and almost never predicted `question` (once) or `advice_analysis` (once), so it is leaning on `progress_update` as a default. `advice_analysis` was also weak: only 1 of 6 was correct, and the rest were spread across the other three labels.

---


## Verdicts and Diagnoses

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 60% across all 3 seeds | MISSED | Accuracy was 0.440, 0.240, 0.440 — all three seeds fall well short of 60%, and the target has to hold across all three, not just some. |
| 2 | Per-label F1 | ≥ 0.40 for all 4 labels, all 3 seeds | MISSED | No single seed cleared 0.40 on all four labels. Seed 7 scored 0.000 on three of four labels. Seed 42 and 2024 each had at least one label below 0.40. |
| 3 | Confidence gap | ≥ 15 points, all 3 seeds | MISSED | Gaps were 62.5, 75.0, and 12.5 points. Seed 2024 falls short of the 15-point target, so the criterion doesn't hold across all three seeds even though two of three seeds cleared it comfortably. |
| 4 | Balance | ≥ 20% per label | MET | Each label sits between 22% and 26% of the 165-example dataset. This is a property of the dataset itself and doesn't change across training seeds. |
| 5 | Consistency (agreement with staff labels) | ≥ 80% | Not yet measured | Requires labeling the staff's 30-post set under their taxonomy — done separately from the training run. |

**Diagnoses**

All three misses trace back to the same root cause: 165 examples split 4 ways and then split again 70/15/15 leaves only 6-7 examples per label in the test set. A test set that small means a single unusual post can swing a label's F1 from 0.5 to 0.0, and that's exactly what happened — seed 7 landed on a test split where the model scored 0.000 F1 on three of four labels, dragging every aggregate measure down with it (accuracy and macro F1). Seed 2024’s 12.5-point confidence gap is a separate small-sample effect: each seed has its own split, so seed 7’s split can’t have caused it.

This isn't a bug in the training code or the prompt — the model trained normally (loss went down each epoch, same as in the single-seed Unit 5 run) and the pipeline ran correctly all three times. The diagnosis is about the dataset's size relative to the number of labels: 165 examples across 4 labels is on the low end for a genuinely stable measurement, and the notebook's own `stability_note()` function confirmed this directly ("Your dataset is too small or too lopsided for a stable measure. That IS a diagnosis.").

The one criterion that did hold (balance) is also the one that doesn't depend on the model or the random split at all — it's a fact about the raw label counts, which is why it's stable while everything downstream of training is not.

## Agreement Report

I labeled the 30 staff posts under staff's taxonomy (`analysis`,
`hot_take`, `reaction`), saved my labels, and only then opened staff's
file and compared them with `agreement.py`.

**Agreement rate:** 30 / 30 = 100%

**First run:** The first run reported 29/30 (97%). The one flagged
"disagreement" was a typo in my file, not a labeling difference: I had
typed `reactioni` instead of `reaction` on the last row ("Signed up.
Card's charged, no going back..."). Staff's label was `reaction`, which
is what I intended. I fixed the typo and re-ran, and the committed
`agreement_results.json` reflects the corrected file. No label's meaning
was changed.

**Disagreements:** None remain, so there is nothing to sort into piles
(a), (b) or (c).

**What the pattern in my disagreements tells me:** With zero real
disagreements I can't claim any gap or ambiguity in staff's rules. This
shows I can apply a written rule consistently, but it was scored under
staff's three labels, not my four, so it does not directly test my own
`question` vs. `advice_analysis` boundary. [ADD 1-2 SENTENCES: name a post
or two that made you hesitate and which staff rule settled it.]

---
## The Improvement

**What I changed:** I increased the number of training epochs from 3 to 5. Nothing else changed: same labels, taxonomy, criteria, dataset (165 rows), learning rate, batch size and seeds (42, 7, 2024). Because the dataset and seeds are the same, the test splits are identical to the "before" run, so the two logs are scored on the same posts.

**Which diagnosis pointed at it:** Honestly, my main diagnosis pointed at dataset size, not training. I did not have time to label 30 more `advice_analysis` posts, so I picked the one change I could finish and measure. There was a small hint of under-training: in the seed 42 run the eval loss was still falling at epoch 5 (1.37 at epoch 1 down to 1.30), and it never got far below chance for four classes (about 1.39).

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 60% | 0.520 | 0.600 | 0.480 | MISSED (seeds 42 and 2024 below target) |
| 2. F1 per label | ≥ 0.40 on all 4 | question: 0.250, progress_update: 0.632, vent: 0.625, advice_analysis: 0.286 | question: 0.667, progress_update: 0.600, vent: 0.833, advice_analysis: 0.000 | question: 0.500, progress_update: 0.667, vent: 0.500, advice_analysis: 0.000 | MISSED (`advice_analysis` below 0.40 on all 3 seeds, `question` also below on seed 42) |
| 3. Confidence gap | ≥ 15 points | 50.0 | 50.0 | 62.5 | MET (all 3 seeds) |
| 4. Balance | ≥ 20% per label | 22-26% | 22-26% | 22-26% | MET (property of the dataset, unchanged) |
| 5. Agreement with staff labels | ≥ 80% | 100% (30/30) | 100% (30/30) | 100% (30/30) | MET (scored under staff's taxonomy, unchanged) |

**Did it help, and how do I know:** Yes, partly. Accuracy rose on every seed, from 0.440 / 0.240 / 0.440 to 0.520 / 0.600 / 0.480 (mean 0.373 to 0.533), and macro F1 rose on every seed too. `question` improved the most (F1 from 0.000 / 0.000 / 0.444 to 0.250 / 0.667 / 0.500). Criterion 3 flipped from MISSED to MET: the confidence gap on seed 2024 went from 12.5 to 62.5 points. Criteria 1 and 2 are still MISSED. `advice_analysis` did not change at all (F1 0.286 / 0.000 / 0.000 before and after), which fits my diagnosis that it is a thin-data problem that more epochs cannot fix. Caveats: each test set is only 25 posts, so one post is 4 points of accuracy; accuracy still moved 12 points across seeds (0.480 to 0.600), so the measurement is still not stable; and the model's average confidence was about 0.30 whether it was right or wrong (near chance for four labels), so the criterion 3 pass rests on comparing the top and bottom thirds of 8 posts each and is fragile.
---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
