from strands import Agent, tool
from strands.models.ollama import OllamaModel
from strands.session.file_session_manager import FileSessionManager


from tools_pokeapi import (
    buscar_pokemon,
    buscar_fraquezas_tipo,
    buscar_movimento,
    buscar_habilidade,
    buscar_cadeia_evolucao,
    buscar_natureza,
)



modelo = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.1",
)

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



session_manager = FileSessionManager(
    session_id="chat",
    storage_dir="./sessions/",
)

# Ajuste a inicialização do agente para incluir o prompt de sistema.
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


while True:
    pergunta = input("👩💻 Você: ")
    
    if pergunta.strip().lower() in ("sair", "exit", "quit"):
        print("Até a próxima, treinador!")
        break
    
    print("🤖 Agente: ", end="", flush=True)
    resposta = agente(pergunta)
    print(resposta)
    print()  # linha em branco entre turnos



