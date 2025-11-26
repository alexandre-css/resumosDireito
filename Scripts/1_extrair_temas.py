#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para converter CSVs de Temas em JSON
"""

import csv
import json
import os
from datetime import datetime

def ler_csv_temas_stf(arquivo_csv):
    """Lê CSV de Temas de Repercussão Geral (STF)"""
    temas = []
    
    with open(arquivo_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            # Limpar keys de BOM ou espaços
            row = {k.strip('\ufeff').strip(): v for k, v in row.items()}
            
            tema = {
                'numero': int(row['Tema']),
                'titulo': '',
                'tese': row['Tese'].strip(),
                'comentario': '',
                'cor': 'blue',
                'chips': []
            }
            temas.append(tema)
    
    return sorted(temas, key=lambda x: x['numero'])

def ler_csv_temas_stj(arquivo_csv):
    """Lê CSV de Temas Repetitivos (STJ)"""
    temas = []
    
    with open(arquivo_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            # Limpar keys de BOM ou espaços
            row = {k.strip('\ufeff').strip(): v for k, v in row.items()}
            
            # Pular linhas vazias
            if not row.get('Tema') or not row['Tema'].strip():
                continue
            
            comentario = row.get('Observação', '').strip()
            if comentario == '-':
                comentario = ''
            
            tema = {
                'numero': int(row['Tema']),
                'titulo': '',
                'tese': row.get('Tese', row.get('Tese ', '')).strip(),
                'comentario': comentario,
                'cor': 'blue',
                'chips': []
            }
            temas.append(tema)
    
    return sorted(temas, key=lambda x: x['numero'])

def salvar_json(dados, arquivo, tribunal):
    """Salva dados em JSON"""
    estrutura = {
        'tribunal': tribunal,
        'total': len(dados),
        'temas': dados
    }
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(estrutura, f, ensure_ascii=False, indent=2)
    
    print(f'✓ {tribunal}: {len(dados)} temas salvos em {arquivo}')

def main():
    print('='*80)
    print('EXTRATOR DE TEMAS - CSV → JSON')
    print('='*80)
    print()
    
    # Diretórios
    csv_dir = 'Data/Tabelas Temas'
    json_dir = 'Data'
    
    # Arquivos
    csv_stf = os.path.join(csv_dir, 'TemasRepercussaoGeralPenalCSV.csv')
    csv_stj = os.path.join(csv_dir, 'TemasRepetitivosPenalCSV.csv')
    
    json_stf = os.path.join(json_dir, 'temas_stf.json')
    json_stj = os.path.join(json_dir, 'temas_stj.json')
    
    # Processar STF
    print('1. Processando Temas de Repercussão Geral (STF)...')
    temas_stf = ler_csv_temas_stf(csv_stf)
    salvar_json(temas_stf, json_stf, 'STF')
    print()
    
    # Processar STJ
    print('2. Processando Temas Repetitivos (STJ)...')
    temas_stj = ler_csv_temas_stj(csv_stj)
    salvar_json(temas_stj, json_stj, 'STJ')
    print()
    
    print('='*80)
    print(f'✓ CONCLUÍDO!')
    print(f'  Total: {len(temas_stf) + len(temas_stj)} temas')
    print('='*80)

if __name__ == '__main__':
    main()
