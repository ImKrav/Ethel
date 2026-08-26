"""Audita los colores que el CLI emite de verdad, no los que el código declara.

Renderiza el banner de bienvenida real a través de rich y clasifica cada
secuencia ANSI truecolor por tono. Útil sobre todo después de un merge con
upstream, para detectar si volvió a colarse el dorado de Hermes.

Uso:
    python scripts/audit_skin_colors.py            # skin activo según config
    python scripts/audit_skin_colors.py ethel      # forzar un skin
    python scripts/audit_skin_colors.py default    # comprobar el de upstream

Sale con código 1 si encuentra tonos dorados, para poder encadenarlo en CI.
"""
import os
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

os.environ.setdefault("COLUMNS", "100")


def clasifica(r: int, g: int, b: int) -> str:
    """Clasifica un RGB en familias de tono."""
    if r == g == b:
        return "gris/neutro"
    if r > 120 and g > 90 and b < 90 and r >= g:
        return "DORADO/AMARILLO"
    if b > 60 and b >= r and r > g:
        return "violeta"
    return "otro"


def main() -> int:
    from rich.console import Console

    from hermes_cli.banner import build_welcome_banner
    from hermes_cli.skin_engine import get_active_skin, set_active_skin

    if len(sys.argv) > 1:
        set_active_skin(sys.argv[1])
    else:
        import yaml

        from hermes_constants import get_hermes_home
        from hermes_cli.skin_engine import init_skin_from_config

        cfg_path = get_hermes_home() / "config.yaml"
        cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) if cfg_path.exists() else {}
        init_skin_from_config(cfg or {})

    print(f"skin auditado: {get_active_skin().name}")

    console = Console(force_terminal=True, color_system="truecolor", width=100, record=True)
    build_welcome_banner(
        console,
        model="audit/model",
        cwd=str(REPO_ROOT),
        tools=[],
        enabled_toolsets=["core"],
        session_id="audit",
        provider="openrouter",
    )

    raw = console.export_text(styles=True)
    rgbs = re.findall(r"\x1b\[[0-9;]*?[34]8;2;(\d+);(\d+);(\d+)", raw)

    tally: Counter = Counter()
    muestras: dict = {}
    for r, g, b in rgbs:
        r, g, b = int(r), int(g), int(b)
        k = clasifica(r, g, b)
        tally[k] += 1
        muestras.setdefault(k, set()).add(f"#{r:02X}{g:02X}{b:02X}")

    print(f"\nsecuencias de color emitidas: {len(rgbs)}")
    for k, n in tally.most_common():
        print(f"  {k:18} {n:4}  tonos: {', '.join(sorted(muestras[k])[:8])}")

    oro = tally.get("DORADO/AMARILLO", 0)
    print(f"\n=> dorado/amarillo: {oro}")

    return 1 if oro else 0


if __name__ == "__main__":
    raise SystemExit(main())
