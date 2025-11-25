# -*- coding: utf-8 -*-
import re

print("=== LISTANDO TODAS AS SÚMULAS DO HTML ===\n")

with open('penal-sumulas.html', 'r', encoding='utf-8') as f:
    html = f.read()

sumulas = []

# Extrair todas as súmulas
for match in re.finditer(r'<!-- Súmula (\d+)/(STF|STJ|ECA) -->(.*?)</div>\s*\n\s*(?=<!-- Súmula|\s*</div>)', html, re.DOTALL):
    numero = match.group(1)
    tribunal = match.group(2)
    conteudo = match.group(3)
    
    # Extrair título
    titulo_match = re.search(r'<h4[^>]*>(.*?)</h4>', conteudo)
    titulo = titulo_match.group(1) if titulo_match else "Sem título"
    
    # Extrair texto
    texto_match = re.search(r'<p class="text-sm text-gray-700 italic text-justify">(.*?)</p>', conteudo, re.DOTALL)
    if texto_match:
        texto = texto_match.group(1).strip()
        texto = re.sub(r'\s+', ' ', texto)
        sumulas.append((tribunal, int(numero), titulo, texto))

# Ordenar
sumulas.sort(key=lambda x: (x[0], x[1]))

# Salvar em arquivo para revisão
with open('sumulas_para_revisar.txt', 'w', encoding='utf-8') as f:
    tribunal_atual = None
    for tribunal, numero, titulo, texto in sumulas:
        if tribunal != tribunal_atual:
            f.write(f"\n{'='*80}\n")
            f.write(f"SÚMULAS DO {tribunal}\n")
            f.write(f"{'='*80}\n\n")
            tribunal_atual = tribunal
        
        f.write(f"SÚMULA {numero} - {titulo}\n")
        f.write(f"{texto}\n\n")

print(f"Total de súmulas encontradas: {len(sumulas)}")
print(f"  - STF: {len([s for s in sumulas if s[0] == 'STF'])}")
print(f"  - STJ: {len([s for s in sumulas if s[0] == 'STJ'])}")
print(f"  - ECA: {len([s for s in sumulas if s[0] == 'ECA'])}")
print(f"\nArquivo 'sumulas_para_revisar.txt' criado!")
print("Compare manualmente com os PDFs em Assets/")
