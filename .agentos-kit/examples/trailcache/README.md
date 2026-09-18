# TrailCache example

TrailCache is a fictional local-first mobile hiking journal used to demonstrate a mature, customized AgentOS instance. The app itself is not implemented here; the repository slice models the institutional memory a real team would keep after repeated offline-sync and usability work.

Try routing from this directory:

```sh
PYTHONPATH=../../src python3 -m agentos context \
  "resume photo upload retry work" --path src/sync/queue.ts

PYTHONPATH=../../src python3 -m agentos context \
  "change the journal list empty-state copy" --path src/journal/EntryList.tsx

PYTHONPATH=../../src python3 -m agentos eval-routing
```

The sync task should retrieve the live plan, sync map, local-first decision, and invariants. The copy task should remain much smaller and avoid the upload failure history.

The routing evaluation is a regression captured from the first continuity
simulation, when a generic word incorrectly pulled synchronization history into
that journal UI task.

This example intentionally demonstrates:

- current product/architecture state without class-by-class documentation;
- a counterintuitive accepted decision;
- a tempting failed approach;
- a plan resumable midway through implementation;
- behavioral personas grounded at different evidence levels;
- raw feedback kept separate from interpretation;
- a reviewed insight proposing a persona scenario update;
- a downstream AgentOS improvement proposal that does not mutate the framework.
