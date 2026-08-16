# ML Doodles

Small, readable experiments for learning machine learning. The active project is
`game/`, a behavior-cloning exercise in which a neural network learns from human
demonstrations to move a blue square into a red target.

Install from the repository root with `python -m pip install -e .`, then launch
the guided workflow with `python -m behavior_cloning_game`.

Start with the [five-minute learner guide](docs/quickstart.md). Classroom
materials are in [guided lessons](docs/lessons.md) and the
[instructor guide](docs/instructor-guide.md).

The current workflow is:

```text
Collect demonstrations -> Inspect the CSV -> Train -> Watch and improve
```

Generated datasets, model weights, and experiment metadata are stored under
`game/data/` unless another output directory is given. The original scripts in
`game/` remain available for learners who want to trace each step in Python.
