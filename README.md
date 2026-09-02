# Baly Sabores

Landing page conceitual (projeto de portfólio, sem vínculo oficial com a Baly Brasil) que conta a
linha de sabores da Baly em forma de scrollytelling: cada sabor dissolve no próximo conforme a
página rola, animado com [Motion](https://motion.dev), fechando com uma seção sobre a marca e o
drop da linha Baly Zero.

**Live:** https://claude.ai/code/artifact/b9db026d-d03b-4954-8cf5-e25c6d8a246d

## Estrutura

- `build.py` — gera `baly-landing.html` a partir dos dados dos sabores (nome, cor, copy) e das
  imagens em `assets/`, já embutindo tudo como HTML single-file (imagens em base64).
- `assets/` — fotos das latas (fornecidas pela Paloma), otimizadas em `.webp`.
- `baly-landing.html` — o arquivo final, gerado — **não edite direto**, edite `build.py` e rode:

  ```bash
  python3 build.py
  ```

## Sequência da experiência

Intro → Baly Tradicional → 7 sabores (crossfade contínuo via scroll) → seção "A Baly" → drop da
linha Baly Zero → CTA para o site oficial (balybrasil.com.br).

## Aviso

Este é um projeto conceitual/portfólio de design e desenvolvimento web. Não é o site oficial da
Baly Brasil — o link para o site oficial está sempre visível na página.
