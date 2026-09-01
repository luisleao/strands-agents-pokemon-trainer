# Passo 2: Primeiro código com Strands Agents

O que vamos aprender aqui:
* Inicializar um agente utilizando Strands Agents
* Escolher um modelo de LLM
* Executar o receber o resultado do agente
* Utilizar uma entrada dinâmica e criar um loop


## Passo-a-passo

A partir deste passo você vai copiar e colar blocos de código.

Em cada etapa explicamos qual a funçnao de cada bloco.

Sempre cole no arquivo `app.py` e obedeça a ordem das funções.



1. Inicialize a biblioteca do Strands Agents

    ```python
    from strands import Agent
    from strands.models.ollama import OllamaModel

    ```

2. Adicione o modelo local do Ollama

    ```python
    modelo = OllamaModel(
        host="http://localhost:11434",
        model_id="llama3.1",
    )
    ```

3. Inicialize o agente

    ```python
    agente = Agent(model=modelo)
    ```

4. Implemente uma pergunta

    ```python
    PERGUNTA= "Qual é o Pokémon mais famoso?"
    print(f"👩‍💻 Prompt: {PERGUNTA}\n")
    print("🤖 Agente: ", end="", flush=True)
    agente(PERGUNTA)
    ```

5. Rode seu script e confira o resultado

    ```bash
    python app.py
    ```

    **Lembre-se:** O seu aplicativo do Ollama deve estar em execução para que a consulta seja realizada. 

6. Adicione um prompt de systema agora.


    ```python
    SYSTEM_PROMPT = """
    Você é um agente que ajuda treinadores de Pokémon a criar estratégias.
    Seus objetivos:
    1. Utilize apenas as ferramentas existentes para consultar informações de Pokémons e não sua própria base de conhecimento.
    2. Identificar fortalezas e fraquezas do deck do participante e de possíveis desafiantes
    3. Ajudar a traçar uma estratégia.
    4. Responder sempre em Português Brasileiro.
    5. Manter as respostar concisas, no máximo entre 2 e 3 parágrafos.
    """

    # Ajuste a inicialização do agente para incluir o prompt de sistema.
    agente = Agent(
        model=modelo,
        system_prompt=SYSTEM_PROMPT
    )
    ```

7. Rode seu script e confira o resultado

    ```bash
    python app.py
    ```

    Observe que o formato da resposta mudou, uma vez que passamos mais instruções no prompt de sistema e agora direciona para que você continue a conversa.

    No próximo passo vamos incluir um loop de conversação.

8. Crie um loop de conversação

    Ajuste para que a pergunta seja uma variável que carregará o input do terminal.
    Na sequência, verifique se o texto enviado corresponde a um comando de saída.
    Finalmente, execute o agente com a pergunta nova.

    ```python
    while True:
        pergunta = input("👩‍💻 Você: ")
        
        if pergunta.strip().lower() in ("sair", "exit", "quit"):
            print("Até a próxima, treinador!")
            break
        
        print("🤖 Agente: ", end="", flush=True)
        agente(pergunta)
        print()  # linha em branco entre turnos
    ```

7. Rode seu script e confira o resultado

    ```bash
    python app.py
    ```

    Agora você já consegue continuar a conversa com o agente.

    Observe que ele ainda não salva em memória o que já foi conversado.

