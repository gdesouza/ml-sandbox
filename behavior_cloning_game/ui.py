"""Graphical launcher for the behavior-cloning learning workflow."""

from __future__ import annotations

import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pygame

WINDOW_SIZE = (920, 640)
BACKGROUND = (244, 247, 252)
PANEL = (255, 255, 255)
INK = (25, 35, 55)
MUTED = (91, 105, 130)
BLUE = (53, 115, 255)
BLUE_DARK = (35, 82, 190)
BORDER = (218, 225, 237)
SUCCESS = (31, 135, 85)
ERROR = (190, 55, 62)

WORKFLOWS = (
    ("collect", "1", "Collect", "Play with the arrow keys and record demonstrations."),
    ("inspect", "2", "Inspect", "Review states, actions, outcomes, and data balance."),
    ("train", "3", "Train", "Fit a policy and save a reproducible experiment."),
    ("evaluate", "4", "Evaluate", "Watch a trained policy attempt the task."),
)


@dataclass(frozen=True)
class Button:
    rectangle: pygame.Rect
    label: str
    value: str

    def contains(self, position: tuple[int, int]) -> bool:
        return self.rectangle.collidepoint(position)


def inspect_dataset(path: Path, game_directory: Path) -> Any:
    """Load a dataset summary using the same services as the script command."""
    game_path = str(game_directory)
    if game_path not in sys.path:
        sys.path.insert(0, game_path)
    from util.data import load_demonstrations
    from util.inspection import summarize_demonstrations

    rows, legacy = load_demonstrations(path)
    return summarize_demonstrations(rows, legacy=legacy)


def discover_artifacts(data_directory: Path, command: str) -> list[Path]:
    """Return newest compatible artifacts for a workflow."""
    patterns = ("*.csv",) if command in {"inspect", "train"} else ("model_*.json", "*.pth")
    paths = {path for pattern in patterns for path in data_directory.glob(pattern)}
    return sorted(paths, key=lambda path: (path.stat().st_mtime, path.name), reverse=True)


def _font(size: int, *, bold: bool = False) -> pygame.font.Font:
    return pygame.font.SysFont("arial", size, bold=bold)


def _text(
    surface: pygame.Surface,
    value: str,
    position: tuple[int, int],
    size: int,
    colour: tuple[int, int, int] = INK,
    *,
    bold: bool = False,
) -> None:
    surface.blit(_font(size, bold=bold).render(value, True, colour), position)


def _draw_header(surface: pygame.Surface) -> None:
    pygame.draw.circle(surface, BLUE, (61, 56), 24)
    pygame.draw.circle(surface, PANEL, (61, 56), 9)
    _text(surface, "Behavior Cloning Lab", (101, 31), 28, bold=True)
    _text(surface, "Collect  →  Inspect  →  Train  →  Evaluate", (102, 66), 15, MUTED)


def _workflow_buttons(surface: pygame.Surface) -> list[Button]:
    buttons: list[Button] = []
    for index, (command, number, title, description) in enumerate(WORKFLOWS):
        column, row = index % 2, index // 2
        rectangle = pygame.Rect(48 + column * 424, 132 + row * 174, 400, 144)
        hovered = rectangle.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(
            surface,
            (248, 251, 255) if hovered else PANEL,
            rectangle,
            border_radius=14,
        )
        pygame.draw.rect(surface, BLUE if hovered else BORDER, rectangle, width=2, border_radius=14)
        pygame.draw.circle(surface, BLUE, (rectangle.x + 38, rectangle.y + 38), 20)
        number_surface = _font(17, bold=True).render(number, True, PANEL)
        number_rectangle = number_surface.get_rect(center=(rectangle.x + 38, rectangle.y + 38))
        surface.blit(number_surface, number_rectangle)
        _text(surface, title, (rectangle.x + 72, rectangle.y + 22), 23, bold=True)
        _text(surface, description, (rectangle.x + 24, rectangle.y + 78), 15, MUTED)
        buttons.append(Button(rectangle, title, command))
    return buttons


def _draw_home(surface: pygame.Surface, status: tuple[str, bool] | None) -> list[Button]:
    surface.fill(BACKGROUND)
    _draw_header(surface)
    _text(surface, "Choose the next step", (48, 105), 17, MUTED)
    buttons = _workflow_buttons(surface)
    pygame.draw.rect(surface, PANEL, (48, 500, 824, 88), border_radius=12)
    if status:
        message, succeeded = status
        _text(surface, message, (72, 523), 17, SUCCESS if succeeded else ERROR, bold=True)
        _text(surface, "Choose another step whenever you are ready.", (72, 550), 14, MUTED)
    else:
        _text(
            surface,
            "Tip: collect several varied demonstrations before training.",
            (72, 531),
            16,
            MUTED,
        )
    _text(surface, "Press 1–4 to choose a step • Esc to exit", (48, 608), 13, MUTED)
    return buttons


def _short_path(path: Path, data_directory: Path) -> str:
    try:
        return str(path.relative_to(data_directory.parent.parent))
    except ValueError:
        return str(path)


def _draw_picker(
    surface: pygame.Surface,
    command: str,
    artifacts: Sequence[Path],
    data_directory: Path,
) -> list[Button]:
    surface.fill(BACKGROUND)
    _draw_header(surface)
    title = next(item[2] for item in WORKFLOWS if item[0] == command)
    noun = "dataset" if command in {"inspect", "train"} else "model"
    _text(surface, f"{title}: choose a {noun}", (48, 112), 24, bold=True)
    _text(surface, "Newest files appear first.", (48, 145), 15, MUTED)
    buttons = [Button(pygame.Rect(48, 572, 112, 42), "Back", "back")]
    if not artifacts:
        _text(surface, f"No compatible {noun} files were found in game/data.", (48, 214), 18, MUTED)
    for index, path in enumerate(artifacts[:7]):
        rectangle = pygame.Rect(48, 184 + index * 51, 824, 42)
        hovered = rectangle.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(surface, PANEL, rectangle, border_radius=8)
        pygame.draw.rect(surface, BLUE if hovered else BORDER, rectangle, width=2, border_radius=8)
        _text(surface, path.name, (rectangle.x + 16, rectangle.y + 8), 16, bold=True)
        _text(
            surface,
            _short_path(path, data_directory),
            (rectangle.x + 430, rectangle.y + 10),
            13,
            MUTED,
        )
        buttons.append(Button(rectangle, path.name, str(path)))
    back = buttons[0]
    pygame.draw.rect(surface, PANEL, back.rectangle, border_radius=8)
    pygame.draw.rect(surface, BORDER, back.rectangle, width=2, border_radius=8)
    _text(surface, "← Back", (back.rectangle.x + 19, back.rectangle.y + 10), 16, INK, bold=True)
    _text(surface, "Esc to go back", (740, 588), 13, MUTED)
    return buttons


def _panel(surface: pygame.Surface, rectangle: pygame.Rect) -> None:
    pygame.draw.rect(surface, PANEL, rectangle, border_radius=12)
    pygame.draw.rect(surface, BORDER, rectangle, width=1, border_radius=12)


def _wrap(value: str, limit: int) -> list[str]:
    words = value.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and len(candidate) > limit:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def _draw_inspection(
    surface: pygame.Surface,
    path: Path,
    summary: Any,
) -> list[Button]:
    surface.fill(BACKGROUND)
    _draw_header(surface)
    _text(surface, "Dataset inspection", (48, 105), 24, bold=True)
    _text(surface, path.name, (48, 138), 15, MUTED)

    metrics = (
        ("Samples", str(summary.samples)),
        ("Episodes", str(summary.episodes)),
        ("No-op actions", f"{summary.no_op_ratio:.1%}"),
    )
    for index, (label, value) in enumerate(metrics):
        rectangle = pygame.Rect(48 + index * 282, 174, 260, 82)
        _panel(surface, rectangle)
        _text(surface, label, (rectangle.x + 18, rectangle.y + 14), 14, MUTED)
        _text(surface, value, (rectangle.x + 18, rectangle.y + 37), 25, bold=True)

    outcomes_panel = pygame.Rect(48, 276, 260, 188)
    _panel(surface, outcomes_panel)
    _text(surface, "Episode outcomes", (66, 294), 17, bold=True)
    outcome_colours = {
        "success": SUCCESS,
        "out_of_bounds": ERROR,
        "stalled": (218, 139, 45),
        "quit": MUTED,
        "unknown": MUTED,
    }
    visible_outcomes = [
        item for item in summary.outcomes.items() if item[1] or item[0] != "quit"
    ]
    for index, (name, count) in enumerate(visible_outcomes[:5]):
        y = 327 + index * 25
        pygame.draw.circle(surface, outcome_colours.get(name, MUTED), (70, y + 7), 5)
        _text(surface, name.replace("_", " ").title(), (84, y), 14, MUTED)
        _text(surface, str(count), (276, y), 14, INK, bold=True)

    actions_panel = pygame.Rect(328, 276, 544, 188)
    _panel(surface, actions_panel)
    _text(surface, "Action distribution", (346, 294), 17, bold=True)
    action_items = sorted(
        summary.action_histogram.items(), key=lambda item: (-item[1], item[0])
    )
    maximum = max((count for _, count in action_items), default=1)
    for index, ((x, y), count) in enumerate(action_items[:5]):
        top = 327 + index * 25
        _text(surface, f"({x:g}, {y:g})", (346, top), 14, MUTED)
        pygame.draw.rect(surface, BORDER, (430, top + 3, 330, 12), border_radius=6)
        width = max(3, round(330 * count / maximum))
        pygame.draw.rect(surface, BLUE, (430, top + 3, width, 12), border_radius=6)
        _text(surface, str(count), (780, top), 14, INK, bold=True)
    if len(action_items) > 5:
        _text(surface, f"+ {len(action_items) - 5} more actions", (346, 447), 12, MUTED)

    guidance_panel = pygame.Rect(48, 484, 824, 96)
    _panel(surface, guidance_panel)
    heading = "Data-quality guidance" if summary.warnings else "Ready to train"
    _text(surface, heading, (66, 500), 16, bold=True)
    guidance = summary.warnings or ("No obvious data-quality warnings were found.",)
    line_y = 526
    for warning in guidance[:2]:
        for line in _wrap(warning, 92)[:2]:
            colour = ERROR if summary.warnings else SUCCESS
            _text(surface, f"• {line}", (66, line_y), 13, colour)
            line_y += 18

    back = Button(pygame.Rect(48, 594, 112, 38), "Back", "back")
    train = Button(pygame.Rect(680, 594, 192, 38), "Train", "train-selected")
    for button, fill, colour in ((back, PANEL, INK), (train, BLUE, PANEL)):
        pygame.draw.rect(surface, fill, button.rectangle, border_radius=8)
        if button is back:
            pygame.draw.rect(surface, BORDER, button.rectangle, width=2, border_radius=8)
        label = "← Datasets" if button is back else "Train this dataset →"
        label_surface = _font(15, bold=True).render(label, True, colour)
        label_rectangle = label_surface.get_rect(center=button.rectangle.center)
        surface.blit(label_surface, label_rectangle)
    return [back, train]


def launch(
    run_workflow: Callable[[str, Sequence[str]], int],
    data_directory: Path,
) -> int:
    """Open the launcher and dispatch selected workflows."""
    try:
        pygame.init()
        surface = pygame.display.set_mode(WINDOW_SIZE)
    except pygame.error as error:
        print(f"Could not open the graphical launcher: {error}")
        print("Run with --text to use the terminal menu instead.")
        pygame.quit()
        return 1

    pygame.display.set_caption("Behavior Cloning Lab")
    clock = pygame.time.Clock()
    screen = "home"
    selected_command = ""
    artifacts: list[Path] = []
    inspected_path: Path | None = None
    inspection: Any = None
    status: tuple[str, bool] | None = None
    running = True

    while running:
        if screen == "home":
            buttons = _draw_home(surface, status)
        elif screen == "inspection":
            buttons = _draw_inspection(surface, inspected_path, inspection)
        else:
            buttons = _draw_picker(surface, selected_command, artifacts, data_directory)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if screen in {"picker", "inspection"}:
                        screen = "home"
                    else:
                        running = False
                elif screen == "home" and event.unicode in "1234":
                    selected_command = WORKFLOWS[int(event.unicode) - 1][0]
                    if selected_command == "collect":
                        code = run_workflow(selected_command, ())
                        status = (
                            "Collection finished."
                            if code == 0
                            else "Collection exited with an error.",
                            code == 0,
                        )
                    else:
                        artifacts = discover_artifacts(data_directory, selected_command)
                        screen = "picker"
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                clicked = next((button for button in buttons if button.contains(event.pos)), None)
                if clicked is None:
                    continue
                if clicked.value == "back":
                    screen = "picker" if screen == "inspection" else "home"
                elif clicked.value == "train-selected":
                    code = run_workflow("train", (str(inspected_path),))
                    status = (
                        "Training finished."
                        if code == 0
                        else "Training exited with an error.",
                        code == 0,
                    )
                    screen = "home"
                elif screen == "home":
                    selected_command = clicked.value
                    if selected_command == "collect":
                        code = run_workflow(selected_command, ())
                        status = (
                            "Collection finished."
                            if code == 0
                            else "Collection exited with an error.",
                            code == 0,
                        )
                    else:
                        artifacts = discover_artifacts(data_directory, selected_command)
                        screen = "picker"
                else:
                    if selected_command == "inspect":
                        inspected_path = Path(clicked.value)
                        try:
                            inspection = inspect_dataset(
                                inspected_path, data_directory.parent
                            )
                        except (OSError, ValueError) as error:
                            status = (f"Inspection failed: {error}", False)
                            screen = "home"
                        else:
                            screen = "inspection"
                    else:
                        code = run_workflow(selected_command, (clicked.value,))
                        title = next(
                            item[2] for item in WORKFLOWS if item[0] == selected_command
                        )
                        status = (
                            f"{title} finished."
                            if code == 0
                            else f"{title} exited with an error.",
                            code == 0,
                        )
                        screen = "home"
        clock.tick(60)

    pygame.quit()
    return 0
