#!/usr/bin/env python3
import base64, os

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

IMG = {
    "amora":       b64(os.path.join(ASSETS, "amora.webp")),
    "tadaly":      b64(os.path.join(ASSETS, "tadaly.webp")),
    "coco-acai":   b64(os.path.join(ASSETS, "coco-acai.webp")),
    "morango":     b64(os.path.join(ASSETS, "morango.webp")),
    "melancia":    b64(os.path.join(ASSETS, "melancia.webp")),
    "maca-verde":  b64(os.path.join(ASSETS, "maca-verde.webp")),
    "tropical":    b64(os.path.join(ASSETS, "tropical.webp")),
    "tradicional": b64(os.path.join(ASSETS, "tradicional.webp")),
}

IMG_ZERO = {
    "zero-tradicional":     b64(os.path.join(ASSETS, "zero-tradicional.webp")),
    "zero-tropical":        b64(os.path.join(ASSETS, "zero-tropical.webp")),
    "zero-morango":         b64(os.path.join(ASSETS, "zero-morango.webp")),
    "zero-melancia":        b64(os.path.join(ASSETS, "zero-melancia.webp")),
    "zero-uvaverde-collab": b64(os.path.join(ASSETS, "zero-uvaverde-collab.webp")),
}

# The "Sem Açúcar" line: same flavours the visitor just met, reformulated without sugar,
# plus one special-edition collab can (printed as-is on the real product).
ZERO_LINE = [
    dict(key="zero-tradicional", name="Tradicional", note=None),
    dict(key="zero-tropical", name="Tropical", note=None),
    dict(key="zero-morango", name="Morango e Pêssego", note=None),
    dict(key="zero-melancia", name="Melancia", note=None),
    dict(key="zero-uvaverde-collab", name="Uva Verde", note="Edição especial · Fernando & Sorocaba"),
]

HERO_BG = "#0E0E10"
FOOTER_BG = "#0B0B0D"

# Order matters: Tradicional opens the sequence (the brand's founding flavour),
# the rest follow in a warm -> cool -> neutral -> green arc, ending on Maçã Verde
# right before the About section. name: giant poster type in the stage (can wrap on \n)
FLAVORS = [
    dict(key="tradicional", name="Tradicional", short="Tradicional",
         bg="#0B0B0C", scheme="light", accent="#E8B923", accent_soft="#8A8680",
         copy="O sabor que começou tudo. Fórmula clássica, direta e sem enrolação — a Baly como ela sempre foi."),
    dict(key="tropical", name="Tropical", short="Tropical",
         bg="#E7A90A", scheme="dark", accent="#7A3B12", accent_soft="#1C1400",
         copy="Um coquetel de frutas tropicais em alta rotação — mistura vibrante que remete às praias e feiras do Brasil."),
    dict(key="morango", name="Morango e\nPêssego", short="Morango e Pêssego",
         bg="#D8432B", scheme="light", accent="#F7D34D", accent_soft="#F5A623",
         copy="Morango maduro e pêssego suculento se misturam num gole quente, frutado e cheio de personalidade."),
    dict(key="melancia", name="Melancia", short="Melancia",
         bg="#C61F2C", scheme="light", accent="#4CB25A", accent_soft="#F2A6AC",
         copy="Melancia gelada em estado puro — refrescância imediata, doçura leve e aquele verão que cabe numa lata."),
    dict(key="amora", name="Amora com\nHortelã", short="Amora com Hortelã",
         bg="#4A1F72", scheme="light", accent="#8FE398", accent_soft="#C6A9E8",
         copy="Amora silvestre encontra hortelã gelada — doce, fresca e com uma pontada mentolada que acorda os sentidos logo no primeiro gole."),
    dict(key="tadaly", name="Tadaly", short="Tadaly",
         bg="#132455", scheme="light", accent="#4FC7EC", accent_soft="#F0C24D",
         copy="A linha noturna da Baly. Notas metálicas, doçura sutil e brilho dourado para quem não desacelera quando o sol se põe."),
    dict(key="coco-acai", name="Coco e\nAçaí", short="Coco e Açaí",
         bg="#EDEAE1", scheme="dark", accent="#2E93C4", accent_soft="#7A6F5D",
         copy="Coco cremoso e açaí amazônico em equilíbrio tropical suave — a energia mais leve da linha, pensada para dias quentes."),
    dict(key="maca-verde", name="Maçã\nVerde", short="Maçã Verde",
         bg="#2E8F30", scheme="light", accent="#EAF7C9", accent_soft="#1F6B22",
         copy="Ácida na medida certa. Maçã verde crocante com final limpo, para quem gosta de energia sem meio-termo."),
]

N = len(FLAVORS)
ABOUT_BG = "#101012"

# ---------- markup builders ----------

def panel_html(f, i):
    name_html = f["name"].replace("\n", "<br>")
    return f"""
      <article class="panel scheme-{f['scheme']}" data-panel="{i}"
        style="background:{f['bg']};--accent:{f['accent']};--accent-soft:{f['accent_soft']};">
        <h2 class="panel__name" aria-hidden="true">{name_html}</h2>
        <div class="panel__stack">
          <img class="panel__can" src="data:image/webp;base64,{IMG[f['key']]}"
            alt="Lata Baly sabor {f['short']}" draggable="false">
        </div>
        <div class="panel__meta">
          <p class="panel__eyebrow">Sabor {i+1:02d} <span aria-hidden="true">/</span> {N:02d}</p>
          <h3 class="panel__title">{f['short']}</h3>
          <p class="panel__desc">{f['copy']}</p>
          <span class="chip">Taurina + Inositol</span>
        </div>
      </article>"""

anchors = "\n".join(
    f'    <span class="stage__anchor" id="{f["key"]}" style="top:{i}00vh;" aria-hidden="true"></span>'
    for i, f in enumerate(FLAVORS)
)

panels = "\n".join(panel_html(f, i) for i, f in enumerate(FLAVORS))

dots = "\n".join(
    f'<a class="dotnav__dot" href="#{f["key"]}" data-dot="{i}" aria-label="Ir para {f["short"]}"><span></span></a>'
    for i, f in enumerate(FLAVORS)
)

def zero_card_html(z, i):
    note_html = f'<span class="zero-card__note">{z["note"]}</span>' if z["note"] else ""
    return f"""
        <figure class="zero-card" data-reveal="card" style="--card-delay:{i}">
          <img class="zero-card__img" src="data:image/webp;base64,{IMG_ZERO[z['key']]}"
            alt="Lata Baly {z['name']} sem açúcar" loading="lazy" draggable="false">
          <figcaption class="zero-card__cap">
            <span class="zero-card__name">{z['name']}</span>
            {note_html}
          </figcaption>
        </figure>"""

zero_cards = "\n".join(zero_card_html(z, i) for i, z in enumerate(ZERO_LINE))

swatches = "\n".join(
    f'      <span class="about__swatch" style="background:{f["bg"]};box-shadow:0 0 0 1px {f["bg"]}, 0 0 0 3px rgba(246,243,236,0.08);" title="{f["short"]}"></span>'
    for f in FLAVORS
)

flavor_js = ",\n".join(
    f'    {{ key:"{f["key"]}", bg:"{f["bg"]}", accent:"{f["accent"]}", accentSoft:"{f["accent_soft"]}", scheme:"{f["scheme"]}" }}'
    for f in FLAVORS
)

HTML = f"""<!doctype html>
<title>Baly Sabores</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/motion@11.18.2/dist/motion.js"></script>
<style>
  :root {{
    --ink: #15161A;
    --paper: #F6F3EC;
    --paper-dim: #C9C4B6;
    --graphite: #0E0E10;
    --graphite-soft: #201F24;
    --line: rgba(246,243,236,0.14);
    --gold: #E8B923;
    --font-display: "Anton", "Arial Narrow", sans-serif;
    --font-body: "Manrope", "Segoe UI", sans-serif;
    --font-mono: "JetBrains Mono", "SFMono-Regular", monospace;
    color-scheme: dark;
  }}

  * {{ box-sizing: border-box; }}
  html {{ scroll-behavior: smooth; }}
  @media (prefers-reduced-motion: reduce) {{ html {{ scroll-behavior: auto; }} }}

  body {{
    margin: 0;
    background: {HERO_BG};
    color: var(--paper);
    font-family: var(--font-body);
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
  }}

  h1, h2, h3 {{ text-wrap: balance; }}
  p {{ text-wrap: pretty; }}
  img {{ max-width: 100%; }}
  a {{ color: inherit; }}

  /* ---------- top disclosure ribbon ---------- */
  .ribbon {{
    position: fixed; top: 0; left: 0; right: 0; z-index: 60;
    display: flex; align-items: center; justify-content: center; gap: 0.5em;
    height: 30px; background: var(--graphite); border-bottom: 1px solid var(--line);
    font-family: var(--font-mono); font-size: 0.66rem; letter-spacing: 0.08em;
    text-transform: uppercase; color: var(--gold); text-align: center; padding: 0 1rem;
    white-space: nowrap; overflow: hidden;
  }}
  .ribbon strong {{ color: var(--paper); font-weight: 600; }}
  .ribbon__long {{ display: inline; }}
  .ribbon__short {{ display: none; }}
  @media (max-width: 640px) {{
    .ribbon {{ font-size: 0.6rem; padding: 0 0.75rem; }}
    .ribbon__long {{ display: none; }}
    .ribbon__short {{ display: inline; }}
  }}

  /* ---------- header ---------- */
  .site-header {{
    position: fixed; top: 30px; left: 0; right: 0; z-index: 50;
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.1rem clamp(1.25rem, 4vw, 3rem); pointer-events: none;
  }}
  .wordmark {{
    font-family: var(--font-display); font-size: 1.3rem; letter-spacing: 0.01em;
    color: var(--paper); pointer-events: auto;
    background: rgba(14,14,16,0.32);
    -webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);
    border-radius: 999px;
    padding: 0.4rem 0.9rem 0.3rem;
    display: inline-block;
  }}

  /* ---------- side dot nav ---------- */
  .dotnav {{
    position: fixed; right: clamp(0.9rem, 2.4vw, 2rem); top: 50%; transform: translateY(-50%);
    z-index: 55; display: flex; flex-direction: column; gap: 0.85rem;
  }}
  .dotnav__dot {{ width: 22px; height: 22px; display: grid; place-items: center; text-decoration: none; }}
  .dotnav__dot span {{
    width: 7px; height: 7px; border-radius: 50%; background: rgba(246,243,236,0.35); display: block;
    transition: transform 0.3s ease, background 0.3s ease, box-shadow 0.3s ease;
  }}
  .dotnav__dot.is-active span {{
    background: var(--dot-color, var(--gold)); transform: scale(1.7);
    box-shadow: 0 0 0 4px color-mix(in srgb, var(--dot-color, var(--gold)) 25%, transparent);
  }}
  @media (max-width: 720px) {{ .dotnav {{ display: none; }} }}

  /* ---------- floating CTA (the only action button on the page) ---------- */
  .cta-float {{
    position: fixed; right: clamp(1rem, 3vw, 2.25rem); bottom: clamp(1rem, 3vw, 2.25rem); z-index: 65;
    display: inline-flex; align-items: center; gap: 0.55rem; padding: 0.85rem 1.4rem; border-radius: 999px;
    background: var(--cta-bg, var(--gold)); color: var(--cta-fg, #17181B);
    font-family: var(--font-body); font-weight: 700; font-size: 0.86rem; letter-spacing: 0.01em;
    text-decoration: none; box-shadow: 0 10px 30px -8px rgba(0,0,0,0.55), 0 0 0 1px rgba(255,255,255,0.08) inset;
    transition: background 0.35s ease, color 0.35s ease, transform 0.2s ease;
  }}
  .cta-float:hover {{ transform: translateY(-2px); }}
  .cta-float:active {{ transform: translateY(0); }}
  .cta-float__arrow {{ display: inline-grid; place-items: center; width: 20px; height: 20px; border-radius: 50%; background: rgba(0,0,0,0.12); font-size: 0.72rem; }}
  @media (max-width: 640px) {{
    .cta-float {{ padding: 0.65rem 1.05rem; font-size: 0.76rem; gap: 0.4rem; }}
    .cta-float__arrow {{ width: 16px; height: 16px; font-size: 0.62rem; }}
  }}

  /* ---------- hero ---------- */
  .hero {{
    position: relative; min-height: 92vh; display: flex; flex-direction: column;
    justify-content: center; align-items: center; text-align: center; padding: 7rem 1.5rem 5rem;
    background: radial-gradient(60% 55% at 50% 28%, rgba(232,185,35,0.14), transparent 70%), var(--graphite);
    overflow: hidden;
  }}
  .hero__eyebrow {{ font-family: var(--font-mono); font-size: 0.78rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--gold); margin: 0 0 1.4rem; }}
  .hero__title {{ font-family: var(--font-display); font-size: clamp(3.4rem, 11vw, 8.5rem); line-height: 0.86; margin: 0; color: var(--paper); }}
  .hero__title em {{ font-style: normal; color: var(--gold); }}
  .hero__sub {{ max-width: 34rem; margin: 1.6rem auto 0; font-size: clamp(1rem, 1.6vw, 1.2rem); line-height: 1.55; color: var(--paper-dim); }}
  .hero__glow {{
    position: absolute; top: 50%; left: 50%; width: min(70vw, 620px); height: min(70vw, 620px);
    transform: translate(-50%, -50%); border-radius: 50%; pointer-events: none;
    background: radial-gradient(closest-side, rgba(232,185,35,0.16), transparent 72%);
    animation: heroPulse 6s ease-in-out infinite;
  }}
  @keyframes heroPulse {{ 0%, 100% {{ opacity: 0.7; transform: translate(-50%, -50%) scale(0.94); }} 50% {{ opacity: 1; transform: translate(-50%, -50%) scale(1.04); }} }}
  @media (prefers-reduced-motion: reduce) {{ .hero__glow {{ animation: none; }} }}
  .hero__scroll {{
    position: absolute; bottom: 2rem; left: 50%; transform: translateX(-50%);
    font-family: var(--font-mono); font-size: 0.68rem; letter-spacing: 0.14em; text-transform: uppercase;
    color: var(--paper-dim); display: flex; flex-direction: column; align-items: center; gap: 0.5rem;
  }}
  .hero__scroll-line {{ width: 1px; height: 34px; background: linear-gradient(to bottom, var(--gold), transparent); }}

  /* ---------- flavor stage: pinned crossfade ---------- */
  .stage-wrap {{
    position: relative;
    height: calc({N} * 100vh);
  }}
  .stage__anchor {{ position: absolute; left: 0; width: 1px; height: 1px; }}
  .stage-sticky {{
    position: sticky; top: 0; height: 100vh; overflow: hidden;
    isolation: isolate;
  }}
  .panel {{
    position: absolute; inset: 0;
    display: flex; align-items: center; justify-content: center;
    opacity: 0;
    will-change: opacity, filter;
  }}
  .panel__grain {{ position: absolute; inset: 0; opacity: 0.05; mix-blend-mode: overlay; pointer-events: none; }}
  .panel__name {{
    position: absolute; inset: 0; margin: 0;
    display: flex; align-items: center; justify-content: center; text-align: center;
    font-family: var(--font-display); font-weight: 400;
    font-size: clamp(3.4rem, 15vw, 12rem); line-height: 0.82; letter-spacing: -0.01em;
    padding: 0 4vw;
    pointer-events: none; user-select: none;
  }}
  .scheme-light .panel__name {{ color: rgba(246,243,236,0.9); }}
  .scheme-dark  .panel__name {{ color: rgba(21,22,26,0.85); }}
  .panel__stack {{ position: relative; z-index: 2; display: grid; place-items: center; }}
  .panel__can {{
    height: clamp(230px, 30vw, 420px); width: auto;
    filter: drop-shadow(0 30px 46px rgba(0,0,0,0.45));
  }}
  .panel__meta {{
    position: absolute; z-index: 3;
    left: clamp(1.25rem, 6vw, 4.5rem); bottom: clamp(1.75rem, 7vh, 4rem);
    max-width: 24rem; text-align: left;
  }}
  .panel__eyebrow {{ font-family: var(--font-mono); font-size: 0.74rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--accent); margin: 0 0 0.6rem; }}
  .panel__title {{ font-family: var(--font-display); font-weight: 400; font-size: clamp(1.5rem, 2.6vw, 2.1rem); margin: 0 0 0.6rem; }}
  .panel__desc {{ font-size: 0.95rem; line-height: 1.55; margin: 0 0 1.1rem; max-width: 30ch; }}
  .scheme-light .panel__title, .scheme-light .panel__desc {{ color: var(--paper); }}
  .scheme-dark  .panel__title, .scheme-dark  .panel__desc {{ color: var(--ink); }}
  .scheme-light .panel__desc {{ color: rgba(246,243,236,0.82); }}
  .scheme-dark  .panel__desc {{ color: rgba(21,22,26,0.75); }}

  .chip {{
    display: inline-flex; align-items: center; gap: 0.4em; font-family: var(--font-mono);
    font-size: 0.66rem; letter-spacing: 0.08em; text-transform: uppercase; padding: 0.5em 0.85em;
    border-radius: 999px; border: 1px solid currentColor;
  }}
  .scheme-light .chip {{ color: rgba(246,243,236,0.7); }}
  .scheme-dark  .chip {{ color: rgba(21,22,26,0.58); }}

  .stage__progress {{
    position: absolute; left: 0; right: 0; bottom: 0; z-index: 4;
    height: 2px; background: rgba(255,255,255,0.16);
  }}
  .stage__progress-bar {{ height: 100%; width: 0%; background: var(--gold); transition: background 0.35s ease; }}

  @media (max-width: 720px) {{
    .panel__name {{ font-size: clamp(2.6rem, 17vw, 6rem); padding: 0 6vw; }}
    .panel__can {{ height: clamp(190px, 46vw, 300px); }}
    .panel__meta {{ left: 1.25rem; right: 1.25rem; bottom: 5rem; max-width: none; text-align: center; }}
    .panel__desc {{ max-width: 34ch; margin-left: auto; margin-right: auto; }}
  }}

  /* ---------- about: closing section, deliberately quieter than the stage ---------- */
  .about {{
    position: relative;
    min-height: 92vh;
    display: flex; align-items: center; justify-content: center;
    text-align: center; padding: clamp(4rem, 12vh, 7rem) 1.5rem;
    background: {ABOUT_BG};
    overflow: hidden;
  }}
  .about::before {{
    content: ""; position: absolute; top: 0; left: 0; right: 0; height: 22vh;
    background: linear-gradient(to bottom, {FLAVORS[-1]['bg']}, {ABOUT_BG});
  }}
  .about::after {{
    content: ""; position: absolute; inset: 0;
    background: radial-gradient(52% 46% at 50% 42%, rgba(232,185,35,0.08), transparent 72%);
    pointer-events: none;
  }}
  .about__inner {{ position: relative; z-index: 1; max-width: 38rem; }}
  .about__eyebrow {{
    font-family: var(--font-mono); font-size: 0.76rem; letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--gold); margin: 0 0 1.1rem;
  }}
  .about__headline {{
    font-family: var(--font-display); font-weight: 400; margin: 0 0 1.4rem;
    font-size: clamp(1.9rem, 4.4vw, 3.1rem); line-height: 1.04; color: var(--paper);
  }}
  .about__text {{
    margin: 0 auto; max-width: 42ch; font-size: clamp(1rem, 1.4vw, 1.12rem);
    line-height: 1.65; color: var(--paper-dim);
  }}
  .about__swatches {{
    display: flex; align-items: center; justify-content: center; gap: 0.6rem;
    margin: 2.4rem 0 0;
  }}
  .about__swatch {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; }}

  [data-reveal] {{ opacity: 1; }}
  .js-ready [data-reveal] {{ opacity: 0; }}

  /* ---------- zero: the Baly Zero line, revealed as a card drop ---------- */
  .zero {{
    position: relative; background: {ABOUT_BG};
    padding: 4rem clamp(1.5rem, 6vw, 5rem) 5rem; text-align: center;
  }}
  .zero__divider {{
    width: 64px; height: 3px; margin: 0 auto 2.75rem; border-radius: 999px;
    background: var(--gold);
  }}
  .zero__eyebrow {{
    font-family: var(--font-mono); font-size: 0.76rem; letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--gold); margin: 0 0 1rem;
  }}
  .zero__headline {{
    font-family: var(--font-display); font-weight: 400; margin: 0 0 0.9rem;
    font-size: clamp(2rem, 5vw, 3.4rem); line-height: 1.02; color: var(--paper);
  }}
  .zero__sub {{
    max-width: 40ch; margin: 0 auto 3rem; font-size: clamp(1rem, 1.4vw, 1.12rem);
    line-height: 1.6; color: var(--paper-dim);
  }}
  .zero__grid {{
    display: flex; flex-wrap: wrap; align-items: flex-start; justify-content: center;
    gap: clamp(1rem, 2.4vw, 1.75rem); max-width: 76rem; margin: 0 auto;
  }}
  .zero-card {{
    margin: 0; width: clamp(148px, 17vw, 208px);
    display: flex; flex-direction: column; align-items: center; gap: 0.85rem;
  }}
  .zero-card__img {{
    width: 100%; height: auto; display: block;
    filter: drop-shadow(0 18px 26px rgba(0,0,0,0.5));
  }}
  .zero-card__cap {{ display: flex; flex-direction: column; gap: 0.25rem; }}
  .zero-card__name {{ font-family: var(--font-body); font-weight: 700; font-size: 0.92rem; color: var(--paper); }}
  .zero-card__note {{ font-family: var(--font-mono); font-size: 0.66rem; letter-spacing: 0.03em; color: var(--gold); }}

  @media (max-width: 720px) {{
    .zero__grid {{
      flex-wrap: nowrap; overflow-x: auto; justify-content: flex-start;
      padding: 0.5rem 1.25rem 1rem; margin: 0 -1.25rem;
      scroll-snap-type: x mandatory; -webkit-overflow-scrolling: touch;
    }}
    .zero-card {{ flex: 0 0 auto; width: 46vw; scroll-snap-align: center; }}
  }}

  /* ---------- footer ---------- */
  .site-footer {{ position: relative; background: {FOOTER_BG}; padding: 5rem clamp(1.5rem, 6vw, 5rem) 3rem; text-align: center; }}
  @media (max-width: 640px) {{ .site-footer {{ padding-bottom: 6rem; }} }}
  .footer__mark {{ font-family: var(--font-display); font-size: clamp(2.2rem, 6vw, 3.6rem); color: var(--paper); margin: 0 0 1rem; }}
  .footer__note {{ max-width: 34rem; margin: 0 auto 2rem; font-size: 0.92rem; line-height: 1.65; color: var(--paper-dim); }}
  .footer__note a {{ color: var(--gold); text-decoration: underline; text-underline-offset: 3px; }}
  .footer__meta {{
    display: flex; flex-wrap: wrap; justify-content: center; gap: 0.5rem 1.4rem;
    font-family: var(--font-mono); font-size: 0.68rem; letter-spacing: 0.06em; text-transform: uppercase;
    color: rgba(246,243,236,0.4); padding-top: 2rem; border-top: 1px solid var(--line);
  }}
</style>

<div class="ribbon">
  <span class="ribbon__long"><strong>Projeto de Portfólio / Conceitual</strong> — sem vínculo oficial com a Baly Brasil</span>
  <span class="ribbon__short"><strong>Portfólio / Conceitual</strong> — não oficial</span>
</div>

<header class="site-header">
  <span class="wordmark">BALY</span>
</header>

<nav class="dotnav" aria-label="Navegação de sabores">
{dots}
</nav>

<a class="cta-float" id="ctaFloat" href="https://balybrasil.com.br/" target="_blank" rel="noopener noreferrer">
  Site oficial da Baly <span class="cta-float__arrow">↗</span>
</a>

<main>
  <section class="hero">
    <div class="hero__glow" aria-hidden="true"></div>
    <p class="hero__eyebrow">Taurina + Inositol · Energy Drink</p>
    <h1 class="hero__title">8 sabores.<br><em>Uma energia.</em></h1>
    <p class="hero__sub">Role a página para descobrir, um de cada vez, os 8 sabores da Baly — começando pelo Tradicional.</p>
    <div class="hero__scroll">
      <span>Role para explorar</span>
      <span class="hero__scroll-line"></span>
    </div>
  </section>

  <noscript>
    <style>
      .stage-wrap {{ height: auto !important; }}
      .stage-sticky {{ position: static !important; height: auto !important; }}
      .panel {{ position: relative !important; opacity: 1 !important; min-height: 100vh; filter: none !important; }}
      .cta-float {{ position: static !important; margin: 2rem auto; }}
    </style>
  </noscript>

  <div class="stage-wrap" id="stageWrap">
{anchors}
    <div class="stage-sticky">
{panels}
      <div class="stage__progress"><div class="stage__progress-bar" id="stageProgressBar"></div></div>
    </div>
  </div>

  <section class="about">
    <div class="about__inner">
      <p class="about__eyebrow" data-reveal>A Baly</p>
      <h2 class="about__headline" data-reveal>Sabores que são<br>a cara do Brasil.</h2>
      <p class="about__text" data-reveal>
        Da lata clássica em preto e dourado às combinações mais tropicais, a Baly nasceu para
        democratizar o energético no Brasil — um sabor pra cada rolê, sempre com taurina e inositol na fórmula.
      </p>
      <div class="about__swatches" data-reveal aria-hidden="true">
{swatches}
      </div>
    </div>
  </section>

  <section class="zero">
    <div class="zero__divider" data-reveal aria-hidden="true"></div>
    <p class="zero__eyebrow" data-reveal>Baly Zero</p>
    <h2 class="zero__headline" data-reveal>Muito sabor.<br>Energia do Brasil.<br>Zero açúcar.</h2>
    <p class="zero__sub" data-reveal>
      A linha Baly Zero equilibra performance, estilo de vida e o sabor Baly de sempre —
      incluindo uma edição especial em parceria com Fernando &amp; Sorocaba.
    </p>
    <div class="zero__grid">
{zero_cards}
    </div>
  </section>

  <footer class="site-footer">
    <p class="footer__mark">BALY</p>
    <p class="footer__note">
      Este site é um <strong>projeto de portfólio / conceitual</strong>, criado apenas para demonstrar design e desenvolvimento web.
      Não possui qualquer vínculo oficial com a Baly Brasil. Para produtos, sabores e informações oficiais, visite
      <a href="https://balybrasil.com.br/" target="_blank" rel="noopener noreferrer">balybrasil.com.br</a>.
    </p>
    <div class="footer__meta">
      <span>Projeto de Portfólio</span>
      <span>Não Oficial</span>
      <span>{N} Sabores</span>
    </div>
  </footer>
</main>

<script>
(function () {{
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasMotion = !!(window.Motion && window.Motion.scroll && window.Motion.animate);

  var FLAVORS = [
{flavor_js}
  ];
  var N = FLAVORS.length;

  var ctaEl = document.getElementById('ctaFloat');
  var dots = Array.prototype.slice.call(document.querySelectorAll('.dotnav__dot'));
  var bar = document.getElementById('stageProgressBar');
  var panels = Array.prototype.slice.call(document.querySelectorAll('.panel'));
  var wrap = document.getElementById('stageWrap');

  function hex2rgb(hex) {{
    var h = hex.replace('#', '');
    return [parseInt(h.substring(0,2),16), parseInt(h.substring(2,4),16), parseInt(h.substring(4,6),16)];
  }}
  function lerp(a, b, t) {{ return a + (b - a) * t; }}
  function mixColor(c1, c2, t) {{
    var a = hex2rgb(c1), b = hex2rgb(c2);
    return 'rgb(' + Math.round(lerp(a[0], b[0], t)) + ',' + Math.round(lerp(a[1], b[1], t)) + ',' + Math.round(lerp(a[2], b[2], t)) + ')';
  }}

  function applyChrome(indexF) {{
    var idx = Math.max(0, Math.min(N - 1, Math.round(indexF)));
    var f = FLAVORS[idx];
    dots.forEach(function (d, i) {{
      d.classList.toggle('is-active', i === idx);
      d.style.setProperty('--dot-color', f.accent);
    }});
    var nextIdx = Math.max(0, Math.min(N - 1, idx + (indexF - idx >= 0 ? 1 : -1)));
    var t = Math.abs(indexF - idx);
    var accentNow = t > 0.02 ? mixColor(f.accent, FLAVORS[nextIdx].accent, Math.min(t, 1)) : f.accent;
    if (ctaEl) {{
      ctaEl.style.setProperty('--cta-bg', accentNow);
      ctaEl.style.setProperty('--cta-fg', f.scheme === 'dark' ? '#F6F3EC' : '#17181B');
    }}
    if (bar) bar.style.background = f.accent;
  }}

  function resetChrome() {{
    dots.forEach(function (d) {{ d.classList.remove('is-active'); }});
    if (ctaEl) {{ ctaEl.style.setProperty('--cta-bg', '#E8B923'); ctaEl.style.setProperty('--cta-fg', '#17181B'); }}
  }}

  // Hero / footer edge reset (independent of the stage math).
  if ('IntersectionObserver' in window) {{
    var heroEl = document.querySelector('.hero');
    var footerEl = document.querySelector('.site-footer');
    var edgeIO = new IntersectionObserver(function (entries) {{
      entries.forEach(function (entry) {{ if (entry.isIntersecting) resetChrome(); }});
    }}, {{ threshold: 0.6 }});
    if (heroEl) edgeIO.observe(heroEl);
    if (footerEl) edgeIO.observe(footerEl);
  }}

  function layoutPanels(indexF) {{
    if (bar) bar.style.width = (Math.min(1, Math.max(0, indexF / (N - 1))) * 100) + '%';
    panels.forEach(function (panel, i) {{
      var local = indexF - i; // negative: still upcoming, 0: fully active, positive: past (covered by later panels)
      var band = reduceMotion ? 0.001 : 0.62;
      var reveal = Math.min(1, Math.max(0, (local + band) / band)); // 0 -> 1 as local goes from -band to 0, then holds at 1
      panel.style.opacity = String(reveal);
      if (!reduceMotion) {{
        var blur = (1 - reveal) * 10;
        var scale = 0.96 + reveal * 0.04;
        panel.style.filter = blur > 0.15 ? 'blur(' + blur.toFixed(2) + 'px)' : 'none';
        panel.style.transform = 'scale(' + scale.toFixed(3) + ')';
      }}
      panel.style.zIndex = String(i);
    }});
  }}

  layoutPanels(0);
  applyChrome(0);

  if (!hasMotion || !wrap) {{
    // Fallback without Motion: keep panels statically revealed via a plain scroll listener.
    var ticking = false;
    function computeIndexFallback() {{
      var rect = wrap.getBoundingClientRect();
      var total = wrap.offsetHeight - window.innerHeight;
      var scrolled = -rect.top;
      var p = total > 0 ? Math.min(1, Math.max(0, scrolled / total)) : 0;
      return p * (N - 1);
    }}
    function onScroll() {{
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {{
        var idxF = computeIndexFallback();
        layoutPanels(idxF);
        applyChrome(idxF);
        ticking = false;
      }});
    }}
    window.addEventListener('scroll', onScroll, {{ passive: true }});
    onScroll();
    return;
  }}

  window.Motion.scroll(function (progress) {{
    var indexF = progress * (N - 1);
    layoutPanels(indexF);
    applyChrome(indexF);
  }}, {{ target: wrap, offset: ['start start', 'end end'] }});

  // About / zero sections: reveal-once as each scrolls into view (same inView pattern
  // throughout) — the "card" variant just gets a livelier drop-in for the product grid.
  document.documentElement.classList.add('js-ready');
  document.querySelectorAll('[data-reveal]').forEach(function (el, i) {{
    var kind = el.getAttribute('data-reveal');
    window.Motion.inView(el, function () {{
      if (kind === 'card') {{
        var delay = parseInt(el.style.getPropertyValue('--card-delay') || '0', 10) * 0.08;
        window.Motion.animate(el, {{ opacity: [0, 1], y: [30, 0], scale: [0.88, 1] }},
          {{ duration: 0.6, delay: delay, easing: [0.16, 1, 0.3, 1] }});
      }} else {{
        window.Motion.animate(el, {{ opacity: [0, 1], y: [22, 0] }}, {{ duration: 0.7, delay: (i % 5) * 0.07, easing: [0.16, 1, 0.3, 1] }});
      }}
    }}, {{ amount: 0.4 }});
  }});
}})();
</script>
"""

with open(os.path.join(ROOT, "baly-landing.html"), "w", encoding="utf-8") as f:
    f.write(HTML)

print("wrote", os.path.join(ROOT, "baly-landing.html"), len(HTML), "chars")
