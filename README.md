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
| question | [8] | [40%] |
| progress_update | [4] | [20%] |
| vent | [3] | [15%] |
| advice_analysis | [5] | [25%] |
| **Total** | [20] | 100% |

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

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



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
