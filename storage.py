import json
from pathlib import Path

from quiz import Quiz


class StateStorage:
    """JSON state 파일의 읽기, 검증, 안전한 저장을 담당합니다."""
    def __init__(self, path="state.json"):
        self.path = Path(path)

    def load(self, defaults):
        if not self.path.exists():
            return defaults, []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            scores = data.get("scores", [])
            if not isinstance(scores, list):
                raise ValueError("scores 형식 오류")
            return quizzes, scores
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            print(f"저장 파일을 읽지 못해 기본 문제를 사용합니다: {error}")
            return defaults, []

    def save(self, quizzes, scores):
        data = {"quizzes": [quiz.to_dict() for quiz in quizzes], "scores": scores}
        temp_path = self.path.with_suffix(".tmp")
        temp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        temp_path.replace(self.path)
