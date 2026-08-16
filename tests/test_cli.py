from pathlib import Path
from unittest.mock import Mock, patch

from behavior_cloning_game import cli


def test_project_directory_is_independent_of_current_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert (cli.project_directory() / "train.py").is_file()


def test_dispatch_uses_active_python_and_game_directory():
    completed = Mock(returncode=7)
    with patch("behavior_cloning_game.cli.subprocess.run", return_value=completed) as run:
        result = cli.run_workflow("inspect", ["example.csv"])

    assert result == 7
    command = run.call_args.args[0]
    assert command[0] == cli.sys.executable
    assert Path(command[1]).name == "inspect_data.py"
    assert command[2:] == [str(Path("example.csv").resolve())]
    assert run.call_args.kwargs["cwd"] == cli.project_directory()
    assert run.call_args.kwargs["check"] is False


def test_subcommand_forwards_arguments():
    with patch("behavior_cloning_game.cli.run_workflow", return_value=0) as run:
        assert cli.main(["train", "dataset.csv", "--", "--epochs", "2"]) == 0
    run.assert_called_once_with("train", ["dataset.csv", "--epochs", "2"])


def test_menu_can_exit(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "5")
    assert cli.interactive_menu() == 0
