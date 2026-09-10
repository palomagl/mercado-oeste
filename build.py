#!/usr/bin/env python3
"""
Mercado Oeste — experiência conceitual.

Reaproveita o motor de scroll da base (palco fixo + painéis que fazem crossfade
via Motion.scroll -> layoutPanels), trocando totalmente o conteudo: cada produto
do mercado ganha seu proprio "momento visual" (cor de embalagem, palavra gigante,
imagem protagonista), e depois vem a parte funcional (catálogo + carrinho + entrega).

Gera um unico index.html, com as imagens reais dos assets embutidas em base64.
"""
import base64, math, os, random

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

# Icones do hero claro (traco, herdam currentColor). Inline pra nao depender de rede.
def _svg(*paths):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"'
            ' stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            + "".join(paths) + '</svg>')

ICON = {
    "arrow": _svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "shield": _svg('<path d="M12 3l7 3v5c0 5-3.5 8-7 9-3.5-1-7-4-7-9V6l7-3z"/>',
                   '<path d="M9 12l2 2 4-4"/>'),
    "truck": _svg('<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/>',
                  '<circle cx="7" cy="18" r="1.6"/><circle cx="17.5" cy="18" r="1.6"/>'),
    "card": _svg('<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M2.5 10h19"/>'),
    "receipt": _svg('<path d="M6 3h12v17l-3-1.6L12 20l-3-1.6L6 20z"/>', '<path d="M9.5 8h5M9.5 11.5h5"/>'),
    "cart": _svg('<path d="M3 4h2l2.4 11.5A1.7 1.7 0 0 0 9 17h8.5a1.7 1.7 0 0 0 1.65-1.3L21 8H6"/>',
                 '<circle cx="9.5" cy="20" r="1.4"/><circle cx="17" cy="20" r="1.4"/>'),
    "bottle": _svg('<path d="M9 8h5l1.5 3v9a1 1 0 0 1-1 1H8.5a1 1 0 0 1-1-1v-9L9 8z"/>',
                   '<path d="M10 8V5h3M13 5l3-1M13 5l3 1"/>'),
    "snow": _svg('<path d="M12 3v18M4.5 7l15 10M19.5 7l-15 10"/>'),
    "spark": _svg('<path d="M12 4l1.8 4.2L18 10l-4.2 1.8L12 16l-1.8-4.2L6 10l4.2-1.8z"/>'),
}

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
        price="R$ 28,90", bg="#0E2E58", scheme="light",
        accent="#F2C14E", entry="rise",
    ),
    dict(
        key="feijao", img=b64("feijao-camil-1kg-cut.png"),
        word="FEIJÃO", title="Feijão Preto Camil 1kg",
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

# ---------------------------------------------------------------------------
# Tratamento cinematográfico por cena. SÓ camadas decorativas (atmosfera, luz,
# grãos/folhas/partículas ao redor) — a imagem do produto nunca muda. Cada
# chave diz quantos elementos a cena espalha; as cores de cada atmosfera moram
# no CSS, casadas por [data-key]. Por enquanto só ARROZ está ligado.
# ---------------------------------------------------------------------------
SCENES = {
    # ratio = faixa de (altura/largura) do grao: arroz alongado, feijao/cafe
    # rechonchudo, cristais/gotas quase redondos.
    "arroz": dict(grains_back=22, grains_front=10, pile=20, streaks=3,
                  leaves=7, leaves_upper=2, motes=26, ratio=(3.0, 4.2)),
    "feijao": dict(grains_back=20, grains_front=9, pile=18, streaks=2,
                   leaves=2, leaves_upper=0, motes=20, ratio=(1.2, 1.6)),
    "acucar": dict(grains_back=26, grains_front=13, pile=16, streaks=0,
                   leaves=0, leaves_upper=0, motes=32, ratio=(1.0, 1.4)),
    "cafe": dict(grains_back=20, grains_front=9, pile=18, streaks=2,
                 leaves=0, leaves_upper=0, motes=22, ratio=(1.3, 1.8)),
    "oleo": dict(grains_back=16, grains_front=10, pile=10, streaks=4,
                 leaves=0, leaves_upper=0, motes=26, ratio=(1.0, 1.25)),
    "leite": dict(grains_back=14, grains_front=10, pile=8, streaks=3,
                  leaves=0, leaves_upper=0, motes=34, ratio=(1.0, 1.2)),
    "fruteira": dict(grains_back=6, grains_front=4, pile=6, streaks=0,
                     leaves=13, leaves_upper=4, motes=24, ratio=(1.8, 2.6)),
}

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
    dict(key="feijao", name="Feijão Preto Camil 1kg",       price=8.49),
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


# Foto do hero (Pexels, licenca livre): entregador com as sacolas de compras,
# luz lateral quente. Usada so como imagem, tratada por cima com CSS pra casar
# com o clima escuro do resto do site. Nao e recortada.
HERO_IMG = b64("hero-delivery.jpg")

# Logo real do cliente: assets/logo-mercado-oeste.png e a MESMA logo original,
# so com o fundo branco removido (knockout mecanico, arte 100% intacta) pra
# funcionar sobre fundo escuro. Sem card branco, sem 3D, sem redesenho.
LOGO_IMG = b64("logo-mercado-oeste.png")

# No catalogo "Meus produtos" todos os cards usam a foto com FUNDO BRANCO. Os 6
# produtos que tambem aparecem no scroll usam la a versao -cut (transparente);
# aqui no catalogo trocamos pela embalagem original (fundo branco) pra ficar tudo
# consistente. Os produtos so-de-catalogo ja vem com fundo branco.
SHOP_CAT_IMG = {
    "acucar": "acucar5kg-caravelas.png",
    "arroz":  "arroz-namorado-5kg.png",
    "feijao": "feijao-camil-1kg.png",
    "leite":  "leite1l-ninho.png",
    "oleo":   "oleodesoja900ml-leve.png",
    "cafe":   "vidrodecafe100g-nescafe.png",
}

# Cada blob de imagem entra UMA vez, como custom property, e e reaproveitado
# no palco, nos cards do catalogo e no anel final (evita repetir base64).
img_vars = "\n".join(
    [f'    --img-{p["key"]}: url("data:image/png;base64,{p["img"]}");'
     for p in PRODUCTS + EXTRA]
    + [f'    --img-{k}-cat: url("data:image/png;base64,{b64(v)}");'
       for k, v in SHOP_CAT_IMG.items()]
)


# ---------- construtores de markup ----------

def scatter_scene(key, cfg):
    """Espalha graos / folhas / particulas de uma cena, ao redor do produto.
    Deterministico (seed por produto) pra nao poluir o diff a cada build.
    Retorna (camada_de_tras, camada_da_frente) ja como <div> prontos."""
    r = random.Random("mercado-oeste::scene::" + key)
    far, near = [], []
    cx, cy = 50.0, 51.0
    rlo, rhi = cfg.get("ratio", (3.0, 4.2))   # faixa altura/largura do grao

    def span(cls, x, y, vs):
        x = max(3.0, min(97.0, x)); y = max(4.0, min(96.0, y))
        style = f"left:{x:.1f}%;top:{y:.1f}%;" + "".join(f"--{k}:{v};" for k, v in vs)
        return f'<span class="{cls}" style="{style}"></span>'

    def drift():
        return [
            ("r", f"{r.uniform(-75, 75):.0f}deg"),
            ("dur", f"{r.uniform(5.5, 9.5):.1f}s"),
            ("delay", f"-{r.uniform(0, 9):.1f}s"),
            ("dx", f"{r.uniform(-7, 7):.0f}px"),
            ("dy", f"{-r.uniform(4, 13):.0f}px"),
            ("dr", f"{r.uniform(-10, 10):.0f}deg"),
        ]

    # graos finos no anel ao redor do produto, atras (alguns desfocados = profundidade)
    for _ in range(cfg["grains_back"]):
        ang = r.uniform(0, 2 * math.pi); rad = r.uniform(14, 42)
        x = cx + rad * math.cos(ang) * 1.28
        y = cy + rad * math.sin(ang)
        if x < 28 and y > 58:          # abre espaco pro texto da esquerda
            x += 20
        soft = r.random() < 0.30
        w = r.uniform(6, 10) if soft else r.uniform(2.6, 4.8)
        vs = [("w", f"{w:.1f}px"), ("h", f"{w * r.uniform(rlo, rhi):.1f}px"),
              ("o", f"{r.uniform(0.24, 0.55):.2f}"),
              ("b", f"{r.uniform(1.6, 3.0):.1f}px" if soft else f"{r.uniform(0, 0.5):.1f}px")]
        far.append(span("grain", x, y, vs + drift()))

    # graos em primeiro plano (bokeh), na frente do produto, espalhados pras bordas
    for _ in range(cfg["grains_front"]):
        ang = r.uniform(0, 2 * math.pi); rad = r.uniform(34, 66)
        x = cx + rad * math.cos(ang) * 1.35
        y = cy + rad * math.sin(ang) * 1.05
        w = r.uniform(4, 7.5)
        vs = [("w", f"{w:.1f}px"), ("h", f"{w * r.uniform(rlo, rhi):.1f}px"),
              ("o", f"{r.uniform(0.35, 0.62):.2f}"), ("b", f"{r.uniform(0.6, 1.6):.1f}px")]
        near.append(span("grain", x, y, vs + drift()))

    # rastros de graos caindo (motion blur) — dao a sensacao de movimento
    for _ in range(cfg.get("streaks", 0)):
        x = 50 + r.uniform(-30, 30); y = r.uniform(16, 70)
        vs = [("w", "2px"), ("h", f"{r.uniform(26, 46):.0f}px"),
              ("o", f"{r.uniform(0.12, 0.26):.2f}"), ("b", f"{r.uniform(2.2, 3.8):.1f}px"),
              ("r", f"{r.uniform(-10, 10):.0f}deg")]
        far.append(span("grain", x, y, vs + drift()))

    # montinho de graos na base do produto (cluster apertado, bem visivel)
    for j in range(cfg["pile"]):
        x = 50 + r.gauss(0, 10); y = 88 + r.uniform(-4, 6)
        w = r.uniform(3.4, 6.0)
        vs = [("w", f"{w:.1f}px"), ("h", f"{w * r.uniform(rlo, rhi):.1f}px"),
              ("o", f"{r.uniform(0.6, 0.92):.2f}"), ("b", f"{r.uniform(0, 0.5):.1f}px")]
        (far if j % 3 == 0 else near).append(span("grain", x, y, vs + drift()))

    # folhas (plantinha de arroz): flanqueando o produto pra ficarem visiveis
    for k in range(cfg["leaves"]):
        upper = k < cfg.get("leaves_upper", 1)
        left = k % 2 == 0
        x = (r.uniform(16, 32) if left else r.uniform(68, 84))
        y = r.uniform(14, 30) if upper else r.uniform(66, 86)
        w = r.uniform(36, 60) if not upper else r.uniform(24, 38)
        vs = [("w", f"{w:.0f}px"), ("h", f"{max(5.0, w * r.uniform(0.15, 0.22)):.0f}px"),
              ("o", f"{r.uniform(0.34, 0.55):.2f}"),
              ("r", f"{(r.uniform(12, 44) if left else r.uniform(-44, -12)):.0f}deg"),
              ("dur", f"{r.uniform(7, 11):.1f}s"), ("delay", f"-{r.uniform(0, 8):.1f}s"),
              ("dx", f"{r.uniform(-5, 5):.0f}px"), ("dy", f"{-r.uniform(3, 8):.0f}px"),
              ("dr", f"{r.uniform(-6, 6):.0f}deg")]
        (far if (not upper and k % 2 == 0) else near).append(span("leaf", x, y, vs))

    # poeira / particulas muito discretas, no fundo
    for _ in range(cfg["motes"]):
        x = r.uniform(5, 95); y = r.uniform(6, 94); w = r.uniform(1.4, 3.2)
        vs = [("w", f"{w:.1f}px"), ("o", f"{r.uniform(0.07, 0.22):.2f}"),
              ("b", f"{r.uniform(0.3, 1.0):.1f}px")]
        far.append(span("mote", x, y, vs + drift()))

    pad = "          "
    return (pad + '<div class="panel__props panel__props--far" aria-hidden="true">'
            + "".join(far) + "</div>",
            pad + '<div class="panel__props panel__props--near" aria-hidden="true">'
            + "".join(near) + "</div>")


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
    eyebrow = (f'<p class="panel__eyebrow">Produto {i+1:02d} '
               f'<span aria-hidden="true">/</span> {N:02d}</p>')

    scene = SCENES.get(p["key"])
    if scene:
        far, near = scatter_scene(p["key"], scene)
        return f"""
      <article class="panel panel--scene scheme-{p['scheme']}" data-panel="{i}"
        data-entry="{p['entry']}" data-key="{p['key']}"
        style="background:{p['bg']};--accent:{p['accent']};">
        <div class="panel__atmos" aria-hidden="true">
          <span class="panel__beam"></span>
          <span class="panel__floor"></span>
        </div>
        <h2 class="panel__word" aria-hidden="true">{word}</h2>
        <div class="panel__stage">
          <span class="panel__glow" aria-hidden="true"></span>
{far}
          <div class="panel__hero">
            <span class="panel__shadow" aria-hidden="true"></span>
            <div class="panel__img" role="img" aria-label="{p['title']}"
              style="background-image:var(--img-{p['key']})"></div>
            <div class="panel__img panel__img--mirror" aria-hidden="true"
              style="background-image:var(--img-{p['key']})"></div>
          </div>
{near}
        </div>
        <div class="panel__meta">
          {eyebrow}
          <h3 class="panel__title">{p['title']}</h3>
          <p class="panel__desc">{p['desc']}</p>
          {action}
        </div>
      </article>"""

    return f"""
      <article class="panel scheme-{p['scheme']}" data-panel="{i}" data-entry="{p['entry']}"
        data-key="{p['key']}" style="background:{p['bg']};--accent:{p['accent']};">
        <h2 class="panel__word" aria-hidden="true">{word}</h2>
        <div class="panel__stage">
          <div class="panel__img" role="img" aria-label="{p['title']}"
            style="background-image:var(--img-{p['key']})"></div>
        </div>
        <div class="panel__meta">
          {eyebrow}
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

def shop_card_html(s, i):
    # catalogo sempre com a foto de fundo branco (versao -cat quando existe)
    img_var = f"--img-{s['key']}-cat" if s["key"] in SHOP_CAT_IMG else f"--img-{s['key']}"
    return f"""
        <figure class="card" data-reveal="card" style="--card-delay:{i};">
          <div class="card__media" role="img" aria-label="{s['name']}"
            style="background-image:var({img_var})"></div>
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
    --font-hand: "Caveat", "Segoe Script", cursive;
    color-scheme: dark;
    --img-hero: url("data:image/jpeg;base64,__HERO_IMG__");
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
  .wordmark { pointer-events: auto; text-decoration: none; display: block; line-height: 0; }
  .wordmark__img {
    height: clamp(48px, 5.5vw, 62px); width: auto; display: block;
    /* leve separacao da arte sobre fundo escuro, sem virar "efeito" */
    filter: drop-shadow(0 2px 5px rgba(0,0,0,0.6)) drop-shadow(0 0 4px rgba(190,235,195,0.14));
  }
  @media (max-width: 640px) { .wordmark__img { height: 46px; } }

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

  /* ---------- hero: abertura escura + entregador ---------- */
  .hero {
    position: relative; min-height: 100vh; overflow: hidden; isolation: isolate;
    display: grid; align-items: center;
    grid-template-columns: minmax(0, 1.04fr) minmax(0, 0.96fr);
    gap: clamp(1.5rem, 4vw, 3rem);
    padding: clamp(5.5rem, 12vh, 8rem) clamp(1.5rem, 7vw, 6rem) clamp(4.5rem, 10vh, 7rem);
    background:
      radial-gradient(88% 68% at 74% 24%, rgba(31,120,60,0.34), transparent 62%),
      radial-gradient(80% 90% at 6% 90%, rgba(20,70,38,0.28), transparent 60%),
      linear-gradient(180deg, #0A1A0F 0%, #08130B 55%, var(--graphite) 100%);
    color: var(--paper); font-family: var(--font-body);
  }
  /* folhas soltas flutuando (mesma linguagem visual das cenas do scroll) */
  .hero__leaf {
    position: absolute; z-index: 1; width: var(--w, 34px); height: calc(var(--w, 34px) * 0.4);
    background: linear-gradient(120deg, transparent, rgba(120,210,110,0.5) 45%, transparent);
    border-radius: 0 100% 0 100% / 0 100% 0 100%;
    filter: blur(0.5px); opacity: 0.5;
    animation: heroLeaf var(--dur, 11s) ease-in-out infinite; animation-delay: var(--delay, 0s);
  }
  @keyframes heroLeaf {
    0%, 100% { transform: translate3d(0,0,0) rotate(var(--r, 0deg)); }
    50%      { transform: translate3d(-14px, 18px, 0) rotate(calc(var(--r, 0deg) + 22deg)); }
  }
  @media (prefers-reduced-motion: reduce) { .hero__leaf { animation: none; } }

  /* foto do entregador: entra pela direita e dissolve no fundo escuro */
  .hero__media { position: absolute; inset: 0 0 0 auto; width: min(56%, 880px); z-index: 0; pointer-events: none; }
  .hero__photo {
    position: absolute; inset: 0;
    background-image: var(--img-hero); background-size: cover; background-position: 44% 30%;
    -webkit-mask-image: linear-gradient(to right, transparent 0%, #000 30%);
            mask-image: linear-gradient(to right, transparent 0%, #000 30%);
  }
  .hero__media::after {
    content: ""; position: absolute; inset: 0;
    background:
      linear-gradient(100deg, rgba(8,19,11,0.92), rgba(8,19,11,0.32) 34%, transparent 66%),
      linear-gradient(to bottom, rgba(8,19,11,0.42), transparent 24%, transparent 70%, rgba(8,19,11,0.8));
  }
  .hero__inner { position: relative; z-index: 2; max-width: 40rem; }

  .hero__eyebrow {
    font-family: var(--font-mono); font-size: 0.72rem; letter-spacing: 0.22em; text-transform: uppercase;
    color: var(--green-bright); font-weight: 600; margin: 0 0 1.3rem;
    display: inline-flex; align-items: center; gap: 0.7rem;
  }
  .hero__eyebrow::before { content: ""; width: 34px; height: 2px; border-radius: 2px; background: var(--green-bright); }

  .hero__brand {
    font-family: var(--font-body); font-weight: 800; text-transform: uppercase;
    font-size: clamp(2.6rem, 7.8vw, 5.8rem); line-height: 0.88; letter-spacing: -0.028em;
    margin: 0 0 1.3rem; text-shadow: 0 20px 60px rgba(0,0,0,0.5);
  }
  .hero__brand span { display: block; }
  .hero__brand .l1 { color: var(--paper); }
  .hero__brand .l2 { color: var(--green-bright); }

  .hero__tagline {
    font-family: var(--font-body); font-weight: 600; margin: 0 0 1.1rem;
    font-size: clamp(1.25rem, 2.5vw, 2rem); line-height: 1.2; color: var(--paper);
  }
  .hero__tagline em { font-style: normal; color: var(--green-bright); }

  .hero__sub {
    max-width: 30rem; margin: 0 0 2rem; font-size: clamp(0.95rem, 1.2vw, 1.05rem);
    line-height: 1.62; color: var(--paper-dim);
  }

  .hero__cta {
    display: inline-flex; align-items: center; gap: 0.6rem;
    padding: 1rem 1.9rem; border-radius: 999px; text-decoration: none;
    background: var(--green); color: #fff; font-weight: 700; font-size: 0.98rem;
    box-shadow: 0 16px 34px -12px rgba(31,162,76,0.55);
    transition: transform 0.2s ease, background 0.25s ease, box-shadow 0.25s ease;
  }
  .hero__cta:hover { transform: translateY(-2px); background: var(--green-bright); box-shadow: 0 22px 40px -12px rgba(31,162,76,0.6); }
  .hero__cta svg { width: 1.15em; height: 1.15em; }

  .hero__badges { display: flex; flex-wrap: wrap; gap: 1rem 1.6rem; margin-top: 2.4rem; }
  .hero__badge {
    display: inline-flex; align-items: center; gap: 0.6rem;
    font-family: var(--font-mono); font-size: 0.64rem; letter-spacing: 0.08em; text-transform: uppercase;
    color: var(--paper-dim); line-height: 1.35;
  }
  .hero__badge svg { width: 22px; height: 22px; color: var(--green-bright); flex: none; }

  /* card de categorias — vidro escuro translucido */
  .hero__cats {
    position: absolute; z-index: 3; top: clamp(6rem, 15vh, 9rem); right: clamp(1.25rem, 4vw, 3rem);
    width: min(80vw, 252px); padding: 0.5rem;
    background: rgba(10,20,13,0.55); -webkit-backdrop-filter: blur(14px); backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.1); border-radius: 20px;
    box-shadow: 0 30px 60px -24px rgba(0,0,0,0.6);
    display: flex; flex-direction: column;
  }
  .hero__cats-lead {
    display: flex; align-items: center; gap: 0.65rem; padding: 0.7rem 0.75rem;
    border-radius: 15px; background: rgba(55,199,102,0.12); margin-bottom: 0.25rem;
    font-size: 0.85rem; font-weight: 700; color: var(--paper); line-height: 1.15;
  }
  .hero__cats-lead .ic {
    width: 34px; height: 34px; flex: none; border-radius: 50%;
    display: grid; place-items: center; background: rgba(55,199,102,0.18); color: var(--green-bright);
  }
  .hero__cats-lead .ic svg { width: 18px; height: 18px; }
  .hero__cat {
    display: flex; align-items: center; gap: 0.65rem; padding: 0.58rem 0.75rem;
    font-size: 0.85rem; font-weight: 500; color: var(--paper-dim); line-height: 1.25;
  }
  .hero__cat + .hero__cat { border-top: 1px solid rgba(255,255,255,0.06); }
  .hero__cat svg { width: 18px; height: 18px; color: var(--green-bright); flex: none; }

  .hero__note {
    position: absolute; z-index: 3; top: clamp(1.4rem, 4.5vh, 2.8rem); right: clamp(1.5rem, 6vw, 5rem);
    max-width: 15rem; text-align: right; transform: rotate(-4deg);
    font-family: var(--font-hand); font-weight: 700; font-size: clamp(1.3rem, 2.1vw, 1.75rem);
    line-height: 1.1; color: var(--green-bright);
  }
  .hero__note::after {
    content: ""; display: block; margin: 0.25rem 0 0 auto; width: 56%; height: 3px; border-radius: 3px;
    background: linear-gradient(to left, var(--green-bright), transparent);
  }

  .hero__cue {
    position: absolute; left: clamp(1.5rem, 7vw, 6rem); bottom: clamp(1.5rem, 5vh, 2.6rem); z-index: 3;
    display: flex; flex-direction: column; align-items: flex-start; gap: 0.55rem;
    font-family: var(--font-mono); font-size: 0.6rem; letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--paper-dim);
  }
  .hero__cue-line { position: relative; width: 1px; height: 42px; overflow: hidden; background: rgba(245,242,232,0.16); }
  .hero__cue-line::after {
    content: ""; position: absolute; inset: 0;
    background: linear-gradient(to bottom, var(--green-bright), transparent);
    animation: cueDrop 2s ease-in-out infinite;
  }
  @keyframes cueDrop { 0% { transform: translateY(-100%); } 55%, 100% { transform: translateY(100%); } }
  @media (prefers-reduced-motion: reduce) { .hero__cue-line::after { animation: none; transform: none; } }

  @media (max-width: 900px) {
    .hero {
      grid-template-columns: 1fr; align-content: start;
      padding: 6.5rem 1.4rem 2.5rem; gap: 1.1rem;
    }
    .hero__media {
      position: relative; inset: auto; width: auto; order: 3;
      height: min(50vh, 400px); margin: 1rem -1.4rem 0;
    }
    .hero__photo {
      background-position: 50% 24%;
      -webkit-mask-image: linear-gradient(to bottom, transparent 0%, #000 32%);
              mask-image: linear-gradient(to bottom, transparent 0%, #000 32%);
    }
    .hero__media::after {
      background: linear-gradient(to top, rgba(8,19,11,0.55), transparent 42%, transparent 82%, rgba(8,19,11,0.85));
    }
    .hero__inner { max-width: none; order: 1; }
    .hero__cats { position: static; order: 2; width: 100%; max-width: 340px; margin-top: 1.3rem; }
    .hero__note, .hero__cue, .hero__leaf { display: none; }
    .hero__brand { font-size: clamp(2.4rem, 13vw, 4rem); }
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

  /* ---------- cena cinematográfica: tratamento visual por produto ---------- */
  /* Só entra nos painéis com .panel--scene (por enquanto, ARROZ). Os demais
     ficam exatamente como estavam. Nada aqui toca a imagem do produto: são
     camadas de atmosfera, luz e elementos decorativos ao redor dele. */
  .panel--scene { --p: 0; }              /* progresso da cena (JS): 0 = em cena */

  .panel__atmos { position: absolute; inset: 0; z-index: 0; overflow: hidden; pointer-events: none; }
  .panel__beam {
    position: absolute; left: 50%; top: -14%; width: min(52vw, 500px); height: 132%;
    transform: translateX(-50%); filter: blur(40px); mix-blend-mode: screen;
    animation: sceneBeam 13s ease-in-out infinite;
  }
  @keyframes sceneBeam {
    0%, 100% { opacity: 0.7; transform: translateX(-52%) scaleX(1); }
    50%      { opacity: 1;   transform: translateX(-48%) scaleX(1.08); }
  }
  .panel__floor {
    position: absolute; left: 0; right: 0; bottom: 0; height: 42%;
    transform: translateY(calc(var(--p) * 12px));
  }

  .panel--scene .panel__word {
    font-size: clamp(4rem, 21vw, 15rem); letter-spacing: -0.02em;
    -webkit-mask-image: linear-gradient(to bottom, #000 50%, transparent 92%);
            mask-image: linear-gradient(to bottom, #000 50%, transparent 92%);
  }
  .panel--scene.scheme-light .panel__word { color: rgba(214, 230, 255, 0.09); }
  .panel--scene.scheme-dark  .panel__word { color: rgba(20, 23, 15, 0.11); }

  .panel--scene .panel__stage { position: relative; }
  .panel--scene .panel__glow {
    position: absolute; left: 50%; top: 52%; z-index: 0; pointer-events: none;
    width: min(66vw, 640px); height: min(78vh, 720px); border-radius: 50%;
    transform: translate(-50%, -50%) scale(calc(1 + var(--p) * 0.05));
    filter: blur(6px); mix-blend-mode: screen;
    animation: sceneGlow 9s ease-in-out infinite;
  }
  @keyframes sceneGlow { 0%, 100% { opacity: 0.8; } 50% { opacity: 1; } }

  .panel--scene .panel__hero { position: relative; z-index: 2; }
  .panel--scene .panel__img {
    height: clamp(300px, 46vw, 600px); width: min(90vw, 600px);
    filter: drop-shadow(0 34px 42px rgba(0, 0, 0, 0.5));
  }
  .panel--scene .panel__img--mirror {
    position: absolute; left: 0; right: 0; top: 100%;
    transform: scaleY(-1); opacity: 0.2; filter: blur(6px); pointer-events: none;
    -webkit-mask-image: linear-gradient(to bottom, rgba(0,0,0,0.55), transparent 58%);
            mask-image: linear-gradient(to bottom, rgba(0,0,0,0.55), transparent 58%);
  }
  .panel--scene .panel__shadow {
    position: absolute; left: 50%; bottom: -2%; width: 60%; height: 10%; z-index: 0;
    transform: translateX(-50%); border-radius: 50%; filter: blur(12px);
    background: radial-gradient(ellipse at center, rgba(0, 0, 0, 0.6), transparent 72%);
  }

  .panel--scene .panel__props { position: absolute; inset: 0; pointer-events: none; }
  .panel--scene .panel__props--far  { z-index: 1; transform: translate3d(0, calc(var(--p) * 24px), 0); }
  .panel--scene .panel__props--near { z-index: 3; transform: translate3d(0, calc(var(--p) * -36px), 0); }

  .grain, .leaf, .mote {
    position: absolute; transform: rotate(var(--r, 0deg));
    animation: sceneDrift var(--dur, 7s) ease-in-out infinite; animation-delay: var(--delay, 0s);
  }
  .grain {
    width: var(--w, 5px); height: var(--h, 15px); border-radius: 50%;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), var(--grain, #e6dfca));
    opacity: var(--o, 0.6); filter: blur(var(--b, 0px));
    box-shadow: 0 0 4px rgba(205, 228, 255, 0.25);
  }
  .leaf {
    width: var(--w, 24px); height: var(--h, 7px); opacity: var(--o, 0.4); filter: blur(0.5px);
    background: linear-gradient(90deg, transparent, var(--leaf, rgba(150, 205, 120, 0.5)) 45%, transparent);
    border-radius: 0 100% 0 100% / 0 100% 0 100%;
  }
  .mote {
    width: var(--w, 2px); height: var(--w, 2px); border-radius: 50%;
    opacity: var(--o, 0.2); filter: blur(var(--b, 0.4px));
    background: radial-gradient(circle, var(--mote, rgba(200, 225, 255, 0.9)), transparent 70%);
  }
  @keyframes sceneDrift {
    0%, 100% { transform: translate3d(0, 0, 0) rotate(var(--r, 0deg)); }
    50%      { transform: translate3d(var(--dx, 0px), var(--dy, -8px), 0)
               rotate(calc(var(--r, 0deg) + var(--dr, 6deg))); }
  }

  /* --- ARROZ: azul profundo, luz fria, grãos e folhas de arroz --- */
  .panel[data-key="arroz"] .panel__atmos {
    background:
      linear-gradient(90deg, rgba(3, 12, 30, 0.74), rgba(3, 12, 30, 0.18) 30%, transparent 48%),
      radial-gradient(85% 62% at 50% 26%, rgba(96, 158, 232, 0.42), transparent 60%),
      radial-gradient(120% 100% at 50% 120%, rgba(2, 11, 28, 0.74), transparent 72%),
      radial-gradient(150% 130% at 50% 45%, transparent 40%, rgba(2, 9, 24, 0.62) 100%);
  }
  .panel[data-key="arroz"] .panel__beam {
    background: linear-gradient(to bottom, rgba(150, 195, 255, 0.42), rgba(130, 180, 255, 0.08) 52%, transparent 80%);
  }
  .panel[data-key="arroz"] .panel__floor {
    background:
      radial-gradient(42% 58% at 50% 92%, rgba(155, 200, 255, 0.28), transparent 70%),
      radial-gradient(95% 120% at 50% 100%, rgba(110, 165, 255, 0.12), transparent 60%),
      linear-gradient(to bottom, transparent 40%, rgba(3, 14, 34, 0.62));
  }
  .panel[data-key="arroz"] .panel__glow {
    background: radial-gradient(closest-side,
      rgba(205, 228, 255, 0.72), rgba(120, 175, 255, 0.28) 38%,
      rgba(58, 120, 210, 0.10) 62%, transparent 78%);
  }
  .panel[data-key="arroz"] .panel__props {
    --grain: #efe9d7; --leaf: rgba(150, 205, 120, 0.5); --mote: rgba(190, 220, 255, 0.9);
  }

  /* --- FEIJÃO: vinho/escuro, atmosfera quente, grãos rechonchudos --- */
  .panel[data-key="feijao"] .panel__atmos {
    background:
      linear-gradient(90deg, rgba(20, 6, 10, 0.74), rgba(20, 6, 10, 0.16) 30%, transparent 48%),
      radial-gradient(85% 62% at 50% 28%, rgba(150, 40, 45, 0.34), transparent 60%),
      radial-gradient(120% 100% at 50% 120%, rgba(14, 4, 8, 0.80), transparent 72%),
      radial-gradient(150% 130% at 50% 45%, transparent 40%, rgba(10, 3, 6, 0.64) 100%);
  }
  .panel[data-key="feijao"] .panel__beam { background: linear-gradient(to bottom, rgba(220, 90, 70, 0.30), rgba(200, 70, 60, 0.05) 55%, transparent 82%); }
  .panel[data-key="feijao"] .panel__floor {
    background:
      radial-gradient(42% 58% at 50% 92%, rgba(210, 90, 70, 0.22), transparent 70%),
      linear-gradient(to bottom, transparent 40%, rgba(12, 3, 6, 0.64));
  }
  .panel[data-key="feijao"] .panel__glow { background: radial-gradient(closest-side, rgba(240, 150, 120, 0.5), rgba(170, 50, 45, 0.2) 42%, transparent 76%); }
  .panel[data-key="feijao"] .panel__props { --grain: #3a1e14; --leaf: rgba(120, 150, 80, 0.4); --mote: rgba(255, 180, 150, 0.85); }
  .panel[data-key="feijao"] .grain {
    border-radius: 46% / 40%;
    background: radial-gradient(circle at 34% 30%, #7a4a38, #24100a 78%);
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.35);
  }

  /* --- AÇÚCAR: creme claro + vermelho, cristais, luz alta (embalagem branca preservada) --- */
  .panel[data-key="acucar"] .panel__atmos {
    background:
      linear-gradient(90deg, rgba(255, 252, 246, 0.62), rgba(255, 252, 246, 0.10) 30%, transparent 46%),
      radial-gradient(80% 60% at 50% 26%, rgba(255, 255, 255, 0.55), transparent 62%),
      radial-gradient(120% 100% at 50% 122%, rgba(196, 38, 46, 0.10), transparent 72%),
      radial-gradient(150% 130% at 50% 46%, transparent 46%, rgba(120, 90, 80, 0.16) 100%);
  }
  .panel[data-key="acucar"] .panel__beam { background: linear-gradient(to bottom, rgba(255, 255, 255, 0.5), rgba(255, 240, 235, 0.08) 55%, transparent 82%); }
  .panel[data-key="acucar"] .panel__floor {
    background:
      radial-gradient(44% 56% at 50% 92%, rgba(255, 255, 255, 0.5), transparent 70%),
      linear-gradient(to bottom, transparent 45%, rgba(150, 120, 110, 0.18));
  }
  .panel[data-key="acucar"] .panel__glow {
    mix-blend-mode: normal;
    background: radial-gradient(closest-side, rgba(255, 255, 255, 0.7), rgba(255, 232, 210, 0.22) 40%, transparent 76%);
  }
  .panel[data-key="acucar"] .panel__shadow { background: radial-gradient(ellipse at center, rgba(120, 90, 80, 0.34), transparent 72%); }
  .panel[data-key="acucar"] .panel__props { --grain: #ffffff; --leaf: transparent; --mote: rgba(255, 255, 255, 0.95); }
  .panel[data-key="acucar"] .grain {
    border-radius: 22%;
    background: linear-gradient(135deg, #ffffff, #f0e6d8);
    box-shadow: 0 0 6px rgba(255, 255, 255, 0.85);
  }

  /* --- CAFÉ: marrom/vermelho escuro, grãos de café, luz aconchegante --- */
  .panel[data-key="cafe"] .panel__atmos {
    background:
      linear-gradient(90deg, rgba(18, 8, 5, 0.76), rgba(18, 8, 5, 0.16) 30%, transparent 48%),
      radial-gradient(85% 62% at 50% 28%, rgba(150, 70, 40, 0.34), transparent 60%),
      radial-gradient(120% 100% at 50% 120%, rgba(14, 6, 4, 0.82), transparent 72%),
      radial-gradient(150% 130% at 50% 45%, transparent 40%, rgba(10, 4, 3, 0.66) 100%);
  }
  .panel[data-key="cafe"] .panel__beam { background: linear-gradient(to bottom, rgba(230, 140, 80, 0.32), rgba(200, 110, 60, 0.06) 55%, transparent 82%); }
  .panel[data-key="cafe"] .panel__floor {
    background:
      radial-gradient(42% 58% at 50% 92%, rgba(220, 130, 70, 0.22), transparent 70%),
      linear-gradient(to bottom, transparent 40%, rgba(10, 4, 3, 0.66));
  }
  .panel[data-key="cafe"] .panel__glow { background: radial-gradient(closest-side, rgba(250, 190, 140, 0.5), rgba(180, 90, 50, 0.2) 42%, transparent 76%); }
  .panel[data-key="cafe"] .panel__props { --grain: #2a1509; --leaf: transparent; --mote: rgba(255, 200, 150, 0.8); }
  .panel[data-key="cafe"] .grain {
    border-radius: 44% / 38%;
    background: radial-gradient(circle at 36% 32%, #6b3c22, #1c0d05 80%);
  }

  /* --- ÓLEO: dourado, reflexos, sensação fluida --- */
  .panel[data-key="oleo"] .panel__atmos {
    background:
      linear-gradient(90deg, rgba(120, 80, 10, 0.5), rgba(120, 80, 10, 0.10) 30%, transparent 46%),
      radial-gradient(82% 60% at 50% 26%, rgba(255, 225, 150, 0.58), transparent 62%),
      radial-gradient(120% 100% at 50% 122%, rgba(120, 70, 10, 0.28), transparent 72%),
      radial-gradient(150% 130% at 50% 46%, transparent 44%, rgba(90, 60, 10, 0.28) 100%);
  }
  .panel[data-key="oleo"] .panel__beam { background: linear-gradient(to bottom, rgba(255, 235, 170, 0.55), rgba(255, 220, 140, 0.10) 55%, transparent 82%); }
  .panel[data-key="oleo"] .panel__floor {
    background:
      radial-gradient(46% 56% at 50% 92%, rgba(255, 235, 170, 0.5), transparent 70%),
      linear-gradient(to bottom, transparent 44%, rgba(90, 60, 12, 0.3));
  }
  .panel[data-key="oleo"] .panel__glow {
    mix-blend-mode: normal;
    background: radial-gradient(closest-side, rgba(255, 240, 190, 0.7), rgba(230, 180, 60, 0.28) 40%, transparent 76%);
  }
  .panel[data-key="oleo"] .panel__props { --grain: #ffd970; --leaf: transparent; --mote: rgba(255, 240, 190, 0.9); }
  .panel[data-key="oleo"] .grain {
    border-radius: 50%;
    background: radial-gradient(circle at 34% 30%, #fff6d8, #e0a92a 75%);
    box-shadow: 0 0 6px rgba(255, 225, 150, 0.7);
  }

  /* --- LEITE: creme/amarelo claro, partículas suaves, luz limpa --- */
  .panel[data-key="leite"] .panel__atmos {
    background:
      linear-gradient(90deg, rgba(255, 252, 240, 0.6), rgba(255, 252, 240, 0.10) 30%, transparent 46%),
      radial-gradient(82% 62% at 50% 26%, rgba(255, 250, 235, 0.7), transparent 64%),
      radial-gradient(120% 100% at 50% 122%, rgba(180, 140, 60, 0.16), transparent 72%),
      radial-gradient(150% 130% at 50% 46%, transparent 46%, rgba(150, 120, 60, 0.2) 100%);
  }
  .panel[data-key="leite"] .panel__beam { background: linear-gradient(to bottom, rgba(255, 255, 250, 0.55), rgba(255, 250, 235, 0.10) 55%, transparent 82%); }
  .panel[data-key="leite"] .panel__floor {
    background:
      radial-gradient(46% 56% at 50% 92%, rgba(255, 255, 250, 0.55), transparent 70%),
      linear-gradient(to bottom, transparent 46%, rgba(150, 120, 60, 0.2));
  }
  .panel[data-key="leite"] .panel__glow {
    mix-blend-mode: normal;
    background: radial-gradient(closest-side, rgba(255, 255, 252, 0.75), rgba(255, 248, 225, 0.25) 42%, transparent 78%);
  }
  .panel[data-key="leite"] .panel__props { --grain: #fffdf6; --leaf: transparent; --mote: rgba(255, 255, 250, 0.95); }
  .panel[data-key="leite"] .grain {
    border-radius: 50%;
    background: radial-gradient(circle, #ffffff, #f3ead6);
    filter: blur(0.6px); box-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
  }

  /* --- HORTIFRÚTI: verde/natural, folhas e frutos, fresco e vivo --- */
  .panel[data-key="fruteira"] .panel__atmos {
    background:
      linear-gradient(90deg, rgba(4, 26, 12, 0.6), rgba(4, 26, 12, 0.14) 30%, transparent 48%),
      radial-gradient(85% 62% at 50% 26%, rgba(120, 220, 140, 0.34), transparent 60%),
      radial-gradient(120% 100% at 50% 120%, rgba(3, 20, 10, 0.72), transparent 72%),
      radial-gradient(150% 130% at 50% 45%, transparent 42%, rgba(2, 16, 8, 0.55) 100%);
  }
  .panel[data-key="fruteira"] .panel__beam { background: linear-gradient(to bottom, rgba(150, 240, 170, 0.34), rgba(120, 220, 150, 0.06) 55%, transparent 82%); }
  .panel[data-key="fruteira"] .panel__floor {
    background:
      radial-gradient(44% 58% at 50% 92%, rgba(150, 240, 170, 0.20), transparent 70%),
      linear-gradient(to bottom, transparent 42%, rgba(3, 18, 9, 0.55));
  }
  .panel[data-key="fruteira"] .panel__glow { background: radial-gradient(closest-side, rgba(200, 255, 210, 0.55), rgba(80, 200, 110, 0.2) 42%, transparent 76%); }
  .panel[data-key="fruteira"] .panel__props { --grain: #d9e8bf; --leaf: rgba(120, 210, 110, 0.62); --mote: rgba(200, 255, 210, 0.9); }
  .panel[data-key="fruteira"] .grain {
    border-radius: 50% 50% 48% 48% / 62% 62% 38% 38%;
    background: linear-gradient(135deg, #eaf3d8, #bcd98f);
  }

  @media (max-width: 720px) {
    .panel--scene .panel__img { height: clamp(220px, 52vw, 360px); width: min(84vw, 380px); }
    .panel--scene .panel__word { font-size: clamp(2.8rem, 24vw, 7rem); }
    .panel--scene .panel__img--mirror { display: none; }
    .panel--scene .panel__props--far .mote:nth-of-type(2n) { display: none; }
    .panel--scene .panel__glow { width: 82vw; height: 46vh; }
  }
  @media (prefers-reduced-motion: reduce) {
    .grain, .leaf, .mote, .panel--scene .panel__glow, .panel__beam { animation: none; }
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
  .finale__core { position: relative; z-index: 2; max-width: 30rem; padding: 0 1rem; }
  .finale__eyebrow {
    font-family: var(--font-mono); font-size: 0.74rem; letter-spacing: 0.28em; text-transform: uppercase;
    color: var(--green-bright); margin: 0 0 1.4rem;
    display: inline-flex; align-items: center; gap: 0.7rem;
  }
  .finale__eyebrow::before, .finale__eyebrow::after { content: ""; width: 24px; height: 1px; background: currentColor; opacity: 0.6; }
  .finale__headline {
    font-family: var(--font-display); font-weight: 400; margin: 0 0 1.9rem;
    font-size: clamp(2.1rem, 5.4vw, 3.5rem); line-height: 1.0; color: var(--paper);
    text-transform: uppercase; letter-spacing: 0.005em;
    text-shadow: 0 2px 24px rgba(12,13,10,0.75), 0 0 8px rgba(12,13,10,0.6);
  }
  .finale__headline em { font-style: normal; color: var(--green-bright); display: block; margin-top: 0.12em; }
  .finale__cta {
    display: inline-flex; align-items: center; gap: 0.55rem;
    padding: 0.9rem 1.7rem; border-radius: 999px; text-decoration: none;
    background: transparent; color: var(--paper); border: 1px solid rgba(245,242,232,0.3);
    font-weight: 700; font-size: 0.88rem; letter-spacing: 0.02em;
    transition: border-color 0.3s ease, background 0.3s ease, transform 0.2s ease;
  }
  .finale__cta:hover { border-color: var(--green-bright); background: rgba(55,199,102,0.12); transform: translateY(-2px); }
  @media (max-width: 720px) {
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
    /* todas as fotos do catalogo tem fundo branco -> mesmo tile claro pra todas */
    background-color: #F7F6F1; padding: 0.6rem;
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

  /* celular: catálogo em 3 por fileira, cards compactos */
  @media (max-width: 720px) {
    .shop { padding: 3.5rem 1rem 3.5rem; }
    .shop__grid { grid-template-columns: repeat(3, 1fr); gap: 0.55rem; }
    .card { padding: 0.5rem; border-radius: 12px; }
    .card__media { height: 84px; margin-bottom: 0.5rem; padding: 0.3rem; border-radius: 8px; }
    .card__body { margin-bottom: 0.5rem; gap: 0.1rem; }
    .card__name { font-size: 0.7rem; line-height: 1.2; }
    .card__price { font-size: 0.7rem; }
    .card__add { padding: 0.45rem 0.3rem; font-size: 0.64rem; border-radius: 8px; }
    .card:hover { transform: none; }
  }
  @media (max-width: 380px) {
    .shop__grid { gap: 0.4rem; }
    .card__media { height: 72px; }
    .card__name { font-size: 0.64rem; }
  }

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
  /* info de serviço: sem caixinhas, sem divisórias — só ícone linear + texto */
  .delivery__grid {
    display: flex; flex-wrap: wrap; align-items: flex-start; justify-content: center;
    gap: clamp(1.8rem, 6vw, 4rem); max-width: 50rem; margin: 0 auto 3rem;
  }
  .delivery__item {
    flex: 0 1 190px; display: flex; flex-direction: column; align-items: center;
    gap: 0.55rem; text-align: center;
  }
  .delivery__ic { display: grid; place-items: center; color: var(--green-bright); }
  .delivery__ic svg { width: 26px; height: 26px; }
  .delivery__label {
    font-weight: 700; font-size: 0.8rem; letter-spacing: 0.08em; text-transform: uppercase;
    color: var(--paper);
  }
  .delivery__hint { font-family: var(--font-mono); font-size: 0.74rem; letter-spacing: 0.03em; color: var(--paper-dim); }
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
          .replace("__HERO_IMG__", HERO_IMG)
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
      if (panel.classList.contains('panel--scene')) {
        panel.style.setProperty('--p', reduceMotion ? '0'
          : Math.max(-1.3, Math.min(1.3, local)).toFixed(3));
      }
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
      if (words[i]) {
        var wx = (local * -3.5).toFixed(2);
        words[i].style.transform = panel.classList.contains('panel--scene')
          ? 'translate(' + wx + 'vw, -7%)'
          : 'translateX(' + wx + 'vw)';
      }
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
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Caveat:wght@600;700&family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/motion@11.18.2/dist/motion.js"></script>
<style>{CSS}</style>
</head>
<body>

<div class="ribbon">
  <span class="ribbon__long"><strong>Projeto conceitual / portfólio</strong> — experiência de marca fictícia, sem vínculo com marcas reais</span>
  <span class="ribbon__short"><strong>Conceitual / portfólio</strong> — não oficial</span>
</div>

<header class="site-header">
  <a class="wordmark" href="#top" aria-label="Mercado Oeste — início">
    <img class="wordmark__img" src="data:image/png;base64,{LOGO_IMG}" alt="Mercado Oeste">
  </a>
</header>

<nav class="dotnav" aria-label="Navegação de produtos">
{dots}
</nav>

<button class="cart-fab" id="cartFab" type="button" aria-label="Abrir carrinho">
  🛒 Carrinho <span class="cart-fab__count" id="cartCount" hidden>0</span>
</button>

<main id="top">
  <section class="hero">
    <div class="hero__media" aria-hidden="true"><div class="hero__photo"></div></div>
    <span class="hero__leaf" aria-hidden="true" style="left:6%;top:22%;--w:44px;--r:-18deg;--dur:12s;--delay:-2s;"></span>
    <span class="hero__leaf" aria-hidden="true" style="left:40%;top:12%;--w:30px;--r:14deg;--dur:9s;--delay:-5s;"></span>
    <span class="hero__leaf" aria-hidden="true" style="left:52%;top:74%;--w:38px;--r:-32deg;--dur:13s;--delay:-1s;"></span>
    <span class="hero__leaf" aria-hidden="true" style="left:12%;top:80%;--w:26px;--r:24deg;--dur:10s;--delay:-7s;"></span>

    <div class="hero__inner">
      <p class="hero__eyebrow">Supermercado · entrega em casa</p>
      <h1 class="hero__brand"><span class="l1">Mercado</span><span class="l2">Oeste.</span></h1>
      <p class="hero__tagline">O mercado que <em>vai até você.</em></p>
      <p class="hero__sub">Tudo o que você precisa, a poucos cliques. Qualidade, variedade e praticidade no seu dia a dia.</p>
      <a class="hero__cta" href="#meus-produtos">{ICON['cart']} Começar a comprar {ICON['arrow']}</a>
      <div class="hero__badges">
        <span class="hero__badge">{ICON['shield']}<span>Produtos<br>de qualidade</span></span>
        <span class="hero__badge">{ICON['truck']}<span>Entrega<br>rápida</span></span>
        <span class="hero__badge">{ICON['card']}<span>Pagamento<br>seguro</span></span>
      </div>
    </div>

    <aside class="hero__cats" aria-hidden="true">
      <span class="hero__cats-lead"><span class="ic">{ICON['truck']}</span>Entrega rápida e segura</span>
      <span class="hero__cat">{ICON['cart']} Alimentos e bebidas</span>
      <span class="hero__cat">{ICON['bottle']} Higiene e limpeza</span>
      <span class="hero__cat">{ICON['snow']} Frios e congelados</span>
      <span class="hero__cat">{ICON['spark']} E muito mais!</span>
    </aside>

    <p class="hero__note" aria-hidden="true">Do seu jeito, no seu tempo.</p>

    <div class="hero__cue" aria-hidden="true">
      <span>Role para explorar</span>
      <span class="hero__cue-line"></span>
    </div>
  </section>

  <div class="stage-wrap" id="stageWrap">
{anchors}
    <div class="stage-sticky">
{panels}
      <div class="stage__progress"><div class="stage__progress-bar" id="stageProgressBar"></div></div>
    </div>
  </div>

  <section class="finale">
    <div class="finale__core">
      <p class="finale__eyebrow" data-reveal>Mercado Oeste</p>
      <h2 class="finale__headline" data-reveal>Tudo o que você precisa,<em>em um só lugar.</em></h2>
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
      <div class="delivery__item" data-reveal>
        <span class="delivery__ic">{ICON['truck']}</span>
        <span class="delivery__label">Entrega em casa</span>
        <span class="delivery__hint">Todo o bairro</span>
      </div>
      <div class="delivery__item" data-reveal>
        <span class="delivery__ic">{ICON['receipt']}</span>
        <span class="delivery__label">Taxa fixa</span>
        <span class="delivery__hint">R$ 5,00</span>
      </div>
      <div class="delivery__item" data-reveal>
        <span class="delivery__ic">{ICON['cart']}</span>
        <span class="delivery__label">Pedido pelo site</span>
        <span class="delivery__hint">Rápido e simples</span>
      </div>
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
