import { describe, expect, it } from 'vitest'

import {
  BUILTIN_THEME_LIST,
  BUILTIN_THEMES,
  DEFAULT_SKIN_NAME,
  DEFAULT_TYPOGRAPHY,
  EMOJI_FALLBACK,
  ethelTheme,
  nousAltTheme
} from './presets'

// #40364: none of the UI text/mono fonts carry emoji glyphs, so every font
// stack must end with a color-emoji fallback or emoji render as tofu on
// platforms whose default font lacks them (e.g. Linux).
describe('theme typography emoji fallback (#40364)', () => {
  const stacks: Array<[string, string]> = [
    ['DEFAULT_TYPOGRAPHY.fontSans', DEFAULT_TYPOGRAPHY.fontSans],
    ['DEFAULT_TYPOGRAPHY.fontMono', DEFAULT_TYPOGRAPHY.fontMono],
    // A theme may override only fontMono (fontSans then falls back to the
    // default, which already carries the emoji stack), so skip undefined.
    ...BUILTIN_THEME_LIST.flatMap(theme =>
      (
        [
          [`${theme.name}.fontSans`, theme.typography?.fontSans],
          [`${theme.name}.fontMono`, theme.typography?.fontMono]
        ] as Array<[string, string | undefined]>
      ).filter((entry): entry is [string, string] => typeof entry[1] === 'string')
    )
  ]

  it.each(stacks)('%s includes a color-emoji font', (_label, stack) => {
    expect(stack).toMatch(/Apple Color Emoji|Segoe UI Emoji|Noto Color Emoji|(^|,\s*)emoji\b/)
  })

  it('EMOJI_FALLBACK lists the major platform emoji fonts', () => {
    expect(EMOJI_FALLBACK).toContain('Apple Color Emoji')
    expect(EMOJI_FALLBACK).toContain('Segoe UI Emoji')
    expect(EMOJI_FALLBACK).toContain('Noto Color Emoji')
  })
})

// The pre-GitHub Nous palette stays available as nous-alt; the `nous` name
// still means GitHub chrome + brand blue.
describe('nous-alt is the retired Nous, distinct from nous', () => {
  it('is registered under its own name and stays distinct from nous', () => {
    expect(BUILTIN_THEMES['nous-alt']).toBe(nousAltTheme)
    expect(BUILTIN_THEMES.nous).not.toBe(nousAltTheme)
    expect(nousAltTheme.darkColors?.background).toBe('#0D2F86')
    expect(BUILTIN_THEMES.nous.darkColors?.background).not.toBe(nousAltTheme.darkColors?.background)
  })
})

// Fork divergence from upstream (which defaults to `nous`): this build opens as
// Ethel with no configuration, so the desktop matches the CLI/TUI skin of the
// same name instead of the user having to pick it in Appearance.
describe('ethel is this fork default skin', () => {
  it('is registered and is what an unconfigured install resolves to', () => {
    expect(DEFAULT_SKIN_NAME).toBe('ethel')
    expect(BUILTIN_THEMES.ethel).toBe(ethelTheme)
  })

  it('is anchored on the same violet ramp as the CLI ethel skin', () => {
    expect(ethelTheme.colors.background).toBe('#10002B')
    expect(ethelTheme.colors.foreground).toBe('#F3E8FF')
    expect(ethelTheme.colors.ring).toBe('#C77DFF')
    expect(ethelTheme.colors.midground).toBe('#C77DFF')
  })
})
