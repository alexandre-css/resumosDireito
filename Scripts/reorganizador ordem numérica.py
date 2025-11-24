# -*- coding: utf-8 -*-
import re

print("Reorganizando súmulas do STJ de forma SIMPLES e SEGURA...")

with open('penal-sumulas.html', 'r', encoding='utf-8') as f:
    linhas = f.readlines()

# Encontrar início e fim da seção STJ
inicio_stj = None
fim_stj = None

for i, linha in enumerate(linhas):
    if 'id="sumulas-stj-penal"' in linha:
        inicio_stj = i
    if '<!-- SÚMULAS DO STJ - ECA -->' in linha and inicio_stj:
        fim_stj = i
        break

# Encontrar onde começam os cards
inicio_cards = None
for i in range(inicio_stj, fim_stj):
    if 'gap-4 p-6">' in linhas[i]:
        inicio_cards = i + 1
        break

# Encontrar onde terminam (antes dos </div></div></div>)
fim_cards = None
for i in range(fim_stj-1, inicio_cards, -1):
    if '</div>' in linhas[i] and '</div>' in linhas[i-1] and '</div>' in linhas[i-2]:
        fim_cards = i - 2
        break

print(f"Seção de cards: linha {inicio_cards+1} até {fim_cards+1}")

# Extrair todos os cards com seus comentários
cards = []
i = inicio_cards

while i < fim_cards:
    linha = linhas[i]
    
    # Se encontrou um comentário de súmula
    if '<!-- Súmula' in linha and '/STJ -->' in linha:
        match = re.search(r'<!-- Súmula (\d+)/STJ -->', linha)
        if match:
            numero = int(match.group(1))
            inicio_card = i
            
            # Encontrar o fim deste card (até o próximo comentário ou fim)
            fim_card = None
            for j in range(i+1, fim_cards):
                if '<!-- Súmula' in linhas[j]:
                    # Voltar até achar </div> seguido de linha vazia ou nova linha
                    for k in range(j-1, i, -1):
                        if '</div>' in linhas[k]:
                            fim_card = k + 1
                            break
                    break
            
            # Se não achou (é o último card)
            if not fim_card:
                fim_card = fim_cards
            
            # Extrair card completo
            card_completo = linhas[inicio_card:fim_card]
            cards.append((numero, card_completo))
            print(f"Card {numero}: linhas {inicio_card+1}-{fim_card}")
            
            i = fim_card
        else:
            i += 1
    else:
        i += 1

print(f"\nTotal: {len(cards)} cards extraídos")

# Ordenar
cards.sort(key=lambda x: x[0])
print(f"Ordenando de {cards[0][0]} até {cards[-1][0]}")

# Reconstruir arquivo
novo = linhas[:inicio_cards]

# Adicionar linha vazia inicial se necessário
if linhas[inicio_cards].strip():
    novo.append('\n')

# Adicionar cards ordenados
for i, (numero, card_linhas) in enumerate(cards):
    novo.extend(card_linhas)
    # Adicionar linha vazia entre cards se necessário
    if i < len(cards) - 1 and card_linhas[-1].strip():
        novo.append('\n')

# Adicionar fechamento
novo.extend(linhas[fim_cards:fim_stj])
novo.extend(linhas[fim_stj:])

# Salvar
with open('penal-sumulas.html', 'w', encoding='utf-8') as f:
    f.writelines(novo)

print(f"\n✓ Súmulas reorganizadas!")
