# -*- coding: utf-8 -*-
import re

print("Adicionando comentários nas súmulas do STF...")

with open('penal-sumulas.html', 'r', encoding='utf-8') as f:
    linhas = f.readlines()

# Encontrar seção STF (começa com id="sumulas-stf" e vai até "SÚMULAS DO STJ")
inicio_stf = None
fim_stf = None

for i, linha in enumerate(linhas):
    if 'id="sumulas-stf"' in linha:
        inicio_stf = i
        print(f"Início STF encontrado na linha {i+1}")
    if '<!-- SÚMULAS DO STJ' in linha and inicio_stf and not fim_stf:
        fim_stf = i
        print(f"Fim STF encontrado na linha {i+1}")
        break

if not inicio_stf or not fim_stf:
    print("ERRO: Seção STF não encontrada")
    exit(1)

print(f"Seção STF: linhas {inicio_stf+1} até {fim_stf+1}")

# Processar
novas_linhas = []
i = 0

while i < len(linhas):
    linha = linhas[i]
    
    # Se estamos na seção STF e encontramos um <div seguido de class="bg-white na próxima linha
    if inicio_stf < i < fim_stf and linha.strip() == '<div':
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
                # Adicionar comentário ANTES do <div
                comentario = ' ' * indentacao + f'<!-- Súmula {numero}/STF -->\n'
                novas_linhas.append(comentario)
                print(f"Comentário adicionado: Súmula {numero}/STF")
            
            # Adicionar a linha do <div
            novas_linhas.append(linha)
        else:
            novas_linhas.append(linha)
    else:
        # Adicionar linha normalmente
        novas_linhas.append(linha)
    
    i += 1

# Salvar
with open('penal-sumulas.html', 'w', encoding='utf-8') as f:
    f.writelines(novas_linhas)

print("\n✓ Comentários adicionados nas súmulas do STF!")
