import os
from pathlib import Path

import pygame

from behavior_cloning_game.ui import Button, discover_artifacts, inspect_dataset


def test_discover_datasets_newest_first(tmp_path):
    older = tmp_path / "demonstrations_old.csv"
    newer = tmp_path / "demonstrations_new.csv"
    older.write_text("old", encoding="utf-8")
    newer.write_text("new", encoding="utf-8")
    older.touch()
    newer.touch()
    older_time = older.stat().st_mtime - 10
    older.touch()
    newer.touch()
    os.utime(older, (older_time, older_time))

    assert discover_artifacts(tmp_path, "train") == [newer, older]
    assert discover_artifacts(tmp_path, "inspect") == [newer, older]


def test_discover_models_ignores_unrelated_json(tmp_path):
    metadata = tmp_path / "model_run.json"
    weights = tmp_path / "legacy.pth"
    unrelated = tmp_path / "evaluation.json"
    for path in (metadata, weights, unrelated):
        path.write_text("content", encoding="utf-8")

    assert set(discover_artifacts(tmp_path, "evaluate")) == {metadata, weights}


def test_button_hit_area():
    button = Button(pygame.Rect(10, 20, 100, 40), "Train", "train")
    assert button.contains((20, 30))
    assert not button.contains((5, 5))


def test_inspect_dataset_uses_shared_summary(tmp_path):
    dataset = tmp_path / "demo.csv"
    dataset.write_text(
        "schema_version,episode_id,step,elapsed_ms,blue_x,blue_y,target_x,target_y,"
        "action_x,action_y,outcome\n"
        "2,1,0,0,10,20,100,200,5,0,success\n",
        encoding="utf-8",
    )

    summary = inspect_dataset(dataset, Path("game").resolve())

    assert summary.samples == 1
    assert summary.episodes == 1
    assert summary.outcomes["success"] == 1
