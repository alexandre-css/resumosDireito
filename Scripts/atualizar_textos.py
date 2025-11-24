# -*- coding: utf-8 -*-
import re

# Carregar súmulas dos TXTs
def carregar_stf():
    with open('Súmulas/SÚMULAS DO STF.txt', 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    sumulas = {}
    matches = re.finditer(r'SÚMULA\s+(?:VINCULANTE\s+)?N?[ºÃO°]?\s*(\d+)\s*\n+(.*?)(?=\nSÚMULA|\Z)', conteudo, re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        numero = int(match.group(1))
        texto = match.group(2).strip()
        texto = re.sub(r'\s+', ' ', texto)
        sumulas[numero] = texto
    
    return sumulas

def carregar_stj():
    with open('Súmulas/SÚMULAS DO STJ.txt', 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    sumulas = {}
    matches = re.finditer(r'Súmula\s+(\d+)\s*[-–]\s*(.*?)(?=Súmula\s+\d+\s*[-–]|\Z)', conteudo, re.DOTALL)
    
    for match in matches:
        numero = int(match.group(1))
        texto = match.group(2).strip()
        texto = re.sub(r'\s+', ' ', texto)
        sumulas[numero] = texto
    
    return sumulas

def carregar_eca():
    with open('Súmulas/SÚMULAS DO STJ (ECA).txt', 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    sumulas = {}
    matches = re.finditer(r'Súmula\s+(\d+)\s*[-–]\s*(.*?)(?=Súmula\s+\d+\s*[-–]|\Z)', conteudo, re.DOTALL)
    
    for match in matches:
        numero = int(match.group(1))
        texto = match.group(2).strip()
        texto = re.sub(r'\s+', ' ', texto)
        sumulas[numero] = texto
    
    return sumulas

print("Carregando súmulas dos TXTs...")
stf_txt = carregar_stf()
stj_txt = carregar_stj()
eca_txt = carregar_eca()

print(f"STF: {len(stf_txt)}")
print(f"STJ: {len(stj_txt)}")
print(f"ECA: {len(eca_txt)}")

# Ler HTML
with open('penal-sumulas.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Substituir súmulas STF
print("\nSubstituindo STF...")
for num, texto_correto in stf_txt.items():
    # Encontrar o comentário da súmula
    pattern = rf'(<!-- Súmula {num}/STF -->.*?<p class="text-sm text-gray-700 italic text-justify">)(.*?)(</p>)'
    
    def substituir(match):
        return match.group(1) + texto_correto + match.group(3)
    
    html_novo = re.sub(pattern, substituir, html, flags=re.DOTALL)
    if html_novo != html:
        print(f"  Atualizada: {num}")
        html = html_novo

# Substituir súmulas STJ
print("\nSubstituindo STJ...")
for num, texto_correto in stj_txt.items():
    pattern = rf'(<!-- Súmula {num}/STJ -->.*?<p class="text-sm text-gray-700 italic text-justify">)(.*?)(</p>)'
    
    def substituir(match):
        return match.group(1) + texto_correto + match.group(3)
    
    html_novo = re.sub(pattern, substituir, html, flags=re.DOTALL)
    if html_novo != html:
        print(f"  Atualizada: {num}")
        html = html_novo

# Substituir súmulas ECA
print("\nSubstituindo ECA...")
for num, texto_correto in eca_txt.items():
    pattern = rf'(<!-- Súmula {num}/ECA -->.*?<p class="text-sm text-gray-700 italic text-justify">)(.*?)(</p>)'
    
    def substituir(match):
        return match.group(1) + texto_correto + match.group(3)
    
    html_novo = re.sub(pattern, substituir, html, flags=re.DOTALL)
    if html_novo != html:
        print(f"  Atualizada: {num}")
        html = html_novo

# Salvar
with open('penal-sumulas.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\nCONCLUÍDO!")
