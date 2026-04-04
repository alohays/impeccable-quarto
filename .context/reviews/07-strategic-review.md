# Strategic Review: Implementation Quality & Missing Capabilities

**Date:** 2026-04-03
**Scope:** Issues NOT covered in reviews 01-06, or marked "implemented" but still broken
**Method:** Multi-agent analysis (code review, impeccable-original deep analysis, external research) + manual verification
**Philosophy:** Fewer, higher-impact findings only. Every item here is actionable as a PR.

---

## Executive Summary

기존 6개 리뷰의 권장사항은 5개 Phase에 걸쳐 잘 반영되었습니다. 하지만 **구현 품질에 심각한 결함**이 있어서, 프로젝트의 핵심 가치 제안 — "객관적 품질 스코어링" — 이 실제로는 작동하지 않습니다.

**가장 중요한 발견:** `quality_score.py`의 파서 버그로 인해 **프로젝트 자체 예제 5개 모두가 자체 품질 게이트를 통과하지 못합니다** (demo.qmd: 57/100). 이는 프로젝트의 신뢰성을 근본적으로 훼손합니다.

---

## Part 1: Critical — 프로젝트 가치 훼손 이슈

### ISSUE-01: quality_score.py의 Ghost Slide 버그

**심각도:** Critical
**파일:** `scripts/quality_score.py:88-179` (`parse_slides()`)
**검증:** `python3 scripts/quality_score.py examples/demo.qmd --no-render --verbose` → 57/100

**문제:** `---` 수평선 구분자가 `## Heading` 바로 앞에 올 때, 파서가 untitled phantom slide를 하나 더 생성합니다.

```
실제 슬라이드: 14개
파서가 보는 슬라이드: 27개 (13개가 유령)
```

**영향 범위:**
- 슬라이드 카운트 ~2배 과대 집계
- 유령 슬라이드에 speaker notes가 없으므로 speaker-notes 감점 폭증 (-8)
- word count 검사도 유령 슬라이드를 검사하므로 무의미한 감점 누적
- **5개 예제 파일 전부 Failing (52-67점)** — 프로젝트의 시연 자체가 불가능

**수정 방향:**
`---` 뒤에 즉시 `## Heading`이 오면 하나의 슬라이드 전환으로 처리. Quarto RevealJS에서 `---`와 `##`는 동일한 의미(새 슬라이드).

```python
# parse_slides()에서 --- 처리 시:
# 다음 non-empty line이 ## heading이면 --- 자체는 슬라이드를 생성하지 않음
```

**ROI:** 이 한 가지 수정으로 모든 예제 점수가 80+ (PASS)로 올라감.

---

### ISSUE-02: quality_score.py의 Word Count가 테이블/Div 마크업 포함

**심각도:** Critical
**파일:** `scripts/quality_score.py:491-528` (`check_word_count()`)

**문제:** 테이블 데이터(pipe-delimited `|` 행)와 Quarto div 속성(`{.class}`)이 body word로 카운트됩니다.

academic-paper.qmd의 "Main Results" 슬라이드: 실제 산문 ~20단어, 파서 계산 118단어 → 거짓 감점.

**수정 방향:**
```python
# 테이블 행 (| 로 시작) 스킵
if re.match(r"^\|", s):
    continue
# Quarto div 속성 스킵
if re.match(r"^:::", s):
    continue
```

---

### ISSUE-03: quality_score.py의 Pure B/W 감지가 인라인 코드 내용 매칭

**심각도:** High
**파일:** `scripts/quality_score.py:481-488` (`check_pure_bw()`)

**문제:** 백틱 안의 `#000000`을 위반으로 감지. demo.qmd의 "Tinted Neutrals" 슬라이드는 의도적으로 `#000000`을 나쁜 예시로 보여주는데, 이것이 -3 감점됨.

**수정 방향:** 코드 블록뿐 아니라 인라인 코드(`` `...` ``)도 스트리핑 후 검사.

---

## Part 2: High — 기능이 존재하지만 작동하지 않는 이슈

### ISSUE-04: Dark Mode는 Dead Code

**심각도:** High
**파일:** `themes/impeccable.scss:746-858`

**문제:** `.reveal.dark-mode` / `[data-theme="dark"]` 스타일이 918줄 중 112줄을 차지하지만, 이를 활성화하는 메커니즘이 **전혀 없습니다**:
- JS 토글 없음
- YAML 옵션 없음
- 문서화 없음
- 예제 없음

추가로, dark mode 내에서도 `background: white !important`(print), `oklch(0 0 0 / 0.3)`(pre shadow) 등 tinted neutral 원칙 위반이 있습니다.

**수정 방향:**
옵션 A: Dark mode 코드를 완전히 제거 (dead code 정리)
옵션 B: 활성화 메커니즘 구현 — YAML `dark-mode: true` → JS가 `.dark-mode` class 추가

**권장:** 옵션 B가 프로젝트 가치에 부합. Quarto의 `theme: [dark, custom.scss]` 또는 커스텀 JS 위젯.

---

### ISSUE-05: pre-commit Hook이 Git Hook으로 설치 시 Silent Fail

**심각도:** High
**파일:** `scripts/pre-commit-quality.sh:23`

**문제:** `$0`의 dirname으로 `quality_score.py` 경로를 계산하는데, symlink로 `.git/hooks/pre-commit`에 설치되면 경로가 `.git/hooks/quality_score.py`가 됩니다. fallback이 `exit 0`이므로 **품질 검사를 완전히 건너뜀**.

hooks/ 도입이 Phase 2에서 구현되었지만, 실제로 작동하지 않는 상태.

**수정 방향:**
```bash
# SCRIPT_DIR 대신 PROJECT_DIR 기반으로 경로 결정
QUALITY_SCRIPT="$(git rev-parse --show-toplevel)/scripts/quality_score.py"
```

---

### ISSUE-06: CI Score Extraction이 ANSI 코드 때문에 실패 가능

**심각도:** High
**파일:** `.github/workflows/quality.yml:73-74`

**문제:** `quality_score.py`의 stdout에 ANSI 색상 코드가 포함됨. `grep -oP`의 `Score:\s+\K\d+` 패턴이 `\033[91m\033[1m57\033[0m/100` 같은 문자열에서 숫자를 추출하지 못할 수 있음. Grade 추출도 `[A-F]` 한 글자만 매칭하므로 "A+" 등을 놓침.

**수정 방향:**
- `quality_score.py`에 `--no-color` 또는 `NO_COLOR` 환경변수 지원 추가
- 또는 CI에서 파이프 시 자동으로 ANSI 비활성화 (isatty 체크)

---

### ISSUE-07: Theme Variant 4개 모두 `.infobox` 스타일 누락

**심각도:** High
**파일:** `themes/impeccable-academic.scss`, `impeccable-corporate.scss`, `impeccable-creative.scss`, `impeccable-lightning.scss`

**문제:** 마스터 테마에는 `.infobox`가 정의되어 있지만, 4개 variant 테마에는 모두 `.infobox`가 빠져 있음. CLAUDE.md와 모든 문서가 `.infobox`를 6개 시맨틱 박스 중 하나로 안내.

variant 테마를 사용하는 유저가 `.infobox`를 쓰면 스타일이 적용되지 않음.

**수정 방향:** 각 variant에 `.infobox` 스타일 추가. DRY를 위해 공통 semantic box mixin을 별도 partial로 추출하는 것이 이상적.

---

## Part 3: Medium — 설계 완성도 이슈

### ISSUE-08: new-deck.sh의 `eval` 인젝션 취약점

**심각도:** Medium (로컬 도구이나 보안 원칙 위반)
**파일:** `scripts/new-deck.sh:29`

```bash
eval "$var_name='$value'"
```

사용자 입력에 single quote가 포함되면 arbitrary shell 실행 가능.

**수정:** `eval` 대신 `declare` 또는 `printf -v` 사용:
```bash
printf -v "$var_name" '%s' "$value"
```

---

### ISSUE-09: Nested Semantic Box Detection이 비-시맨틱 Div에 혼동

**심각도:** Medium
**파일:** `scripts/quality_score.py:406-417`

**문제:** `:::` 닫기 태그가 시맨틱 박스의 닫기인지 레이아웃 div(`.two-col`, `.three-col`)의 닫기인지 구분하지 못함. depth counter가 비-시맨틱 div에 의해 잘못 감소될 수 있음.

**수정 방향:** 시맨틱 박스 열기 스택을 유지하고, `:::`가 스택의 마지막 항목을 닫을 때만 depth 감소.

---

### ISSUE-10: Templates가 자체 품질 기준을 위반

**심각도:** Medium
**파일:** `templates/academic.qmd`, `templates/corporate.qmd`

**문제:** 템플릿들이 여러 슬라이드에서 speaker notes가 없음. 템플릿은 "올바른 패턴"을 가르치는 역할인데, 자체 기준(MAJ-01: -5/slide)을 위반. `impeccable-academic.scss`의 `$base-size: 26px`도 문서화된 "28px minimum" 위반.

**수정 방향:** 모든 템플릿의 모든 content slide에 placeholder notes 추가. academic theme base-size를 28px로 변경.

---

### ISSUE-11: `_quarto.yml`이 사용하지 않는 8개 Google Fonts를 로드

**심각도:** Medium
**파일:** `_quarto.yml:47`

**문제:** 프로젝트 전역 config가 8개 폰트 패밀리를 로드하지만, 대부분의 테마는 3개만 사용. 불필요한 네트워크 요청.

**수정 방향:** `_quarto.yml`에서는 마스터 테마용 3개만 로드. variant 테마용 폰트는 각 예제 파일에서 개별 로드.

---

## Part 4: Strategic — 프로젝트 레벨 개선

### ISSUE-12: Skills에 Mandatory Context Loading Cascade 부재

**심각도:** Strategic
**참조:** impeccable-original의 "Mandatory Preparation" 패턴

**문제:** impeccable-original은 모든 디자인 스킬이 `/frontend-design`을 mandatory 첫 단계로 호출하고, `.impeccable.md`가 없으면 `/teach-impeccable` 실행을 강제합니다.

impeccable-quarto의 `/slide-design` hub는 존재하지만:
- 다른 스킬들이 이를 **실제로 호출**하는 메커니즘이 없음 (문서에 "should reference" 수준)
- `.impeccable-quarto.md` 없이도 스킬이 정상 실행됨 → 일관되지 않은 디자인 컨텍스트

**수정 방향:** 각 디자인 스킬 프롬프트의 첫 줄에 explicit mandatory step 추가:
```markdown
## MANDATORY PREPARATION
Before proceeding, invoke /slide-design to load design context.
If .impeccable-quarto.md does not exist, inform the user and suggest /teach-style.
Do NOT proceed without active design context.
```

---

### ISSUE-13: Reference Documents as LLM Conditioning — 부재

**심각도:** Strategic
**참조:** `.context/references/impeccable-original-deep-patterns.md`

**문제:** impeccable-original의 가장 강력한 패턴은 skills 내에 `reference/` 서브디렉토리를 두어 domain-specific knowledge를 LLM 컨텍스트에 주입하는 것입니다.

예: `/typeset` 실행 시 typography reference가 로드되어 "Plus Jakarta Sans 대신 Inter를 추천"하는 일반적 실수를 방지.

impeccable-quarto는 `.claude/references/`에 디자인 참조 문서가 있지만, **스킬이 이를 명시적으로 읽도록 지시하지 않음**.

**수정 방향:** 핵심 스킬(typeset, colorize, arrange, critique)에 `Read .claude/references/<relevant-doc>` 스텝 추가. 모든 참조를 읽을 필요 없이, 각 스킬의 도메인에 맞는 1-2개만.

---

## Priority Matrix

| Issue | Impact | Effort | Priority |
|-------|--------|--------|----------|
| ISSUE-01: Ghost slide bug | 🔴 프로젝트 무력화 | S (1 함수 수정) | **P0 — 즉시** |
| ISSUE-02: Word count 테이블 포함 | 🔴 점수 왜곡 | S (필터 추가) | **P0 — 즉시** |
| ISSUE-03: Pure B/W 인라인 코드 | 🟠 거짓 감점 | S (스트리핑 추가) | **P1 — 이번 주** |
| ISSUE-04: Dark mode dead code | 🟠 미완성 기능 | M (JS + 문서) | **P1 — 이번 주** |
| ISSUE-05: pre-commit silent fail | 🟠 안전망 미작동 | S (경로 수정) | **P1 — 이번 주** |
| ISSUE-06: CI ANSI 코드 문제 | 🟠 CI 불안정 | S (no-color 추가) | **P1 — 이번 주** |
| ISSUE-07: Variant .infobox 누락 | 🟠 기능 불완전 | S (4 파일 수정) | **P1 — 이번 주** |
| ISSUE-08: new-deck.sh eval | 🟡 보안 원칙 | S (1줄 변경) | P2 |
| ISSUE-09: Nested box detection | 🟡 감지 부정확 | M (로직 재설계) | P2 |
| ISSUE-10: Template 기준 위반 | 🟡 나쁜 예시 | S (notes 추가) | P2 |
| ISSUE-11: 과도한 폰트 로드 | 🟡 성능 | S (config 정리) | P3 |
| ISSUE-12: Mandatory context cascade | 🟡 일관성 | M (스킬 수정) | P2 |
| ISSUE-13: Reference conditioning | 🟡 품질 향상 | M (스킬 수정) | P3 |

---

## Recommended Execution Order

### Phase A: 품질 시스템 정상화 (ISSUE-01, 02, 03)
`quality_score.py` 수정 → 모든 예제 80+ 통과 확인.
**이것이 없으면 나머지 모든 개선의 의미가 없습니다.**

### Phase B: 인프라 신뢰성 (ISSUE-05, 06, 08)
pre-commit hook, CI, new-deck.sh 수정. 자동화 안전망 실제 작동 보장.

### Phase C: 기능 완성 (ISSUE-04, 07, 10, 11)
Dark mode 활성화, variant theme 보완, template/config 정리.

### Phase D: 설계 성숙도 (ISSUE-09, 12, 13)
스코어러 로직 고도화, 스킬 아키텍처 개선.

---

## Part 5: Strategic — External Research 기반 발견

### ISSUE-14: Agent Frontmatter에서 `context: fork` 오용

**심각도:** High (정확성)
**파일:** `.claude/agents/slide-critic.md`, `layout-auditor.md`, `typography-reviewer.md`, `verifier.md`, `slide-fixer.md`
**참조:** `.context/references/agent-harness-2026.md`

**문제:** Claude Code 공식 문서에서 `context: fork`는 **skill** frontmatter 필드이지, agent frontmatter 필드가 아닙니다. Agent는 `isolation: worktree`를 사용합니다.

현재 agent 정의에서 "Context: fork"라고 기술되어 있으나, 이는 실제 Claude Code 런타임에서 무시될 가능성이 높습니다. 즉 **적대적 격리가 실제로는 적용되지 않고 있을 수 있습니다**.

**수정 방향:**
- Agent에서 `context: fork` 제거
- 대신 review/critique 관련 **skill**에 `context: fork` 추가
- 또는 agent에 `isolation: worktree` 사용

---

### ISSUE-15: Agent `model` 필드 미지정 — 비용 최적화 기회

**심각도:** Medium (비용)
**참조:** `.context/references/agent-harness-2026.md`

**문제:** 모든 agent가 동일 모델을 사용합니다. read-only 진단 에이전트(critic, typography-reviewer, layout-auditor)는 `haiku`나 `sonnet`으로도 충분하고, fixer만 `opus`가 필요합니다.

**수정 방향:**
```yaml
# slide-critic.md
model: sonnet

# slide-fixer.md
model: inherit  # (uses calling session's model)
```

이는 리뷰 파이프라인의 토큰 비용을 50-70% 절감할 수 있습니다.

---

### ISSUE-16: Quarto 1.8 `_brand.yml` 미활용

**심각도:** Strategic
**참조:** `.context/references/quarto-ecosystem-2026.md`

**문제:** Quarto 1.8 (현재 최신)의 `_brand.yml`은 모든 Quarto 포맷(HTML, RevealJS, 대시보드, 문서)에 일관된 브랜딩을 적용하는 공식 메커니즘입니다. impeccable-quarto의 디자인 시스템이 여기에 표현되면:
- SCSS 테마뿐 아니라 HTML 문서에도 일관된 스타일 적용
- `brand-mode: dark`로 dark mode 문제(ISSUE-04) 네이티브 해결
- Brand extension으로 팀 간 공유 가능

impeccable-quarto가 현재 SCSS만 제공하는 것은 Quarto 생태계 활용의 절반만 쓰는 것입니다.

**수정 방향:** impeccable 디자인 시스템의 `_brand.yml` 버전 생성. 테마 variant마다 brand variant 제공.

---

## Updated Priority Matrix (전체)

| Issue | Impact | Effort | Priority |
|-------|--------|--------|----------|
| ISSUE-01: Ghost slide bug | 🔴 프로젝트 무력화 | S | **P0** |
| ISSUE-02: Word count 테이블 포함 | 🔴 점수 왜곡 | S | **P0** |
| ISSUE-03: Pure B/W 인라인 코드 | 🟠 거짓 감점 | S | **P1** |
| ISSUE-14: context:fork 오용 | 🟠 격리 미작동 | S | **P1** |
| ISSUE-04: Dark mode dead code | 🟠 미완성 | M | **P1** |
| ISSUE-05: pre-commit silent fail | 🟠 안전망 | S | **P1** |
| ISSUE-06: CI ANSI 문제 | 🟠 CI 불안정 | S | **P1** |
| ISSUE-07: Variant .infobox 누락 | 🟠 불완전 | S | **P1** |
| ISSUE-08: new-deck.sh eval | 🟡 보안 | S | P2 |
| ISSUE-09: Nested box detection | 🟡 부정확 | M | P2 |
| ISSUE-10: Template 기준 위반 | 🟡 나쁜 예시 | S | P2 |
| ISSUE-12: Mandatory context cascade | 🟡 일관성 | M | P2 |
| ISSUE-15: Agent model 미지정 | 🟡 비용 | S | P2 |
| ISSUE-11: 과도한 폰트 로드 | 🟡 성능 | S | P3 |
| ISSUE-13: Reference conditioning | 🟡 품질 | M | P3 |
| ISSUE-16: _brand.yml 미활용 | 🔵 전략적 | L | P3 |

---

*Generated by multi-agent analysis (4 agents: code-reviewer + impeccable-original-analyst + harness-researcher + quarto-ecosystem-researcher + manual verification) on 2026-04-03*
