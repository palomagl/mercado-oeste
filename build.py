#!/usr/bin/env python3
"""
Mercado Oeste — experiência conceitual.

Reaproveita o motor de scroll da base (palco fixo + painéis que fazem crossfade
via Motion.scroll -> layoutPanels), trocando totalmente o conteudo: cada produto
do mercado ganha seu proprio "momento visual" (cor de embalagem, palavra gigante,
imagem protagonista), e depois vem a parte funcional (catálogo + carrinho + entrega).

Gera um unico index.html, com as imagens reais dos assets embutidas em base64.
"""
import base64, math, os

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")


def b64(name):
    with open(os.path.join(ASSETS, name), "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


# A logo do Mercado Oeste (assets/logomercadooeste.png.jpeg) e um JPEG chapado
# sobre branco puro — nao recorta limpo pra um hero escuro. Em vez de um card
# branco, o lockup e remontado com a MESMA estrutura da marca (carrinho + wordmark
# em dois tons de verde), nitido em qualquer fundo. A identidade nao muda.
CART_SVG = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"'
    ' stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M2.4 3.4h2.5l2.3 11.5a1.7 1.7 0 0 0 1.67 1.35h8.9a1.7 1.7 0 0 0 1.66-1.3L22 7.4H5.2"/>'
    '<circle cx="9.6" cy="20" r="1.5"/><circle cx="17.6" cy="20" r="1.5"/></svg>'
)
LOCKUP = (
    f'<span class="lockup__mark">{CART_SVG}</span>'
    '<span class="lockup__word">Mercado <span>Oeste</span></span>'
)

# ---------------------------------------------------------------------------
# Os 7 momentos do palco, NA ORDEM do scroll:
#   arroz -> feijao -> acucar -> cafe -> oleo -> leite -> hortifruti
# bg = atmosfera da cena (cor predominante da embalagem); scheme "light" =
# tipografia clara sobre fundo escuro, "dark" = o inverso. entry = tempero da
# animacao de entrada. img = PNG ja com fundo transparente (so o fundo externo
# foi removido; branco/letras/reflexos da embalagem ficam intactos).
# ---------------------------------------------------------------------------
PRODUCTS = [
    dict(
        key="arroz", img=b64("arroz-namorado-5kg-cut.png"),
        word="ARROZ", title="Arroz Namorado 5kg",
        desc="Aquele básico que não pode faltar.",
        price="R$ 28,90", bg="#123C72", scheme="light",
        accent="#F2C14E", entry="slide",
    ),
    dict(
        key="feijao", img=b64("feijao-camil-1kg-cut.png"),
        word="FEIJÃO", title="Camil Carioca 1kg",
        desc="Para completar a mesa.",
        price="R$ 8,49", bg="#1A1620", scheme="light",
        accent="#D8402F", entry="rise",
    ),
    dict(
        key="acucar", img=b64("acucar5kg-caravelas-cut.png"),
        word="AÇÚCAR", title="Açúcar Cristal Caravelas 5kg",
        desc="A doçura de sempre pra adoçar o dia inteiro.",
        price="R$ 19,90", bg="#ECE4D6", scheme="dark",
        accent="#C4262E", entry="rise",
    ),
    dict(
        key="cafe", img=b64("vidrodecafe100g-nescafe-cut.png"),
        word="CAFÉ", title="Nescafé 100g",
        desc="Comece bem o seu dia.",
        price="R$ 14,90", bg="#241310", scheme="light",
        accent="#E0392E", entry="finale",
    ),
    dict(
        key="oleo", img=b64("oleodesoja900ml-leve-cut.png"),
        word="ÓLEO", title="Óleo de Soja Liza 900ml",
        desc="Um essencial da cozinha.",
        price="R$ 7,49", bg="#E2A61A", scheme="dark",
        accent="#5A3A12", entry="spin",
    ),
    dict(
        key="leite", img=b64("leite1l-ninho-cut.png"),
        word="LEITE", title="Leite Ninho 1L",
        desc="Para começar bem o dia.",
        price="R$ 6,99", bg="#EFC24C", scheme="dark",
        accent="#6B4A1E", entry="rise",
    ),
    dict(
        key="fruteira", img=b64("fruteira-cut.png"),
        word="FRESCO.\nTODO DIA.", title="Hortifrúti selecionado",
        desc="Variedade para deixar sua rotina mais leve.",
        price=None, bg="#1E7A38", scheme="light",
        accent="#F6D24B", entry="open",
    ),
]

N = len(PRODUCTS)
LAST_BG = PRODUCTS[-1]["bg"]

# ---------------------------------------------------------------------------
# Catálogo da seção "Meus Produtos" — parte funcional, FORA da experiência de
# scroll. São os 6 produtos vendáveis das cenas (a fruteira fica só no palco)
# MAIS os produtos que existem apenas no catálogo. Nenhum destes novos entra
# na sequência cinematográfica nem ganha cena própria. preço demonstrativo.
# ---------------------------------------------------------------------------
SHOP = [
    dict(key="acucar", name="Açúcar Cristal Caravelas 5kg", price=19.90),
    dict(key="arroz",  name="Arroz Namorado 5kg",           price=28.90),
    dict(key="feijao", name="Feijão Camil 1kg",             price=8.49),
    dict(key="leite",  name="Leite Ninho 1L",               price=6.99),
    dict(key="oleo",   name="Óleo de Soja Liza 900ml",      price=7.49),
    dict(key="cafe",   name="Nescafé 100g",                 price=14.90),
]

# produtos que só aparecem no catálogo (carregam a própria imagem)
EXTRA = [
    dict(key="massa_parafuso", img=b64("macarraoparafuso500gGalo.png"),
         name="Massa Parafuso Galo 500g", price=4.49),
    dict(key="massa_espaguete", img=b64("macarraoespaguete500gRenata.png"),
         name="Massa Espaguete Renata 500g", price=4.29),
    dict(key="ovos", img=b64("bandeijaovosbrancos20unidades.png"),
         name="Ovos Brancos 20 unidades", price=17.90),
    dict(key="coca", img=b64("cocacola2l.png"),
         name="Coca-Cola 2L", price=9.90),
    dict(key="agua", img=b64("aguasemgas5lcrystal.png"),
         name="Água Crystal sem Gás 5L", price=6.90),
    dict(key="detergente", img=b64("detergenteype500ml.png"),
         name="Detergente Ypê 500ml", price=2.79),
    dict(key="papel", img=b64("papelhigienico4rolos.png"),
         name="Papel Higiênico 4 rolos", price=6.49),
    dict(key="sabao", img=b64("sabaoempobrilhante1,6kg.png"),
         name="Sabão em Pó Brilhante 1,6kg", price=12.90),
]

CATALOG = SHOP + EXTRA
DELIVERY_FEE = 5.00


def brl(v):
    return ("R$ " + f"{v:,.2f}").replace(",", "@").replace(".", ",").replace("@", ".")


# Cada blob de imagem entra UMA vez, como custom property, e e reaproveitado
# no palco, nos cards do catalogo e no anel final (evita repetir base64).
img_vars = "\n".join(
    f'    --img-{p["key"]}: url("data:image/png;base64,{p["img"]}");'
    for p in PRODUCTS + EXTRA
)


# ---------- construtores de markup ----------

def panel_html(p, i):
    word = p["word"].replace("\n", "<br>")
    if p["price"] is None:
        action = '<span class="panel__chip">Hortifrúti fresco</span>'
    else:
        action = (
            f'<p class="panel__price">{p["price"]}</p>'
            f'<button class="panel__buy" type="button" data-add="{p["key"]}">'
            f'Quero comprar <span aria-hidden="true">→</span></button>'
        )
    return f"""
      <article class="panel scheme-{p['scheme']}" data-panel="{i}" data-entry="{p['entry']}"
        style="background:{p['bg']};--accent:{p['accent']};">
        <h2 class="panel__word" aria-hidden="true">{word}</h2>
        <div class="panel__stage">
          <div class="panel__img" role="img" aria-label="{p['title']}"
            style="background-image:var(--img-{p['key']})"></div>
        </div>
        <div class="panel__meta">
          <p class="panel__eyebrow">Produto {i+1:02d} <span aria-hidden="true">/</span> {N:02d}</p>
          <h3 class="panel__title">{p['title']}</h3>
          <p class="panel__desc">{p['desc']}</p>
          {action}
        </div>
      </article>"""


anchors = "\n".join(
    f'    <span class="stage__anchor" id="p-{p["key"]}" style="top:{i}00vh;" aria-hidden="true"></span>'
    for i, p in enumerate(PRODUCTS)
)
panels = "\n".join(panel_html(p, i) for i, p in enumerate(PRODUCTS))
dots = "\n".join(
    f'  <a class="dotnav__dot" href="#p-{p["key"]}" data-dot="{i}" aria-label="Ir para {p["title"]}"><span></span></a>'
    for i, p in enumerate(PRODUCTS)
)

# anel de produtos ao redor da logo, na grande transição final.
# offset de meio passo -> nenhum produto cai exatamente em cima do texto central.
finale_thumbs = []
for i, p in enumerate(PRODUCTS):
    a = -math.pi / 2 + math.pi / N + i * 2 * math.pi / N
    x = 50 + 40 * math.cos(a)
    y = 50 + 40 * math.sin(a)
    finale_thumbs.append(
        f'      <span class="finale__thumb" data-reveal="orbit" aria-hidden="true"'
        f' style="left:{x:.2f}%;top:{y:.2f}%;--d:{i};background-image:var(--img-{p["key"]})"></span>'
    )
finale_thumbs = "\n".join(finale_thumbs)


def shop_card_html(s, i):
    return f"""
        <figure class="card" data-reveal="card" style="--card-delay:{i};">
          <div class="card__media" role="img" aria-label="{s['name']}"
            style="background-image:var(--img-{s['key']})"></div>
          <figcaption class="card__body">
            <span class="card__name">{s['name']}</span>
            <span class="card__price">{brl(s['price'])}</span>
          </figcaption>
          <button class="card__add" type="button" data-add="{s['key']}">+ Adicionar</button>
        </figure>"""


shop_cards = "\n".join(shop_card_html(s, i) for i, s in enumerate(CATALOG))

product_js = ",\n".join(
    f'    {{ key:"{p["key"]}", bg:"{p["bg"]}", accent:"{p["accent"]}", scheme:"{p["scheme"]}" }}'
    for p in PRODUCTS
)
prices_js = ", ".join(f'{s["key"]}:{s["price"]:.2f}' for s in CATALOG)
names_js = ", ".join(f'{s["key"]}:"{s["name"]}"' for s in CATALOG)

# ---------------------------------------------------------------------------
CSS = r"""
  :root {
    --ink: #14170F;
    --paper: #F5F2E8;
    --paper-dim: #B7BCA8;
    --graphite: #0C0D0A;
    --graphite-soft: #16180F;
    --line: rgba(245,242,232,0.14);
    --green: #1FA24C;
    --green-bright: #37C766;
    --green-deep: #0B5228;
    --font-display: "Anton", "Arial Narrow", sans-serif;
    --font-body: "Manrope", "Segoe UI", sans-serif;
    --font-mono: "JetBrains Mono", "SFMono-Regular", monospace;
    color-scheme: dark;
__IMG_VARS__
  }

  * { box-sizing: border-box; }
  html { scroll-behavior: smooth; }
  @media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }

  body {
    margin: 0;
    background: var(--graphite);
    color: var(--paper);
    font-family: var(--font-body);
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
  }

  h1, h2, h3 { text-wrap: balance; }
  p { text-wrap: pretty; }
  img { max-width: 100%; }
  a { color: inherit; }
  ::selection { background: var(--green); color: #fff; }

  /* ---------- ribbon ---------- */
  .ribbon {
    position: fixed; top: 0; left: 0; right: 0; z-index: 60;
    display: flex; align-items: center; justify-content: center; gap: 0.5em;
    height: 30px; background: var(--green-deep); border-bottom: 1px solid var(--line);
    font-family: var(--font-mono); font-size: 0.66rem; letter-spacing: 0.08em;
    text-transform: uppercase; color: var(--paper); text-align: center; padding: 0 1rem;
    white-space: nowrap; overflow: hidden;
  }
  .ribbon strong { color: #fff; font-weight: 600; }
  .ribbon__short { display: none; }
  @media (max-width: 640px) {
    .ribbon { font-size: 0.6rem; padding: 0 0.75rem; }
    .ribbon__long { display: none; }
    .ribbon__short { display: inline; }
  }

  /* ---------- header ---------- */
  .site-header {
    position: fixed; top: 30px; left: 0; right: 0; z-index: 50;
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem clamp(1.25rem, 4vw, 3rem); pointer-events: none;
  }
  .wordmark {
    pointer-events: auto; text-decoration: none; font-size: 1rem;
    background: rgba(12,13,10,0.42); -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px);
    border-radius: 999px; padding: 0.5rem 1rem 0.45rem;
  }

  /* ---------- lockup da marca (carrinho + wordmark) ---------- */
  .lockup {
    display: inline-flex; align-items: center; gap: 0.5em;
    font-family: var(--font-display); font-weight: 400; line-height: 1;
    text-transform: uppercase; letter-spacing: 0.045em; white-space: nowrap;
  }
  .lockup__mark { display: inline-flex; color: var(--green-bright); }
  .lockup__mark svg { width: 1.3em; height: 1.3em; display: block; }
  .lockup__word { color: var(--paper); }
  .lockup__word span { color: var(--green-bright); }

  /* ---------- side dot nav ---------- */
  .dotnav {
    position: fixed; right: clamp(0.9rem, 2.4vw, 2rem); top: 50%; transform: translateY(-50%);
    z-index: 55; display: flex; flex-direction: column; gap: 0.85rem;
  }
  .dotnav__dot { width: 22px; height: 22px; display: grid; place-items: center; text-decoration: none; }
  .dotnav__dot span {
    width: 7px; height: 7px; border-radius: 50%; background: rgba(245,242,232,0.32); display: block;
    transition: transform 0.3s ease, background 0.3s ease, box-shadow 0.3s ease;
  }
  .dotnav__dot.is-active span {
    background: var(--green-bright); transform: scale(1.7);
    box-shadow: 0 0 0 4px rgba(55,199,102,0.22);
  }
  @media (max-width: 720px) { .dotnav { display: none; } }

  /* ---------- cart FAB ---------- */
  .cart-fab {
    position: fixed; right: clamp(1rem, 3vw, 2.25rem); bottom: clamp(1rem, 3vw, 2.25rem); z-index: 65;
    display: inline-flex; align-items: center; gap: 0.55rem; padding: 0.85rem 1.35rem; border: 0; border-radius: 999px;
    background: var(--green); color: #fff; cursor: pointer;
    font-family: var(--font-body); font-weight: 700; font-size: 0.86rem; letter-spacing: 0.01em;
    box-shadow: 0 12px 30px -10px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.08) inset;
    transition: transform 0.2s ease, background 0.3s ease;
  }
  .cart-fab:hover { transform: translateY(-2px); background: var(--green-bright); }
  .cart-fab:active { transform: translateY(0); }
  .cart-fab.is-bump { animation: fabBump 0.45s ease; }
  @keyframes fabBump { 0%,100% { transform: scale(1); } 40% { transform: scale(1.09); } }
  .cart-fab__count {
    min-width: 20px; height: 20px; padding: 0 0.35rem; border-radius: 999px;
    background: #fff; color: var(--green-deep); font-size: 0.72rem; font-weight: 800;
    display: inline-grid; place-items: center;
  }
  .cart-fab__count[hidden] { display: none; }
  @media (max-width: 640px) { .cart-fab { padding: 0.7rem 1.05rem; font-size: 0.78rem; } }
  @media (prefers-reduced-motion: reduce) { .cart-fab.is-bump { animation: none; } }

  /* ---------- hero: abertura cinematografica ---------- */
  .hero {
    position: relative; min-height: 100vh; overflow: hidden; isolation: isolate;
    display: flex; align-items: center;
    padding: clamp(6rem, 14vh, 9rem) clamp(1.5rem, 8vw, 7rem) clamp(8rem, 20vh, 12rem);
    background: linear-gradient(180deg, #06120A 0%, #0A130C 46%, var(--graphite) 100%);
  }
  /* profundidade: dois focos de luz verde em planos diferentes + vinheta */
  .hero__bg { position: absolute; inset: 0; z-index: -2; pointer-events: none; }
  .hero__glow { position: absolute; border-radius: 50%; will-change: transform; }
  .hero__glow--far {
    top: -22%; right: -14%; width: min(74vw, 840px); aspect-ratio: 1;
    background: radial-gradient(closest-side, rgba(31,162,76,0.38), transparent 70%);
    animation: heroGlow 17s ease-in-out infinite;
  }
  .hero__glow--near {
    bottom: -28%; left: -18%; width: min(56vw, 620px); aspect-ratio: 1;
    background: radial-gradient(closest-side, rgba(55,199,102,0.18), transparent 66%);
    animation: heroGlow 23s ease-in-out infinite reverse;
  }
  @keyframes heroGlow {
    0%, 100% { transform: translate3d(0,0,0) scale(1); opacity: 0.82; }
    50% { transform: translate3d(1.5%, 2.5%, 0) scale(1.09); opacity: 1; }
  }
  @media (prefers-reduced-motion: reduce) { .hero__glow { animation: none; } }
  .hero::after {
    content: ""; position: absolute; inset: 0; z-index: -1; pointer-events: none;
    background: radial-gradient(135% 92% at 50% 22%, transparent 36%, rgba(0,0,0,0.52) 100%);
  }
  /* rodape do hero: um calor que sobe do fundo, "prepara" a chegada da 1a cena
     (acucar, creme) — mesmo principio de crossfade de cor do resto da experiencia */
  .hero__fade {
    position: absolute; left: 0; right: 0; bottom: 0; height: 26vh; z-index: -1; pointer-events: none;
    background:
      radial-gradient(60% 100% at 50% 100%, rgba(236,228,214,0.16), transparent 72%),
      linear-gradient(to bottom, transparent, rgba(236,228,214,0.10));
  }
  .hero__inner { position: relative; z-index: 1; max-width: 64rem; }
  .hero__eyebrow {
    font-family: var(--font-mono); font-size: 0.8rem; letter-spacing: 0.24em; text-transform: uppercase;
    color: var(--green-bright); margin: 0 0 1.1rem;
    display: inline-flex; align-items: center; gap: 0.7rem;
  }
  .hero__eyebrow::before { content: ""; width: 32px; height: 1px; background: currentColor; }
  /* MERCADO OESTE grande, protagonista — o lockup da marca virando titulo */
  .hero__brand {
    font-size: clamp(2.1rem, 9vw, 6rem); gap: 0.42em; margin: 0 0 1.5rem;
    align-items: center; flex-wrap: wrap; letter-spacing: 0.02em;
    text-shadow: 0 18px 50px rgba(0,0,0,0.6), 0 0 40px rgba(55,199,102,0.12);
  }
  .hero__brand .lockup__mark { color: var(--green-bright); }
  .hero__brand .lockup__mark svg { width: 1.15em; height: 1.15em; }
  /* dois tons de verde da identidade: MERCADO mais claro, OESTE mais saturado */
  .hero__brand .lockup__word { color: #6FD98F; white-space: normal; }
  .hero__brand .lockup__word span { color: var(--green-bright); }
  .hero__tagline {
    font-family: var(--font-display); font-weight: 400; margin: 0 0 1.4rem;
    font-size: clamp(1.4rem, 3.6vw, 2.6rem); line-height: 1.04; letter-spacing: 0.005em;
    text-transform: uppercase; color: var(--paper);
  }
  .hero__tagline em { font-style: normal; color: var(--green-bright); }
  .hero__sub {
    max-width: 34rem; margin: 0; font-size: clamp(0.98rem, 1.35vw, 1.12rem);
    line-height: 1.6; color: var(--paper-dim);
  }
  .hero__cue {
    position: absolute; left: 50%; bottom: clamp(1.75rem, 5vh, 3rem); transform: translateX(-50%); z-index: 2;
    display: flex; flex-direction: column; align-items: center; gap: 0.65rem;
    font-family: var(--font-mono); font-size: 0.64rem; letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--paper-dim);
  }
  .hero__cue-line {
    position: relative; width: 1px; height: 44px; overflow: hidden;
    background: rgba(245,242,232,0.14);
  }
  .hero__cue-line::after {
    content: ""; position: absolute; inset: 0;
    background: linear-gradient(to bottom, var(--green-bright), transparent);
    animation: cueDrop 2s ease-in-out infinite;
  }
  @keyframes cueDrop { 0% { transform: translateY(-100%); } 55%, 100% { transform: translateY(100%); } }
  @media (prefers-reduced-motion: reduce) { .hero__cue-line::after { animation: none; transform: none; } }
  @media (max-width: 860px) {
    .hero { padding: 7rem 1.5rem 8.5rem; }
    .hero__brand { font-size: clamp(2rem, 12vw, 3.6rem); }
    .hero__tagline { font-size: clamp(1.25rem, 5vw, 1.9rem); }
    .hero__glow--far { top: -8%; right: -34%; }
    .hero__glow--near { bottom: -34%; left: -34%; }
  }

  /* ---------- palco: crossfade fixo ---------- */
  .stage-wrap { position: relative; height: calc(__N__ * 100vh); }
  .stage__anchor { position: absolute; left: 0; width: 1px; height: 1px; }
  .stage-sticky { position: sticky; top: 0; height: 100vh; overflow: hidden; isolation: isolate; }
  .panel {
    position: absolute; inset: 0;
    display: flex; align-items: center; justify-content: center;
    opacity: 0; will-change: opacity, filter, transform;
  }
  .panel__word {
    position: absolute; inset: 0; margin: 0;
    display: flex; align-items: center; justify-content: center; text-align: center;
    font-family: var(--font-display); font-weight: 400;
    font-size: clamp(3.2rem, 15vw, 12rem); line-height: 0.82; letter-spacing: -0.01em;
    text-transform: uppercase; padding: 0 4vw;
    pointer-events: none; user-select: none; will-change: transform;
  }
  .scheme-light .panel__word { color: rgba(245,242,232,0.92); }
  .scheme-dark  .panel__word { color: rgba(20,23,15,0.82); }
  .panel__stage { position: relative; z-index: 2; display: grid; place-items: center; }
  .panel__img {
    height: clamp(240px, 34vw, 440px); width: min(80vw, 460px);
    background-repeat: no-repeat; background-position: center bottom; background-size: contain;
  }
  .panel__meta {
    position: absolute; z-index: 3;
    left: clamp(1.25rem, 6vw, 4.5rem); bottom: clamp(1.75rem, 7vh, 4rem);
    max-width: 24rem; text-align: left;
  }
  .panel__eyebrow { font-family: var(--font-mono); font-size: 0.74rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--accent); margin: 0 0 0.6rem; }
  .panel__title { font-family: var(--font-display); font-weight: 400; font-size: clamp(1.55rem, 2.8vw, 2.2rem); margin: 0 0 0.55rem; text-transform: uppercase; letter-spacing: 0.01em; }
  .panel__desc { font-size: 0.98rem; line-height: 1.55; margin: 0 0 1rem; max-width: 32ch; }
  .scheme-light .panel__title { color: var(--paper); }
  .scheme-dark  .panel__title { color: var(--ink); }
  .scheme-light .panel__desc { color: rgba(245,242,232,0.82); }
  .scheme-dark  .panel__desc { color: rgba(20,23,15,0.74); }
  .panel__price {
    font-family: var(--font-display); font-weight: 400; letter-spacing: 0.02em;
    font-size: clamp(1.7rem, 3.4vw, 2.6rem); margin: 0 0 0.9rem; color: var(--accent);
  }
  .panel__buy {
    display: inline-flex; align-items: center; gap: 0.5rem; border: 0; cursor: pointer;
    padding: 0.8rem 1.4rem; border-radius: 999px; background: var(--green); color: #fff;
    font-family: var(--font-body); font-weight: 700; font-size: 0.86rem; letter-spacing: 0.02em;
    box-shadow: 0 12px 28px -12px rgba(0,0,0,0.55);
    transition: transform 0.2s ease, background 0.3s ease;
  }
  .panel__buy:hover { transform: translateY(-2px); background: var(--green-bright); }
  .panel__buy:active { transform: translateY(0); }
  .panel__chip {
    display: inline-flex; align-items: center; gap: 0.4em; font-family: var(--font-mono);
    font-size: 0.68rem; letter-spacing: 0.08em; text-transform: uppercase; padding: 0.55em 0.95em;
    border-radius: 999px; border: 1px solid currentColor; color: rgba(245,242,232,0.78);
  }
  .stage__progress { position: absolute; left: 0; right: 0; bottom: 0; z-index: 4; height: 2px; background: rgba(255,255,255,0.14); }
  .stage__progress-bar { height: 100%; width: 0%; background: var(--green-bright); }

  @media (max-width: 720px) {
    .panel__word { font-size: clamp(2.6rem, 17vw, 6rem); padding: 0 6vw; }
    .panel__img { height: clamp(200px, 48vw, 320px); }
    .panel__meta { left: 1.25rem; right: 1.25rem; bottom: 4.5rem; max-width: none; text-align: center; }
    .panel__desc { max-width: 34ch; margin-left: auto; margin-right: auto; }
    .panel__buy { justify-content: center; }
  }

  /* ---------- grande transição final ---------- */
  /* altura garantida pra caber o anel de produtos inteiro (sem corte):
     raio do anel ~40% de 620px + folga dos thumbs + respiro vertical */
  .finale {
    position: relative; min-height: max(100vh, 45rem);
    display: flex; align-items: center; justify-content: center;
    text-align: center; padding: clamp(5rem, 13vh, 7.5rem) 1.5rem;
    background: var(--graphite); overflow: hidden;
  }
  .finale::before {
    content: ""; position: absolute; top: 0; left: 0; right: 0; height: 24vh;
    background: linear-gradient(to bottom, __LASTBG__, var(--graphite));
  }
  .finale::after {
    content: ""; position: absolute; inset: 0; pointer-events: none;
    background: radial-gradient(52% 48% at 50% 50%, rgba(31,162,76,0.16), transparent 72%);
  }
  /* elipse (mais larga que alta): espalha os produtos pros lados, longe do texto,
     e encurta a extensao vertical pra nunca cortar em tela baixa */
  .finale__orbit {
    position: absolute; z-index: 1; top: 50%; left: 50%;
    transform: translate(-50%, calc(-50% + 26px));
    width: min(96vw, 860px); height: min(82vw, 690px); pointer-events: none;
  }
  .finale__thumb {
    position: absolute; width: clamp(38px, 6vw, 58px); height: clamp(38px, 6vw, 58px);
    transform: translate(-50%, -50%);
    background-repeat: no-repeat; background-position: center; background-size: contain;
    opacity: 0.8; /* so recua os produtos distantes; nao altera a imagem */
    animation: orbitFloat 6s ease-in-out infinite;
    animation-delay: calc(var(--d) * -0.8s);
  }
  @keyframes orbitFloat { 0%,100% { margin-top: -5px; } 50% { margin-top: 5px; } }
  @media (prefers-reduced-motion: reduce) { .finale__thumb { animation: none; } }
  .finale__core { position: relative; z-index: 2; max-width: 22rem; padding: 0 1rem; }
  .finale__lockup { font-size: clamp(1.35rem, 3.2vw, 2.1rem); margin-bottom: clamp(1.4rem, 4vh, 2rem); }
  .finale__headline {
    font-family: var(--font-display); font-weight: 400; margin: 0 0 1.6rem;
    font-size: clamp(1.9rem, 5vw, 3.2rem); line-height: 1.02; color: var(--paper);
    text-transform: uppercase; letter-spacing: 0.01em;
    text-shadow: 0 2px 24px rgba(12,13,10,0.75), 0 0 8px rgba(12,13,10,0.6);
  }
  .finale__headline em { font-style: normal; color: var(--green-bright); display: block; }
  .finale__cta {
    display: inline-flex; align-items: center; gap: 0.55rem;
    padding: 0.9rem 1.7rem; border-radius: 999px; text-decoration: none;
    background: transparent; color: var(--paper); border: 1px solid rgba(245,242,232,0.3);
    font-weight: 700; font-size: 0.88rem; letter-spacing: 0.02em;
    transition: border-color 0.3s ease, background 0.3s ease, transform 0.2s ease;
  }
  .finale__cta:hover { border-color: var(--green-bright); background: rgba(55,199,102,0.12); transform: translateY(-2px); }
  @media (max-width: 720px) {
    /* encolhe um pouco o anel pra folgar nas laterais do celular */
    .finale__orbit { transform: translate(-50%, calc(-50% + 16px)) scale(0.84); }
    .finale__headline { font-size: clamp(1.7rem, 7vw, 2.3rem); }
  }

  /* ---------- meus produtos (catálogo) ---------- */
  .shop { position: relative; background: var(--graphite); padding: 5rem clamp(1.5rem, 6vw, 5rem) 5rem; }
  .shop__head { max-width: 60rem; margin: 0 auto 3rem; text-align: center; }
  .shop__eyebrow { font-family: var(--font-mono); font-size: 0.76rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--green-bright); margin: 0 0 0.9rem; }
  .shop__title {
    font-family: var(--font-display); font-weight: 400; margin: 0 0 0.8rem;
    font-size: clamp(2rem, 5vw, 3.2rem); line-height: 1.02; color: var(--paper);
    text-transform: uppercase; letter-spacing: 0.01em;
  }
  .shop__sub { max-width: 44ch; margin: 0 auto; font-size: 1rem; line-height: 1.6; color: var(--paper-dim); }
  .shop__grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: clamp(1rem, 2vw, 1.6rem); max-width: 76rem; margin: 0 auto;
  }
  .card {
    margin: 0; display: flex; flex-direction: column;
    background: var(--graphite-soft); border: 1px solid var(--line); border-radius: 16px;
    padding: 1.1rem; transition: border-color 0.3s ease, transform 0.3s ease;
  }
  .card:hover { border-color: rgba(55,199,102,0.4); transform: translateY(-3px); }
  .card__media {
    height: 170px; margin-bottom: 1rem; border-radius: 10px;
    background-repeat: no-repeat; background-position: center; background-size: contain;
  }
  .card__body { display: flex; flex-direction: column; gap: 0.3rem; margin-bottom: 1rem; flex: 1; }
  .card__name { font-weight: 700; font-size: 0.94rem; color: var(--paper); }
  .card__price { font-family: var(--font-mono); font-size: 0.9rem; color: var(--green-bright); }
  .card__add {
    border: 0; cursor: pointer; padding: 0.7rem 1rem; border-radius: 10px;
    background: rgba(55,199,102,0.12); color: var(--green-bright);
    font-family: var(--font-body); font-weight: 700; font-size: 0.82rem; letter-spacing: 0.02em;
    transition: background 0.25s ease, color 0.25s ease;
  }
  .card__add:hover { background: var(--green); color: #fff; }

  /* ---------- entrega ---------- */
  .delivery {
    position: relative; background: linear-gradient(180deg, var(--graphite) 0%, #0A1A0F 100%);
    padding: 5rem clamp(1.5rem, 6vw, 5rem) 6rem; text-align: center; overflow: hidden;
  }
  .delivery__headline {
    font-family: var(--font-display); font-weight: 400; margin: 0 0 2.4rem;
    font-size: clamp(2.4rem, 8vw, 5.4rem); line-height: 0.98; color: var(--paper);
    text-transform: uppercase; letter-spacing: 0.01em;
  }
  .delivery__headline em { font-style: normal; color: var(--green-bright); display: block; }
  .delivery__grid {
    display: flex; flex-wrap: wrap; align-items: stretch; justify-content: center;
    gap: 1rem; max-width: 54rem; margin: 0 auto 2.8rem;
  }
  .delivery__item {
    flex: 1 1 200px; max-width: 260px; padding: 1.6rem 1.2rem; border-radius: 14px;
    background: rgba(245,242,232,0.04); border: 1px solid var(--line);
    display: flex; flex-direction: column; gap: 0.5rem; align-items: center;
  }
  .delivery__emoji { font-size: 1.7rem; }
  .delivery__label { font-weight: 700; font-size: 0.96rem; color: var(--paper); }
  .delivery__hint { font-family: var(--font-mono); font-size: 0.72rem; letter-spacing: 0.04em; color: var(--paper-dim); }
  .delivery__cta {
    display: inline-flex; align-items: center; gap: 0.55rem; border: 0; cursor: pointer;
    padding: 1rem 2rem; border-radius: 999px; background: var(--green); color: #fff;
    font-family: var(--font-body); font-weight: 800; font-size: 0.92rem; letter-spacing: 0.03em;
    text-transform: uppercase; box-shadow: 0 16px 36px -14px rgba(31,162,76,0.6);
    transition: transform 0.2s ease, background 0.3s ease;
  }
  .delivery__cta:hover { transform: translateY(-2px); background: var(--green-bright); }

  /* ---------- footer ---------- */
  .site-footer { position: relative; background: #070806; padding: 4.5rem clamp(1.5rem, 6vw, 5rem) 3rem; text-align: center; }
  @media (max-width: 640px) { .site-footer { padding-bottom: 6rem; } }
  .footer__mark { font-family: var(--font-display); font-size: clamp(2rem, 6vw, 3.4rem); color: var(--paper); margin: 0 0 1rem; text-transform: uppercase; letter-spacing: 0.04em; }
  .footer__mark em { font-style: normal; color: var(--green-bright); }
  .footer__note { max-width: 36rem; margin: 0 auto 2rem; font-size: 0.9rem; line-height: 1.65; color: var(--paper-dim); }
  .footer__meta {
    display: flex; flex-wrap: wrap; justify-content: center; gap: 0.5rem 1.4rem;
    font-family: var(--font-mono); font-size: 0.68rem; letter-spacing: 0.06em; text-transform: uppercase;
    color: rgba(245,242,232,0.4); padding-top: 2rem; border-top: 1px solid var(--line);
  }

  /* ---------- carrinho (drawer) ---------- */
  .cart { position: fixed; inset: 0; z-index: 90; visibility: hidden; }
  .cart.is-open { visibility: visible; }
  .cart__scrim {
    position: absolute; inset: 0; background: rgba(6,8,5,0.55);
    opacity: 0; transition: opacity 0.3s ease;
  }
  .cart.is-open .cart__scrim { opacity: 1; }
  .cart__panel {
    position: absolute; top: 0; right: 0; height: 100%; width: min(92vw, 400px);
    background: var(--graphite-soft); border-left: 1px solid var(--line);
    display: flex; flex-direction: column; padding: 1.4rem;
    transform: translateX(100%); transition: transform 0.35s cubic-bezier(0.16,1,0.3,1);
    overflow-y: auto;
  }
  .cart.is-open .cart__panel { transform: translateX(0); }
  @media (prefers-reduced-motion: reduce) {
    .cart__panel, .cart__scrim { transition: none; }
  }
  .cart__head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.2rem; }
  .cart__head h2 { font-family: var(--font-display); font-weight: 400; font-size: 1.4rem; margin: 0; text-transform: uppercase; letter-spacing: 0.02em; }
  .cart__close { border: 0; background: transparent; color: var(--paper-dim); font-size: 1.1rem; cursor: pointer; padding: 0.3rem; }
  .cart__close:hover { color: var(--paper); }
  .cart__empty { color: var(--paper-dim); font-size: 0.9rem; text-align: center; padding: 2rem 0; }
  .cart__items { display: flex; flex-direction: column; gap: 0.9rem; margin-bottom: 1.2rem; }
  .cart-line { display: grid; grid-template-columns: 44px 1fr auto; gap: 0.7rem; align-items: center; }
  .cart-line__img { width: 44px; height: 44px; background-repeat: no-repeat; background-position: center; background-size: contain; }
  .cart-line__name { font-size: 0.84rem; font-weight: 600; color: var(--paper); }
  .cart-line__unit { font-family: var(--font-mono); font-size: 0.72rem; color: var(--paper-dim); }
  .cart-line__qty { display: inline-flex; align-items: center; gap: 0.4rem; }
  .cart-line__qty button {
    width: 22px; height: 22px; border-radius: 6px; border: 1px solid var(--line);
    background: transparent; color: var(--paper); cursor: pointer; font-size: 0.8rem; line-height: 1;
  }
  .cart-line__qty button:hover { border-color: var(--green-bright); color: var(--green-bright); }
  .cart-line__qty span { font-family: var(--font-mono); font-size: 0.8rem; min-width: 1ch; text-align: center; }
  .cart__summary { border-top: 1px solid var(--line); padding-top: 1rem; margin-top: auto; display: flex; flex-direction: column; gap: 0.5rem; }
  .cart__row { display: flex; justify-content: space-between; font-size: 0.86rem; color: var(--paper-dim); }
  .cart__row span:last-child { font-family: var(--font-mono); color: var(--paper); }
  .cart__row--total { font-size: 1rem; color: var(--paper); font-weight: 700; padding-top: 0.5rem; border-top: 1px dashed var(--line); }
  .cart__row--total span:last-child { color: var(--green-bright); }
  .cart__cta {
    margin-top: 1.1rem; border: 0; cursor: pointer; padding: 0.95rem 1rem; border-radius: 12px;
    background: var(--green); color: #fff; font-family: var(--font-body); font-weight: 800;
    font-size: 0.9rem; letter-spacing: 0.03em; text-transform: uppercase;
    transition: background 0.3s ease;
  }
  .cart__cta:hover { background: var(--green-bright); }
  .cart__cta:disabled { opacity: 0.45; cursor: not-allowed; }
  .cart__confirm { margin: 0.9rem 0 0; font-size: 0.82rem; line-height: 1.5; color: var(--green-bright); text-align: center; }
  .cart__fine { margin: 0.9rem 0 0; font-family: var(--font-mono); font-size: 0.66rem; letter-spacing: 0.03em; color: rgba(245,242,232,0.4); text-align: center; }

  /* ---------- toast ---------- */
  .toast {
    position: fixed; left: 50%; bottom: clamp(5rem, 12vh, 7rem); transform: translateX(-50%) translateY(20px);
    z-index: 80; background: var(--paper); color: var(--ink);
    padding: 0.7rem 1.2rem; border-radius: 999px; font-size: 0.82rem; font-weight: 700;
    box-shadow: 0 16px 40px -12px rgba(0,0,0,0.5);
    opacity: 0; pointer-events: none; transition: opacity 0.3s ease, transform 0.3s ease;
  }
  .toast.is-show { opacity: 1; transform: translateX(-50%) translateY(0); }

  /* progressive reveal */
  [data-reveal] { opacity: 1; }
  .js-ready [data-reveal] { opacity: 0; }

  /* ---------- fallback sem JS ---------- */
  .no-js .stage-wrap { height: auto; }
  .no-js .stage-sticky { position: static; height: auto; }
  .no-js .panel { position: relative; opacity: 1; min-height: 100vh; filter: none; }
  .no-js [data-reveal] { opacity: 1; }
"""

CSS = (CSS.replace("__N__", str(N))
          .replace("__LASTBG__", LAST_BG)
          .replace("__IMG_VARS__", img_vars))

# ---------------------------------------------------------------------------
JS = r"""
(function () {
  var root = document.documentElement;
  root.classList.remove('no-js');
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasMotion = !!(window.Motion && window.Motion.scroll && window.Motion.animate);

  var PRODUCTS = [
__PRODUCT_JS__
  ];
  var N = PRODUCTS.length;
  var PRICES = { __PRICES__ };
  var NAMES = { __NAMES__ };
  var cs = getComputedStyle(document.documentElement);
  var IMG = {};
  Object.keys(NAMES).forEach(function (k) {
    IMG[k] = cs.getPropertyValue('--img-' + k).trim();
  });
  var DELIVERY = 5.00;

  var dots = Array.prototype.slice.call(document.querySelectorAll('.dotnav__dot'));
  var bar = document.getElementById('stageProgressBar');
  var panels = Array.prototype.slice.call(document.querySelectorAll('.panel'));
  var words = panels.map(function (p) { return p.querySelector('.panel__word'); });
  var wrap = document.getElementById('stageWrap');

  /* ---------- palco: revela / cobre painel por painel ---------- */
  function layoutPanels(indexF) {
    if (bar) bar.style.width = (Math.min(1, Math.max(0, indexF / (N - 1))) * 100) + '%';
    panels.forEach(function (panel, i) {
      var local = indexF - i; // <0 a caminho, 0 em cena, >0 já passou
      var band = reduceMotion ? 0.001 : 0.62;
      var reveal = Math.min(1, Math.max(0, (local + band) / band));
      panel.style.opacity = String(reveal);
      panel.style.zIndex = String(i);
      if (reduceMotion) return;

      var entry = panel.getAttribute('data-entry');
      var away = 1 - reveal;
      var tx = 0, ty = 0, rot = 0, extra = 0;
      if (entry === 'slide')       { tx = away * 13; }
      else if (entry === 'spin')   { rot = away * -7; extra = 0.06; }
      else if (entry === 'open')   { extra = 0.10; }
      else if (entry === 'finale') { extra = 0.14; }
      else                         { ty = away * 7; }

      var blur = away * 9;
      var scale = 0.96 + reveal * 0.04 - extra * away;
      panel.style.filter = blur > 0.15 ? 'blur(' + blur.toFixed(2) + 'px)' : 'none';
      panel.style.transform = 'translate(' + tx.toFixed(2) + 'vw,' + ty.toFixed(2) + 'vh) rotate(' + rot.toFixed(2) + 'deg) scale(' + scale.toFixed(3) + ')';
      if (words[i]) words[i].style.transform = 'translateX(' + (local * -3.5).toFixed(2) + 'vw)';
    });
  }

  function applyChrome(indexF) {
    var idx = Math.max(0, Math.min(N - 1, Math.round(indexF)));
    dots.forEach(function (d, i) { d.classList.toggle('is-active', i === idx); });
  }
  function resetChrome() { dots.forEach(function (d) { d.classList.remove('is-active'); }); }

  if ('IntersectionObserver' in window) {
    var edgeIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) resetChrome(); });
    }, { threshold: 0.6 });
    var heroEl = document.querySelector('.hero');
    var finaleEl = document.querySelector('.finale');
    if (heroEl) edgeIO.observe(heroEl);
    if (finaleEl) edgeIO.observe(finaleEl);
  }

  layoutPanels(0);
  applyChrome(0);

  if (hasMotion && wrap) {
    window.Motion.scroll(function (progress) {
      var indexF = progress * (N - 1);
      layoutPanels(indexF);
      applyChrome(indexF);
    }, { target: wrap, offset: ['start start', 'end end'] });
  } else if (wrap) {
    var ticking = false;
    function onScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var rect = wrap.getBoundingClientRect();
        var total = wrap.offsetHeight - window.innerHeight;
        var p = total > 0 ? Math.min(1, Math.max(0, -rect.top / total)) : 0;
        var idxF = p * (N - 1);
        layoutPanels(idxF);
        applyChrome(idxF);
        ticking = false;
      });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- reveal ao entrar em cena ---------- */
  root.classList.add('js-ready');
  if (hasMotion) {
    document.querySelectorAll('[data-reveal]').forEach(function (el, i) {
      var kind = el.getAttribute('data-reveal');
      window.Motion.inView(el, function () {
        if (kind === 'card') {
          var delay = parseInt(el.style.getPropertyValue('--card-delay') || '0', 10) * 0.07;
          window.Motion.animate(el, { opacity: [0, 1], y: [28, 0], scale: [0.9, 1] },
            { duration: 0.6, delay: delay, easing: [0.16, 1, 0.3, 1] });
        } else if (kind === 'orbit') {
          var d = parseInt(el.style.getPropertyValue('--d') || '0', 10) * 0.06;
          window.Motion.animate(el, { opacity: [0, 1], scale: [0.4, 1] },
            { duration: 0.7, delay: d, easing: [0.16, 1, 0.3, 1] });
        } else {
          window.Motion.animate(el, { opacity: [0, 1], y: [22, 0] },
            { duration: 0.7, delay: (i % 5) * 0.07, easing: [0.16, 1, 0.3, 1] });
        }
      }, { amount: 0.35 });
    });
  } else {
    document.querySelectorAll('[data-reveal]').forEach(function (el) { el.style.opacity = 1; });
  }

  /* ---------- carrinho ---------- */
  var cart = {};
  var drawer = document.getElementById('cartDrawer');
  var fab = document.getElementById('cartFab');
  var fabCount = document.getElementById('cartCount');
  var itemsEl = document.getElementById('cartItems');
  var emptyEl = document.getElementById('cartEmpty');
  var subEl = document.getElementById('cartSubtotal');
  var delEl = document.getElementById('cartDelivery');
  var totEl = document.getElementById('cartTotal');
  var continueBtn = document.getElementById('cartContinue');
  var confirmEl = document.getElementById('cartConfirm');
  var toastEl = document.getElementById('toast');
  var toastTimer = null;

  function brl(v) {
    return 'R$ ' + v.toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  }
  function count() {
    var n = 0; for (var k in cart) n += cart[k]; return n;
  }
  function openCart() { drawer.classList.add('is-open'); drawer.setAttribute('aria-hidden', 'false'); }
  function closeCart() { drawer.classList.remove('is-open'); drawer.setAttribute('aria-hidden', 'true'); }

  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add('is-show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove('is-show'); }, 1600);
  }

  function render() {
    var n = count();
    if (fabCount) {
      fabCount.textContent = n;
      fabCount.hidden = n === 0;
    }
    if (confirmEl) confirmEl.hidden = true;

    itemsEl.innerHTML = '';
    var keys = Object.keys(cart);
    emptyEl.hidden = keys.length > 0;
    if (continueBtn) continueBtn.disabled = keys.length === 0;

    var subtotal = 0;
    keys.forEach(function (k) {
      var qty = cart[k];
      var unit = PRICES[k] || 0;
      subtotal += unit * qty;
      var line = document.createElement('div');
      line.className = 'cart-line';
      line.innerHTML =
        '<span class="cart-line__img"></span>' +
        '<div><div class="cart-line__name"></div>' +
        '<div class="cart-line__unit"></div></div>' +
        '<div class="cart-line__qty">' +
          '<button type="button" data-dec="' + k + '" aria-label="Menos">−</button>' +
          '<span>' + qty + '</span>' +
          '<button type="button" data-inc="' + k + '" aria-label="Mais">+</button>' +
        '</div>';
      if (IMG[k]) line.querySelector('.cart-line__img').style.backgroundImage = IMG[k];
      line.querySelector('.cart-line__name').textContent = NAMES[k];
      line.querySelector('.cart-line__unit').textContent = brl(unit) + ' un.';
      itemsEl.appendChild(line);
    });

    var delivery = subtotal > 0 ? DELIVERY : 0;
    subEl.textContent = brl(subtotal);
    delEl.textContent = brl(delivery);
    totEl.textContent = brl(subtotal + delivery);
  }

  function add(key) {
    if (!(key in PRICES)) return;
    cart[key] = (cart[key] || 0) + 1;
    render();
    if (fab) {
      fab.classList.remove('is-bump');
      void fab.offsetWidth;
      fab.classList.add('is-bump');
    }
    toast(NAMES[key] + ' adicionado');
  }

  document.addEventListener('click', function (e) {
    var addBtn = e.target.closest('[data-add]');
    if (addBtn) { add(addBtn.getAttribute('data-add')); return; }
    var inc = e.target.closest('[data-inc]');
    if (inc) { cart[inc.getAttribute('data-inc')]++; render(); return; }
    var dec = e.target.closest('[data-dec]');
    if (dec) {
      var k = dec.getAttribute('data-dec');
      cart[k]--; if (cart[k] <= 0) delete cart[k];
      render(); return;
    }
    if (e.target.closest('#cartFab')) { openCart(); return; }
    if (e.target.closest('#cartClose') || e.target.closest('#cartScrim')) { closeCart(); return; }
    if (e.target.closest('#orderBtn')) { openCart(); return; }
  });

  if (continueBtn) {
    continueBtn.addEventListener('click', function () {
      if (count() === 0) return;
      if (confirmEl) confirmEl.hidden = false;
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeCart();
  });

  render();
})();
"""

JS = (JS.replace("__PRODUCT_JS__", product_js)
        .replace("__PRICES__", prices_js)
        .replace("__NAMES__", names_js))

# ---------------------------------------------------------------------------
HTML = f"""<!doctype html>
<html lang="pt-BR" class="no-js">
<head>
<meta charset="utf-8">
<title>Mercado Oeste</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Mercado Oeste — o mercado que vai até você. Experiência conceitual de um supermercado local.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/motion@11.18.2/dist/motion.js"></script>
<style>{CSS}</style>
</head>
<body>

<div class="ribbon">
  <span class="ribbon__long"><strong>Projeto conceitual / portfólio</strong> — experiência de marca fictícia, sem vínculo com marcas reais</span>
  <span class="ribbon__short"><strong>Conceitual / portfólio</strong> — não oficial</span>
</div>

<header class="site-header">
  <a class="wordmark lockup" href="#top" aria-label="Mercado Oeste — início">{LOCKUP}</a>
</header>

<nav class="dotnav" aria-label="Navegação de produtos">
{dots}
</nav>

<button class="cart-fab" id="cartFab" type="button" aria-label="Abrir carrinho">
  🛒 Carrinho <span class="cart-fab__count" id="cartCount" hidden>0</span>
</button>

<main id="top">
  <section class="hero">
    <div class="hero__bg" aria-hidden="true">
      <span class="hero__glow hero__glow--far"></span>
      <span class="hero__glow hero__glow--near"></span>
    </div>
    <div class="hero__inner">
      <p class="hero__eyebrow">Supermercado · entrega em casa</p>
      <h1 class="lockup hero__brand">{LOCKUP}</h1>
      <p class="hero__tagline">O mercado que <em>vai até você.</em></p>
      <p class="hero__sub">Tudo o que você precisa, a poucos cliques. Role a página e conheça os produtos do Mercado Oeste, um de cada vez.</p>
    </div>
    <div class="hero__cue" aria-hidden="true">
      <span>Role para explorar</span>
      <span class="hero__cue-line"></span>
    </div>
    <div class="hero__fade" aria-hidden="true"></div>
  </section>

  <div class="stage-wrap" id="stageWrap">
{anchors}
    <div class="stage-sticky">
{panels}
      <div class="stage__progress"><div class="stage__progress-bar" id="stageProgressBar"></div></div>
    </div>
  </div>

  <section class="finale">
    <div class="finale__orbit" aria-hidden="true">
{finale_thumbs}
    </div>
    <div class="finale__core">
      <span class="lockup finale__lockup" data-reveal>{LOCKUP}</span>
      <h2 class="finale__headline" data-reveal>Tudo que você precisa.<em>Em um só lugar.</em></h2>
      <a class="finale__cta" href="#meus-produtos" data-reveal>Ver produtos <span aria-hidden="true">→</span></a>
    </div>
  </section>

  <section class="shop" id="meus-produtos">
    <div class="shop__head">
      <p class="shop__eyebrow" data-reveal>Catálogo</p>
      <h2 class="shop__title" data-reveal>Meus produtos</h2>
      <p class="shop__sub" data-reveal>O catálogo do Mercado Oeste. Preços demonstrativos — adicione ao carrinho e a gente entrega na sua casa.</p>
    </div>
    <div class="shop__grid">
{shop_cards}
    </div>
  </section>

  <section class="delivery" id="entrega">
    <h2 class="delivery__headline" data-reveal>Comprou?<em>A gente entrega.</em></h2>
    <div class="delivery__grid">
      <div class="delivery__item" data-reveal><span class="delivery__emoji">🚚</span><span class="delivery__label">Entrega em casa</span><span class="delivery__hint">Todo o bairro</span></div>
      <div class="delivery__item" data-reveal><span class="delivery__emoji">💰</span><span class="delivery__label">Taxa fixa</span><span class="delivery__hint">R$ 5,00</span></div>
      <div class="delivery__item" data-reveal><span class="delivery__emoji">🛒</span><span class="delivery__label">Pedido pelo site</span><span class="delivery__hint">Rápido e simples</span></div>
    </div>
    <button class="delivery__cta" id="orderBtn" type="button" data-reveal>Fazer pedido</button>
  </section>

  <footer class="site-footer">
    <p class="footer__mark">Mercado <em>Oeste</em></p>
    <p class="footer__note">
      Este site é um <strong>projeto conceitual / portfólio</strong>, criado para demonstrar design e desenvolvimento web.
      Mercado Oeste é uma marca fictícia; nomes de produtos aparecem apenas de forma ilustrativa e valores são demonstrativos.
    </p>
    <div class="footer__meta">
      <span>Projeto Conceitual</span>
      <span>Entrega em Casa</span>
      <span>{N} Produtos</span>
    </div>
  </footer>
</main>

<aside class="cart" id="cartDrawer" aria-hidden="true" aria-label="Meu carrinho">
  <div class="cart__scrim" id="cartScrim"></div>
  <div class="cart__panel" role="dialog" aria-modal="true" aria-label="Meu carrinho">
    <div class="cart__head">
      <h2>🛒 Meu carrinho</h2>
      <button class="cart__close" id="cartClose" type="button" aria-label="Fechar carrinho">✕</button>
    </div>
    <div class="cart__items" id="cartItems"></div>
    <p class="cart__empty" id="cartEmpty">Seu carrinho está vazio.</p>
    <div class="cart__summary">
      <div class="cart__row"><span>Subtotal</span><span id="cartSubtotal">R$ 0,00</span></div>
      <div class="cart__row"><span>Entrega em casa</span><span id="cartDelivery">R$ 0,00</span></div>
      <div class="cart__row cart__row--total"><span>Total</span><span id="cartTotal">R$ 0,00</span></div>
    </div>
    <button class="cart__cta" id="cartContinue" type="button" disabled>Continuar</button>
    <p class="cart__confirm" id="cartConfirm" hidden>Pedido simulado ✓ — o Mercado Oeste entra em contato para combinar a entrega. 🚚</p>
    <p class="cart__fine">Entrega em casa · taxa fixa de R$ 5,00 · valores demonstrativos.</p>
  </div>
</aside>

<div class="toast" id="toast" role="status" aria-live="polite"></div>

<script>{JS}</script>
</body>
</html>
"""

with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(HTML)

print("wrote", os.path.join(ROOT, "index.html"), len(HTML), "chars")
