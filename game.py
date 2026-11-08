from quiz import Quiz


class QuizGame:
    def __init__(self, quizzes, scores=None):
        self.quizzes = quizzes
        self.scores = scores or []

    def play(self, input_func=input):
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
