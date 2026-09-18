# Curiosity / simplification review

This review questions accumulated assumptions and surfaces deletion opportunities. It does not autonomously remove mechanisms.

Ask:

- Why does this concept exist today?
- Which user outcome or invariant requires it?
- What observable failure occurs if it is removed?
- Are two named concepts actually one state or responsibility?
- Is current code compensating for a historical constraint that no longer applies?
- Could a platform, standard library, framework, or dependency now replace custom machinery?
- Could hundreds of lines disappear through a simpler representation rather than a careful refactor?
- Is the requirement evidenced by real users, product intent, or only inherited assumption?
- What is the cheapest experiment that would test removal safely?

Output opportunities with evidence, estimated deletion/simplification, affected invariants, experiment, rollback path, and confidence. Classify speculative ideas as speculative. Surface the opportunity; obtain appropriate product/architecture authority before removing a real requirement.

