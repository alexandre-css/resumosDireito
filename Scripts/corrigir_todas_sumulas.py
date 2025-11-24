# -*- coding: utf-8 -*-
import re

def extrair_sumulas_txt_stf(arquivo):
    """Extrai súmulas do arquivo TXT do STF"""
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    sumulas = {}
    # Padrão: SÚMULA Nº 123 ou SÚMULA VINCULANTE Nº 123
    matches = re.finditer(r'SÚMULA\s+(?:VINCULANTE\s+)?N[ºÃO°]\s*(\d+)\s*\n\n?(.*?)(?=\n\nSÚMULA|\Z)', conteudo, re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        numero = int(match.group(1))
        texto = match.group(2).strip()
        # Limpar texto
        texto = re.sub(r'^[A-ZÇÃÍÓÁÂÊÔ\s]+\n+', '', texto)
        texto = re.sub(r'\s+', ' ', texto).strip()
        sumulas[numero] = texto
        print(f"  STF {numero}: {texto[:60]}...")
    
    return sumulas

def extrair_sumulas_txt_stj(arquivo):
    """Extrai súmulas do arquivo TXT do STJ"""
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    sumulas = {}
    # Padrão: Súmula 123 - texto
    matches = re.finditer(r'Súmula\s+(\d+)\s*[-–]\s*(.*?)(?=Súmula\s+\d+\s*[-–]|\Z)', conteudo, re.DOTALL)
    
    for match in matches:
        numero = int(match.group(1))
        texto = match.group(2).strip()
        texto = re.sub(r'\s+', ' ', texto).strip()
        sumulas[numero] = texto
        print(f"  STJ {numero}: {texto[:60]}...")
    
    return sumulas

print("=" * 80)
print("CARREGANDO SUMULAS DOS ARQUIVOS TXT")
print("=" * 80)

print("\nSTF:")
sumulas_stf = extrair_sumulas_txt_stf('Súmulas/SÚMULAS DO STF.txt')
print(f"\nTotal STF: {len(sumulas_stf)}")

print("\nSTJ:")
sumulas_stj = extrair_sumulas_txt_stj('Súmulas/SÚMULAS DO STJ.txt')
print(f"\nTotal STJ: {len(sumulas_stj)}")

print("\nECA:")
sumulas_eca = extrair_sumulas_txt_stj('Súmulas/SÚMULAS DO STJ (ECA).txt')
print(f"\nTotal ECA: {len(sumulas_eca)}")

# Ler HTML
print("\n" + "=" * 80)
print("LENDO HTML")
print("=" * 80)

with open('penal-sumulas.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Substituir súmulas
correcoes = 0

print("\n" + "=" * 80)
print("CORRIGINDO SUMULAS NO HTML")
print("=" * 80)

# Padrão: encontrar cada súmula no HTML
pattern = r'(<!-- Súmula (\d+)/(STF|STJ|ECA) -->.*?<p class="text-sm text-gray-700 italic text-justify">)(.*?)(</p>)'

def substituir_sumula(match):
    global correcoes
    comentario = match.group(1)
    numero = int(match.group(2))
    tribunal = match.group(3)
    texto_html = match.group(4)
    fechamento = match.group(5)
    
    # Limpar texto HTML atual
    texto_html_limpo = re.sub(r'<.*?>', '', texto_html)
    texto_html_limpo = re.sub(r'\s+', ' ', texto_html_limpo).strip().lower()
    
    # Buscar texto correto
    texto_correto = None
    if tribunal == 'STF' and numero in sumulas_stf:
        texto_correto = sumulas_stf[numero]
    elif tribunal == 'STJ' and numero in sumulas_stj:
        texto_correto = sumulas_stj[numero]
    elif tribunal == 'ECA' and numero in sumulas_eca:
        texto_correto = sumulas_eca[numero]
    
    if texto_correto:
        # Comparar
        texto_correto_limpo = texto_correto.lower()
        
        # Calcular similaridade básica
        if texto_html_limpo != texto_correto_limpo:
            # Textos diferentes - corrigir
            correcoes += 1
            print(f"\n[{correcoes}] Corrigindo Sumula {numero}/{tribunal}")
            print(f"  ANTES: {texto_html_limpo[:100]}...")
            print(f"  DEPOIS: {texto_correto_limpo[:100]}...")
            
            # Retornar com texto correto
            return comentario + texto_correto + fechamento
    
    # Manter original
    return match.group(0)

# Substituir todas
html_corrigido = re.sub(pattern, substituir_sumula, html, flags=re.DOTALL)

# Salvar
with open('penal-sumulas.html', 'w', encoding='utf-8') as f:
    f.write(html_corrigido)

print("\n" + "=" * 80)
print("CONCLUIDO")
print("=" * 80)
print(f"\nTotal de correcoes: {correcoes}")
print("\nArquivo atualizado: penal-sumulas.html")
