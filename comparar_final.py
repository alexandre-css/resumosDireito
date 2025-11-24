# -*- coding: utf-8 -*-
import re
from difflib import SequenceMatcher

def limpar_texto(texto):
    """Remove espaços extras, quebras de linha e normaliza o texto"""
    texto = re.sub(r'\s+', ' ', texto)
    texto = texto.strip().lower()
    texto = re.sub(r'["""]', '"', texto)
    return texto

def extrair_sumulas_txt_stf(arquivo):
    """Extrai súmulas do arquivo TXT do STF"""
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    sumulas = {}
    # Padrão: SÚMULA Nº 123 seguido do texto
    matches = re.finditer(r'SÚMULA\s+(?:VINCULANTE\s+)?N[ºÃO°]\s*(\d+)\s*\n\n?(.*?)(?=\n\nSÚMULA|\Z)', conteudo, re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        numero = int(match.group(1))
        texto = match.group(2).strip()
        # Remover título de seção se houver
        texto = re.sub(r'^[A-ZÇÃÍÓÁÂÊÔ\s]+\n+', '', texto)
        sumulas[numero] = limpar_texto(texto)
    
    return sumulas

def extrair_sumulas_txt_stj(arquivo):
    """Extrai súmulas do arquivo TXT do STJ"""
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    sumulas = {}
    # Padrão: Súmula 123 - texto (até próxima súmula ou fim)
    matches = re.finditer(r'Súmula\s+(\d+)\s*[-–]\s*(.*?)(?=Súmula\s+\d+\s*[-–]|\Z)', conteudo, re.DOTALL)
    
    for match in matches:
        numero = int(match.group(1))
        texto = match.group(2).strip()
        sumulas[numero] = limpar_texto(texto)
    
    return sumulas

def extrair_sumulas_html(arquivo):
    """Extrai súmulas do HTML"""
    with open(arquivo, 'r', encoding='utf-8') as f:
        html = f.read()
    
    sumulas_stf = {}
    sumulas_stj = {}
    sumulas_eca = {}
    
    # Extrair súmulas com comentários
    # Padrão: <!-- Súmula XXX/TRIBUNAL --> seguido do card
    pattern = r'<!-- Súmula (\d+)/(STF|STJ|ECA) -->.*?<p class="text-sm text-gray-700 italic text-justify">(.*?)</p>'
    
    matches = re.finditer(pattern, html, re.DOTALL)
    
    for match in matches:
        numero = int(match.group(1))
        tribunal = match.group(2)
        texto = match.group(3)
        # Remover tags HTML
        texto = re.sub(r'<.*?>', '', texto)
        texto = limpar_texto(texto)
        
        if tribunal == 'STF':
            sumulas_stf[numero] = texto
        elif tribunal == 'STJ':
            sumulas_stj[numero] = texto
        elif tribunal == 'ECA':
            sumulas_eca[numero] = texto
    
    return sumulas_stf, sumulas_stj, sumulas_eca

def similaridade(texto1, texto2):
    """Calcula similaridade entre dois textos"""
    return SequenceMatcher(None, texto1, texto2).ratio()

print("=" * 80)
print("COMPARAÇÃO DE SÚMULAS - HTML vs TXT")
print("=" * 80)

# Carregar súmulas dos TXTs
print("\nCarregando súmulas dos arquivos TXT...")
sumulas_txt_stf = extrair_sumulas_txt_stf('Súmulas/SÚMULAS DO STF.txt')
sumulas_txt_stj = extrair_sumulas_txt_stj('Súmulas/SÚMULAS DO STJ.txt')
sumulas_txt_eca = extrair_sumulas_txt_stj('Súmulas/SÚMULAS DO STJ (ECA).txt')

print(f"  STF: {len(sumulas_txt_stf)} súmulas")
print(f"  STJ: {len(sumulas_txt_stj)} súmulas")
print(f"  ECA: {len(sumulas_txt_eca)} súmulas")

# Carregar súmulas do HTML
print("\nCarregando súmulas do HTML...")
sumulas_html_stf, sumulas_html_stj, sumulas_html_eca = extrair_sumulas_html('penal-sumulas.html')

print(f"  STF: {len(sumulas_html_stf)} súmulas")
print(f"  STJ: {len(sumulas_html_stj)} súmulas")
print(f"  ECA: {len(sumulas_html_eca)} súmulas")

# Comparar
diferencas = []

print("\n" + "=" * 80)
print("COMPARANDO STF...")
print("=" * 80)

for num in sumulas_html_stf:
    if num in sumulas_txt_stf:
        html_texto = sumulas_html_stf[num]
        txt_texto = sumulas_txt_stf[num]
        sim = similaridade(html_texto, txt_texto)
        
        if sim < 0.85:  # Menos de 85% similar
            diferencas.append({
                'tribunal': 'STF',
                'numero': num,
                'html': html_texto[:200],
                'txt': txt_texto[:200],
                'similaridade': sim
            })
            print(f"\nDIFERENCIA na Sumula {num}/STF (Similaridade: {sim:.1%})")
            print(f"   HTML: {html_texto[:150]}...")
            print(f"   TXT:  {txt_texto[:150]}...")
    else:
        print(f"\nERRO: Sumula {num}/STF nao encontrada no TXT")

print("\n" + "=" * 80)
print("COMPARANDO STJ...")
print("=" * 80)

for num in sumulas_html_stj:
    if num in sumulas_txt_stj:
        html_texto = sumulas_html_stj[num]
        txt_texto = sumulas_txt_stj[num]
        sim = similaridade(html_texto, txt_texto)
        
        if sim < 0.85:
            diferencas.append({
                'tribunal': 'STJ',
                'numero': num,
                'html': html_texto[:200],
                'txt': txt_texto[:200],
                'similaridade': sim
            })
            print(f"\nDIFERENCIA na Sumula {num}/STJ (Similaridade: {sim:.1%})")
            print(f"   HTML: {html_texto[:150]}...")
            print(f"   TXT:  {txt_texto[:150]}...")
    else:
        print(f"\nERRO: Sumula {num}/STJ nao encontrada no TXT")

print("\n" + "=" * 80)
print("COMPARANDO ECA...")
print("=" * 80)

for num in sumulas_html_eca:
    if num in sumulas_txt_eca:
        html_texto = sumulas_html_eca[num]
        txt_texto = sumulas_txt_eca[num]
        sim = similaridade(html_texto, txt_texto)
        
        if sim < 0.85:
            diferencas.append({
                'tribunal': 'ECA',
                'numero': num,
                'html': html_texto[:200],
                'txt': txt_texto[:200],
                'similaridade': sim
            })
            print(f"\nDIFERENCIA na Sumula {num}/ECA (Similaridade: {sim:.1%})")
            print(f"   HTML: {html_texto[:150]}...")
            print(f"   TXT:  {txt_texto[:150]}...")
    else:
        print(f"\nERRO: Sumula {num}/ECA nao encontrada no TXT")

# Resumo
print("\n" + "=" * 80)
print("RESUMO")
print("=" * 80)
print(f"\nTotal de diferenças encontradas: {len(diferencas)}")

if diferencas:
    print("\nLISTA DE SUMULAS COM DIFERENCAS:")
    for diff in diferencas:
        print(f"  - Sumula {diff['numero']}/{diff['tribunal']} (Similaridade: {diff['similaridade']:.1%})")
else:
    print("\nTodas as sumulas estao corretas!")
