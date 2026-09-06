---
name: logo-to-swiftui-draw
description: Transforma a imagem (PNG) de um logo num `Shape` do SwiftUI e num componente que desenha o contorno a traço e depois preenche (splash screen, loading, hero). Use quando o usuário disser "desenhar o logo", "animar o logo", "vetorizar o logo", "logo draw", "trace do logo", "splash com o logo desenhando", ou mandar a imagem de um logo pedindo um componente SwiftUI. Cobre logos geométricos (primitivas + ajuste por IoU) e orgânicos (potrace → SVG → Path).
---

# logo-to-swiftui-draw

## Princípio

Um logo animado a traço só fica bom se o `Path` for **limpo**: poucas primitivas, sem
self-intersection, subpaths na ordem em que uma caneta desenharia. Vetorização automática
(potrace) dá um path fiel, mas cheio de nós; pra logos geométricos vale mais reconstruir
com primitivas e **medir a fidelidade** contra a imagem, em vez de confiar no olho.

O componente de animação é genérico (`LogoDraw<S: Shape>`, em `Sources/LogoDraw/LogoDraw.swift`
deste repositório). O trabalho da skill é produzir o `Shape`.

## Pré-requisitos

- macOS com Xcode (o `swiftc` e o `ImageRenderer` do SwiftUI rodam fora de simulador).
- Python 3 com `numpy`, `pillow`, `scipy`.
- Pro caminho B (orgânico): `brew install potrace`.

Scripts em `scripts/` desta skill. Rode tudo a partir de um diretório de trabalho temporário.

## Workflow

### Etapa 0 — Classificar o logo

Abra a imagem e decida:

- **Geométrico** (traços de largura constante, círculos, cantos arredondados, retas): caminho A.
  Ex.: pictogramas, monogramas, símbolos "flat".
- **Orgânico** (caligrafia, formas livres, larguras variáveis): caminho B.

Se tiver dúvida, comece pelo A e meça: se o IoU não passar de ~0.90 com poucas primitivas,
o logo não é geométrico o bastante.

### Etapa 1 — Medir (os dois caminhos)

```
python3 scripts/measure.py logo.png --mask mask.png
```

Saída: tamanho da imagem, componentes conexos com bounding box. Confira `mask.png`: o
threshold precisa isolar só o glifo (use `--threshold` / `--dark`). Se a imagem tiver
wordmark ou fundo com brilho, anote um `y` abaixo do qual ignorar (`--ignore-below`).

Pra cada componente, tire runs por linha e coluna:

```
python3 scripts/measure.py logo.png --rows 520 720 6
python3 scripts/measure.py logo.png --cols 400 700 12
```

Com os runs você deriva, sem chute: largura do traço (largura horizontal × sin do ângulo),
ângulo das retas (dx/dy entre duas linhas), centros e raios de pontas redondas (ponto
extremo + metade da largura), onde uma reta vira curva (onde a diferença entre linhas muda).

### Etapa 2A — Modelar com primitivas (geométrico)

Copie `scripts/models/runner.py` como ponto de partida. Um modelo é:

- `PARAMS`: dicionário com os números medidos (larguras, centros, ângulos, raios);
- `build(P)`: devolve uma lista de polígonos, **um por subpath**, construídos só com
  `fillet` (= `addArc(tangent1End:tangent2End:radius:)`), `arc` (= `addRelativeArc`) e retas;
- `STEPS` / `VEC_STEPS`: passo de busca de cada parâmetro.

Regras que evitam retrabalho:

- Construa **contornos explícitos**, não `strokedPath`. Contorno explícito dá controle de
  onde o traço começa e evita self-intersection em curvas com raio menor que meia largura.
- Cantos externo e interno de um traço nem sempre são concêntricos em logos desenhados à
  mão ou por IA. Meça os dois raios separadamente (no exemplo: 99 fora, 54 dentro, com
  traço de 70).
- A ordem dos subpaths é a ordem da animação. Comece pela peça maior, termine no detalhe
  (a cabeça do corredor é o "ponto final").

Meça e ajuste:

```
python3 scripts/tune.py logo.png models/meu_logo.py                 # IoU + overlay.png
python3 scripts/tune.py logo.png models/meu_logo.py --tune          # coordinate descent → params.json
```

Leia o `overlay.png`: vermelho é onde o modelo sobra, verde onde falta. Ajuste a
construção (não só os números) até o resíduo ser só borda. Referência: 0.96 no exemplo.

### Etapa 2B — Vetorizar (orgânico)

```
potrace mask.pbm -s -o logo.svg --turdsize 20 --alphamax 1 --opttolerance 0.4
```

(gere o `.pbm` a partir de `mask.png` com o Pillow). Simplifique no Figma/Illustrator se
o path vier com nós demais, e exporte de novo. Converta o `d` do SVG pra `Path` (move/line/
cubic/close). O componente funciona igual; só a fidelidade da animação de traço depende de
o path ter poucos nós e a direção de desenho fazer sentido.

### Etapa 3 — Portar pra Swift

Crie `MeuLogoShape.swift` seguindo `Sources/LogoDraw/RunnerLogoShape.swift`:

- `designSize` = bbox do glifo na imagem; `path(in:)` calcula `scale = min(w/W, h/H)` e centra.
- Função `pt(x, y)` que converte coordenadas da imagem pro `rect`; `len(v)` pra raios.
- Reproduza `build(P)` chamada por chamada: `fillet` → `addArc(tangent1End:tangent2End:radius:)`,
  `arc(c, r, a, a+180)` → `addRelativeArc(center:radius:startAngle:delta:)`, círculo → `addRelativeArc` de 360°.
  Use `addRelativeArc`, nunca `addArc(... clockwise:)`: o sentido de `clockwise` inverte com o
  eixo y pra baixo e é a fonte clássica de arco "pelo lado errado".
- Cole os números finais de `params.json` como constantes comentadas.

### Etapa 4 — Verificar o Shape (obrigatório)

```
scripts/render_shape.sh MeuLogoShape.swift MeuLogoShape render.png \
    --canvas 1254 1254 --frame 418 441 387 370          # canvas = imagem; frame = bbox
python3 scripts/compare.py logo.png render.png            # IoU + overlay
scripts/render_shape.sh MeuLogoShape.swift MeuLogoShape outline.png --mode stroke --canvas 400 400 --frame 50 50 300 300
scripts/render_shape.sh MeuLogoShape.swift MeuLogoShape half.png --mode trim --trim 0.5 --canvas 400 400 --frame 50 50 300 300
```

O IoU do Swift deve bater com o do Python (diferença < 0.01). Se não bater, um arco está
indo pelo lado errado ou um sinal de normal está trocado. Olhe `outline.png` (contorno
limpo, sem laços) e `half.png` (o traço para onde você espera).

### Etapa 5 — Plugar no app

```swift
LogoDraw(MeuLogoShape(), drawDuration: 1.2, fillStartPercent: 70, size: 150,
         outlineColor: .primary, fillColor: .primary, freezeAt: freeze) { splashDone() }
```

- Use `onComplete` pra encadear (fechar splash, mostrar wordmark).
- Exponha `freezeAt` num launch arg (`-splash.freeze 0.45`) pra revisar e tirar screenshot
  de qualquer frame no simulador.
- Reduce Motion já está tratado: aparece completo e `onComplete` dispara na hora.

## Entregáveis

1. `MeuLogoShape.swift` (com comentário de onde vieram os números);
2. `models/meu_logo.py` + `params.json` (pra refazer quando o logo mudar);
3. `overlay.png` com o IoU no chat, como prova de fidelidade;
4. o ponto de uso no app.
