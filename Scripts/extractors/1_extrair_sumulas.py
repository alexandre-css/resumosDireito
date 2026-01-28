# -*- coding: utf-8 -*-
"""
Extrai súmulas do HTML atual e converte para JSON
Versão simplificada usando regex
"""
import json
import re

def extrair_sumulas_html(arquivo_html):
    """Extrai súmulas do HTML usando regex"""
    with open(arquivo_html, 'r', encoding='utf-8') as f:
        html = f.read()
    
    sumulas = {
        'stf': [],
        'stj': [],
        'eca': []
    }
    
    # Padrão para encontrar comentários e cards (melhorado)
    # Procura desde o comentário até o próximo comentário ou fim da seção
    pattern = r'<!-- Súmula (?:Vinculante )?(\d+)/(STF|STJ|ECA) -->\s*<div[^>]*?class="([^"]*)"[^>]*>(.*?)(?=<!-- Súmula|<script>)'
    
    matches = re.finditer(pattern, html, re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        numero = int(match.group(1))
        tribunal = match.group(2).lower()
        classes = match.group(3)
        card_html = match.group(4)
        
        # Detectar vinculante
        vinculante = 'Vinculante' in match.group(0)
        
        # Extrair título
        titulo_match = re.search(r'<h4[^>]*>([^<]+)</h4>', card_html)
        titulo = titulo_match.group(1).strip() if titulo_match else ''
        
        # Extrair texto - pegar o parágrafo com text-sm e italic e text-justify
        # Para vinculantes o texto está em branco (text-white), para normais em cinza (text-gray)
        texto_matches = re.findall(r'<p\s+class="[^"]*text-sm[^"]*text-justify[^"]*">([^<]+(?:<[^>]+>[^<]*</[^>]+>)*[^<]*)</p>', card_html, re.DOTALL)
        texto = ''
        if texto_matches:
            # Pegar o último parágrafo que não é nota (notas têm bg-)
            for t in texto_matches:
                if 'bg-' not in t:
                    texto = re.sub(r'<[^>]+>', '', t)
                    texto = re.sub(r'\s+', ' ', texto).strip()
        
        # Extrair cor da borda - procurar por border-{cor}-
        cor = 'blue'  # padrão
        cor_match = re.search(r'border-([a-z]+)-(?:500|600|700|900)', classes)
        if cor_match:
            cor = cor_match.group(1)
        else:
            # Para gradientes, procurar from-{cor}-
            cor_match = re.search(r'from-([a-z]+)-(?:500|700)', classes)
            if cor_match:
                cor = cor_match.group(1)
        
        # Extrair chips
        chips = []
        if vinculante:
            chips.append('VINCULANTE')
        
        chip_matches = re.findall(r'px-3 py-1 rounded-full[^>]*>([^<]+)</div>', card_html)
        for chip_text in chip_matches:
            chip_clean = chip_text.strip()
            if chip_clean and chip_clean not in chips and chip_clean != titulo:
                chips.append(chip_clean)
        
        # Extrair nota
        nota_match = re.search(r'<p class="text-xs bg-[^"]+">(.+?)</p>', card_html, re.DOTALL)
        nota = ''
        if nota_match:
            nota = re.sub(r'<[^>]+>', '', nota_match.group(1))
            nota = re.sub(r'\s+', ' ', nota).strip()
        
        sumula = {
            'numero': numero,
            'titulo': titulo,
            'texto': texto,
            'cor': cor,
            'vinculante': vinculante,
            'chips': chips,
            'nota': nota if nota else None
        }
        
        sumulas[tribunal].append(sumula)
    
    # Ordenar por número
    for tribunal in sumulas:
        sumulas[tribunal].sort(key=lambda x: x['numero'])
    
    return sumulas

def salvar_json(sumulas_dict, diretorio='Data'):
    """Salva súmulas em arquivos JSON"""
    import os
    os.makedirs(diretorio, exist_ok=True)
    
    for tribunal, lista in sumulas_dict.items():
        arquivo = f'{diretorio}/{tribunal}.json'
        # Remover notas None antes de salvar
        for s in lista:
            if s.get('nota') is None:
                del s['nota']
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump({
                'tribunal': tribunal.upper(),
                'total': len(lista),
                'sumulas': lista
            }, f, ensure_ascii=False, indent=2)
        print(f'✓ {arquivo}: {len(lista)} súmulas')

if __name__ == '__main__':
    print("Extraindo súmulas do HTML...\n")
    
    try:
        # Usar public/public\sumulas.html por padrão
        arquivo = 'public/public\sumulas.html'
        sumulas = extrair_sumulas_html(arquivo)
        salvar_json(sumulas)
        
        print("\n✓ Total extraído:")
        print(f"  STF: {len(sumulas['stf'])} súmulas")
        print(f"  STJ: {len(sumulas['stj'])} súmulas")
        print(f"  ECA: {len(sumulas['eca'])} súmulas")
        print("\nArquivos JSON criados em: Data/")
        
    except Exception as erro:
        print(f"✗ Erro: {erro}")
        import traceback
        traceback.print_exc()
