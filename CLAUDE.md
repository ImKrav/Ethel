# Ethel — Guía del fork

Contexto para asistentes de IA (y para mí mismo) que trabajen en este repositorio.

Documento en español a propósito: es un fork personal. Los identificadores,
rutas, comandos y mensajes de commit siguen siendo en inglés.

---

## Qué es este repositorio

**Ethel** es un fork personal de [Hermes Agent](https://github.com/NousResearch/hermes-agent)
(Nous Research, MIT). El motor es el mismo; lo que cambia es la **identidad**:
nombre, voz, paleta y presentación visual.

- Remoto: `origin` → `https://github.com/ImKrav/Ethel.git`. **No hay remoto
  `upstream` configurado todavía** — hay que añadirlo a mano para sincronizar.
- Uso personal, no distribución. Nada de esto se publica como producto propio.
- La atribución a Nous Research y la licencia MIT **se conservan siempre**
  (`LICENSE`, badges del README, enlaces al repo original).

Ethel se trata **en femenino** en todo texto en español ("Ethel está lista",
"la agente"). En inglés el nombre va solo, sin sufijo tipo "Ethel Agent".

## El objetivo del fork (y su límite)

**El rebrand es de superficie, no estructural.** Esta es la regla que gobierna
cualquier cambio de identidad aquí, y viene de los commits `6ec6cf4` / `15f3a26`
(PR #2):

| Sí se retematiza | No se toca |
|---|---|
| Colores, spinner, ASCII art, strings de branding del skin | Nombres de módulos y archivos (`hermes_cli/`, `hermes_state.py`, …) |
| Banner del CLI/TUI (`hermes_cli/banner.py`) | El comando `hermes` y sus subcomandos |
| Cabecera de `README.md`, título/navbar del sitio, CSS del sitio | `~/.hermes/` como home de estado y config |
| Assets visuales (`assets/banner.png`, favicons, logo) | URLs funcionales (docs upstream, releases, Discord) |
| Copy visible al usuario | Símbolos públicos de Python/TS, esquemas, claves de config |

Motivo: mantener el fork **mergeable con upstream**. Renombrar internals
convierte cada `git merge upstream/main` en un campo de conflictos y rompe
buena parte de los ~17k tests. Si algo tienta a renombrarse por dentro, la
respuesta por defecto es *no*.

## Estado actual del rebrand

Hecho (PR #2):

- **Skin `ethel`** en `hermes_cli/skin_engine.py` (dentro de `_BUILTIN_SKINS`):
  paleta violeta glitchcore, variante `light_colors`, spinner con caras
  `(◈) (▓) (░)` y verbos de estática, `tool_prefix: "▒"`, branding
  (`agent_name: "Ethel"`, `response_label: " ◈ Ethel "`, `prompt_symbol: "◈"`,
  goodbye "Signal lost. ◈"), logo ASCII "ETHEL" y hero halftone.
- **Banner**: `_banner_agent_name()` en `hermes_cli/banner.py` lee
  `branding.agent_name` del skin activo, con fallback a `"Hermes Agent"`.
- **`cli-config.yaml.example`**: `skin: ethel` para instalaciones nuevas.
  Ojo: el fallback en código (`skin_engine.py`) sigue siendo `"default"`;
  el default de Ethel solo aplica vía el archivo de ejemplo.
- **Sitio y README**: título/navbar Docusaurus, `custom.css`, cabecera de
  `README.md`, banner/logo/favicons.

Pendiente / gaps conocidos:

- `website/docs/user-guide/features/skins.md` (y su i18n `zh-Hans`) **no lista
  `ethel`** en la tabla de skins.
- `README.es.md`, `README.zh-CN.md`, `README.ur-pk.md` siguen con la cabecera
  de Hermes. Decisión abierta: retematizarlos o dejarlos como upstream.
- La app de escritorio (`apps/desktop/`) y el dashboard no están retematizados.

## Paleta Ethel

Rampa violeta compartida por ambos modos (claro y oscuro):

```
#F3E8FF  texto claro / fondos light
#E0AAFF  banner_title (dark)
#C77DFF  accent
#9D4EDD  piso de roles de primer plano
#7B2CBF  rellenos / superficies
#5A189A  superficies profundas
#3C096C  fondos de selección
#10002B  status bar / menús (dark)
```

**Regla dura de contraste:** `tests/hermes_cli/test_skin_palettes.py` impone
un piso de contraste contra el polo oscuro (`#101014`): `>= 3.9` para
`status_bar_strong`, `>= 2.8` para el resto de roles de texto/borde. `#7B2CBF`
(2.67) y `#5A189A` (1.84) **no pasan** — por eso `banner_border`, `banner_dim`,
`input_rule`, `status_bar_dim` y `session_border` se subieron a `#9D4EDD`
(4.13) en `15f3a26`. Los tonos profundos quedan reservados para rellenos y
fondos, donde no aplica el piso.

Escalera legible en oscuro que hay que preservar al tocar la paleta:
`text 16.1 > title 10.3 > accent 7.1 > dim/border 4.1`.

Antes de dar por bueno cualquier retoque de color:

```bash
scripts/run_tests.sh tests/hermes_cli/test_skin_palettes.py
```

## Cómo se trabaja aquí

`AGENTS.md` (1784 líneas, de upstream) **sigue siendo la guía de ingeniería
vigente** y manda sobre cualquier cambio funcional. Lo que hay que tener
presente sin falta:

- **El prompt caching por conversación es sagrado**: nada que mute el contexto
  pasado, cambie toolsets o reconstruya el system prompt a mitad de una
  conversación.
- **El core es una cintura estrecha**: cada tool del modelo se envía en cada
  llamada a la API. Capacidad nueva → skill, comando CLI o plugin, no core.
- La sección **"Skin/Theme System"** (`AGENTS.md:685`) documenta el motor de
  skins: son **datos puros**, no hace falta código para añadir uno.

Comandos:

```bash
source .venv/bin/activate                 # o venv/
scripts/run_tests.sh                      # suite completa (aislada por archivo)
scripts/run_tests.sh tests/hermes_cli/    # subconjunto
```

Python 3.11, Node 26.

## Sincronizar con upstream

```bash
git remote add upstream https://github.com/NousResearch/hermes-agent.git
git fetch upstream && git merge upstream/main
```

Los conflictos esperables son pocos y están acotados a los archivos del
rebrand: `hermes_cli/skin_engine.py` (bloque `"ethel"` al final de
`_BUILTIN_SKINS`), `hermes_cli/banner.py`, `cli-config.yaml.example`,
`README.md`, `website/docusaurus.config.ts`, `website/src/css/custom.css` y los
binarios de `assets/` + `website/static/img/`. **En conflicto, la versión de
Ethel gana en identidad y la de upstream gana en lógica.**

## Convenciones

- Commits: prefijos de upstream (`fix(scope):`, `feat(scope):`, `chore:`),
  cuerpo explicando el *porqué*. Los cambios de identidad van en su propio
  commit, separados de cualquier arreglo funcional.
- No mezclar rebrand con lógica en el mismo commit: mantiene los merges
  con upstream limpios y hace obvio qué es "mío" en el historial.
- No romper tests de upstream para acomodar el skin: el skin se ajusta al
  test, no al revés (precedente: `15f3a26`).
