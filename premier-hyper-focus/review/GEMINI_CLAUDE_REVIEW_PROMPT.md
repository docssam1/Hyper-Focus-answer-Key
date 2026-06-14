# G-FIELD Premier Hyper Focus — Gemini/Claude 검수 작업 지시서

## 목적
이미 GitHub에 업로드된 54유형 유사문항 데이터와 별도 튜터 스크립트를 이용하여 다음 작업을 수행한다.

1. 54유형 유사문항 전체 검수
2. 각 문항 정답 확정
3. 초등 사고력 방식 해설 작성
4. 기존 튜터 스크립트 업그레이드
5. 최종 JS 데이터 파일로 정리

---

## 현재 GitHub에 올라간 유사문항 데이터

- Part A: typeIds 1~17
- Part B: typeIds 18~34
- Part C: typeIds 35~54

각 데이터는 다음 구조를 기준으로 한다.

```js
window.GFIELD_SQ_A = [ ... ];
window.GFIELD_SQ_B = [ ... ];
window.GFIELD_SQ_C = [ ... ];
```

각 typeId에는 보통 다음 필드가 들어 있다.

```js
{
  typeId,
  typeTitle,
  questions: [
    {
      id,
      difficulty,
      question,
      answer,
      solution,
      hint1,
      hint2,
      tutorTypeId,
      imagePrompt
    }
  ]
}
```

---

## 별도 제공 스크립트

DOCSSAM이 제공한 튜터 스크립트는 다음 구조다.

```js
window.GFIELD_TUTOR_SCRIPTS = [
  {
    typeId,
    typeTitle,
    scriptSummary,
    tutorIntro,
    hint1,
    hint2,
    commonMistake,
    docssamExplanation
  }
]
```

이 스크립트는 54유형 설명/힌트/오답 포인트/독쌤 설명의 기준이다. 유사문항 검수 시 반드시 이 스크립트의 의도와 풀이 흐름을 우선한다.

---

## 검수 기준

각 문항마다 다음 항목을 확인한다.

### 1. 원본 유형 일치
- typeTitle과 question의 유형이 맞는가?
- 원래 유형의 풀이 방식과 동일한가?
- 조건 수, 보기 수, 구조가 너무 달라지지 않았는가?

### 2. 답 검산
- answer가 실제 정답과 일치하는가?
- solution 계산 과정에 오류가 없는가?
- 단위, 각도, 개수, 날짜, 시각, 방향이 맞는가?

### 3. 초등 풀이 적합성
- x, y, 연립방정식, 함수식 중심 풀이를 피한다.
- 가능하면 표, 경우 나누기, 거꾸로 생각하기, 합차, 배수, 그림 해석으로 설명한다.
- 초등 상위권 학생이 따라갈 수 있는 단계로 쓴다.

### 4. 난이도 유지
- 기존 기출 유형보다 지나치게 쉬워지면 안 된다.
- 숫자만 바꿔도 구조가 무너지면 수정한다.
- 답이 너무 뻔한 문항은 조건을 보강한다.

### 5. 문장 품질
- 오타 수정
- 말이 어색한 부분 수정
- 조건 누락 수정
- 질문이 모호하면 명확히 수정

---

## 최종 출력 형식

검수 후 최종 데이터는 아래 형식으로 통합한다.

```js
window.GFIELD_VERIFIED_SQ = [
  {
    typeId: 1,
    typeTitle: "...",
    tutorScript: {
      scriptSummary: "...",
      tutorIntro: "...",
      commonMistake: "...",
      docssamExplanation: "..."
    },
    questions: [
      {
        id: "1-A",
        question: "...",
        answer: "...",
        explanation: "...",
        hint1: "...",
        hint2: "...",
        checkStatus: "verified",
        issueNote: ""
      },
      {
        id: "1-B",
        question: "...",
        answer: "...",
        explanation: "...",
        hint1: "...",
        hint2: "...",
        checkStatus: "verified",
        issueNote: ""
      }
    ]
  }
];
```

문제에 오류가 있으면 `checkStatus`를 `needs_fix`로 두고, `issueNote`에 이유를 적는다.

---

## 작업 순서

1. GFIELD_SQ_A, GFIELD_SQ_B, GFIELD_SQ_C를 합친다.
2. typeId 1~54가 모두 있는지 확인한다.
3. 각 typeId에 2문항씩 있는지 확인한다.
4. GFIELD_TUTOR_SCRIPTS의 같은 typeId와 연결한다.
5. 문항별 정답과 해설을 검산한다.
6. 오류가 있으면 문항 또는 답/해설을 수정한다.
7. 최종 `window.GFIELD_VERIFIED_SQ`를 만든다.
8. 별도로 오류 리포트를 만든다.

---

## 오류 리포트 형식

```md
# 검수 리포트

## 전체 요약
- 총 유형 수:
- 총 문항 수:
- 정상 문항 수:
- 수정 문항 수:
- 재검토 필요 문항 수:

## 수정 목록
| typeId | 문항 ID | 문제점 | 수정 내용 | 상태 |
|---:|---|---|---|---|
```

---

## 주의

- `premier-hyper-focus/index.html`의 로그인/소개 화면 구조는 건드리지 않는다.
- `premier-hyper-focus/book/` 폴더는 건드리지 않는다.
- 기존 유사문항 데이터 원본은 백업으로 남긴다.
- 최종본은 새 파일로 만든다.

권장 저장 위치:

```text
premier-hyper-focus/data/gfield-verified-similar-questions.js
premier-hyper-focus/data/gfield-verified-similar-questions-review.md
```
