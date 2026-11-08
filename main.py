from game import QuizGame
from quiz import Quiz
from storage import StateStorage


DEFAULT_QUIZZES = [
    Quiz("Python에서 여러 값을 순서대로 저장하는 자료구조는?", ["리스트", "함수", "클래스", "예외"], 1, "리스트는 여러 값을 순서대로 보관합니다."),
    Quiz("Git에서 변경 내용을 다음 커밋에 넣을 준비를 하는 명령은?", ["git push", "git add", "git pull", "git clone"], 2),
    Quiz("Python에서 예외를 처리할 때 사용하는 구조는?", ["if/else", "for/in", "try/except", "class/import"], 3),
    Quiz("Git의 로컬 기록을 저장하는 명령은?", ["git commit", "git status", "git branch", "git diff"], 1),
    Quiz("한 문제의 데이터와 동작을 묶는 Python 문법 요소는?", ["리스트", "문자열", "클래스", "주석"], 3),
]


def run():
    storage = StateStorage()
    quizzes, scores = storage.load(DEFAULT_QUIZZES)
    game = QuizGame(quizzes, scores)
    while True:
        print("\n=== Python·Git 퀴즈 ===")
        print("1. 퀴즈 풀기  2. 문제 추가  3. 문제 목록  4. 최고 점수  5. 종료")
        try:
            choice = input("선택: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n종료합니다.")
            storage.save(game.quizzes, game.scores)
            return
        if choice == "1":
            game.play()
            storage.save(game.quizzes, game.scores)
        elif choice == "2":
            question = input("문제: ").strip()
            choices = [input(f"보기 {i}: ").strip() for i in range(1, 5)]
            try:
                answer = int(input("정답 번호(1~4): "))
                game.add_quiz(Quiz(question, choices, answer))
                storage.save(game.quizzes, game.scores)
                print("문제를 추가했습니다.")
            except ValueError as error:
                print(f"추가하지 못했습니다: {error}")
        elif choice == "3":
            for index, quiz in enumerate(game.quizzes, 1):
                print(f"{index}. {quiz.question}")
        elif choice == "4":
            print(f"최고 점수: {game.high_score()}/{len(game.quizzes)}")
        elif choice == "5":
            storage.save(game.quizzes, game.scores)
            print("저장하고 종료합니다.")
            return
        else:
            print("1~5 중에서 선택하세요.")


if __name__ == "__main__":
    run()
