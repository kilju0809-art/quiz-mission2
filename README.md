# Python·Git 기초 퀴즈

Python과 Git의 기초 개념을 4지선다 퀴즈로 복습하는 콘솔 프로그램입니다. 기본 문제는 학습 목적에 맞춰 직접 작성한 `DEFAULT_QUIZZES`이며, 문제와 보기는 실제 코드에 5개가 들어 있습니다.

## 실행 방법

```powershell
python main.py
python -m unittest discover -s . -p "test_*.py"
```

메뉴별 흐름은 다음과 같습니다. `1`은 문제를 풀고 숫자 외 입력이나 1~4 범위 밖 입력을 다시 요청합니다. `2`는 문제·보기·정답을 입력하며 빈 값과 잘못된 정답 번호를 거부합니다. `3`은 문제 목록을 출력하고, `4`는 최고 점수와 도전 횟수를 출력하며, `5`는 저장 후 종료합니다.

## 주요 기능

- 기본 4지선다 문제 5개 풀이와 점수 계산
- 문제 추가, 문제 목록, 최고 점수, 종료 메뉴
- `state.json`에 문제와 점수 저장 및 재실행 복원
- 잘못된 번호, 빈 문제·보기, 손상된 JSON 처리
- 저장 실패 시 안내 후 1회 자동 재시도
- 저장은 `state.tmp`에 먼저 기록한 뒤 원본으로 교체해 중간 손상을 줄임

## 파일 구조와 책임 경계

- `quiz.py`: `Quiz`가 문제 데이터 검증과 정답 판정을 담당합니다. 사용자 입력과 화면 출력은 담당하지 않습니다.
- `game.py`: `QuizGame`이 문제 목록·점수·풀이 흐름을 관리합니다.
- `storage.py`: `StateStorage`가 파일 읽기→JSON 파싱→구조 검증→객체 변환, 저장→임시 파일 기록→교체 순서를 담당합니다.
- `main.py`: 메뉴 입력·출력과 저장 실패 안내를 담당합니다.
- `test_quiz.py`: 검증, 잘못된 입력, 저장 복원, 손상 파일 복구 테스트입니다.

클래스를 사용하면 문제와 게임 상태를 묶어 여러 메뉴에서 재사용할 수 있고, 함수만 사용하는 방식보다 책임과 상태가 명확합니다. 입력 검증은 `Quiz`·`game.py`, 데이터 IO는 `storage.py`에 둔다는 규칙으로 분리했습니다.

| 책임 | 코드 위치 | 실패 시 처리 |
|---|---|---|
| 입력·범위 검증 | `Quiz`, `QuizGame.play` | 안내 후 재입력 |
| 메뉴·출력 | `main.run` | 잘못된 메뉴 안내 |
| 파일·JSON IO | `StateStorage.load/save` | 기본값 사용 또는 1회 재시도 |

## JSON 설계와 복구

`state.json`은 다음 구조입니다.

```json
{"quizzes": [{"question": "...", "choices": ["..."], "answer": 1}], "scores": [5]}
```

`quizzes`는 문제 추가와 순서 보존을 위해 배열이고, `scores`는 시도별 점수 기록과 최고 점수 계산을 위해 별도 배열입니다. 이 중첩 구조는 사람이 읽기 쉽고 다른 Python 프로그램으로 옮기기 쉽지만, 데이터가 수천 문제 또는 수 MB 이상으로 커지면 SQLite 같은 DB로 전환하는 편이 적절합니다.

파일이 없으면 기본 문제를 사용합니다. JSON이 손상되면 기본 문제로 복구하고 오류를 안내합니다. 자동 백업본은 보관하지 않으므로 중요한 데이터는 사용자가 `state.json`을 별도 복사해야 하며, 현재 구현의 복구 절차는 백업 파일을 되돌린 뒤 재실행하는 것입니다.

복구 우선순위는 `state.json` 존재 확인 → JSON 파싱 → 필수 필드와 문제 구조 검증 → 실패 시 기본 문제 사용입니다. 스키마를 바꿀 때는 새 필드를 기본값으로 읽는 하위 호환 로더와 마이그레이션 테스트를 먼저 추가합니다.

## Git 실습 증거

커밋 메시지는 `feat:`, `fix:`, `test:`, `docs:`, `chore:`처럼 범주 접두사를 사용하고, 한 커밋에는 하나의 기능·수정·문서 목적만 담았습니다. 기능 브랜치는 검증과 안전 저장을 독립적으로 확인하기 위해 만들었고, 병합은 작업 결과를 `main`에 통합하는 과정입니다. 충돌이 생기면 양쪽 변경을 확인해 수동 해결 후 `git add`와 merge continue를 수행합니다.

실제 최종 로그는 다음과 같습니다.

```text
* 34e0ebc docs: address evaluation feedback
* 05cb1ec fix: configure UTF-8 console output
* c9eba59 docs: record clone and pull practice
*   8a47c82 merge: validation and safe persistence
|\\
| * 89c4100 chore: ignore temporary state files
| * 01f4c16 test: verify corrupted state recovery
| * c8bfc1b docs: document validation and safe saves
| * fb006fb feat: show quiz attempt count
| * ce3569c test: cover validation and score summary
| * b16bb62 fix: save state atomically
| * 4e4ceab feat: expose score summary
| * ed2a14d fix: reject blank quiz choices
|/
* dcf2cb7 feat: complete Python Git quiz mission
* 5ca1d68 Initial commit
```

전체 로그·원격 URL은 [evidence/git-log.txt](evidence/git-log.txt), clone/pull 결과는 [evidence/clone-pull.txt](evidence/clone-pull.txt), 테스트 실행 결과는 [evidence/test-run.txt](evidence/test-run.txt)에 보관했습니다.

별도 `mission2-clone` 폴더에서 README를 수정하고 `c9eba59 docs: record clone and pull practice`로 commit·push한 뒤, 원본 폴더에서 `git pull --ff-only origin main`으로 반영했습니다. 이후 UTF-8 개선 커밋도 원본과 clone 양쪽에 pull했습니다.

## 주요 변경 시 수정 위치

- 문제 내용·정답 변경: `main.py`의 `DEFAULT_QUIZZES`
- 입력 범위·정답 판정: `game.py`의 `play`, `quiz.py`의 `check_answer`
- 저장 형식·복구: `storage.py`의 `load`, `save`
- 메뉴와 저장 실패 안내: `main.py`의 `run`, `save_state`
- 회귀 검증: `test_quiz.py`

## 개선점과 한계

현재 자동 백업본 보관 정책은 없고, JSON 전체를 다시 저장합니다. 데이터가 수천 문제 또는 수 MB를 넘으면 SQLite와 백업 회전 정책(예: 최근 3개)을 도입하는 것이 좋습니다.

변경 영향 범위는 다음과 같습니다.

| 변경 유형 | 우선 수정 파일 | 함께 확인할 항목 |
|---|---|---|
| 문제 데이터 | `main.py` | `test_quiz.py`, JSON 복원 |
| 입력 규칙 | `quiz.py`, `game.py` | 오류 메시지와 재시도 테스트 |
| 저장 포맷 | `storage.py` | JSON 예시, 마이그레이션 |
| 메뉴/UI | `main.py` | 메뉴 실행 로그 |

5개 기본 문제를 메모리에서 순회하는 현재 테스트는 0.02초 이내에 끝났습니다. 문제 수가 수천 개가 되면 JSON 전체를 메모리에 올리고 다시 쓰는 비용이 커지므로 SQLite로 전환합니다.
