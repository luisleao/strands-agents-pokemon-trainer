"""
Tools para o agente Pokémon usando a PokeAPI.
Cada tool faz chamadas HTTP à API e retorna dados formatados para o agente.
"""

import json
import requests
from strands import tool

BASE_URL = "https://pokeapi.co/api/v2"


@tool
def buscar_pokemon(nome: str) -> str:
    """Busca informações completas de um Pokémon pelo nome ou número.
    Retorna tipos, stats, habilidades e movimentos principais.

    Args:
        nome: Nome ou ID do Pokémon (ex: 'charizard', '6', 'pikachu')

    Returns:
        Dados formatados do Pokémon ou mensagem de erro se não existir.
    """
    nome_lower = nome.strip().lower()
    try:
        r = requests.get(f"{BASE_URL}/pokemon/{nome_lower}", timeout=10)
        if r.status_code == 404:
            return f"❌ Pokémon '{nome}' não existe. Verifique o nome e tente novamente."
        r.raise_for_status()
        data = r.json()

        tipos = [t["type"]["name"] for t in data["types"]]
        stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}
        abilities = [a["ability"]["name"].replace("-", " ").title() for a in data["abilities"]]
        # Top 8 moves
        moves = [m["move"]["name"].replace("-", " ").title() for m in data["moves"][:8]]

        resultado = {
            "id": data["id"],
            "nome": data["name"].title(),
            "tipos": tipos,
            "stats": stats,
            "stats_total": sum(stats.values()),
            "habilidades": abilities,
            "movimentos": moves,
            "altura": data["height"] / 10,  # decímetros -> metros
            "peso": data["weight"] / 10,  # hectogramas -> kg
        }
        return json.dumps(resultado, ensure_ascii=False, indent=2)

    except requests.exceptions.ConnectionError:
        return "❌ Erro de conexão com a PokeAPI. Verifique sua internet."
    except Exception as e:
        return f"❌ Erro ao buscar '{nome}': {str(e)}"


@tool
def buscar_fraquezas_tipo(tipo: str) -> str:
    """Busca as relações de dano de um tipo específico.
    Mostra contra quais tipos é forte, fraco, resistente e imune.

    Args:
        tipo: Nome do tipo em inglês (ex: 'fire', 'water', 'grass', 'electric', 'dragon')

    Returns:
        Relações de dano completas do tipo.
    """
    tipo_lower = tipo.strip().lower()
    try:
        r = requests.get(f"{BASE_URL}/type/{tipo_lower}", timeout=10)
        if r.status_code == 404:
            return f"❌ Tipo '{tipo}' não existe. Tipos válidos: normal, fire, water, grass, electric, ice, fighting, poison, ground, flying, psychic, bug, rock, ghost, dragon, dark, steel, fairy."
        r.raise_for_status()
        data = r.json()

        dr = data["damage_relations"]
        resultado = {
            "tipo": tipo_lower,
            "causa_dano_dobro_em": [t["name"] for t in dr["double_damage_to"]],
            "recebe_dano_dobro_de": [t["name"] for t in dr["double_damage_from"]],
            "causa_metade_dano_em": [t["name"] for t in dr["half_damage_to"]],
            "recebe_metade_dano_de": [t["name"] for t in dr["half_damage_from"]],
            "nao_causa_dano_em": [t["name"] for t in dr["no_damage_to"]],
            "imune_a": [t["name"] for t in dr["no_damage_from"]],
        }
        return json.dumps(resultado, ensure_ascii=False, indent=2)

    except requests.exceptions.ConnectionError:
        return "❌ Erro de conexão com a PokeAPI."
    except Exception as e:
        return f"❌ Erro ao buscar tipo '{tipo}': {str(e)}"


@tool
def buscar_movimento(nome_movimento: str) -> str:
    """Busca detalhes de um movimento/ataque específico.
    Retorna poder, precisão, PP, tipo, classe de dano e efeito.

    Args:
        nome_movimento: Nome do movimento em inglês (ex: 'thunderbolt', 'flamethrower', 'ice-beam')

    Returns:
        Dados completos do movimento.
    """
    nome_lower = nome_movimento.strip().lower().replace(" ", "-")
    try:
        r = requests.get(f"{BASE_URL}/move/{nome_lower}", timeout=10)
        if r.status_code == 404:
            return f"❌ Movimento '{nome_movimento}' não encontrado. Verifique o nome em inglês."
        r.raise_for_status()
        data = r.json()

        # Buscar efeito em inglês
        efeito = ""
        for entry in data.get("effect_entries", []):
            if entry["language"]["name"] == "en":
                efeito = entry.get("short_effect", entry.get("effect", ""))
                break

        resultado = {
            "nome": data["name"].replace("-", " ").title(),
            "tipo": data["type"]["name"],
            "classe": data["damage_class"]["name"],  # physical, special, status
            "poder": data["power"],
            "precisao": data["accuracy"],
            "pp": data["pp"],
            "prioridade": data["priority"],
            "efeito": efeito,
        }
        return json.dumps(resultado, ensure_ascii=False, indent=2)

    except requests.exceptions.ConnectionError:
        return "❌ Erro de conexão com a PokeAPI."
    except Exception as e:
        return f"❌ Erro ao buscar movimento '{nome_movimento}': {str(e)}"


@tool
def buscar_habilidade(nome_habilidade: str) -> str:
    """Busca detalhes de uma habilidade (ability) de Pokémon.
    Retorna o efeito e quais Pokémon podem ter essa habilidade.

    Args:
        nome_habilidade: Nome da habilidade em inglês (ex: 'intimidate', 'levitate', 'static')

    Returns:
        Descrição do efeito e lista de Pokémon com essa habilidade.
    """
    nome_lower = nome_habilidade.strip().lower().replace(" ", "-")
    try:
        r = requests.get(f"{BASE_URL}/ability/{nome_lower}", timeout=10)
        if r.status_code == 404:
            return f"❌ Habilidade '{nome_habilidade}' não encontrada."
        r.raise_for_status()
        data = r.json()

        efeito = ""
        for entry in data.get("effect_entries", []):
            if entry["language"]["name"] == "en":
                efeito = entry.get("short_effect", entry.get("effect", ""))
                break

        # Lista de pokémon com essa habilidade (max 10)
        pokemons = [p["pokemon"]["name"].title() for p in data.get("pokemon", [])[:10]]

        resultado = {
            "nome": data["name"].replace("-", " ").title(),
            "efeito": efeito,
            "pokemons_com_essa_habilidade": pokemons,
        }
        return json.dumps(resultado, ensure_ascii=False, indent=2)

    except requests.exceptions.ConnectionError:
        return "❌ Erro de conexão com a PokeAPI."
    except Exception as e:
        return f"❌ Erro ao buscar habilidade '{nome_habilidade}': {str(e)}"


@tool
def buscar_cadeia_evolucao(nome: str) -> str:
    """Busca a cadeia evolutiva completa de um Pokémon.
    Mostra todas as evoluções possíveis e condições para evoluir.

    Args:
        nome: Nome do Pokémon (ex: 'charmander', 'eevee', 'pikachu')

    Returns:
        Cadeia evolutiva completa.
    """
    nome_lower = nome.strip().lower()
    try:
        # Primeiro buscar a species para pegar o evolution_chain
        r = requests.get(f"{BASE_URL}/pokemon-species/{nome_lower}", timeout=10)
        if r.status_code == 404:
            return f"❌ Pokémon '{nome}' não encontrado."
        r.raise_for_status()
        species_data = r.json()

        evo_url = species_data["evolution_chain"]["url"]
        r2 = requests.get(evo_url, timeout=10)
        r2.raise_for_status()
        evo_data = r2.json()

        # Parse recursivo da cadeia
        def parse_chain(chain):
            result = {"pokemon": chain["species"]["name"].title(), "evolui_para": []}
            for evo in chain.get("evolves_to", []):
                details = evo.get("evolution_details", [{}])
                trigger = details[0].get("trigger", {}).get("name", "desconhecido") if details else "desconhecido"
                min_level = details[0].get("min_level") if details else None

                evo_info = {
                    "pokemon": evo["species"]["name"].title(),
                    "metodo": trigger,
                }
                if min_level:
                    evo_info["nivel_minimo"] = min_level

                # Recursão para evoluções adicionais
                sub_evos = parse_chain(evo)
                if sub_evos["evolui_para"]:
                    evo_info["evolui_para"] = sub_evos["evolui_para"]

                result["evolui_para"].append(evo_info)
            return result

        cadeia = parse_chain(evo_data["chain"])
        return json.dumps(cadeia, ensure_ascii=False, indent=2)

    except requests.exceptions.ConnectionError:
        return "❌ Erro de conexão com a PokeAPI."
    except Exception as e:
        return f"❌ Erro ao buscar evolução de '{nome}': {str(e)}"


@tool
def buscar_natureza(nome_natureza: str) -> str:
    """Busca os efeitos de uma natureza (nature) nos stats do Pokémon.
    Mostra qual stat aumenta (+10%) e qual diminui (-10%).

    Args:
        nome_natureza: Nome da natureza em inglês (ex: 'adamant', 'modest', 'jolly', 'timid')

    Returns:
        Stats afetados pela natureza.
    """
    nome_lower = nome_natureza.strip().lower()
    try:
        r = requests.get(f"{BASE_URL}/nature/{nome_lower}", timeout=10)
        if r.status_code == 404:
            return f"❌ Natureza '{nome_natureza}' não encontrada."
        r.raise_for_status()
        data = r.json()

        resultado = {
            "nome": data["name"].title(),
            "stat_aumentado": data["increased_stat"]["name"] if data["increased_stat"] else "nenhum (natureza neutra)",
            "stat_diminuido": data["decreased_stat"]["name"] if data["decreased_stat"] else "nenhum (natureza neutra)",
        }
        return json.dumps(resultado, ensure_ascii=False, indent=2)

    except requests.exceptions.ConnectionError:
        return "❌ Erro de conexão com a PokeAPI."
    except Exception as e:
        return f"❌ Erro ao buscar natureza '{nome_natureza}': {str(e)}"
