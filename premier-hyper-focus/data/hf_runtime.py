# premier-hyper-focus/data/hf_runtime.py

import json

class HFRuntime:
    def __init__(self, hf_data_path):
        with open(hf_data_path, 'r', encoding='utf-8') as f:
            self.hf_data = json.load(f)
        self.type_map = {item['typeId']: item for item in self.hf_data}

        self.LOCK_POLICY = {
            "lv1": {
                "aiTutorDailyLimit": 2,
                "visionAnalysisLimit": 2,
                "handwritingScope": "fixedSimilarsOnly",
                "audioScope": "fixedSimilars+parentGuide",
                "aiGeneratedSimilarLimit": 1,
                "pdfScope": "selectedOne",
                "adsEnabled": True
            },
            "lv2": {
                "aiTutorDailyLimit": -1,
                "visionAnalysisLimit": 5,
                "handwritingScope": "all",
                "audioScope": "all",
                "aiGeneratedSimilarLimit": -1,
                "pdfScope": "all",
                "adsEnabled": False
            }
        }
        
        self.BLOCKED_WORDS = ["교차점", "단면화", "단면", "교차"]

    def _validate_text(self, text):
        """모든 피드백 텍스트에 금지어 포함 여부 검증"""
        for word in self.BLOCKED_WORDS:
            if word in text:
                print(f"Warning: Blocked word '{word}' found in text: '{text}'")
        return True

    def _get_user_policy(self, user_level):
        """사용자 레벨에 맞는 정책 반환"""
        return self.LOCK_POLICY.get(user_level, self.LOCK_POLICY["lv1"])

    def build_hf_problem_package(self, type_id, user_level="lv1"):
        """지정된 type_id와 사용자 레벨에 맞는 문제 패키지를 빌드"""
        problem_data = self.type_map.get(type_id)
        if not problem_data:
            return {"error": f"Type ID {type_id} not found."}
            
        policy = self._get_user_policy(user_level)
        
        ui_package = {
            "typeId": problem_data["typeId"],
            "title": problem_data["title"],
            "classification": {
                "legacyGroup": problem_data["legacyGroup"],
                "functionalGroup": problem_data["functionalGroup"]
            },
            "originalProblem": problem_data["originalProblem"],
            "uiSettings": {
                "isAdsEnabled": policy["adsEnabled"],
                "isAudioAvailable": (problem_data.get("aiTutorPack", {}).get("conceptAudioPath") is not None)
            }
        }
        
        ui_package["similarProblems"] = problem_data["fixedSimilars"]
        
        self._validate_text(problem_data["originalProblem"]["answerStory"])
        for similar in problem_data["fixedSimilars"]:
            self._validate_text(similar["answerStory"])
            
        return ui_package

    def build_hf_feedback_package(self, type_id, user_answer, correct_answer, error_type="NONE"):
        """사용자 답변 및 오류 유형에 따른 피드백 패키지 생성"""
        problem_data = self.type_map.get(type_id)
        if not problem_data:
            return {"error": f"Type ID {type_id} not found."}

        feedback_package = {}

        if error_type == "CONCEPT_ERROR":
            feedback_package["nextDifficulty"] = "easy"
            feedback_package["cardType"] = "RedClinicCard"
            feedback_package["message"] = "개념을 다시 한번 천천히 살펴볼까?"
            easy_problems = [p for p in problem_data["fixedSimilars"] if p["difficulty"] == "easy"]
            if easy_problems:
                feedback_package["recommendedProblem"] = easy_problems[0]
                if "handwritingData" in easy_problems[0]:
                    feedback_package["handwritingData"] = easy_problems[0]["handwritingData"]
                    
        elif error_type == "CALCULATION_ERROR":
            feedback_package["nextDifficulty"] = "same"
            feedback_package["cardType"] = "YellowClinicCard"
            feedback_package["message"] = "아깝다! 거의 다 맞았는데, 계산을 다시 확인해볼까?"
            feedback_package["handwritingData"] = {
                "svgPath": "M100,150 Q200,50 300,150 C400,250 200,250 100,150",
                "duration": 1500,
                "color": "#FFD700",
                "emphasisTrigger": "CALCULATION_ERROR"
            }
            
        else:
            feedback_package["nextDifficulty"] = "hard"
            feedback_package["cardType"] = "GreenWinCard"
            feedback_package["message"] = "정답이야! 정말 대단한걸? 더 어려운 문제에 도전해보자!"
            hard_problems = problem_data.get("aiTutorPack", {}).get("problemPool", {}).get("hard", [])
            if hard_problems:
                feedback_package["recommendedProblem"] = hard_problems[0]

        return feedback_package
