# Passo 2: Primeiro código com Strands Agents

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


