# Passo 3: Crie uma nova ferramenta para seu agente


O que vamos aprender aqui:
* Criar uma nova ferramenta para consultar um arquivo local
* Implementar uma função de callback para monitorar a execução das ferramentas
* Ajustar o prompt de sistema para criar guardrails



## Passo-a-passo

A partir deste passo você vai copiar e colar blocos de código.

Em cada etapa explicamos qual a funçnao de cada bloco.

Sempre cole no arquivo `app.py` e obedeça a ordem das funções.



1. Ajustar o prompt de systema para incluir

    Com o app ainda em execução, tente perguntar sobre um pokémon que não existe.

    Observe que a LLM vai halucinar e inventar atributos para ele, portanto precisamos resolver isso.

    A ideia é criar uma base de pokémons aonde ela possa consultar os que existem e não inventar novos pokémons e ainda inventar atributos.

    Ajuste a constante SYSTEM_PROMPT conforme abaixo:

    ```python
    SYSTEM_PROMPT = """
    Você é um agente que ajuda treinadores de Pokémon a criar estratégias.

    REGRAS OBRIGATÓRIAS:
    - Você NÃO possui conhecimento próprio sobre Pokémon. Toda informação DEVE vir das ferramentas.
    - SEMPRE use a ferramenta buscar_pokemon ANTES de responder qualquer pergunta sobre um Pokémon.
    - Passe o nome EXATAMENTE como o usuário digitou para a ferramenta. NÃO traduza, corrija ou modifique o nome.
    - Se a ferramenta retornar que o Pokémon não foi encontrado, diga: "O Pokémon [nome exato] não existe na minha Pokédex." e ofereça listar os disponíveis.
    - NUNCA invente nomes, dados, stats, tipos ou habilidades. Se não veio da ferramenta, não existe.

    Seus objetivos:
    1. Consultar APENAS as ferramentas para obter dados — nunca gerar dados de memória.
    2. Identificar fortalezas e fraquezas do deck do participante.
    3. Ajudar a traçar uma estratégia.
    4. Responder sempre em Português Brasileiro.
    5. Manter as respostas concisas, no máximo 2-3 parágrafos.

    FLUXO CORRETO:
    1. Usuário menciona um Pokémon → chamar buscar_pokemon com o nome EXATO que o usuário digitou
    2. Ferramenta retorna dados → usar APENAS esses dados
    3. Ferramenta retorna "não encontrado" → dizer que não existe na Pokédex, sem inventar alternativas
    """
    ```

    Execute o código e tente pergunntar sobre um pokémon que não existe.

    Agora o agente irá tentar executar as funções, porém elas não existem ainda e vamos criar a seguir.

1. Ajuste o import para considerar também as ferramentas (tools)

    ```python
    from strands import Agent, tool
    ```

2. Importa nossa base fixa de pokemons


    ```python
    import json
    from pathlib import Path

    POKEDEX_DATA = json.loads(Path("data/pokemons.json").read_text())["pokedex"]
    ```

3. Implemente as funções das ferramentas

    ```python

    @tool
    def buscar_pokemon(nome: str) -> str:
        """Busca informações estratégicas de um Pokémon pelo nome.
        
        Args:
            nome: Nome do Pokémon (ex: 'charizard', 'pikachu')
        
        Returns:
            Dados completos do Pokémon incluindo tipos, habilidades, poderes, stats, forças e fraquezas.
        """
        nome_lower = nome.strip().lower()
        for pokemon in POKEDEX_DATA:
            if pokemon["nome"].lower() == nome_lower:
                return json.dumps(pokemon, ensure_ascii=False, indent=2)
        
        # Busca parcial
        matches = [p for p in POKEDEX_DATA if nome_lower in p["nome"].lower()]
        if matches:
            return json.dumps(matches[0], ensure_ascii=False, indent=2)
        
        nomes_disponiveis = [p["nome"] for p in POKEDEX_DATA]
        return f"Pokémon '{nome}' não encontrado. Disponíveis: {', '.join(nomes_disponiveis)}"


    @tool
    def listar_pokemons() -> str:
        """Lista todos os Pokémon disponíveis na Pokédex com seus tipos.
        
        Returns:
            Lista formatada de todos os Pokémon disponíveis.
        """
        resultado = []
        for p in POKEDEX_DATA:
            tipos = ", ".join(p["tipos"])
            resultado.append(f"• {p['nome']} ({tipos})")
        return "\n".join(resultado)


    ```

4. Implemente um callback handler para monitorar o que está acontecendo.

    Este callback handler permite que você acompanha a execução do `agentic loop`, que roda continuamente entre raciocínio, ação e observação. Uma vez que o objetivo do prompt de sistema é alcançado, o loop se encerra.


    ```python

    _after_tool = False

    def callback_handler(**kwargs):
        global _after_tool
        if "reasoningText" in kwargs:
            print(f"💭 {kwargs['reasoningText']}", end="", flush=True)
        if "data" in kwargs:
            if _after_tool:
                print("\n")
                _after_tool = False
            print(kwargs["data"], end="", flush=True)
        if "current_tool_use" in kwargs:
            _after_tool = True
            t = kwargs["current_tool_use"]
            if t.get("name"):
                print(f"\n\n🔧 Ferramenta: {t['name']}")
            if t.get("input"):
                print(f"   Parâmetros: {t['input']}")


    ```

5. Adicione o callback handler e as ferramentas no agente.

    ```python
    agente = Agent(
        model=modelo,
        system_prompt=SYSTEM_PROMPT,
        tools=[buscar_pokemon, listar_pokemons],
        callback_handler=callback_handler
    )
    ```

    Execute o código e faça perguntas para entender como o agente está executando as funções.





