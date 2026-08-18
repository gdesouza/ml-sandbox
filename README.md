# ML Sandbox

Small, readable machine-learning experiments. The active project is a behavior-cloning
game: record a person moving a blue circle into a target, train a PyTorch policy on
those demonstrations, and evaluate how well the policy imitates them.

## Quick start

The project supports Python 3.11 through 3.13. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\Activate.ps1      # Windows PowerShell
python -m pip install -e .
python -m behavior_cloning_game
```

The final command opens a graphical launcher for the full learning loop:

```text
Collect demonstrations -> Inspect the data -> Train a policy -> Evaluate it
```

Dataset inspection is displayed in the launcher with sample and episode counts,
outcomes, action balance, no-op ratio, and data-quality guidance.
Before training, the launcher lets you choose preprocessing, feature representation,
presets, and individual hyperparameters.

Start with the [five-minute quick start](docs/quickstart.md) for a guided first run.
Use `python -m behavior_cloning_game --text` when you prefer the terminal menu or
are working without a graphical display.

## Command-line workflow

The same steps can be run directly from the repository root:

```bash
python -m behavior_cloning_game collect -- --episodes 10 --seed 7
python -m behavior_cloning_game inspect game/data/demonstrations_TIMESTAMP.csv
python -m behavior_cloning_game train game/data/demonstrations_TIMESTAMP.csv -- --preset quick
python -m behavior_cloning_game evaluate game/data/model_RUN_ID.json -- --episodes 20
```

Use `--headless` during evaluation to collect reproducible metrics without opening a
window:

```bash
python -m behavior_cloning_game evaluate game/data/model_RUN_ID.json -- --headless
```

Options placed after `--` are forwarded to the underlying workflow. Run the scripts
in `game/` directly when you want to explore each implementation step or see all of
its options:

```bash
cd game
python play.py --help
python inspect_data.py --help
python train.py --help
python execute.py --help
```

## Outputs

Generated artifacts are stored in `game/data/` by default:

- `demonstrations_*.csv` contains recorded states, actions, and episode outcomes.
- `model_*.pth` contains trained PyTorch weights.
- `model_*.json` describes the matching feature transform, normalization, training
  configuration, data split, and metrics.

Prefer the JSON experiment file when evaluating a newly trained model. It supplies
the metadata needed to reproduce inference, especially for relative feature
transforms. Generated datasets and checkpoints should not be committed unless they
are intentional fixtures.

## Project map

- `behavior_cloning_game/` provides the guided menu and packaged command-line entry
  point.
- `game/` contains the collection, inspection, training, and evaluation scripts.
- `game/util/` contains reusable game, data, feature, model, and evaluation logic.
- `game/tests/` and `tests/` contain the automated test suites.
- `docs/` contains the [guided lessons](docs/lessons.md),
  [instructor guide](docs/instructor-guide.md), and extension documentation.

See the [game workflow guide](game/readme.md) for data semantics, training controls,
feature transforms, and downsampling plugins.

## Development

Install the development tools and run the tests from the repository root:

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

Keep reusable behavior in `game/util/` and entry-point scripts focused on
orchestration. Potential future teaching extensions include a graphical menu,
corrective-demonstration tooling, experiment charts, and an optional classification
policy; these are ideas rather than a committed implementation schedule.
