# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.

## 1. Overall Accuracy

The classifier must achieve at least 60% overall accuracy across all three random seeds.

**Why this target:**

My dataset has 165 examples across four labels, with each label making up about 22–26% of the data. Since random guessing would achieve about 25% accuracy, 60% would be a meaningful improvement while still being a realistic target for a first classifier trained on a relatively small dataset.
---

## 2. Per-Label Performance

The classifier must achieve an **F1 score of at least 0.40 for each of the four labels across all three random seeds**.

**Why this target:** My dataset has between 37 and 43 examples per label, so each label has a relatively small number of examples, and only about 6–7 examples per label will appear in each test split. Because F1 scores can fluctuate significantly with so few test examples, I chose a lower threshold than I would for a larger dataset, while still requiring the model to perform better than simply ignoring a category.
---

## 3. Confidence

The accuracy of the most-confident third of predictions must be **at least 15 percentage points higher** than the accuracy of the least-confident third across all three random seeds.

**Why this target:** My dataset contains only 165 examples, so the test split is relatively small and individual predictions can noticeably affect accuracy. I chose a 15-percentage-point difference because the model’s confidence should provide a useful signal about which predictions are more reliable, rather than being nearly unrelated to correctness.


## 4. Balance

Each of the four labels must represent **at least 20% of the dataset after any data preparation or filtering**.

**Why this target:** My dataset contains 165 examples, with 37–43 examples per label, so each label currently represents approximately 22–26% of the data. Setting a 20% minimum allows some flexibility if data needs to be removed while helping prevent any category from becoming underrepresented.

## 5.

## 5. Consistency

The classifier’s labels must achieve **at least 80% agreement with the staff-labeled examples** in the Agreement Report.

**Why this target:** My dataset contains four labels that can sometimes overlap, especially when distinguishing `question` from `advice_analysis` or identifying whether a post is a `vent` or a `progress_update`. I chose 80% agreement as a meaningful target for consistent labeling while allowing for some ambiguity in interpreting real Reddit posts.
---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
