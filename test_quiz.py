import tempfile
import unittest
from pathlib import Path

from game import QuizGame
from quiz import Quiz
from storage import StateStorage


class QuizTests(unittest.TestCase):
    def test_quiz_validation(self):
        with self.assertRaises(ValueError):
            Quiz("문제", ["1", "2"], 1)
        with self.assertRaises(ValueError):
            Quiz("문제", ["1", "", "3", "4"], 1)

    def test_game_score_and_invalid_input(self):
        quiz = Quiz("1+1?", ["1", "2", "3", "4"], 2)
        answers = iter(["abc", "9", "2"])
        game = QuizGame([quiz])
        self.assertEqual(game.play(lambda _: next(answers)), 1)

    def test_storage_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            storage = StateStorage(Path(folder) / "state.json")
            quiz = Quiz("저장?", ["a", "b", "c", "d"], 1)
            storage.save([quiz], [1])
            quizzes, scores = storage.load([])
            self.assertEqual(quizzes[0].question, "저장?")
            self.assertEqual(scores, [1])

    def test_score_summary(self):
        game = QuizGame([], [2, 4])
        self.assertEqual(game.score_summary(), {"attempts": 2, "high_score": 4})

    def test_corrupted_state_uses_defaults(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "state.json"
            path.write_text("{broken", encoding="utf-8")
            default = Quiz("기본?", ["a", "b", "c", "d"], 1)
            quizzes, scores = StateStorage(path).load([default])
            self.assertEqual(quizzes[0].question, "기본?")
            self.assertEqual(scores, [])


if __name__ == "__main__":
    unittest.main()
