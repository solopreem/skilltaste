<div align="center">

# video-skills

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | **한국어** | [Español](README.es.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Português](README.pt.md)

**완성된 영상을, 당신의 코딩 에이전트가 당신의 제품으로 다시 만들어 줍니다.**

마음에 드는 영상을 고르고 에이전트에게 제품을 알려 주면, 같은 영상이 나옵니다.

좋은 영상을 몇 분 만에 당신의 제품으로 다시 만듭니다. 좋은 감각은 기본입니다.

</div>

```bash
npx skills add sonnyproto/video-skills                       # 라이브러리 전체 (에이전트가 항목을 고름)
npx skills add sonnyproto/video-skills/launch/broll-wheel   # 이 한 편만
```

그다음 Claude Code나 Codex에서:

```text
broll-wheel로 https://your-product.com 런칭 영상을 만들어 줘.
```

직접 설치할 것은 없습니다. 에이전트가 항목의 `scripts/setup.sh`를 실행해 Node 20+, ffmpeg, Python 3을 확인하고,
HyperFrames 스킬이 없으면 설치합니다. 렌더러는 `npx`가 고정된 버전으로 받아옵니다.

## 왜 만들었나

지금의 영상 스킬은 크게 두 가지입니다. 하나는 닫힌 번들: 스타일 하나에 한 번 구매, 빠르지만 안을 볼 수도 섞을 수도 없습니다.
다른 하나는 깊이 있는 오픈 툴킷인데, 저마다 형식이 달라 서로 맞물리지 않습니다.

video-skills는 앞의 것을 평평하게, 그리고 공개적으로 만든 버전입니다:

- **항목 하나 = 영상 한 편.** 각 항목에는 그것이 만든 `result.mp4`가 들어 있어 눈으로 보고 고를 수 있습니다.
- **재현 가능.** 모든 항목에 영상을 그대로 렌더링하는 완전한 프로젝트와, 스톡 영상의 소스 ID, 생성 미디어의 프롬프트가 들어 있습니다. API 키는 필요 없습니다.
- **어디서나 같은 형식.** 모든 항목이 같은 파일과 같은 `taste.json` 카드를 가지므로 비교할 수 있고, 에이전트가 조합할 수 있습니다 ([spec/ENTRY.md](spec/ENTRY.md)).
- **제품은 파일 하나에.** 내 제품으로 바꾸려면 `film.json`과 에셋만 고치면 되고, 생성기는 건드리지 않습니다.

## 라이브러리

<!-- CATALOG -->
| Preview | Entry | Category · method | Length | Events / 10 s |
|---|---|---|---|---|
| <img src="launch/broll-wheel/result/preview.gif" width="240"> | [**broll-wheel**](launch/broll-wheel/) B-roll wheel launch | launch · broll-under-type | 90 s 16:9 | 8.7 |
| <img src="launch/feature-roster/result/preview.gif" width="240"> | [**feature-roster**](launch/feature-roster/) Feature roster | launch · rebuilt-ui-roster | 26.7 s 16:9 + 9:16 | 3.0 |
<!-- /CATALOG -->

## 항목의 구성

```
<category>/<id>/
├── SKILL.md       이것을 불러와 영상을 만든다
├── taste.json     카드: 요구 사항, 일곱 레이어, 사양, 측정값, 필요한 것, 어울리는 용도
├── references/    floor.md (공통 규칙), sourcing.md (launch: 실제 소재 수집), RECIPE.md (샷별 구성), SWAP.md (제품 교체), REFERENCE.md
├── scripts/       setup.sh (없는 것을 설치)와 측정 스크립트
├── result/        result.mp4, 포스터, 콘택트 시트, 미리보기, metrics.json
└── project/       렌더링 가능한 프로젝트: film.json, tools/, assets/
```

모든 항목은 같은 일곱 레이어 위에 놓입니다:

| 레이어 | 질문 |
|---|---|
| floor | 절대 타협할 수 없는 것은? (실제 제품만, 샘플은 표시, 브랜드) |
| category | 어떤 종류의 영상인가? (런칭, 설명, 튜토리얼, 데이터 스토리, 소셜 컷, 스팅) |
| method | 화면을 어떻게 만들고 뼈대를 어떻게 이어가나? (B롤 위 타이포, 끊지 않는 하나의 도형, 비트 몽타주, 3D UI…) |
| moves | 어떤 구체적인 기법으로 채우나? (휠 챕터 구분, 형광펜 스윕, 앵커 몽타주, 필 모핑…) |
| craft | 무엇이 고급스럽게 보이게 하나? (3초 안의 훅, 35% 부근의 폭발, 착지에 맞춘 효과음, -14 LUFS) |
| style | 어떻게 보이나? (그레이드, 서체, 색의 역할) |
| tool | 무엇으로 렌더링하나? (HyperFrames, Remotion…) |

서로 다른 레이어끼리는 충돌하지 않습니다. 같은 레이어 안에서는 floor > category > method > moves > craft > style 순으로 우선합니다.

각 항목은 자기완결적입니다. 공통 파일(floor 규칙, 측정 스크립트)은 각 항목에 복사되고, 외부 도구(HyperFrames, ffmpeg)는
`taste.json`의 `requires`에 선언만 하며, 취향은 절대 공유하지 않습니다. 자세한 내용은 [spec/ENTRY.md](spec/ENTRY.md).

## 도구

| | |
|---|---|
| `tools/floor.md` | 공통 floor 규칙 (각 항목의 `references/`에 복사됨) |
| `launch/sourcing.md` | launch용: 제품의 실제 화면, 로고, 문구를 모으는 방법 (각 launch 항목의 `references/`에 복사됨) |
| `tools/validate.py` | 모든 항목을 형식에 맞춰 검사하고, 공통 파일 사본이 `tools/`와 같은지 확인 |
| `tools/catalog.py` | `catalog.json`과 위의 표를 다시 만듦 |
| `tools/analyze.py <video> <out>` | 컷, 샷, 콘택트 시트, LUFS, 트루 피크, BPM, 비트에 맞은 컷 |
| `tools/events.py <video> <out>` | 10초당 시각 변화 이벤트 수와 정지 비율 |

## 요구 사항

Node 20+, ffmpeg, Python 3. 그 밖에 필요한 것(렌더러 버전, B롤용 영상 모델, 음악 모델)은 각 항목에 적혀 있습니다.

## 기여

새 항목을 환영합니다. [CONTRIBUTING.md](CONTRIBUTING.md)를 보세요. 기준: 프로젝트가 결과 영상을 그대로 렌더링할 것,
제품 내용이 `film.json`에 있을 것, 결과가 측정되어 있을 것, 레퍼런스의 어떤 것도 재배포하지 않을 것.

## 감사의 말

아이디어와 규칙을 감사한 마음으로 빌려 왔습니다: [HyperFrames](https://hyperframes.heygen.com),
[huashu-motion](https://github.com/alchaincyf/huashu-motion) (리듬과 연출 노트),
[video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) (레시피 카드와 교체 가이드),
[product-launch-motion](https://github.com/AbubakrChan/product-launch-motion) (크래프트 디테일).

## 라이선스

broll-wheel 예시는 Meta의 개인 AI 에이전트 Muse를 위한 비공식 스펙 필름입니다. Meta와 관련이 없으며,
승인이나 후원을 받지 않았습니다. Muse와 그 에셋은 Meta의 것이며 이 저장소에 포함되어 있지 않습니다.

코드: MIT. 결과 영상과 생성 미디어: CC BY 4.0. 예시 제품 에셋은 각 소유자에게 속하며, 재사용 가능한 범위는 각 항목의 `taste.json`에 적혀 있습니다.
