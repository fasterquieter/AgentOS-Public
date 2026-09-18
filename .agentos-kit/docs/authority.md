# Product, content, and runtime authority

Use an authority map when repository files are not the only plausible current
truth. Common competing sources include generated code, databases, CMS content,
external editorial documents, configuration, device state, and deployed systems.

Record only material boundaries:

| Kind of truth | Current authority | Other representations | Synchronization direction | Verification needed before change |
|---|---|---|---|---|

Do not infer authority from filename, modification time, or dump size. Separate:

- accepted product intent from observed implementation;
- bootstrap/seed data from mutable live content;
- checked-in configuration from deployed configuration;
- a snapshot from the system that produced it;
- an accepted or echoed API value from measured external behavior.

Prefer placing a small authority section in `project.md` or `architecture.md`.
Create a standalone record only when the boundary is independently routed and
expensive to reconstruct.

Authority answers “what kind of claim is this?” It does not answer “who may
change it?” For that separate question, use the defaults or selective
`change_control` fields described in `governance.md`. A source-of-truth map and a
write policy solve different problems and should not be collapsed into one
label.
