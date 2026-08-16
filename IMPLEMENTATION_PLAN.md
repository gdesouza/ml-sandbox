# Behavior Cloning Teaching Platform — Implementation Plan

## Objective

Create a beginner-friendly, cross-platform teaching tool that makes the complete behavior-cloning loop visible:

**Collect → Inspect → Train → Evaluate → Improve**

A learner must be able to complete this loop without editing Python. The implementation should remain small enough that a learner with basic Python knowledge can trace state, action, data, model, and outcome through the source.

## Product Principles

- Correctness before interface polish: never train silently on incomplete or malformed data.
- One concept per layer: prefer typed functions and dataclasses over framework-heavy abstractions.
- Observable learning: show the data, configuration, loss, and gameplay metrics behind every result.
- Reproducible experiments: seed randomness and preserve configuration and metrics with each model.
- Progressive complexity: teach regression first; add classification and corrective demonstrations later.
- Preserve existing CSV and checkpoint support through explicit compatibility loaders.

## Target Structure

Migrate incrementally toward:

```text
pyproject.toml
src/behavior_cloning_game/
  __main__.py       # python -m behavior_cloning_game
  cli.py            # menu and collect/inspect/train/evaluate commands
  config.py         # game, training, and evaluation configurations
  domain.py         # GameState, Action, EpisodeResult
  environment.py    # rules and transitions; no Pygame dependency
  rendering.py      # Pygame window, HUD, and feedback
  controllers.py    # keyboard and model policies
  data.py           # recording, validation, migration, summaries
  model.py          # intentionally small policy models
  training.py       # split, normalization, training, artifacts
  evaluation.py     # finite seeded evaluation and metrics
tests/
  fixtures/
  unit/
  integration/
docs/
```

Keep `play.py`, `train.py`, and `execute.py` as thin compatibility wrappers until the new workflow is documented and stable.

## Phase 0 — Freeze Contracts and Establish a Safety Net

This phase is the integration gate; do not parallelize contract design.

### Tasks

- Define `GameState`, `Action`, `EpisodeResult`, `TrainingConfig`, and `EvaluationConfig` dataclasses.
- Define versioned CSV schema v2:
  `schema_version, episode_id, step, elapsed_ms, blue_x, blue_y, target_x, target_y, action_x, action_y, outcome`.
- Record one row per simulation tick, including left, up, diagonal, and no-op actions. Buffer each episode so every row receives its outcome.
- Define backward-compatible mappings for current CSV columns and two-/four-layer checkpoints. Legacy outcomes remain `unknown`.
- Add tests for geometry, collision, action mapping, legacy data/checkpoints, device selection, and a tiny CPU train/save/load cycle.
- Add a headless Pygame smoke test using `SDL_VIDEODRIVER=dummy`.

### Acceptance Criteria

- All action directions survive a CSV round trip.
- Invalid or missing columns produce one actionable error, not a traceback chain.
- Existing committed CSVs and checkpoints load with an explicit compatibility notice.
- Tests run offline and CPU-only from one documented command.

## Phase 1 — Correct the Game and Collection Lifecycle

### Tasks

- Replace recursive `Game.start()` calls with iterative `run_session()` and `run_episode()` methods.
- Initialize Pygame before creating display resources.
- Return quit intent and episode results instead of calling `quit()` or `sys.exit()` inside controllers.
- Own cleanup in entry points with context managers or `try/finally`; flush completed episodes on exit.
- Fix rectangle center calculations, parking rendering, success percentage formatting, and mutable default inputs.
- Add a seed, episode limit, maximum-step policy, and injectable random generator.
- Replace blocking one-second sleeps with timed feedback that continues processing events.
- Add a HUD showing objective, controls, episode number, successes, and collected sample count.

### Acceptance Criteria

- A 1,000-episode headless run has no stack or resource growth.
- Window close and Escape exit cleanly and lose at most the current incomplete episode.
- The same seed produces the same initial scenarios.
- Success, out-of-bounds, stalled, and user-quit outcomes are independently tested.

## Phase 2 — Make Data Visible and Trustworthy

### Tasks

- Implement pure recorder, loader, validator, legacy migrator, and summary functions in `data.py`.
- Add Start, Pause, Finish, and episode-goal controls to collection mode.
- Ask for an experiment name; generate collision-safe paths and show the saved location.
- Add an `inspect` workflow showing:
  - row and episode counts;
  - success/failure/unknown totals;
  - action distribution and no-op ratio;
  - coordinate ranges and imbalance warnings;
  - CSV preview and example trajectories;
  - which columns form features (`X`) and labels (`y`).
- Include a tiny built-in tutorial dataset.

### Acceptance Criteria

- A novice can collect, finish, locate, and inspect data without using filenames manually.
- Empty, interrupted, out-of-bounds, or imbalanced datasets receive plain-language guidance.
- Summary values are covered by deterministic fixture tests.

## Phase 3 — Build Reproducible, Configurable Training

### Tasks

- Provide Quick, Balanced, and Explore presets plus validated controls for epochs, learning rate, batch size, hidden size/layers, validation fraction, and seed.
- Split by episode, never by row. Refuse training with too few episodes and explain how to collect more.
- Normalize positions using statistics fitted only on the training partition; apply and save the same transformation for inference.
- Shuffle training batches with a seeded generator.
- Track training and validation loss; retain the best validation checkpoint.
- Save a self-describing experiment bundle containing weights and JSON metadata:
  schema/model version, feature/action definitions, normalization, configuration, seed, dataset fingerprint, split episode IDs, dependency versions, and metrics.
- Prevent accidental overwrite by assigning each run a stable identifier.
- Keep regression with MSE as the initial teaching model.

### Acceptance Criteria

- Hyperparameters can be changed without source edits.
- Identical data, configuration, and seed reproduce the split and near-identical metrics.
- Training progress remains responsive and explains loss in plain language.
- Saved models load on CPU regardless of the device used during training.

## Phase 4 — Add Objective Evaluation and Comparison

### Tasks

- Separate environment transitions from rendering so evaluation can run headlessly and quickly.
- Evaluate a model over a finite, seeded scenario set.
- Report successes/N, success percentage, mean/median successful steps, stalled episodes, and out-of-bounds episodes.
- Add a simple hand-coded expert and untrained model as contextual baselines.
- Save evaluation JSON linked to the experiment bundle.
- Provide watch, pause, speed, and model-selection controls.
- Add a comparison view for dataset size, configuration, loss curves, and gameplay results.
- Offer “collect corrective demonstrations” from failure scenarios.

### Acceptance Criteria

- Evaluation always terminates after N episodes and metric counts reconcile to N.
- Repeated evaluation with the same seed uses identical scenarios.
- Training loss and gameplay success are clearly distinguished.
- Model/schema/normalization incompatibilities fail with corrective guidance.

## Phase 5 — Beginner Workflow, Packaging, and Portability

### Tasks

- Make `python -m behavior_cloning_game` open a menu for the complete learning loop.
- Also expose scriptable `collect`, `inspect`, `train`, and `evaluate` subcommands with useful `--help`.
- Add PEP 621 packaging in `pyproject.toml` and use `pathlib` so commands work outside the repository directory.
- Initially support a deliberately tested Python range, then expand only when CI verifies it.
- Keep direct runtime dependencies only: NumPy, pandas, Pygame, and PyTorch. Remove unused TorchVision and TorchAudio.
- Put pytest, Ruff, and optional typing tools in a development extra.
- Add Linux, macOS, and Windows CI for installation, unit tests, tiny training, artifact loading, and headless smoke tests where reliable.
- Document Bash/zsh, PowerShell, and Command Prompt setup separately.

### Acceptance Criteria

- A fresh virtual environment on all supported platforms can install, show help, collect data, train a fixture, and evaluate it.
- No workflow depends on the current working directory or an OS-specific font/path.
- `pip check`, tests, lint, and formatting pass in CI.

## Phase 6 — Guided Lessons and Classroom Materials

### Lessons

1. Map state features to expert action labels.
2. Compare 5 demonstrations with 50 demonstrations.
3. Diagnose balanced versus directionally biased data.
4. Change one of epochs, learning rate, or batch size and predict the effect.
5. Contrast training loss with validation loss and gameplay success.
6. Observe distribution shift, collect corrective demonstrations, and retrain.
7. Compare continuous regression/MSE with optional nine-class action classification.

Each 10–20 minute lesson should state an objective, ask the learner to predict an outcome, change one variable, visualize the result, and end with a reflection question. Add a five-minute learner quick start and an instructor guide.

### Acceptance Criteria

- Every lesson produces a saved, comparable result.
- Explanations avoid claiming that one stochastic run proves a general rule.
- A learner can explain features, labels, loss, validation, generalization, and covariate shift after completing the sequence.

## Parallel Work Strategy

After Phase 0 contracts are reviewed and frozen, use parallel agents or contributors with exclusive ownership:

| Workstream | Scope | Primary files | Depends on |
|---|---|---|---|
| A — Game core | Domain, iterative lifecycle, deterministic environment | `domain.py`, `environment.py` | Phase 0 |
| B — Data/ML | Recorder, validation, splitting, training, artifacts | `data.py`, `model.py`, `training.py` | Phase 0 events/schema |
| C — UX/evaluation | Renderer, menu, HUD, inspection and evaluation views | `rendering.py`, `cli.py`, `evaluation.py` | Stable A/B APIs |
| D — Platform/docs | Packaging, CI, setup, lessons, manual OS checks | `pyproject.toml`, CI, `docs/` | CLI contract |

One integration owner should review shared contracts and assemble end-to-end changes. Avoid concurrent edits to current `game.py`, `train.py`, or the future `pyproject.toml`. Integrate A before B, B before C, and D continuously once command contracts stabilize.

## Suggested Pull Request Sequence

1. Test harness, fixtures, domain/data contracts.
2. Game lifecycle and correctness fixes.
3. Versioned recorder, loader, validation, and inspection.
4. Pure environment extraction and deterministic scenarios.
5. Reproducible training and portable experiment bundles.
6. Finite evaluation, baselines, and comparison metrics.
7. Beginner menu, HUD, and compatibility wrappers.
8. Packaging, dependency cleanup, and cross-platform CI.
9. Guided lessons and instructor documentation.
10. Remove deprecated code after the replacement workflow is proven.

Each PR should include tests, documentation for learner-visible behavior, and a runnable acceptance command. Avoid combining behavior changes with broad formatting or file moves.

## Risks and Mitigations

- **Breaking existing artifacts:** version schemas, preserve legacy adapters, and retain committed fixtures.
- **Overengineering a teaching tool:** limit architecture to domain, adapters, and small pure services; every abstraction must clarify a taught concept.
- **Pygame CI instability:** keep rules independent of rendering and restrict SDL smoke tests to reliable runners.
- **PyTorch size/platform differences:** use CPU-only CI, a tested Python range, tiny fixtures, and optional manual accelerator checks.
- **Biased or sparse demonstrations:** validate action coverage and episode count before training, but explain warnings rather than hiding data.
- **UI blocking during training:** run training outside the rendering loop or pump UI events between epochs.

## End-to-End Release Gate

From a fresh environment on Linux, macOS, or Windows, a beginner can:

1. Launch one command.
2. Collect at least three complete demonstrations.
3. Inspect states, actions, outcomes, and balance.
4. Choose a preset or adjust documented hyperparameters.
5. Train while viewing training and validation loss.
6. Evaluate on a finite seeded scenario set.
7. Compare the result with a baseline or previous experiment.
8. Add corrective demonstrations and repeat.

The workflow requires no source editing, manual extension removal, or unexplained file selection; all artifacts are portable, self-describing, and covered by automated tests.
