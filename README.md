# Mercado Oeste

**Experiência conceitual para um supermercado de bairro — uma apresentação visual dos principais produtos, com scroll cinematográfico.**

---

## Sobre

**Mercado Oeste** é um projeto conceitual e não oficial: um supermercado tradicional transformado
em uma experiência digital moderna. A ideia é o usuário sentir que está navegando por uma
apresentação dos produtos, e não por um e-commerce genérico.

A primeira metade da página é a experiência de marca: cada produto entra em cena durante o scroll,
fica grande na tela, ganha sua própria atmosfera de cor (puxada da embalagem) e depois dá lugar
ao próximo. A segunda metade mostra como isso viraria uma compra de verdade — catálogo, carrinho
e entrega em casa.

`INTRO` → `ARROZ` → `FEIJÃO` → `AÇÚCAR` → `CAFÉ` → `ÓLEO` → `LEITE` → `HORTIFRUTI` → `TRANSIÇÃO FINAL` → `MEUS PRODUTOS` → `ENTREGA`

**Só estes 7 produtos participam do scroll cinematográfico**, cada um com o PNG de
fundo já removido (só o fundo externo — branco/letras/reflexos da embalagem ficam
intactos). A seção "Meus produtos" é a parte funcional (catálogo): os 6 vendáveis
das cenas + itens que existem apenas no catálogo (massas, ovos, Coca-Cola, água,
detergente, papel higiênico, sabão). Produtos novos entram só aqui — nunca no scroll.

---

## Identidade

- Verde e verde escuro como identidade da marca e da navegação/UI.
- Branco e o carrinho de supermercado (logo).
- Cada produto tem seu "momento visual" próprio — açúcar branco/vermelho, arroz azul/branco,
  feijão escuro, fruteira verde/natural, leite amarelo/creme, óleo dourado, café vermelho/marrom.
  As transições entre esses climas são feitas por crossfade + blur ligado ao scroll, nunca por
  troca brusca de fundo.

---

## Como funciona

Página única, autossuficiente. Tudo é gerado por [`build.py`](build.py), que embute as imagens
reais dos produtos e escreve o `index.html`. Os 7 do scroll usam versões `-cut.png` (só o
fundo externo removido, por flood fill a partir das bordas — nunca máscara global por cor);
os produtos só de catálogo entram como estão.

```
python build.py
```

O motor de scroll é o mesmo padrão de "palco fixo": um bloco alto (`7 × 100vh`), um `sticky`
que ocupa a viewport, e painéis sobrepostos cujo `opacity`/`blur`/`scale` são controlados pelo
progresso do scroll (`Motion.scroll` → `layoutPanels`). Sem JavaScript, os painéis empilham e
tudo continua legível.

O carrinho é apenas demonstrativo (sem back-end): estado em memória, taxa de entrega fixa de
R$ 5,00, valores ilustrativos.

---

## Projeto conceitual

**Mercado Oeste é uma marca fictícia.** Nomes de produtos aparecem apenas de forma ilustrativa
e os preços são demonstrativos. Projeto feito para estudo de direção de arte, motion,
scrollytelling e design de interação.
