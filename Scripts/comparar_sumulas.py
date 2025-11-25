# -*- coding: utf-8 -*-
import re
import PyPDF2

print("=== COMPARANDO SÚMULAS DO HTML COM OS PDFs ===\n")

# Ler HTML e extrair súmulas
with open('penal-sumulas.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extrair súmulas do HTML
sumulas_html = {}

# STF
for match in re.finditer(r'<!-- Súmula (\d+)/STF -->(.*?)</div>\s*(?=<!-- Súmula|\s*</div>\s*</div>\s*</div>|<!-- SÚMULAS DO STJ)', html, re.DOTALL):
    numero = match.group(1)
    conteudo = match.group(2)
    texto_match = re.search(r'<p class="text-sm text-gray-700 italic text-justify">(.*?)</p>', conteudo, re.DOTALL)
    if texto_match:
        texto = texto_match.group(1).strip()
        texto = re.sub(r'\s+', ' ', texto)  # Normalizar espaços
        sumulas_html[f'STF-{numero}'] = texto

print(f"Extraídas {len([k for k in sumulas_html.keys() if k.startswith('STF')])} súmulas do STF do HTML")

# STJ
for match in re.finditer(r'<!-- Súmula (\d+)/STJ -->(.*?)</div>\s*(?=<!-- Súmula|\s*</div>\s*</div>\s*</div>)', html, re.DOTALL):
    numero = match.group(1)
    conteudo = match.group(2)
    texto_match = re.search(r'<p class="text-sm text-gray-700 italic text-justify">(.*?)</p>', conteudo, re.DOTALL)
    if texto_match:
        texto = texto_match.group(1).strip()
        texto = re.sub(r'\s+', ' ', texto)
        sumulas_html[f'STJ-{numero}'] = texto

print(f"Extraídas {len([k for k in sumulas_html.keys() if k.startswith('STJ')])} súmulas do STJ do HTML")

# ECA
for match in re.finditer(r'<!-- Súmula (\d+)/ECA -->(.*?)</div>\s*(?=<!-- Súmula|\s*</div>\s*</div>\s*</div>)', html, re.DOTALL):
    numero = match.group(1)
    conteudo = match.group(2)
    texto_match = re.search(r'<p class="text-sm text-gray-700 italic text-justify">(.*?)</p>', conteudo, re.DOTALL)
    if texto_match:
        texto = texto_match.group(1).strip()
        texto = re.sub(r'\s+', ' ', texto)
        sumulas_html[f'ECA-{numero}'] = texto

print(f"Extraídas {len([k for k in sumulas_html.keys() if k.startswith('ECA')])} súmulas do ECA do HTML\n")

# Ler PDFs
def extrair_texto_pdf(caminho):
    with open(caminho, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        texto = ''
        for page in reader.pages:
            texto += page.extract_text() + '\n'
    return texto

# Extrair súmulas dos PDFs
print("Lendo PDFs...\n")

# STF
texto_stf = extrair_texto_pdf('Assets/SÚMULAS DO STF - Penal, Processo Penal e Execução Penal (2025.2).pdf')
# STJ
texto_stj = extrair_texto_pdf('Assets/SÚMULAS DO STJ - Penal e Processo Penal.pdf')
# ECA
texto_eca = extrair_texto_pdf('Assets/SÚMULAS DO STJ - ECA.pdf')

# Função para limpar e normalizar texto
def normalizar(texto):
    texto = texto.lower()
    texto = re.sub(r'\s+', ' ', texto)
    texto = re.sub(r'["""]', '"', texto)
    texto = texto.replace(''', "'").replace(''', "'")
    return texto.strip()

# Comparar
diferencas = []

print("=== VERIFICANDO DIFERENÇAS ===\n")

# Verificar apenas uma amostra para teste
for chave in sorted(sumulas_html.keys())[:5]:
    tribunal, numero = chave.split('-')
    texto_html = normalizar(sumulas_html[chave])
    
    if tribunal == 'STF':
        texto_pdf = texto_stf
    elif tribunal == 'STJ':
        texto_pdf = texto_stj
    else:
        texto_pdf = texto_eca
    
    # Procurar o número da súmula no PDF
    pattern = f'súmula.*?{numero}[^0-9]'
    match = re.search(pattern, normalizar(texto_pdf), re.IGNORECASE | re.DOTALL)
    
    if match:
        # Extrair contexto
        inicio = match.end()
        contexto = normalizar(texto_pdf[inicio:inicio+500])
        
        print(f"\n{chave}:")
        print(f"HTML: {texto_html[:100]}...")
        print(f"PDF:  {contexto[:100]}...")

print("\n\nScript de teste concluído. Executando análise completa...")
