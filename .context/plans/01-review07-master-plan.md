# Review-07 Resolution Master Plan

**Date:** 2026-04-03
**Source:** `.context/reviews/07-strategic-review.md` (16 issues)
**Status:** 🟡 PLANNED
**Execution:** Issue-level commits, Phase-level PRs
**Numbering:** Continues from completed Phase 1-5 (00-master-plan.md)

---

## Overview

| Phase | Name | Issues | Commits | PR Title | Deps |
|-------|------|--------|---------|----------|------|
| 6 | Quality Scorer Fix | 01, 02, 03 | 3 | `fix: quality_score.py parser bugs (ghost slides, word count, pure bw)` | None |
| 7 | Infrastructure Reliability | 05, 06, 08, 14 | 4 | `fix: pre-commit, CI, eval injection, agent frontmatter` | Phase 6 |
| 8 | Theme & Brand System | 04, 07, 10, 11, 16 | 5 | `feat: _brand.yml integration, dark mode, variant completeness` | None |
| 9 | Scoring Accuracy | 09, 15 | 2 | `fix: nested box detection, agent model routing` | Phase 6 |
| 10 | Skill Architecture | 12, 13 | 2 | `feat: mandatory context cascade, reference conditioning` | None |

### Dependency Graph

```
Phase 6 (Scorer Fix) ──→ Phase 7 (Infrastructure) ──→ ✅
                    └──→ Phase 9 (Scoring Accuracy)

Phase 8 (Theme & Brand) ── independent ──→ ✅

Phase 10 (Skill Architecture) ── independent ──→ ✅
```

**Phase 6은 반드시 첫 번째.** Phase 8, 10은 독립적이므로 병렬 가능.

---

## Phase 6: Quality Scorer Fix

**Goal:** `quality_score.py`를 정상화하여 모든 예제가 80+ 점수를 받도록 수정.
**Verification:** `python3 scripts/quality_score.py examples/*.qmd --no-render` 전부 PASS.

### Commit 6.1: ISSUE-01 — Ghost Slide 파서 수정

**파일:** `scripts/quality_score.py`
**함수:** `parse_slides()` (lines 88-179)

**현재 동작:**
```
## Slide A → slide 1
---         → slide 2 (phantom!)
## Slide B → slide 3
```

**수정 후 동작:**
```
## Slide A → slide 1
---         → (slide transition marker, not a new slide)
## Slide B → slide 2
```

**구체적 변경:**

```python
# parse_slides() 내 --- 처리 로직 변경
# 현재: --- 만나면 즉시 새 슬라이드 생성
# 수정: --- 만나면 현재 슬라이드를 저장하되, 다음 ## heading이 오면
#        --- 자체는 슬라이드를 생성하지 않음

# 접근법: --- 를 만나면 pending_separator = True 설정.
# 다음 줄이 ## heading이면 pending slide를 생성하지 않고 heading으로 새 슬라이드 시작.
# 다음 줄이 content이면 pending slide를 생성 (실제 untitled 슬라이드).
```

**대안 (더 단순):** `---` 뒤 빈 줄을 스킵하고, 다음 non-empty line이 `## `로 시작하면 `---`가 만든 슬라이드를 폐기. lookahead 방식.

**테스트 기준:**
- `examples/demo.qmd`: 27 → ~14 slides
- `examples/academic-paper.qmd`: ghost slides 0
- 모든 5개 예제: score ≥ 80

---

### Commit 6.2: ISSUE-02 — Word Count에서 테이블/Div 마크업 제외

**파일:** `scripts/quality_score.py`
**함수:** `check_word_count()` (lines 491-528), `count_body_words()` (lines 337-357)

**추가할 필터:**
```python
# 테이블 행 스킵
if re.match(r"^\s*\|", s):
    continue
# Quarto div 속성/펜스 스킵
if re.match(r"^:::", s):
    continue
# 이미지 마크업 스킵
if re.match(r"^!\[", s):
    continue
# Quarto 속성 블록 스킵 ({.class} 단독 줄)
if re.match(r"^\{[.#]", s):
    continue
```

`count_body_words()`에도 동일한 필터 적용 (LLM bias 체크에서 사용).

**테스트 기준:**
- academic-paper.qmd "Main Results" 슬라이드: word count 118 → ~20
- 테이블이 있는 슬라이드에서 false-positive word-count 감점 0

---

### Commit 6.3: ISSUE-03 — Pure B/W Detection에서 인라인 코드 제외

**파일:** `scripts/quality_score.py`
**함수:** `check_pure_bw()` (lines 481-488)

**현재:**
```python
stripped = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
stripped = re.sub(r"^---\n.*?\n---", "", stripped, flags=re.DOTALL)
```

**추가:**
```python
# 인라인 코드도 스트리핑
stripped = re.sub(r"`[^`]+`", "", stripped)
```

**테스트 기준:**
- `demo.qmd`의 "Tinted Neutrals" 슬라이드: `#000000` in backticks → 감점 없음
- 실제 인라인 스타일의 `#000000` → 여전히 감점

---

### Phase 6 검증

```bash
# 전체 예제 스코어링 (렌더 없이 빠르게)
for f in examples/*.qmd; do
  python3 scripts/quality_score.py "$f" --no-render
done
# 기대: 5개 모두 exit code 0 (score ≥ 80)
```

---

## Phase 7: Infrastructure Reliability

**Goal:** 자동화 안전망(pre-commit, CI)이 실제로 작동하도록 수정.
**Depends on:** Phase 6 (scorer가 정상이어야 CI도 의미 있음)

### Commit 7.1: ISSUE-05 — pre-commit Hook 경로 수정

**파일:** `scripts/pre-commit-quality.sh`

**현재 (line 23):**
```bash
QUALITY_SCRIPT="$SCRIPT_DIR/quality_score.py"
```

**수정:**
```bash
# git rev-parse로 프로젝트 루트 기준 경로 결정
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "$SCRIPT_DIR/..")"
QUALITY_SCRIPT="$PROJECT_ROOT/scripts/quality_score.py"
```

**테스트:**
```bash
# symlink 시뮬레이션
ln -sf ../../scripts/pre-commit-quality.sh /tmp/test-hook
/tmp/test-hook  # quality_score.py 찾아야 함
```

---

### Commit 7.2: ISSUE-06 — CI Score Extraction ANSI 문제 수정

**파일:** `scripts/quality_score.py`, `.github/workflows/quality.yml`

**quality_score.py 변경:**
```python
# main()에서 isatty 체크 또는 NO_COLOR 환경변수 지원
import os

# ANSI codes 정의 부분에서:
if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
    RED = YELLOW = GREEN = CYAN = BOLD = DIM = RESET = ""
```

**quality.yml 변경 (lines 73-74):**
```yaml
# ANSI 문제 해결 후 더 안정적인 grep:
score=$(echo "$output" | grep -oP 'Score:\s+\K\d+' | head -1)
grade=$(echo "$output" | grep -oE '\([A-Z][+-]? [A-Za-z]+\)' | head -1 | tr -d '()')
```

또는 `quality_score.py`에 `--json` 출력 옵션을 추가하여 CI에서 파싱하기 쉽게.

**테스트:**
- CI에서 `NO_COLOR=1 python3 scripts/quality_score.py ...` 실행
- score/grade 추출 정상 확인

---

### Commit 7.3: ISSUE-08 — new-deck.sh eval 인젝션 수정

**파일:** `scripts/new-deck.sh`

**현재 (line 29):**
```bash
eval "$var_name='$value'"
```

**수정:**
```bash
printf -v "$var_name" '%s' "$value"
```

**테스트:**
- Title에 single quote 포함 (`O'Brien's Talk`) → 정상 동작
- Title에 shell metachar (`$(whoami)`) → 실행되지 않음

---

### Commit 7.4: ISSUE-14 — Agent `context: fork` → Skill로 이동

**파일들:**
- `.claude/agents/slide-critic.md` — "Context: fork" 제거
- `.claude/agents/layout-auditor.md` — 동일
- `.claude/agents/typography-reviewer.md` — 동일
- `.claude/agents/verifier.md` — 동일
- `.claude/agents/slide-fixer.md` — 동일
- `AGENTS.md` — Agent Enforcement 테이블에서 context 컬럼 수정

**추가:** Read-only agent에 `disallowedTools: [Edit, Write]` 추가 (실제 tool 제한).

**대안 검토 필요:**
Claude Code 최신 문서에서 agent frontmatter의 정확한 스펙을 재확인.
현재 `.claude/agents/` 파일들이 YAML frontmatter가 아닌 prose 형태로 "Context: fork"를 명시하고 있으므로, 이것이 실제 런타임에서 어떻게 처리되는지 확인 필요.

---

## Phase 8: Theme & Brand System

**Goal:** `_brand.yml` 도입, dark mode 네이티브 구현, variant 테마 완성.
**Independent:** Phase 6과 무관하게 병렬 진행 가능.

### Commit 8.1: ISSUE-16 — `_brand.yml` 생성

**새 파일:** `_brand.yml` (프로젝트 루트)

```yaml
# Quarto 1.8 Brand Definition
# impeccable design system — OKLCH-based, typography-first

color:
  palette:
    primary: "#3730a3"        # oklch(0.45 0.18 265) Deep Indigo
    secondary: "#1a8a8a"      # oklch(0.55 0.12 195) Warm Teal
    accent: "#c69a2d"         # oklch(0.72 0.16 85) Marigold
    success: "#2d9050"        # oklch(0.60 0.15 145)
    warning: "#c69a2d"        # oklch(0.72 0.16 85)
    danger: "#b83a3a"         # oklch(0.55 0.18 25)
    info: "#3a6ab8"           # oklch(0.55 0.12 240)
    light: "#f3f2f7"          # oklch(0.96 0.012 265) near-white
    dark: "#1a1625"           # oklch(0.12 0.015 265) near-black
  foreground: "#2e2746"       # neutral-900
  background: "#f3f2f7"       # neutral-50

typography:
  fonts:
    - family: Plus Jakarta Sans
      source: google
      weight: 200..800
    - family: Source Sans 3
      source: google
      weight: 200..900
    - family: JetBrains Mono
      source: google
      weight: 100..800
  headings:
    family: Plus Jakarta Sans
    weight: 700
  base:
    family: Source Sans 3
    size: 28px
    line-height: 1.55
  monospace:
    family: JetBrains Mono
    size: 0.75em

logo:
  # TODO: impeccable logo if/when created
```

**_quarto.yml 변경:**
```yaml
# Google Fonts 인라인 링크 제거 (ISSUE-11 동시 해결)
# _brand.yml이 폰트 관리를 담당
brand: _brand.yml
```

---

### Commit 8.2: ISSUE-04 — Dark Mode를 `brand-mode: dark`로 재구현

**파일:** `themes/impeccable.scss`

**변경:**
1. `.reveal.dark-mode` / `[data-theme="dark"]` 블록 (lines 746-858) 전체 삭제
2. 새 파일: `themes/impeccable-dark.scss` — dark mode 전용 variant

또는 Quarto 1.8 네이티브 방식:
```yaml
# _quarto.yml 또는 deck YAML에서:
format:
  revealjs:
    brand-mode: dark
```

**구체적 접근:**
- `_brand.yml`에 dark variant 추가 (Quarto 1.8이 지원하는 경우)
- 또는 `themes/impeccable-dark.scss`를 별도 생성하여 dark 전용 semantic token remapping
- master theme에서 112줄의 dead code 제거 → 깔끔해짐

**검증:** dark mode 적용된 예제 1개 생성, 렌더 확인.

---

### Commit 8.3: ISSUE-07 — Variant 테마에 `.infobox` 추가

**파일들:**
- `themes/impeccable-academic.scss`
- `themes/impeccable-corporate.scss`
- `themes/impeccable-creative.scss`
- `themes/impeccable-lightning.scss`

각 파일에 `.infobox` 스타일 추가. 마스터 테마의 `.infobox` (line 474) 패턴을 각 variant의 색상 팔레트에 맞게 적용.

**선택적 개선:** 공통 semantic box mixin을 `themes/_semantic-boxes.scss` partial로 추출하여 DRY 원칙 적용. 단, Quarto의 SCSS 처리가 @import/@use를 지원하는지 확인 필요.

---

### Commit 8.4: ISSUE-10 — Templates에 누락된 Speaker Notes 추가

**파일들:**
- `templates/academic.qmd` — 모든 content slide에 `{.notes}` 블록 확인/추가
- `templates/corporate.qmd` — 동일

**추가:** `impeccable-academic.scss`의 `$base-size: 26px` → `28px`로 수정 (디자인 표준 준수).

---

### Commit 8.5: ISSUE-11 — `_quarto.yml` 과도한 폰트 정리

**파일:** `_quarto.yml`

`_brand.yml` 도입 후 `include-in-header`의 Google Fonts 링크 제거.
`_brand.yml`의 `fonts` 섹션이 필요한 폰트만 로드.

variant 테마(academic: Cormorant Garamond, corporate: IBM Plex Sans 등)의 추가 폰트는 각 예제/템플릿의 YAML에서 개별 로드.

---

## Phase 9: Scoring Accuracy

**Goal:** Scorer의 나머지 부정확성 수정, agent 비용 최적화.
**Depends on:** Phase 6 (scorer 기반)

### Commit 9.1: ISSUE-09 — Nested Semantic Box Detection 로직 재설계

**파일:** `scripts/quality_score.py`
**함수:** `check_llm_bias_patterns()` (lines 406-417)

**현재 문제:** `:::` 닫기가 시맨틱 박스인지 레이아웃 div인지 구분 불가.

**수정 접근: Stack-based tracking**
```python
# 현재 single counter → stack으로 변경
div_stack = []  # stack of div types: "semantic" | "other"

for line in content.splitlines():
    stripped = line.strip()
    if not stripped.startswith(":::"):
        continue
    
    # Opening div
    if stripped.startswith(":::") and len(stripped) > 3 and stripped != ":::":
        classes = SEMANTIC_BOX_RE.findall(stripped)
        if classes:
            if any(t == "semantic" for t in div_stack):
                report.deduct("MIN-10", 2, f"Nested semantic box: {classes[0]}")
            div_stack.append("semantic")
        else:
            div_stack.append("other")
    # Closing div
    elif stripped == ":::":
        if div_stack:
            div_stack.pop()
```

**테스트:**
- `.keybox` inside `.two-col` → 감점 없음 (정상)
- `.infobox` inside `.keybox` → MIN-10 감점 (정상)
- 중첩 레이아웃 + 시맨틱 → 혼동 없음

---

### Commit 9.2: ISSUE-15 — Agent Model 지정

**파일들:**
- `.claude/agents/slide-critic.md` — `model: sonnet` 추가
- `.claude/agents/layout-auditor.md` — `model: sonnet`
- `.claude/agents/typography-reviewer.md` — `model: sonnet`
- `.claude/agents/pedagogy-reviewer.md` — `model: sonnet`
- `.claude/agents/verifier.md` — `model: sonnet`
- `.claude/agents/slide-fixer.md` — `model: inherit` (calling session의 모델 사용)
- `.claude/agents/theme-designer.md` — `model: inherit`
- `.claude/agents/content-translator.md` — `model: inherit`
- `AGENTS.md` — Agent Enforcement 테이블에 Model 컬럼 추가

**주의:** model 필드가 실제 agent frontmatter에서 지원되는지 최신 Claude Code 문서 재확인 필요. `.claude/agents/` 파일의 현재 형식이 YAML frontmatter가 아니면 변환 필요.

---

## Phase 10: Skill Architecture

**Goal:** 스킬의 디자인 컨텍스트 일관성 강화.
**Independent:** 다른 Phase와 무관.

### Commit 10.1: ISSUE-12 — Mandatory Context Loading Cascade

**파일들:** 모든 디자인 스킬 (12개)
- `.claude/skills/critique-slides.md`
- `.claude/skills/audit-slides.md`
- `.claude/skills/typeset-slides.md`
- `.claude/skills/colorize-slides.md`
- `.claude/skills/arrange-slides.md`
- `.claude/skills/animate-slides.md`
- `.claude/skills/bolder-slides.md`
- `.claude/skills/quieter-slides.md`
- `.claude/skills/polish-slides.md`
- `.claude/skills/normalize-slides.md`
- `.claude/skills/distill-slides.md`
- `.claude/skills/create-deck.md`

**각 스킬의 프롬프트 첫 부분에 추가:**
```markdown
## MANDATORY PREPARATION

Before proceeding with any work:

1. **Read `/slide-design`** to load the active design context.
2. **Check `.impeccable-quarto.md`** in the project root.
   - If it exists: read it for project-specific design context.
   - If it does NOT exist: inform the user and suggest running `/teach-style`.
3. **Check YAML frontmatter** of the target `.qmd`:
   - Verify a custom theme is specified (not default Reveal.js).
   - Extract slide dimensions, transition settings.
4. **Confirm design context is active** before proceeding.

Do NOT skip this step. Proceeding without design context produces generic output.
```

**변형:** 이 텍스트를 모든 스킬에 복사하지 않고, `/slide-design`을 호출하라는 한 줄 지시로 간소화할 수도 있음:
```markdown
## MANDATORY: Run `/slide-design` first to load design context.
```

---

### Commit 10.2: ISSUE-13 — Reference Conditioning 연결

**파일들:** 핵심 스킬 4개에 관련 참조 문서 읽기 지시 추가

| Skill | Reference to Read |
|-------|-------------------|
| `/typeset-slides` | `.context/references/impeccable-original-deep-patterns.md` §1 Typography |
| `/colorize-slides` | `.context/references/impeccable-original-deep-patterns.md` §1 Color |
| `/animate-slides` | `.context/references/impeccable-original-deep-patterns.md` §1 Motion |
| `/critique-slides` | `.context/references/impeccable-original-deep-patterns.md` (전체) |

**각 스킬에 추가:**
```markdown
## REFERENCE MATERIAL

Read the following reference for domain-specific knowledge before this task:
- `.context/references/impeccable-original-deep-patterns.md`, section [relevant section]

This reference contains non-obvious design rules (e.g., vertical rhythm mathematics,
chroma reduction at lightness extremes, the 80ms perception threshold) that prevent
generic output.
```

---

## Execution Order & Parallelism

```
Week 1:
├── Phase 6 (scorer fix) — SEQUENTIAL, must be first
│   ├── Commit 6.1 (ghost slides)
│   ├── Commit 6.2 (word count)
│   └── Commit 6.3 (pure bw)
│
├── Phase 8 (theme & brand) — PARALLEL with Phase 6
│   ├── Commit 8.1 (_brand.yml)
│   ├── Commit 8.2 (dark mode)
│   ├── Commit 8.3 (.infobox)
│   ├── Commit 8.4 (templates)
│   └── Commit 8.5 (fonts)
│
└── Phase 10 (skill architecture) — PARALLEL with Phase 6
    ├── Commit 10.1 (mandatory context)
    └── Commit 10.2 (reference conditioning)

Week 2:
├── Phase 7 (infrastructure) — AFTER Phase 6
│   ├── Commit 7.1 (pre-commit)
│   ├── Commit 7.2 (CI ANSI)
│   ├── Commit 7.3 (eval)
│   └── Commit 7.4 (agent frontmatter)
│
└── Phase 9 (scoring accuracy) — AFTER Phase 6
    ├── Commit 9.1 (nested box)
    └── Commit 9.2 (agent model)
```

---

## Verification Criteria (Phase-Level)

### Phase 6 ✅ Criteria
- [ ] `python3 scripts/quality_score.py examples/demo.qmd --no-render` → score ≥ 80
- [ ] All 5 examples score ≥ 80 with `--no-render`
- [ ] No "(untitled)" ghost slides in verbose output
- [ ] demo.qmd backtick `#000000` not flagged as pure-bw
- [ ] academic-paper.qmd table slide word count < 40

### Phase 7 ✅ Criteria
- [ ] `scripts/pre-commit-quality.sh` works when symlinked to `.git/hooks/`
- [ ] CI workflow runs successfully (ANSI-free output for grep)
- [ ] `new-deck.sh` handles single quotes and metacharacters in input safely
- [ ] Agent definitions use correct Claude Code frontmatter fields

### Phase 8 ✅ Criteria
- [ ] `_brand.yml` exists and is referenced from `_quarto.yml`
- [ ] Dark mode activatable via `brand-mode: dark` or `theme: impeccable-dark.scss`
- [ ] All 4 variant themes have `.infobox` styled
- [ ] All templates have speaker notes on every content slide
- [ ] `_quarto.yml` loads ≤ 3 font families (or defers to `_brand.yml`)

### Phase 9 ✅ Criteria
- [ ] `.keybox` inside `.two-col` → no false-positive nesting deduction
- [ ] `.infobox` inside `.keybox` → correctly flagged
- [ ] Agent model fields present in agent definitions (if supported by runtime)

### Phase 10 ✅ Criteria
- [ ] All 12 design skills reference `/slide-design` as mandatory first step
- [ ] `/typeset-slides`, `/colorize-slides`, `/animate-slides`, `/critique-slides` reference relevant `.context/references/` docs

---

## Risk Register

| Risk | Mitigation |
|------|-----------|
| `_brand.yml` 기능이 RevealJS format에서 완전히 지원되지 않을 수 있음 | Quarto 1.8 릴리즈 노트 재확인. 미지원 시 SCSS-only 접근으로 fallback |
| Agent `model` frontmatter가 현재 agent 파일 형식에서 무시될 수 있음 | Claude Code 최신 문서 확인. 미지원 시 해당 커밋 skip |
| Ghost slide 수정이 다른 QMD 패턴 (--- only slides) 을 깨뜨릴 수 있음 | untitled slide가 의도적인 케이스도 테스트 (빈 슬라이드, 이미지 only) |
| Dark mode SCSS 삭제 시 기존 사용자가 수동으로 class 추가해 쓰고 있을 수 있음 | CHANGELOG에 breaking change 명시. migration guide 1줄 추가 |
| `_brand.yml` 도입이 기존 `include-in-header` 폰트 로드와 충돌 | 순서: _brand.yml 먼저 작성 → 테스트 → include-in-header 제거 |

---

*Plan authored 2026-04-03 based on 07-strategic-review.md (16 issues, 4 agent reports)*
