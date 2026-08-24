# Passo 1: Configure o seu ambiente


1. Você deve estar utilizando a IDE de sua preferência, com python 3.1+ instalado

2. Você deve instalar o [Ollama](https://ollama.com/)
    
    Utilize a opção `Download` ou rode o script `curl -fsSL https://ollama.com/install.sh | sh`

3. Faça download do modelo do Ollama

    ```bash
    ollama pull llama3.1
    ```

4. Crie um ambiente virtual com o venv e instale as dependências:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install "strands-agents[ollama]"
    ```

    Edite o arquivo 

5. Execute o arquivo `app.py`


    ```bash
    python app.py
    ```

    Você deve ver no terminal um `Hello World!`, o que significa que seu código executou corretamente.


# Erros

* `command not found: python`

    Você pode ter o `python3` instalado e precisa criar um alias. Rode os seguintes comandos no seu terminal:
    
    ```bash
    alias python='python3'
    alias pip='pip3'
    ```

* `ERROR: Ignored the following versions that require a different python version: 0.0.1 `

    Você deve atualizar o Python para uma versão igual ou superior a 3.10.
    
    Caso já tenha sido criada a pasta `.venv`, você deve fechar o terminal e excluir a pasta para que a nova versão seja atualizada no ambiente. 
