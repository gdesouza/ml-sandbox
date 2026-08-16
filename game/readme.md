# Move Square: Behavior Cloning

Move the blue square fully inside the red target without touching the screen border. While a person plays, the program records game states and actions. A small PyTorch network then learns to imitate those actions.

## Learning workflow

From the repository root, create and activate a virtual environment, then install the package:

```bash
python3 -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\Activate.ps1       # Windows PowerShell
python -m pip install -e .
```

Open the beginner menu:

```bash
python -m behavior_cloning_game
```

The original scripts remain useful for seeing each step explicitly. Run them from `game/`:

```bash
cd game
python play.py --episodes 10 --seed 7
python inspect_data.py data/demonstrations_YYYYMMDD_HHMMSS.csv
python train.py data/demonstrations_YYYYMMDD_HHMMSS.csv --preset quick
```

`train.py --help` lists configurable epochs, learning rate, batch size, hidden size/layers, validation fraction, seed, and output directory. The trainer splits whole episodes into training and validation sets, normalizes position features, and saves portable `.pth` weights plus self-describing `.json` metadata.

Watch the trained model using the printed weights path without `.pth`:

```bash
python execute.py data/model_RUN_ID
```

The current evaluation is interactive. Observe a fixed number of attempts when comparing models so the comparison is fair.

## What the data means

Each recorded row pairs a state with the action the player chose:

- Features `X`: blue-square position (`blue_x`, `blue_y`) and target position (`target_x`, `target_y`)
- Labels `y`: horizontal and vertical movement (`action_x`, `action_y`)
- Episode context: step, elapsed time, and outcome

Use `inspect_data.py` before training to find sparse, repetitive, or directionally biased demonstrations. The current network predicts continuous action values and trains with mean squared error (MSE).

## Teaching materials

- [Five-minute quick start](../docs/quickstart.md)
- [Seven guided lessons](../docs/lessons.md)
- [Instructor guide](../docs/instructor-guide.md)

The unified command-line menu and finite seeded evaluation are available now. A graphical menu, automated corrective-demonstration workflow, comparison charts, and optional nine-class action model remain planned extensions; they are not required for the current workflow.

## Tests

```bash
python -m unittest discover -s tests -v
```

Keep reusable behavior in `util/`, orchestration in the entry scripts, and generated learning artifacts out of version control unless they are intentional fixtures.
