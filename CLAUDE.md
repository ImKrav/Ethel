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
- **Sitio y README**: título/navbar Docusaurus, `custom.css`, cabecera de
  `README.md`, banner/logo/favicons.

Pendiente / gaps conocidos:

- `website/docs/user-guide/features/skins.md` (y su i18n `zh-Hans`) **no lista
  `ethel`** en la tabla de skins.
- `README.es.md`, `README.zh-CN.md`, `README.ur-pk.md` siguen con la cabecera
  de Hermes. Decisión abierta: retematizarlos o dejarlos como upstream.
- El dashboard web (`web/`) no está retematizado.

Hecho después (rebrand del Desktop y del `--help`):

- `hermes --help` dice «Ethel - AI assistant...» (`hermes_cli/_parser.py`). El
  `prog` sigue siendo `hermes` y los ejemplos del epílogo también.
- **Desktop (`apps/desktop/`) — rebrand de pantalla, no de empaquetado.**
  `APP_NAME` en `electron/main.ts`, `<title>` de `index.html`, los cinco
  ficheros de `src/i18n/` (en, ar, ja, zh, zh-hant) y el texto visible de
  `src/` + `electron/`. Las expectativas de test se alinearon con los textos
  nuevos.
- Ojo, contra lo que parece: **el Desktop sí consume el skin del backend.**
  `src/themes/backend-sync.ts` escucha `gateway.ready` / `skin.changed` y
  `src/themes/skin.ts` (`skinToDesktopTheme`) convierte la paleta del CLI en un
  `DesktopTheme`. La paleta morada de Ethel ya llegaba sola; lo único que
  faltaba era el nombre.

### Qué sigue diciendo Hermes en el Desktop, y por qué

No lo «arregles» sin querer — cada uno tiene un motivo:

| Superficie | Motivo |
|---|---|
| `package.json` `build.*` (productName, executableName, appId, artifactName, protocolo `hermes://`, NSIS/DMG) | Decisión explícita: el rebrand es de pantalla. El ejecutable, el instalador y la carpeta de instalación siguen siendo Hermes |
| `Hermes Cloud` | Servicio hospedado de Nous (`makeNousCloudBackendDownError`). Renombrarlo haría que la app mienta sobre en qué cuenta inicias sesión |
| `X-Hermes-Session-Token` | Cabecera HTTP del protocolo con el backend |
| `hermes:` en IPC (`hermes:fs:readDir`, …) | Namespace de canales de Electron, interno |
| `Hermes.app`, `Hermes.exe`, `[\\/]Hermes$` en `desktop-uninstall.ts`, fixtures de ruta en tests | Rutas reales derivadas del productName, que no cambia |
| `/No (?:inference\|Hermes) provider/` en `provider-setup-errors.ts` | Empareja el mensaje de error que emite el backend **Python**, que no está retematizado |
| «portal's Hermes Agent page» | Página del Nous Portal, servicio de terceros |
| `Copyright © 2026 Nous Research` en el panel About | Es un aviso de copyright, no branding. Sustituirlo por uno propio sería reclamar autoría ajena |
| Comentarios y JSDoc | Se dejan a propósito: no son visibles y cambiarlos multiplica los conflictos al mergear con upstream |

Consecuencia asumida: el instalador, el `.exe` y la carpeta de instalación
siguen llamándose Hermes. En la barra de tareas y en Agregar o quitar
programas verás Hermes; dentro de la app, Ethel.

## Ethel es el default, no una opción

Una instalación sin configurar arranca en Ethel en las tres superficies. Esto
diverge de upstream a propósito, así que si un merge lo revierte, es regresión:

| Dónde | Qué |
|---|---|
| `hermes_cli/skin_engine.py` | `DEFAULT_SKIN_NAME = "ethel"` — la fuente de verdad. Ojo: `_BUILTIN_SKINS["default"]` sigue siendo la **base de herencia** en `_build_skin_config` (rellena las claves que un skin omite); eso no se toca |
| `hermes_cli/skin_cmd.py`, `tui_gateway/server.py`, `tui_gateway/methods_config.py` | Resolvían el skin activo por su cuenta con fallback `"default"`; ahora importan `DEFAULT_SKIN_NAME` |
| `hermes_cli/config_defaults.py`, `cli.py` | `"skin": "ethel"` en los diccionarios de config por defecto |
| `apps/desktop/src/themes/presets.ts` | `ethelTheme` en `BUILTIN_THEMES` (primero en la lista) + `DEFAULT_SKIN_NAME = 'ethel'` |
| `apps/desktop/src/themes/context.tsx` | Los `?? nousTheme` de respaldo y el valor por defecto del contexto pasan a `ethelTheme`. **Excepción**: la línea de `typography` sigue en `nousTheme` — es la base tipográfica de toda la app, no identidad |
| `apps/desktop/src/themes/use-skin-command.ts` | Alias `default → ethel` (coherente con `RETIRED_SKINS`). `gold` y `hermes` siguen apuntando a `nous`: nombran el look de upstream, no «el default» |

Como `ethel` es built-in del Desktop, `ingestBackendSkin` **no** lo sobreescribe
con la conversión automática del skin del CLI — gana la paleta hecha a mano.

Test de upstream ajustado a propósito: `presets.test.ts` afirmaba
`DEFAULT_SKIN_NAME === 'nous'`. La divergencia vive en su propio `describe`
(«ethel is this fork default skin») para que el test de upstream siga
reconocible al mergear.

### Cero dorado

Decisión del dueño del fork: **no queda dorado en ningún camino que se renderice.**
Auditado emitiendo el banner real y clasificando cada secuencia ANSI truecolor:
**72 secuencias, 72 violetas, 0 doradas.**

Qué se convirtió, más allá del skin:

- `HERMES_AGENT_LOGO` / `HERMES_CADUCEUS` (`hermes_cli/banner.py`, y las copias
  muertas de `cli.py`) — eran el wordmark «HERMES AGENT» y el caduceo en dorado,
  y salían con cualquier skin que no traiga arte propio (el skin `default` no lo
  trae). Ahora son el wordmark ETHEL y el hero `◈` en la rampa violeta.
- `_GOLD` y `_ACCENT_ANSI_DEFAULT` — ANSI crudo `#FFD700` → `#C77DFF` / `#9D4EDD`.
- `_tui_style_base` en `cli.py` — la barra de estado y los `input-rule` base
  estaban en dorado y bronce sobre `#1a1a2e`; ahora violeta sobre `#10002B`. Los
  tonos semánticos (good/bad/critical/yolo) se quedan: son estado, no marca.
- El panel de «Out of credits» tenía borde bronce cableado.
- Todos los fallbacks `get_color(clave, "#FFD700")` y las ramas `except`.
- `_build_compact_banner` ya no tiene la rama especial que imprimía
  «⚕ NOUS HERMES» para el skin `default`: el producto es Ethel con cualquier
  paleta, así que siempre usa el `agent_name` del skin.

Lo único dorado que queda a propósito:

- `_BUILTIN_SKINS["default"]` en `skin_engine.py` — es el skin «Classic Hermes —
  gold and kawaii». Si lo eliges explícitamente, dorado es lo correcto.
- Las **claves** de `_LIGHT_MODE_REMAP` en `cli.py` — son la entrada de una tabla
  de búsqueda para remapear colores a terminales claros, no marca. Se añadieron
  las entradas de Ethel (`#F3E8FF`, `#E0AAFF`, `#C77DFF`, `#9D4EDD`) para que la
  paleta sea legible sobre fondo crema.
- Comentarios que citan hex dorados al explicar esa tabla.

Test de upstream ajustado: `tests/hermes_cli/test_banner.py` afirmaba
`"Hermes Agent v" in raw`; ahora `"Ethel v"`.

**Brillo y paleta son ejes distintos** (el propio panel lo dice: «Mode is
brightness; theme is palette»). El modo por defecto sigue al sistema, así que en
un Windows en claro Ethel se ve como violeta claro sintetizado, y en oscuro como
el glitchcore de `#10002B`. Si algún día quieres el oscuro siempre, eso es el
default de `mode`, no del tema.

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
