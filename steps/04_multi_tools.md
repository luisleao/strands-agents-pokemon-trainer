# Passo 4: Utilize múltiplas ferramentas

O que vamos aprender aqui:
* Implementar ferramentas com acesso à APIs




## Passo-a-passo

1. Limpe as ferramentas que estão fazendo acesso ao arquivo estático

    Comente os blocos de código relacionados às ferramentas que estão utilizando os arquivos estátivos

    ```python
    # import json
    # from pathlib import Path
    # POKEMONS = json.loads(Path("./data/pokemons.json").read_text())
    ```

    E também as funções `def buscar_pokemon(nome: str) -> str:` e `ef listar_pokemons() -> str:`


2. Instale a biblioteca `requests` no seu projeto

    ```bash
    pip install requests
    ```

    Esta biblioteca será responsável por fazer requisições HTTP na API de Pokémons [https://pokeapi.co/](https://pokeapi.co/).


3. Importe as ferramentas do arquivo `tools_pokeapi.py`

    Já incorporamos um arquivo `tools_pokeapi.py`, responsável por fazer as chamadas da API, portanto não será necessário codificar esta parte.

    ```python
    from tools_pokeapi import (
        buscar_pokemon,
        buscar_fraquezas_tipo,
        buscar_movimento,
        buscar_habilidade,
        buscar_cadeia_evolucao,
        buscar_natureza,
    )
    ```

4. Ajuste a inicialização do seu agente, substituindo pelas ferramentas da API de Pokémons


    ```python

    agente = Agent(
        model=modelo,
        system_prompt=SYSTEM_PROMPT,
        tools=[
            buscar_pokemon,
            buscar_fraquezas_tipo,
            buscar_movimento,
            buscar_habilidade,
            buscar_cadeia_evolucao,
            buscar_natureza,
        ],
        session_manager=session_manager,
        callback_handler=callback_handler
    )

    ```

    A partir deste momento o agente já possui acesso em todas as ferramentas criadas e pode decidir qual ferramenta utilizar com base na pergunta que você fizer.


5. Ajuste o prompt do sistema para considerar as novas ferramentas

    ```python
    SYSTEM_PROMPT = """
    Você é um agente que ajuda treinadores de Pokémon a criar estratégias.

    REGRAS OBRIGATÓRIAS:
    - Você NÃO possui conhecimento próprio sobre Pokémon. Toda informação DEVE vir das ferramentas.
    - SEMPRE use as ferramentas ANTES de responder qualquer pergunta sobre Pokémon.
    - Passe o nome EXATAMENTE como o usuário digitou para a ferramenta. NÃO traduza, corrija ou modifique nomes.
    - Se a ferramenta retornar que o Pokémon não existe, diga: "O Pokémon [nome exato] não existe." e ofereça listar alternativas.
    - NUNCA invente nomes, dados, stats, tipos ou habilidades. Se não veio da ferramenta, não existe.

    FERRAMENTAS DISPONÍVEIS:
    - buscar_pokemon: dados completos (tipos, stats, habilidades, movimentos)
    - buscar_fraquezas_tipo: relações de dano entre tipos (forte contra, fraco contra)
    - buscar_movimento: detalhes de um ataque (poder, precisão, efeito)
    - buscar_habilidade: efeito de uma ability e quais Pokémon a possuem
    - buscar_cadeia_evolucao: cadeia evolutiva completa
    - buscar_natureza: efeitos de uma nature nos stats

    FLUXO CORRETO:
    1. Usuário menciona um Pokémon → chamar buscar_pokemon com o nome EXATO
    2. Ferramenta retorna dados → usar APENAS esses dados
    3. Ferramenta retorna erro/não encontrado → informar que não existe, sem inventar

    Seus objetivos:
    1. Identificar fortalezas e fraquezas dos Pokémon usando as ferramentas.
    2. Ajudar a traçar estratégias de batalha.
    3. Responder sempre em Português Brasileiro.
    4. Manter as respostas concisas, no máximo 2-3 parágrafos.
    """
    ```


6. Execute seu código e teste

    ```bash
    python app.py
    ```

