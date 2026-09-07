---
name: localize-unity4-tk2d-games
description: Unity 4.x Windows 게임의 한국어 패치를 분석·제작·검증한다. tk2d/tk2dFontData 비트맵 폰트, resources.assets, Texture2D, Material, MonoBehaviour 타입 트리, Noto Sans KR/CJK KR 글리프 아틀라스, 언어별 문자열 파일을 다룰 때 사용한다. 구형 Unity 에디터 없이 기존 CJK 언어 슬롯을 한국어로 교체하거나, 한글이 네모로 나오거나, 누락 문자 때문에 KeyNotFoundException이 발생하거나, 폰트 패치 후에도 중국어가 표시되는 문제를 진단할 때도 사용한다.
---

# Unity 4 tk2d 게임 한국어화

## 목표

Unity 4.x Windows 독립 실행형 게임에서 기존 CJK 언어 슬롯의 `tk2dFontData`, `Texture2D`, `Material` 연결과 문자열 데이터를 보존적으로 교체하여 한국어 패치를 제작한다. 현대 Unity 에디터로 구형 자산을 재직렬화하지 말고 원본 바이너리의 객체 ID와 참조 관계를 유지한다.

완료 조건을 “한글이 들어간 파일 생성”이 아니라 다음 상태로 정의한다.

- 게임 언어 목록에서 `한국어`를 선택할 수 있다.
- 기본 UI, 튜토리얼, DLC, 자동 생성 이름이 한국어로 표시된다.
- 누락 글리프, 네모 글자, 텍스트 위치 붕괴, 런타임 예외가 없다.
- 원본과 패치 파일의 객체 차이가 의도한 FontData와 Texture2D로 제한된다.
- 격리된 게임 복사본에서 실제 플레이 진입을 확인한다.

## 전제 환경

다음 구조를 기본 대상으로 가정하되 실제 경로와 버전은 먼저 조사한다.

```text
Game.exe
GameName_Data/
  resources.assets
  Managed/*.dll
  GameData/strings-<locale>.data
  GameData/<DLC>/strings-<locale>.data
  GameData/names-<locale>.data
  GameData/drugNames-<locale>.data
```

다음 도구 조합을 우선 사용한다.

- UnityPy: Unity 자산 읽기·쓰기와 객체 비교
- UnityPy `TypeTreeGenerator`: Unity 4 MonoBehaviour 타입 트리 재구성
- ILSpy 또는 동등한 .NET 디컴파일러: 언어 선택 및 tk2d 런타임 동작 확인
- Pillow와 NumPy: 글리프 래스터화, 아틀라스, ARGB32 밉 체인 처리
- Noto Sans CJK KR Regular OTF: 한글과 기존 CJK 호환 글리프를 함께 유지

Unity 4 에디터가 없어도 진행한다. 더 최신 Unity 에디터로 `resources.assets`를 열어 저장하지 않는다.

## 작업 원칙

1. 설치된 파일을 직접 실험 대상으로 사용하지 않는다.
2. 원본 파일의 SHA-256과 크기를 먼저 기록한다.
3. 출력은 별도 작업 폴더와 배포 폴더에 생성한다.
4. Path ID, 파일명, 폰트 수, 아틀라스 크기를 고정값으로 가정하지 않는다.
5. 기존 언어 슬롯의 객체를 새로 만들지 말고 가능한 한 같은 Path ID에서 내용만 교체한다.
6. 이미 패치된 `resources.assets`를 다음 빌드의 원본으로 사용하지 않는다.
7. 문자열 번역과 폰트 패치를 별개 산출물로 생각하되 최종 문자 집합은 둘의 합으로 만든다.
8. 각 단계에서 재파싱과 비교 검증을 통과한 뒤 다음 단계로 진행한다.

## 1. 원본과 Unity 버전 조사

먼저 읽기 전용으로 다음 정보를 수집하고 `analysis-manifest.json` 같은 작업 기록에 남긴다.

- 실행 파일과 `*_Data` 폴더 위치
- `resources.assets` 및 백업 파일의 SHA-256
- `Managed` 어셈블리 목록
- Unity의 정확한 버전 문자열
- 지원 언어 코드와 언어 설정 저장 위치
- 기본 게임·DLC·이름 생성용 언어 데이터 파일
- 기존 CJK 폰트 이름과 크기 변형

Unity 버전은 플레이어 로그, 자산 메타데이터, 실행 파일 문자열을 교차 확인한다. 타입 트리를 만들 때 `4.x` 같은 대략값이 아니라 정확한 버전을 사용한다.

관리 어셈블리를 디컴파일하여 다음을 찾는다.

- 언어 코드가 어떤 문자열 파일과 폰트 접미사를 선택하는지
- CJK 슬롯이 `SC`, `TC`, `JP` 중 어떤 폰트 경로를 사용하는지
- `tk2dTextGeomGen`, `tk2dFontData`, `tk2dFontChar`의 실제 필드와 폴백 동작
- 번역 문자열의 참조 토큰과 포맷 함수

폰트만 바꾸면 기존 언어 문자열은 그대로 남는다. 사용자가 “한글 폰트인데 중국어가 표시된다”고 보고하면 문자열 파일과 현재 언어 코드부터 확인한다.

## 2. 교체할 객체 그래프 식별

`resources.assets`를 읽고 후보 `MonoBehaviour`, `Texture2D`, `Material`을 이름과 참조 관계로 찾는다. Path ID는 검색 결과로 기록하고 이후 동일 빌드에서만 사용한다.

각 폰트 크기 변형마다 다음 관계를 확정한다.

```text
tk2dFontData MonoBehaviour
        │
        ├── charDictKeys / charDictValues
        ├── texelSize / lineHeight / largestWidth
        └── Material ── _MainTex ──> Texture2D atlas
```

Material의 `_MainTex`가 예상 Texture2D Path ID를 정확히 참조하는지 검사한다. 셰이더 이름과 Material Path ID를 기록한다. Material이 정상이라면 수정 대상에서 제외한다.

Unity 4 자산에 MonoBehaviour 타입 트리가 없거나 불완전하면 다음 순서를 사용한다.

```python
environment = UnityPy.load(str(resources_path))
generator = TypeTreeGenerator(exact_unity_version)
generator.load_local_dll_folder(str(managed_directory))
environment.typetree_generator = generator

node = font_object.generate_monobehaviour_node()
font_tree = font_object.read_typetree(node)
```

게임에 포함된 어셈블리를 사용하여 타입 트리를 생성한다. 다른 버전의 DLL이나 추측한 필드 정의로 저장하지 않는다.

## 3. 번역 데이터 제작

영문 또는 기준 언어 파일을 원본으로 사용하고 선택한 CJK 슬롯의 파일명으로 한국어판을 출력한다. 예를 들어 `zh` 슬롯을 사용한다면 다음과 같이 구성한다.

```text
strings-en.data            -> strings-zh.data
DLC/strings-en.data        -> DLC/strings-zh.data
names-en.data              -> names-zh.data
drugNames-en.data          -> drugNames-zh.data
```

언어 자체 이름을 나타내는 레코드는 `한국어`로 바꾼다.

JSON처럼 보이는 파일이라도 주석, 리터럴 탭, 중복 코드가 있을 수 있다. 일반 JSON 파서로 다시 직렬화하기 전에 실제 형식을 조사한다. 주석과 레코드 순서를 보존해야 하면 원문 문자열 리터럴만 치환한다.

번역표의 키를 최소한 다음 세 값으로 구성한다.

```text
(파일 범위, code, 원문 text)
```

`code`가 중복되고 원문이 다른 경우가 있으므로 `code`만 키로 사용하지 않는다.

다음 런타임 토큰을 원문과 완전히 동일하게 보존한다.

- `{0}`, `{1}` 같은 포맷 자리표시자
- `&W>`, `&LTBLUE>`, `&eff1>` 같은 문자열 참조·스타일 토큰
- `^CFFFFFFFF`, `^cff0f` 같은 tk2d 색상 코드
- `\n`, 탭, URL, 통화·단위 토큰

토큰 검사용 정규식의 출발점으로 다음 패턴을 사용하고 게임 코드에 맞게 보완한다.

```python
PROTECTED_RE = re.compile(
    r'&[^>\r\n]*>|\{[^{}\r\n]+\}|\^[cCgG][0-9A-Fa-f]+|https?://\S+'
)
```

각 레코드에서 `sorted(PROTECTED_RE.findall(source))`와 대상 결과가 같지 않으면 빌드를 실패시킨다. 문자열 코드의 수와 순서도 원본과 같아야 한다.

이름 생성 트리에서는 식별자, 정렬 순서, 내부 조합 규칙을 번역하지 않는다. `id`, `order`, `endType`, 화학 접두·접미사처럼 게임이 특별히 취급하는 키는 원문을 유지하고 화면에 표시되는 값만 번역한다.

## 4. 최종 문자 집합 산출

번역 완료 후 실제 출력 파일 전체에서 문자를 추출한다. 번역보다 먼저 고정된 완성형 목록만 사용하지 않는다.

문자 집합을 NFC로 정규화하고 다음의 합집합을 만든다.

1. 번역 파일에 실제로 등장하는 모든 BMP 문자
2. 사용자가 제공한 완성형 한글 목록
3. 기존 폰트의 ASCII, Latin-1, 문장 부호, 통화, UI 기호
4. 기존 폰트의 제어 문자와 폴백 문자
5. 선택한 언어 슬롯에 번역하지 않고 남겨 둔 문자

최소한 다음 코드 포인트를 반드시 포함한다.

```text
U+0000  fallback
U+000A  line feed
U+000D  carriage return
U+0020  space
```

구형 tk2d 런타임은 문자를 먼저 `charDict`에서 조회한 뒤 줄바꿈 분기를 처리할 수 있다. 누락 문자를 `U+0000`으로 치환한 다음 `charDict[0]`을 검사 없이 읽는 구현도 있다. 따라서 보이지 않는 문자라고 삭제하지 않는다.

Unity 4의 일반적인 tk2d 문자열 경로는 UTF-16 `char` 단위이므로 BMP 밖의 문자와 서로게이트 쌍은 별도 런타임 분석 없이 지원한다고 가정하지 않는다. 한글 음절과 호환 자모는 BMP에 있으므로 안전하다.

## 5. 글리프와 아틀라스 생성

각 기존 폰트 크기 변형을 독립적으로 처리한다. 폰트 파일명의 숫자만 믿지 말고 기존 ASCII 글리프의 크기, `texelSize`, `lineHeight`, 아틀라스 크기와 기준선을 측정한다.

Noto Sans CJK KR OTF를 사용하여 글리프를 래스터화한다. 번역되지 않은 CJK 문자를 유지해야 한다면 한글 전용 서브셋 TTF보다 전체 CJK KR OTF를 우선한다.

각 표시 글리프에서 다음 값을 계산한다.

- 마스크와 베어링: `font.getmask2(char, mode="L", anchor="ls")`
- advance: `font.getlength(char)`를 픽셀 단위로 반올림
- atlas 좌표: 결정적 패커로 배치하고 글리프 사이에 1~2px 여백 유지
- 좌표 배율: 기존 `font_tree["texelSize"]["x"]` 사용

`tk2dFontChar`를 다음 필드 구조로 생성한다.

```text
p0: Vector3
p1: Vector3
uv0: Vector3
uv1: Vector3
flipped: bool/int
gradientUv: Vector2[]
advance: float
channel: int
```

아틀라스의 이미지 좌표가 좌상단 원점이라면 tk2d UV의 Y축을 다음처럼 뒤집는다.

```python
uv0.x = atlas_x / atlas_width
uv0.y = (atlas_height - atlas_y) / atlas_height
uv1.x = (atlas_x + glyph_width) / atlas_width
uv1.y = (atlas_height - atlas_y - glyph_height) / atlas_height
```

글리프 지오메트리는 측정한 기준선 `baseline_px`와 기존 배율로 계산한다.

```python
p0.x = x_offset * scale
p1.x = (x_offset + glyph_width) * scale
p0.y = (baseline_px - y_offset) * scale
p1.y = (baseline_px - y_offset - glyph_height) * scale
advance = advance_px * scale
```

공백은 투명한 작은 사각형과 정상 advance를 사용한다. 제어 문자는 그리지 않고 `p0`, `p1`, `uv0`, `uv1`, `advance`를 0으로 둔다. `U+0000`은 완전히 빈 폴백 글리프로 만들고 원본 스키마가 요구하면 0인 `gradientUv` 네 개를 유지한다.

원래 아틀라스 크기에 모든 글리프가 들어가는지 먼저 확인한다. 들어가지 않으면 무조건 크기를 늘리지 말고 다음 순서로 해결한다.

1. 패킹 방식과 여백을 개선한다.
2. 실제 번역에 사용하지 않는 표의 문자를 제외한다.
3. 여러 폰트 아틀라스 또는 더 큰 텍스처가 런타임과 하드웨어에서 안전한지 조사한다.

## 6. tk2dFontData 직렬화

기존 FontData 트리에서 참조와 레이아웃 필드를 보존하고 문자 관련 필드만 교체한다.

```python
font_tree["chars"] = []
font_tree["charDictKeys"] = sorted_codepoints
font_tree["charDictValues"] = values_in_the_same_order
font_tree["useDictionary"] = 1
font_tree["kerning"] = measured_kerning
font_tree["largestWidth"] = max(v["advance"] for v in values)
```

`version`은 원본과 런타임의 사전 형식을 확인하여 유지하거나 같은 형식의 값으로 설정한다. `lineHeight`와 `texelSize`는 기존 값을 우선 보존한다. `charDictKeys`와 `charDictValues`의 인덱스 대응을 절대로 깨뜨리지 않는다.

커닝은 없어도 한글 표시가 가능하지만 기존 ASCII UI 품질을 위해 실제 폰트의 쌍 길이 차이로 생성한다. 지원 문자 전체의 O(n²) 계산을 피하고 ASCII 등 필요한 범위로 제한한다.

## 7. Texture2D와 Material 처리

기존 Texture2D 객체의 Path ID와 크기를 유지하고 픽셀 데이터만 바꾸는 방식을 우선한다. Unity 4 인라인 `Texture2D`가 `ARGB32`라면 다음 규칙을 적용한다.

- `m_TextureFormat = 5` (`ARGB32`)
- `m_MipMap = true`
- `m_CompleteImageSize = len(all_mips)`
- `image data = all_mips`

Unity 4의 해당 형식은 행이 아래에서 위로 저장될 수 있으므로 각 밉을 수직 반전하고 RGBA를 ARGB 바이트 순서로 바꾼다.

```python
flipped = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
rgba = np.asarray(flipped, dtype=np.uint8)
argb = rgba[:, :, [3, 0, 1, 2]]
```

각 단계에서 너비와 높이를 절반으로 줄여 1×1까지 밉을 생성하고 순서대로 이어 붙인다. 흰색 RGB와 글리프 알파를 사용하면 기존 폰트 셰이더의 색상 처리를 유지하기 쉽다.

텍스처가 스트리밍 데이터나 다른 압축 형식을 사용한다면 위 규칙을 바로 적용하지 말고 해당 객체의 저장 방식을 먼저 구현한다.

정상 Material은 재생성하거나 교체하지 않는다. `_MainTex` 참조와 기존 tk2d 폰트 셰이더를 유지한다. Material이 없거나 손상된 경우에만 같은 언어 슬롯의 정상 Material을 복제하고 `_MainTex`만 대상 Texture2D로 연결한다.

## 8. 자산 저장과 정적 검증

반드시 원본 `resources.assets`를 입력으로 로드하여 별도 출력 경로에 저장한다. 저장한 파일을 다시 열어 다음을 검사한다.

1. 원본과 출력의 Unity 객체 Path ID 집합이 같다.
2. 변경 객체가 의도한 `tk2dFontData`와 `Texture2D`뿐이다.
3. Material 객체의 원시 데이터와 `_MainTex` 참조가 보존되었다.
4. 모든 `charDictKeys`가 유일하고 정렬되어 있다.
5. `len(charDictKeys) == len(charDictValues)`이다.
6. `U+0000`, LF, CR, space가 존재한다.
7. `U+0000`의 지오메트리와 advance가 0이다.
8. Texture2D를 다시 RGBA로 디코딩한 기본 밉이 생성 PNG와 픽셀 단위로 같다.
9. 각 번역 파일의 모든 표시 문자가 한국어 UI에 쓰이는 모든 대상 폰트에 존재한다.
10. 문자열 파일이 게임이 허용하는 JSON/JSONC 형식으로 다시 파싱된다.
11. 문자열 코드 수·순서와 보호 토큰이 원본과 같다.

검증 결과와 각 파일의 크기·SHA-256을 기계 판독 가능한 manifest에 기록한다. 검증 하나라도 실패하면 설치용 패키지를 만들지 않는다.

## 9. 배포 패키지 구성

실제 게임 폴더 구조를 그대로 복제하여 복사만으로 설치할 수 있게 만든다.

```text
package/
  GameName_Data/
    resources.assets
    GameData/
      strings-<donor-locale>.data
      names-<donor-locale>.data
      drugNames-<donor-locale>.data
      DLC/strings-<donor-locale>.data
manifest.json
```

설치 설명에는 다음을 명시한다.

- 교체하는 언어 슬롯
- 백업해야 할 모든 파일
- 게임을 완전히 종료한 뒤 복사할 것
- 언어 메뉴에서 `한국어`를 선택할 것
- 원복 방법과 파일 해시

상업 게임의 원본 전체 자산을 공개 배포하기 전에 권리와 배포 범위를 확인한다. 기술 검증용 로컬 패키지와 공개 배포물을 구분한다.

## 10. 격리 런타임 검증

정적 검증만으로 완료 처리하지 않는다. 게임 전체를 임시 폴더에 복사하고 패키지를 그 복사본에만 적용한다.

1. 사용자 언어 설정과 저장 데이터의 원본 바이트 및 SHA-256을 기록한다.
2. 복사본이 사용할 언어를 대상 CJK 슬롯으로 임시 설정한다.
3. 일반 GUI 모드로 실행하여 메인 메뉴, 저장 데이터 로딩, 튜토리얼 또는 새 게임까지 진입한다.
4. 최소 30초 동안 대상 tk2d 폰트 경로가 실제로 사용되게 한다.
5. 플레이어 로그에서 다음 패턴을 검사한다.

```text
KeyNotFoundException
ArgumentException
IndexOutOfRangeException
NullReferenceException
missing character
could not load
error
```

6. 메뉴와 주요 화면을 캡처하여 한글, 줄바꿈, 기준선, 잘림을 육안 확인한다.
7. 임시 언어 설정을 원래 바이트로 복원하고 해시가 같은지 확인한다.

실제 설치 폴더와 사용자 저장 데이터를 시험 과정에서 변경하지 않는다. 사용자가 설치까지 명시적으로 요청한 경우에만 검증된 패키지를 라이브 폴더에 복사한다.

## 고장 진단

### 패치 후 UI가 멈추거나 아무것도 할 수 없음

다음 순서로 확인한다.

1. `U+0000`, LF, CR, space가 `charDict`에 있는지 확인한다.
2. 빈 폴백 `tk2dFontChar`가 올바른지 확인한다.
3. 키와 값 배열 길이 및 순서가 같은지 확인한다.
4. 정확한 Unity 버전과 로컬 Managed DLL로 타입 트리를 만들었는지 확인한다.
5. 저장 전후 객체 테이블과 변경 Path ID를 비교한다.
6. 플레이어 로그의 첫 번째 예외를 기준으로 진단한다.

### 한글 폰트 패치 후에도 중국어가 표시됨

폰트 문제가 아니라 문자열 선택 문제로 본다.

- 현재 언어 코드가 대상 슬롯인지 확인한다.
- 기본 문자열과 DLC 문자열을 모두 교체했는지 확인한다.
- 실제 로딩 경로와 패키지 경로가 같은지 확인한다.
- 언어 표시 이름이 `한국어`인지 확인한다.
- 캐시 또는 사용자 설정이 이전 언어를 가리키는지 확인한다.

### 네모 글자 또는 일부 한글만 누락됨

- 최종 번역 파일에서 문자 집합을 다시 추출한다.
- NFC 정규화를 확인한다.
- 전체 Noto Sans CJK KR 폰트를 사용했는지 확인한다.
- 아틀라스 패킹 누락과 `.notdef` 마스크를 검사한다.
- 번역에 추가된 한글이 모든 크기 변형의 사전에 들어갔는지 확인한다.

### 글자가 뒤집히거나 엉뚱한 글리프가 표시됨

- Unity Texture2D의 수직 방향과 ARGB 채널 순서를 확인한다.
- `uv0`과 `uv1`의 Y축 계산을 확인한다.
- 키와 값의 인덱스 대응을 확인한다.
- Texture2D 재디코딩 결과와 PNG를 픽셀 비교한다.

### 글자 위치가 높거나 낮고 줄이 겹침

- 각 크기별 기준선을 다시 측정한다.
- `texelSize.x`를 좌표 배율로 사용했는지 확인한다.
- `lineHeight`를 불필요하게 바꾸지 않았는지 확인한다.
- 폰트 라벨의 숫자를 래스터 크기로 그대로 사용하지 않았는지 확인한다.

### 재빌드했는데 변경 객체가 없음

입력이 이미 패치된 자산인지 확인한다. 원본 백업을 입력으로 다시 실행하고 원본 해시를 manifest와 대조한다.

## 최종 보고

사용자에게 다음 정보만 간결하게 전달한다.

- 패키지 경로
- 교체 언어 슬롯
- 번역 레코드 수와 글리프 수
- `resources.assets`와 문자열 파일의 SHA-256
- 정적 검증 및 격리 플레이 검증 결과
- 설치·원복 방법
- 실제 플레이에서 추가 교정이 필요한 UI 문구가 있을 수 있다는 범위
