import os
import sys
import json
from pathlib import Path

TYPE_MASTER = {4: {"group": "A", "title": "구멍 뚫린 쌓기나무 추론"}}
STATIC_PROBLEM_POOLS = {
    4: {
        "easy": [{"id": "p4_e1", "text": "2x2x2 크기에서 한 줄만 관통했을 때 남은 쌓기나무의 개수는?"}],
        "same": [{"id": "p4_s1", "text": "3x3x3 크기에서 대각선 방향으로 관통했을 때 남은 쌓기나무의 개수는?"}],
        "hard": [{"id": "p4_h1", "text": "4x4x4 크기에서 3개의 축이 동시에 관통했을 때 남은 쌓기나무의 개수는?"}]
    }
}

def main():
    if len(sys.argv) < 2:
        print("❌ 에러: typeId가 누락되었습니다.")
        sys.exit(1)
    type_id = int(sys.argv[1])
    script_path = Path("youtube_script/cleaned_audio_script.md")
    audio_script_content = script_path.read_text(encoding="utf-8") if script_path.exists() else "기본 대본"
    metadata = TYPE_MASTER[type_id]
    render_data = {"gridSize": [3, 3, 3], "blocks": [[0,0,0,1], [1,0,0,1], [2,0,0,1]]}

    final_output = {
        "typeId": type_id, "group": metadata["group"], "title": metadata["title"],
        "originalProblem": {"questionId": f"q{type_id}_origin", "text": "7세 영재용 문장제", "renderData": render_data},
        "fixedSimilars": [{"questionId": f"q{type_id}_f1", "text": "유사 1번", "renderData": render_data, "audioPath": "url"}],
        "aiTutorPack": {"conceptAudioPath": "url", "audioScriptText": audio_script_content, "problemPool": STATIC_PROBLEM_POOLS[type_id]}
    }

    with open(f"type{type_id}_data.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, ensure_ascii=False, indent=2)
    print(f"✅ [빌드 완료] type{type_id}_data.json 생성됨.")

if __name__ == "__main__":
    main()
