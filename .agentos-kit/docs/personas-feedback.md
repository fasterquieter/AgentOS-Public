# Personas and real feedback

Synthetic personas are exploratory test lenses. Real feedback is evidence. AgentOS links them without pretending either is infallible.

## Define behavioral personas

A useful persona varies conditions that change product behavior or comprehension:

- familiarity and memory of the product;
- time pressure, interruption, or reluctance to read;
- assistive technology or input mode;
- data volume and account history;
- domain expertise and willingness to configure;
- a plausible incorrect mental model grounded in research or observed feedback.

Avoid demographic caricatures. “Uses VoiceOver and navigates by headings” is actionable; “older and bad with technology” is not.

Each persona names a context, goals, behaviors, known evidence basis, likely failure modes, and scenarios. A synthetic assumption is marked as such. Update a persona from real feedback only after an explicit synthesis review; one unusual report does not redefine a user population.

## Run a persona test

Use the real application when tooling and authorization permit. Give the testing agent the persona and goal, not the expected bug. Capture:

1. expected next behavior;
2. attempted action;
3. observed result;
4. hesitation, missed control, misunderstood term, or recovery attempt;
5. exact environment and data scale;
6. finding severity and confidence;
7. whether the issue is reproducible outside the persona narrative.

Run personas for onboarding, navigation/mental-model changes, high-consequence flows, accessibility work, workflows implicated by feedback, or periodic UX coherence review. Do not run every persona for an internal refactor or cosmetic change with no behavioral impact.

## Preserve raw feedback

The user's original words and observed context are immutable evidence except for necessary privacy redaction. Their causal explanation is a hypothesis.

```text
Evidence: “Why does this stupid thing disappear when I press that?”
Observed context: iPhone; pressed Save; item absent from current list; exact version unknown.
Interpretation (low confidence): the active filter may hide the saved item.
```

Raw records may link to one or more structured insights. Never replace the raw report with a polished agent summary. Apply the project's privacy/retention policy and avoid storing unnecessary personal data.

## Synthesize insights

Cluster by observed behavior and user intent, not merely matching words. An insight should state:

- linked raw reports and other evidence;
- repeated observable pattern;
- causal hypotheses with confidence;
- affected journey and severity;
- counterevidence;
- next validation or product action;
- status and eventual resolution.

Several similar independent reports, a high-severity reproducible failure, or explicit research can justify a persona evolution proposal. A human or designated product/UX reviewer accepts the update.

## Learning loop

```text
real report → preserved raw evidence → reviewed insight
      → deliberate persona/scenario update → future exploratory run
      → reproducible finding → deterministic regression test where possible
```

The loop is intentionally gated at insight and persona update. Automatic persona rewriting would amplify noise and agent interpretation errors.

