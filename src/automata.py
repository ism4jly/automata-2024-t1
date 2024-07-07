"""Implementação de autômatos finitos."""

from typing import List, Dict, Tuple

class AutomataException(Exception):
    pass
    
def load_automata(filename: str) -> Tuple[List[str], List[str], Dict[Tuple[str, str], str], str, List[str]]:
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()

        if len(lines) < 5:
            raise AutomataException("Formato do arquivo incorreto ou incompleto.")

        alfabeto = lines[0].split()
        estados = lines[1].split()
        finais = lines[2].split()
        inicial = lines[3]
        
        delta = {}
        for line in lines[4:]:
            parts = line.split()
            if len(parts) != 3:
                raise AutomataException(f"Transição inválida: {line}")
            origem, simbolo, destino = parts
            if origem not in estados or destino not in estados or simbolo not in alfabeto:
                raise AutomataException(f"Transição inválida: {line}")
            delta[(origem, simbolo)] = destino
        
        return estados, alfabeto, delta, inicial, finais

    except FileNotFoundError:
        raise AutomataException(f"Arquivo {filename} não encontrado.")
    except Exception as e:
        raise AutomataException(f"Erro ao carregar o autômato: {str(e)}")
        
def process(automata: Tuple[List[str], List[str], Dict[Tuple[str, str], str], str, List[str]], 
            words: List[str]) -> Dict[str, str]:
    estados, alfabeto, delta, inicial, finais = automata
    results = {}

    for word in words:
        if any(symbol not in alfabeto for symbol in word):
            results[word] = 'INVÁLIDA'
            continue
        
        current_state = inicial
        for symbol in word:
            if (current_state, symbol) in delta:
                current_state = delta[(current_state, symbol)]
            else:
                current_state = None
                break
        
        if current_state is None:
            results[word] = 'REJEITA'
        elif current_state in F:
            results[word] = 'ACEITA'
        else:
            results[word] = 'REJEITA'

    return results
