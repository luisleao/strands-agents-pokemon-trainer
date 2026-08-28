# Atividades Extras

Aqui estão algumas ideias para implementações que serão consideradas como extras e podem te garantir um brinde especial se estiver no HackTown 2026:


## Publique seu agente em produção na AWS utilizando [Amazon Bedrock](https://aws.amazon.com/pt/bedrock/?trk=6ac81577-2c30-4287-a906-3e10c4cf7625&sc_channel=el)

Para utilizar o Amazon Bedrok, você deve carregar a biblioteca `BedrockModel`

```python
from strands.models import BedrockModel
```

Em seguida, ajuste a inicialização do modelo:

```python
modelo = BedrockModel(
    model_id="us.anthropic.claude-opus-4-6-v1", # define o modelo utilizado
    additional_request_fields={
        "thinking": {
            "type": "enabled", # ativa o reasoning
            "budget_tokens": 4096, # define o limite máximo de tokens para o reasoning
        }
    },
)
```

Você também deve implementar uma interface de webchat para conseguir demonstrar a execução do seu agente. Fique atento sobre o controle de sessão das conversas!

> Você precisa ter uma conta AWS para fazer este processo!


## Crie um novo agente utilizando Kiro

(Kiro)[https://kiro.dev/?trk=6ac81577-2c30-4287-a906-3e10c4cf7625&sc_channel=el] é uma IDE agêntica da AWS que vai além de um assistente de código. Ela transforma prompts em requisitos, design técnico e tarefas sequenciadas, implementando tudo com agentes em paralelo.

Com o modo `Spec`, você define funcionalidades usando *Spec Driven Development*: a partir de uma descrição em linguagem natural, o Kiro gera user stories com critérios de aceitação, diagramas de fluxo, endpoints de API e planos de implementação com testes. Depois, os agentes executam cada tarefa conforme a spec.

Procure o time da AWS durante o HackTown para receber créditos e experimentar a ferramenta.

## Implemente uma chamada de API diferente

Implemente outras APIs que sejam interessantes, por exemplo:

* APIs de geocodificação reversa: [https://nominatim.org/](https://nominatim.org/)
* APIs de previsão do tempo: [https://open-meteo.com/](https://open-meteo.com/)

Faça a combinação de APIs, assim você poderá entender melhor como funciona o "agentic loop" do Strands Agents.


## Implemente um bot de WhatsApp (sandbox)

Você vai precisar implementar um endpoint web que servirá como WebHook do WhatsApp.

Você pode utilizar o ambiente de testes do WhatsApp, seja via API oficial ou pela API da Twilio.

Não será necessário tratar recebimento de arquivos multimídia, porém você deve implementar o tratamento caso receba um arquivo na mensagem.

## Implemente um assistente de voz em tempo real

Consulte a documentação [Voice &amp; Realtime](https://strandsagents.com/docs/user-guide/concepts/bidirectional-streaming/quickstart/?trk=6ac81577-2c30-4287-a906-3e10c4cf7625&sc_channel=el) e implemente seu assistente com voz.


O que vamos aprender aqui:
* 


## Passo-a-passo

Crea `05_nube.py`. El mismo agente, cambiando una línea: `OllamaModel` → `BedrockModel`.

Agrega la dependencia:

```bash
pip install "botocore[crt]"
```

`botocore[crt]` agrega el AWS Common Runtime, necesario si usas credenciales SSO (`aws sso login`).

El cambio clave en el código:

```python
# Antes (local):
from strands.models.ollama import OllamaModel
modelo = OllamaModel(host="http://localhost:11434", model_id="llama3.1")

# Después (nube):
from strands.models import BedrockModel
modelo = BedrockModel(model_id="us.anthropic.claude-opus-4-6-v1")
```

El resto del código — system prompt, tools, lógica — es idéntico.


