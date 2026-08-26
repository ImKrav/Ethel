"""Preview de un skin sin instalar nada: renderiza logo, hero y paleta.

Uso:  py scripts/preview_skin.py [nombre-del-skin]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from hermes_cli.skin_engine import load_skin  # noqa: E402

RESET = "\033[0m"


def fg(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"\033[38;2;{r};{g};{b}m"


def render(markup: str) -> str:
    """Traduce el markup de rich ([#RRGGBB]...[/]) a ANSI truecolor."""
    out = re.sub(r"\[(?:bold |dim )?(#[0-9A-Fa-f]{6})\]", lambda m: fg(m.group(1)), markup)
    return out.replace("[/]", RESET)


def main() -> int:
    name = sys.argv[1] if len(sys.argv) > 1 else "ethel"
    skin = load_skin(name)

    print()
    print(render(skin.banner_logo or ""))
    print(render(skin.banner_hero or ""))
    print()

    accent = skin.get_color("banner_accent", "#FFFFFF")
    print(f"{fg(accent)}skin{RESET}       {skin.name} — {skin.description}")
    print(f"{fg(accent)}agent_name{RESET} {skin.get_branding('agent_name', '?')}")
    print(f"{fg(accent)}welcome{RESET}    {skin.get_branding('welcome', '?')}")
    print(f"{fg(accent)}prompt{RESET}     "
          f"{fg(skin.get_color('prompt', accent))}{skin.get_branding('prompt_symbol', '>')} {RESET}")
    print(f"{fg(accent)}response{RESET}   "
          f"{fg(skin.get_color('response_border', accent))}{skin.get_branding('response_label', '')}{RESET}")
    print(f"{fg(accent)}goodbye{RESET}    {skin.get_branding('goodbye', '?')}")
    print()

    print(f"{fg(accent)}colores{RESET}")
    for key in sorted(skin.colors):
        value = skin.colors[key]
        if isinstance(value, str) and value.startswith("#"):
            print(f"  {fg(value)}████{RESET} {value}  {key}")
    print()

    spinner = skin.spinner or {}
    faces = " ".join(spinner.get("thinking_faces", []))
    verbs = ", ".join(spinner.get("thinking_verbs", []))
    print(f"{fg(accent)}spinner{RESET}    {faces}")
    print(f"{fg(accent)}verbos{RESET}     {verbs}")
    print(f"{fg(accent)}tool_prefix{RESET} {skin.tool_prefix}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
