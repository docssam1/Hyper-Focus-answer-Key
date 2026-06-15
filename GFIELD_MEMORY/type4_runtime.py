from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

TYPE_ID = 4
TYPE_GROUP = "A"
TYPE_TITLE = "쏙쏙 구멍 블록 놀이"
CONCEPT_AUDIO_PATH = "/api/audio/type4/concept-guide.mp3"
RETRY_AUDIO_PATH = "/api/audio/type4/retry-cheer.mp3"
LOCK_MESSAGE = "프리미엄 비전 분석 체험 1회가 끝났어. 이제 8번 패스로 이어서 놀아 보자!"
CALCULATION_CORE_SENTENCE = "아까운 산수 실수야! 연필 들고 다시 한 번만 콕콕 세어볼까?"
BLOCKED_WORDS = ["교차점", "단면화", "단면", "교차"]


def get_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _read_reference_transcript(repo_root: Path) -> str:
    transcript_path = repo_root / "youtube_script" / "cleaned_audio_script.md"
    if not transcript_path.exists():
        return ""
    return transcript_path.read_text(encoding="utf-8")


def _build_child_audio_script() -> str:
    return "\n".join(
        [
            "우리 같이 블록 케이크를 쓱쓱 잘라 보듯 생각해 보자.",
            "맨 먼저 블록이 모두 몇 개인지 큰 바구니처럼 한 번에 세어 줘.",
            "그다음 구멍이 지나간 길을 손가락으로 콕콕 따라가 줘.",
            "길이 두 개 만나면 가운데 대장 블록은 한 번만 빼야 해.",
            "식은 맞는데 숫자만 헷갈렸으면 천천히 다시 세면 돼.",
            "길 찾기부터 헷갈렸다면 쉬운 문제로 한 번 더 놀면서 감을 잡아 보자.",
        ]
    )


def _validate_no_blocked_words(text: str) -> bool:
    """금지어가 없으면 True 반환"""
    for word in BLOCKED_WORDS:
        if word in text:
            return False
    return True


def _line_x(size: int, y: int, z: int) -> Set[Tuple[int, int, int]]:
    return {(x, y, z) for x in range(size)}


def _line_y(size: int, x: int, z: int) -> Set[Tuple[int, int, int]]:
    return {(x, y, z) for y in range(size)}


def _line_z(size: int, x: int, y: int) -> Set[Tuple[int, int, int]]:
    return {(x, y, z) for z in range(size)}


def _sorted_blocks(blocks: Iterable[Tuple[int, int, int]]) -> List[Dict[str, int]]:
    return [
        {"x": x, "y": y, "z": z}
        for x, y, z in sorted(blocks, key=lambda item: (item[2], item[1], item[0]))
    ]


def _build_render_data(size: int, removed_blocks: Set[Tuple[int, int, int]]) -> Dict[str, Any]:
    all_blocks = {(x, y, z) for x in range(size) for y in range(size) for z in range(size)}
    filled_blocks = all_blocks - removed_blocks
    return {
        "shape": "hole-punched-cube",
        "gridSize": [size, size, size],
        "filledBlocks": _sorted_blocks(filled_blocks),
        "removedBlocks": _sorted_blocks(removed_blocks),
        "viewLabels": ["앞", "옆", "위"],
        "storyHint": "구멍 길을 손가락으로 콕콕 따라가 보고, 가운데 대장 블록은 한 번만 빼 줘.",
    }


def _build_problem(
    *,
    question_id: str,
    difficulty: str,
    text: str,
    size: int,
    removed_blocks: Set[Tuple[int, int, int]],
    answer_story: str,
    audio_path: str,
) -> Dict[str, Any]:
    answer = (size ** 3) - len(removed_blocks)
    return {
        "questionId": question_id,
        "difficulty": difficulty,
        "text": text,
        "answer": answer,
        "answerStory": answer_story,
        "renderData": _build_render_data(size, removed_blocks),
        "audioPath": audio_path,
    }


def _build_problem_sets(audio_path: str) -> Dict[str, Any]:
    easy_removed = _line_x(2, 0, 0)
    same_removed = _line_x(3, 1, 1) | _line_y(3, 1, 1)
    hard_removed = _line_x(4, 1, 1) | _line_y(4, 1, 1) | _line_z(4, 1, 1)

    original_problem = _build_problem(
        question_id="q4_origin",
        difficulty="same",
        text="3칸, 3칸, 3칸으로 쌓은 대장 블록이 있어. 가운데로 가로 구멍 하나랑 세로 구멍 하나를 쏙 뚫었지. 남은 블록은 몇 개일까?",
        size=3,
        removed_blocks=same_removed,
        answer_story="처음엔 27개야. 가로 길 3개와 세로 길 3개를 빼는데, 가운데 대장 블록 1개는 두 번 빼면 안 되니까 27 - (3 + 3 - 1) = 22야.",
        audio_path=audio_path,
    )

    easy_problem = _build_problem(
        question_id="q4_easy_1",
        difficulty="easy",
        text="2칸씩 쌓은 작은 블록 케이크가 있어. 옆으로 구멍 하나만 쏙 뚫으면 남은 블록은 몇 개일까?",
        size=2,
        removed_blocks=easy_removed,
        answer_story="처음엔 8개야. 구멍 길로 빠진 블록 2개를 빼면 6개가 남아.",
        audio_path=audio_path,
    )

    same_problem = _build_problem(
        question_id="q4_same_1",
        difficulty="same",
        text="3칸씩 쌓은 블록 케이크에서 가로 길 하나와 앞뒤 길 하나를 쏙 뚫었어. 두 길이 만나는 대장 블록은 하나야. 남은 블록은 몇 개일까?",
        size=3,
        removed_blocks=same_removed,
        answer_story="처음엔 27개야. 구멍 길은 3개, 또 다른 길도 3개지만 가운데 대장 블록은 한 번만 빼서 27 - 5 = 22야.",
        audio_path=audio_path,
    )

    hard_problem = _build_problem(
        question_id="q4_hard_1",
        difficulty="hard",
        text="4칸씩 쌓은 큰 블록 케이크에서 가로 길, 세로 길, 위아래 길을 모두 쏙 뚫었어. 세 길이 모두 한 대장 블록에서 만나. 남은 블록은 몇 개일까?",
        size=4,
        removed_blocks=hard_removed,
        answer_story="처음엔 64개야. 길마다 4개씩 빠지지만 세 길이 만나는 대장 블록은 한 번만 빼야 하니까 빠진 블록은 모두 10개, 그래서 54개가 남아.",
        audio_path=audio_path,
    )

    return {
        "originalProblem": original_problem,
        "fixedSimilars": [easy_problem, same_problem, hard_problem],
        "problemPool": {
            "easy": [easy_problem],
            "same": [same_problem],
            "hard": [hard_problem],
        },
    }


def build_type4_data(repo_root: Optional[Path] = None) -> Dict[str, Any]:
    repo_root = repo_root or get_repo_root()
    reference_transcript = _read_reference_transcript(repo_root)
    concept_script = _build_child_audio_script()
    problem_sets = _build_problem_sets(CONCEPT_AUDIO_PATH)

    calculation_feedback = (
        "와, 식 길을 찾은 눈이 정말 반짝반짝해! "
        f"{CALCULATION_CORE_SENTENCE} "
        "식은 이미 아주 멋지게 찾았으니까 마지막 숫자만 천천히 잡으면 정답에 바로 닿을 수 있어!"
    )
    concept_feedback = (
        "괜찮아, 우리 친구! 이번엔 구멍 길이 지나가는 자리를 조금 다르게 봤구나. "
        "독쌤 목소리를 들으면서 케이크 쪼개기처럼 길을 다시 찾아보자. "
        "가운데 대장 블록을 찾으면 훨씬 쉬워져!"
    )
    success_feedback = "정답이야! 블록 길 찾기를 정말 똑똑하게 해냈네. 이제 다음 놀이로 가 보자!"

    # 금지어 검증
    for text in [calculation_feedback, concept_feedback, success_feedback, concept_script]:
        assert _validate_no_blocked_words(text), f"금지어 포함됨: {text}"

    flow_routes = {
        "CALCULATION_ERROR": {
            "recommendedDifficulty": "SAME",
            "queueBucket": "same",
            "feedbackTitle": "아까운 계산 실수!",
            "feedbackText": calculation_feedback,
            "stitchesCard": "YellowClinicCard",
            "showRetryButton": True,
            "showAudioPlayer": False,
            "conceptAudioPath": None,
            "retryAudioPath": RETRY_AUDIO_PATH,
            "badgeText": "다시 콕콕",
        },
        "CONCEPT_ERROR": {
            "recommendedDifficulty": "EASY",
            "queueBucket": "easy",
            "feedbackTitle": "개념 콕콕 클리닉",
            "feedbackText": concept_feedback,
            "stitchesCard": "RedClinicCard",
            "showRetryButton": True,
            "showAudioPlayer": True,
            "conceptAudioPath": CONCEPT_AUDIO_PATH,
            "retryAudioPath": None,
            "badgeText": "꿀팁 듣기",
        },
        "NONE": {
            "recommendedDifficulty": "HARD",
            "queueBucket": "hard",
            "feedbackTitle": "정답 반짝 카드",
            "feedbackText": success_feedback,
            "stitchesCard": "GreenWinCard",
            "showRetryButton": False,
            "showAudioPlayer": False,
            "conceptAudioPath": None,
            "retryAudioPath": None,
            "badgeText": "다음 도전",
        },
    }

    return {
        "typeId": TYPE_ID,
        "group": TYPE_GROUP,
        "title": TYPE_TITLE,
        "targetUser": {
            "profile": "수학 앞서가는 7세",
            "mathReadyLevel": ["초2 주력", "초3 연산 허용"],
        },
        "languagePolicy": {
            "voice": "따뜻한 유아어",
            "blockedWords": BLOCKED_WORDS,
            "preferredPhrases": ["케이크 쪼개기", "대장 블록", "콕콕 세기"],
        },
        "originalProblem": problem_sets["originalProblem"],
        "fixedSimilars": problem_sets["fixedSimilars"],
        "aiTutorPack": {
            "conceptAudioPath": CONCEPT_AUDIO_PATH,
            "audioScriptText": concept_script,
            "referenceTranscriptPath": "youtube_script/cleaned_audio_script.md",
            "referenceTranscriptLoaded": bool(reference_transcript),
            "problemPool": problem_sets["problemPool"],
        },
        "flowController": {
            "lockPolicy": {
                "lv1": {
                    "aiTutorDailyLimit": 2,
                    "visionAnalysisLimit": 2,
                    "handwritingScope": "fixedSimilarsOnly",
                    "audioScope": "fixedSimilars+parentGuide",
                    "aiGeneratedSimilarLimit": 1,
                    "pdfScope": "selectedOne",
                    "adsEnabled": True,
                },
                "lv2": {
                    "aiTutorDailyLimit": -1,
                    "visionAnalysisLimit": 5,
                    "handwritingScope": "all",
                    "audioScope": "all",
                    "aiGeneratedSimilarLimit": -1,
                    "pdfScope": "all",
                    "adsEnabled": False,
                },
            },
            "routes": flow_routes,
        },
        "stitchesUi": {
            "schemaVersion": "type4-static-v1",
            "queueBuckets": {
                "EASY": "easy",
                "SAME": "same",
                "HARD": "hard",
            },
            "lockModal": {
                "title": "하이퍼 패스 전용 기능",
                "buttonText": "8번 프리미엄 패스로 이어서 하기",
            },
            "cards": {
                "YellowClinicCard": {
                    "accent": "sun",
                    "retryButtonText": "다시 콕콕 풀어보기",
                },
                "RedClinicCard": {
                    "accent": "tomato",
                    "audioButtonText": "꿀팁 목소리 듣기",
                },
                "GreenWinCard": {
                    "accent": "mint",
                    "nextButtonText": "다음 블록 놀이 가기",
                },
            },
        },
    }


def _pick_next_problem(payload: Dict[str, Any], difficulty: str) -> Optional[Dict[str, Any]]:
    queue_bucket = payload["stitchesUi"]["queueBuckets"][difficulty]
    pool = payload["aiTutorPack"]["problemPool"].get(queue_bucket, [])
    return pool[0] if pool else None


def evaluate_type4_submission(
    *,
    user_tier: int,
    image_attached: bool,
    used_vision_count: int,
    math_logic_score: int,
    calculation_score: int,
    repo_root: Optional[Path] = None,
) -> Dict[str, Any]:
    payload = build_type4_data(repo_root)
    lock_policy = payload["flowController"]["lockPolicy"]
    routes = payload["flowController"]["routes"]

    # LV1 체험 한도 초과 시 LOCK
    lv1 = lock_policy["lv1"]
    if user_tier == 7 and used_vision_count >= lv1["visionAnalysisLimit"]:
        return {
            "status": "LOCKED",
            "msg": LOCK_MESSAGE,
            "typeId": TYPE_ID,
            "image_attached": image_attached,
        }

    if math_logic_score == 100 and calculation_score < 100:
        error_type = "CALCULATION_ERROR"
    elif math_logic_score < 100:
        error_type = "CONCEPT_ERROR"
    else:
        error_type = "NONE"

    route = routes[error_type]
    recommended_difficulty = route["recommendedDifficulty"]
    next_problem = _pick_next_problem(payload, recommended_difficulty)

    return {
        "status": "SUCCESS",
        "typeId": TYPE_ID,
        "image_attached": image_attached,
        "error_type": error_type,
        "recommended_difficulty": recommended_difficulty,
        "feedback_title": route["feedbackTitle"],
        "feedback_text": route["feedbackText"],
        "concept_audio_path": route["conceptAudioPath"],
        "retry_audio_path": route["retryAudioPath"],
        "stitches_card": route["stitchesCard"],
        "show_retry_button": route["showRetryButton"],
        "show_audio_player": route["showAudioPlayer"],
        "next_problem": next_problem,
    }


def write_type4_data_file(
    output_path: Optional[Path] = None,
    repo_root: Optional[Path] = None,
) -> Path:
    repo_root = repo_root or get_repo_root()
    output_path = output_path or (repo_root / "type4_data.json")
    payload = build_type4_data(repo_root)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path
