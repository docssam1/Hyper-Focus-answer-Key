import json

def analyze_user_solution(user_tier, image_attached, used_vision_count, math_logic_score, calculation_score):
    """
    7세 영재용 하이퍼포커스 실시간 채점 분기 엔진
    - 주력 연산: 초2~3 덧뺄셈 및 곱셈구구
    """
    # 🔒 1. 7번 유저 1회 제한 게이트키퍼
    if user_tier == 7 and used_vision_count >= 1:
        return {
            "status": "LOCKED",
            "msg": "🔒 프리미엄 비전 분석 체험 1회가 소진되었습니다. 8번 패스로 전환하세요!"
        }

    # 👁️ 2. 비전 분석 및 에러 타입 판정 (상고모드)
    if math_logic_score == 100 and calculation_score < 100:
        # 계산 실수 판정 -> 난이도 유지(SAME) + 칭찬 샌드위치 멘트
        error_type = "CALCULATION_ERROR"
        recommended_difficulty = "SAME"
        feedback = (
            "와! 우리 친구, 쌓기나무 구멍이 지나가는 길을 머릿속으로 싹둑 쪼개서 식을 세우다니 정말 천재적이야! "
            "하지만 아까운 산수 실수야! 연필 들고 다시 한 번만 콕콕 세어볼까? 식은 100점짜리로 완벽하니까 "
            "마지막 뺄셈만 천천히 다시 하면 이번엔 무조건 정답 레이저가 뿜어져 나올 거야!"
        )
    elif math_logic_score < 100:
        # 개념 오류 판정 -> 난이도 하향(EASY) + 독쌤 직강 오디오 연계
        error_type = "CONCEPT_ERROR"
        recommended_difficulty = "EASY"
        feedback = (
            "괜찮아, 우리 친구! 가로 세로 구멍을 뚫을 때 가운데서 쿵! 만나는 대장 블록을 겹쳐서 뺐구나? "
            "독쌤이 준비한 꿀팁 음성을 들으면서 케이크 쪼개기 비법으로 다시 도전해볼까?"
        )
    else:
        error_type = "NONE"
        recommended_difficulty = "HARD"
        feedback = "정답이야! 완벽해! 다음 챌린지 문제로 가보자!"

    return {
        "status": "SUCCESS",
        "error_type": error_type,
        "recommended_difficulty": recommended_difficulty,
        "feedback_text": feedback
    }

# 4번 유형 가상 테스트 구동 (7번 유저 최초 1회, 계산 실수 상황 시뮬레이션)
result = analyze_user_solution(user_tier=7, image_attached=True, used_vision_count=0, math_logic_score=100, calculation_score=80)
print(json.dumps(result, ensure_ascii=False, indent=2))
