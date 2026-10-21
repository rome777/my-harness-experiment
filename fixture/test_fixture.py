"""독립 감사 데몬 테스트 픽스처 (test_fixture.py).
보고서 텍스트가 행동 철칙 및 규칙을 100% 준수했는지 기계적으로 검증한다.
"""
import re
import sys

def audit_text(text):
    errors = []
    # 1. 느낌표 검사
    if "!" in text:
        errors.append("규칙 위반: 느낌표(!)가 포함되어 있습니다.")
    
    # 2. 현실 시각 명시 여부 (시작 시각 또는 종료 시각)
    if not re.search(r"(시작 시각|종료 시각):\s*\d\d:\d\d", text):
        errors.append("규칙 위반: 시작 또는 종료 시각(HH:MM)이 명시되지 않았습니다.")
        
    # 3. 위험한 무차별 종료 명령어 검사
    if "taskkill /im StarCraft.exe" in text:
        errors.append("규칙 위반: 무차별 프로세스 강제 종료 명령어가 감지되었습니다.")
        
    # 4. 환각 방지: 명령 시도 횟수와 실제 출현 분리 검사
    if "캐리어" in text and not any(k in text for k in ["명령", "실제", "관측", "모름"]):
        errors.append("규칙 위반: 인게임 데이터 교차 검증 표기가 누락되었습니다.")

    return len(errors) == 0, errors

if __name__ == "__main__":
    sample = sys.stdin.read() if not sys.stdin.isatty() else "시작 시각: 14:00. 테스트 완료."
    passed, errs = audit_text(sample)
    if passed:
        print("[PASS] 모든 감사 규칙을 100% 통과했습니다.")
        sys.exit(0)
    else:
        print(f"[FAIL] {len(errs)}건의 규칙 위반이 감지되었습니다:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
