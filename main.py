import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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


def save_state(storage, game):
    """저장 실패를 안내하고 한 번 재시도한다."""
    for attempt in range(2):
        try:
            storage.save(game.quizzes, game.scores)
            return True
        except OSError as error:
            if attempt == 0:
                print(f"저장에 실패했습니다({error}). 한 번 더 시도합니다.")
            else:
                print("재시도도 실패했습니다. 프로그램을 종료하기 전에 state.json 권한을 확인하세요.")
    return False


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
            print("\n중단되었습니다. 임시 파일을 만든 뒤 교체하는 방식으로 저장하고 종료합니다.")
            save_state(storage, game)
            return
        if choice == "1":
            game.play()
            save_state(storage, game)
        elif choice == "2":
            question = input("문제: ").strip()
            choices = [input(f"보기 {i}: ").strip() for i in range(1, 5)]
            try:
                answer = int(input("정답 번호(1~4): "))
                game.add_quiz(Quiz(question, choices, answer))
                save_state(storage, game)
                print("문제를 추가했습니다.")
            except ValueError as error:
                print(f"추가하지 못했습니다: {error}")
        elif choice == "3":
            for index, quiz in enumerate(game.quizzes, 1):
                print(f"{index}. {quiz.question}")
        elif choice == "4":
            summary = game.score_summary()
            print(f"최고 점수: {summary['high_score']}/{len(game.quizzes)}")
            print(f"도전 횟수: {summary['attempts']}")
        elif choice == "5":
            save_state(storage, game)
            print("저장하고 종료합니다.")
            return
        else:
            print("1~5 중에서 선택하세요.")


if __name__ == "__main__":
    run()
