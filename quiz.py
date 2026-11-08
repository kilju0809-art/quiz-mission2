class Quiz:
    def __init__(self, question, choices, answer, explanation=""):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있을 수 없습니다.")
        if len(choices) != 4 or any(not isinstance(choice, str) or not choice.strip() for choice in choices):
            raise ValueError("보기는 4개여야 합니다.")
        if not 1 <= answer <= 4:
            raise ValueError("정답 번호는 1~4여야 합니다.")
        self.question = question
        self.choices = choices
        self.answer = answer
        self.explanation = explanation

    def ask(self):
        print(f"\n{self.question}")
        for number, choice in enumerate(self.choices, 1):
            print(f"{number}. {choice}")

    def check_answer(self, selected):
        return selected == self.answer

    def to_dict(self):
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data):
        return cls(data["question"], data["choices"], data["answer"], data.get("explanation", ""))
