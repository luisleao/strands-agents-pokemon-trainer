# Passo 5: Adicione memória ao seu agente


O que vamos aprender aqui:
* Implementar o gerenciamento de memória do agente



## Passo-a-passo

1. Importe a biblioteca de gerenciamento de sessão por arquivos (FileSessionManager) no seu código

    ```python
    from strands.session.file_session_manager import FileSessionManager
    ```

2. Inicialize o controle de sessão

    ```python
    session_manager = FileSessionManager(
        session_id="chat",
        storage_dir="./sessions",
    )
    ```

    Observe que você pode criar um ID de sessão pelo campo `session_id` e escolher a pasta aonde serão gravadas as sessões de conversa

3. Ajuste seu agente para incorporar o gerenciamento de sessão através da variável `session_manager`

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

4. Execute novamente o seu código python

    ```bash
    python app.py
    ```



