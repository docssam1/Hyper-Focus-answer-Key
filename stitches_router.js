// stitches_router.js - 프론트엔드 화면 바인딩 엔진

function handleTutorResponse(response) {
    // 1. 상고모드 락 팝업 제어
    if (response.status === "LOCKED") {
        renderPremiumModal({
            title: "🔒 하이퍼 패스 전용 기능",
            content: response.msg,
            buttonText: "8번 프리미엄 패스 결제하기"
        });
        return;
    }

    // 2. 계산 실수(CALCULATION_ERROR) 스티치 컴포넌트 렌더링
    if (response.error_type === "CALCULATION_ERROR") {
        // 노란색 피드백 카드 가동 + 7세용 격려 오디오 재생
        Stitches.renderComponent("YellowClinicCard", {
            title: "아까운 계산 실수!",
            feedback: response.feedback_text,
            showRetryButton: true
        });
        
        // 난이도 유지(SAME)로 다음 문제 대기열 세팅
        QueueManager.setNextProblem(response.recommended_difficulty);
    } 
    // 3. 개념 오류(CONCEPT_ERROR) 스티치 컴포넌트 렌더링
    else if (response.error_type === "CONCEPT_ERROR") {
        // 빨간색 챌린지 카드 가동 + 독쌤 개념 TTS 자동 재생
        Stitches.renderComponent("RedClinicCard", {
            title: "개념 콕콕 클리닉",
            feedback: response.feedback_text,
            showAudioPlayer: true
        });
        
        // 난이도 하향(EASY) 자동 매칭
        QueueManager.setNextProblem(response.recommended_difficulty);
    }
}

console.log("⚡ [Stitches UI] 프론트엔드 라우터 세팅 완료.");
