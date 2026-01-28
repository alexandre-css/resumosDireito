# -*- coding: utf-8 -*-
import re

print("Adicionando comentários CORRETAMENTE (antes das linhas <div>)...")

with open('penal-public/public\sumulas.html', 'r', encoding='utf-8') as f:
    linhas = f.readlines()

# Encontrar seção STJ
inicio_stj = None
fim_stj = None

for i, linha in enumerate(linhas):
    if 'id="sumulas-stj-penal"' in linha:
        inicio_stj = i
    if '<!-- SÚMULAS DO STJ - ECA -->' in linha and inicio_stj:
        fim_stj = i
        break

print(f"Seção STJ: linhas {inicio_stj+1} até {fim_stj+1}")

# Processar
novas_linhas = []
i = 0

while i < len(linhas):
    linha = linhas[i]
    
    # Se estamos na seção STJ e encontramos um <div seguido de class="bg-white na próxima linha
    if inicio_stj < i < fim_stj and linha.strip() == '<div':
        # Verificar se a próxima linha tem class="bg-white border-l-4
        if i+1 < len(linhas) and 'class="bg-white border-l-4' in linhas[i+1]:
            # Procurar o número da súmula nas próximas linhas
            numero = None
            for j in range(i+1, min(i+15, len(linhas))):
                match = re.search(r'^\s*(\d+)</div>', linhas[j])
                if match:
                    numero = match.group(1)
                    break
            
            if numero:
                # Pegar a indentação da linha do <div
                indentacao = len(linha) - len(linha.lstrip())
                # Adicionar comentário ANTES do <div, com a mesma indentação
                comentario = ' ' * indentacao + f'<!-- Súmula {numero}/STJ -->\n'
                novas_linhas.append(comentario)
                print(f"Comentário adicionado: Súmula {numero}")
            
            # Agora adicionar a linha do <div
            novas_linhas.append(linha)
        else:
            novas_linhas.append(linha)
    else:
        # Adicionar linha normalmente
        novas_linhas.append(linha)
    
    i += 1

# Salvar
with open('penal-public/public\sumulas.html', 'w', encoding='utf-8') as f:
    f.writelines(novas_linhas)

print("\n✓ AGORA SIM! Comentários adicionados ANTES de cada <div>!")
