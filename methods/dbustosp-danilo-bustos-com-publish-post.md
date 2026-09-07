---
name: publish-post
description: Crea o publica un ensayo en danilobustos.com con el frontmatter, el slug y la categoría correctos. Usar cuando Danilo quiera empezar un post nuevo, migrar uno de LinkedIn, marcar un destacado o pasar un borrador a publicado.
---

# Publicar un ensayo

Tarea mecánica y repetitiva. Sigue estos pasos en orden y no inventes
campos ni prosa. Lee `CLAUDE.md` si no lo has hecho: allí están las reglas
de voz, categorías y divulgación que este flujo asume.

## 1. Reunir los datos

Pregunta (o deduce del contexto) exactamente esto:

- **Título.** Tiene que hacer todo el trabajo: no hay imágenes en el índice.
- **Descripción.** Una o dos frases (≤ 220 caracteres). Es lo que se ve en
  LinkedIn, Google y RSS.
- **Categoría.** `engineering` | `enterprise` | `notes`. Una sola.
- **Idioma.** `en` (por defecto) o `es`. Un ensayo se escribe en un solo
  idioma; no hay traducciones. Si la categoría es `notes`, **pregúntalo
  siempre**: ahí conviven el texto profesional (inglés) y el que va a amigos
  y familia (español), y el defecto acierta solo la mitad de las veces.
- **Fecha.** La de publicación prevista; formato `YYYY-MM-DD`.
- **Destacado.** ¿Va entre los tres o cuatro definitorios? Si sí, revisa
  cuáles están marcados y propón cuál sale.
- **Origen.** Si es una migración desde LinkedIn u otro sitio, la URL del
  original.

## 2. Crear el archivo

```sh
node scripts/new-post.mjs "Título del ensayo" --category notes [--lang es] [--date 2026-10-13] [--featured] [--origin URL]
```

El script deriva el slug (minúsculas, sin acentos, guiones), comprueba que no
esté reservado ni exista, y escribe `src/content/writing/<slug>.md` con el
frontmatter completo y `draft: true`. Si prefieres hacerlo a mano, copia
`src/content/writing/_plantilla.md`.

Reglas del slug que no se negocian: sin fechas, sin categoría, sin acentos,
sin mayúsculas. Un slug publicado no se cambia nunca (la URL es permanente).

## 3. El cuerpo

Claude **no redacta la prosa**. El cuerpo inicial de un borrador son las
preguntas de entrevista, en negrita, una por bloque, pensadas para ese
ensayo y su categoría. Danilo dicta debajo de cada una. Después, Claude
corrige solo la mecánica (ver `CLAUDE.md`, sección 4) y borra las preguntas.

Si el ensayo tiene un flujo o una arquitectura, propón un bloque
```` ```mermaid ```` en vez de describirlo en prosa.

## 4. Comprobar

```sh
npm run dev      # el borrador se ve en http://localhost:4321/writing/<slug>
npm run build    # el build valida el frontmatter y el slug
```

Revisa: título y descripción propios, categoría correcta, `lang` correcto,
guardarraíles de divulgación cumplidos, ningún nombre interno ni cifra no
pública.

## 5. Publicar

1. `draft: false` y la fecha real en `date`.
2. Si es destacado, `featured: true` (y baja el que sale, si toca).
3. `npm run build` en verde.
4. Commit propio para el ensayo, con el título en el mensaje y una línea
   sobre por qué existe (migración, lanzamiento, etc.).
5. Push a la rama de producción: Vercel despliega solo.

Después del despliegue, la imagen para redes está en
`https://danilobustos.com/og/<slug>.png` y la URL canónica en
`https://danilobustos.com/writing/<slug>`. Distribución: LinkedIn primero;
el resto, una semana después.
