import argparse
from datetime import datetime
from pathlib import Path

from util.data import EpisodeRecorder
from util.domain import GameMode
from util.game import Game


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect behavior-cloning demonstrations.")
    parser.add_argument("--episodes", type=int, help="Stop after this many episodes.")
    parser.add_argument("--seed", type=int, help="Repeat the same target sequence.")
    parser.add_argument("--output", type=Path, help="Destination CSV file.")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = args.output or Path(__file__).parent / "data" / f"demonstrations_{timestamp}.csv"
    recorder = EpisodeRecorder(destination)
    game = Game(seed=args.seed, recorder=recorder, mode=GameMode.COLLECTION)
    try:
        results = game.start(max_episodes=args.episodes)
    finally:
        game.quit()

    completed = sum(result.outcome.value != "quit" for result in results)
    print(f"Saved {completed} completed episode(s) to {destination.resolve()}")


if __name__ == "__main__":
    main()
