from quiz import Quiz


class QuizGame:
    """문제 목록을 순회하고 점수를 기록하는 게임 관리자입니다."""
    def __init__(self, quizzes, scores=None):
        self.quizzes = quizzes
        self.scores = scores or []

    def play(self, input_func=input):
        """입력을 받아 한 라운드의 점수를 계산합니다."""
        score = 0
        for quiz in self.quizzes:
            quiz.ask()
            while True:
                try:
                    selected = int(input_func("답 번호: "))
                    if not 1 <= selected <= 4:
                        raise ValueError
                    break
                except (ValueError, TypeError):
                    print("1~4 사이의 숫자를 입력하세요.")
            if quiz.check_answer(selected):
                print("정답입니다!")
                score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")
            if quiz.explanation:
                print(quiz.explanation)
        self.scores.append(score)
        print(f"총점: {score}/{len(self.quizzes)}")
        return score

    def add_quiz(self, quiz):
        self.quizzes.append(quiz)

    def high_score(self):
        return max(self.scores, default=0)

    def score_summary(self):
        return {"attempts": len(self.scores), "high_score": self.high_score()}
