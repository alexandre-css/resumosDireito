# EXEMPLO PRÁTICO: Adicionar Súmula 720/STJ

## Cenário

Você quer adicionar a nova Súmula 720 do STJ sobre "Detração Penal"

## Passo a Passo

### 1. Abrir o arquivo

Abra: `Data/stj.json`

### 2. Localizar o final do array de súmulas

Procure pelo último objeto e adicione uma vírgula

### 3. Adicionar a nova súmula

```json
{
    "numero": 720,
    "titulo": "Detração Penal",
    "texto": "A detração penal prevista no art. 42 do Código Penal aplica-se às penas restritivas de direitos substitutas de pena privativa de liberdade.",
    "cor": "teal",
    "vinculante": false,
    "chips": []
}
```

### 4. Salvar o arquivo (Ctrl+S)

### 5. Rodar o script

No PowerShell:

```powershell
cd "C:\Apps\Resumos Direito\resumosDireito"
python Scripts/gerar_sumulas_html.py
```

### 6. Resultado esperado

```
================================================================================
GERADOR DE HTML DE SÚMULAS
================================================================================

1. Carregando súmulas dos JSONs...
   ✓ STF: 77 súmulas
   ✓ STJ: 100 súmulas  ← Note que aumentou!
   ✓ ECA: 9 súmulas

2. Gerando HTML...
   ✓ HTML gerado

3. Salvando arquivo...
✓ Backup criado: penal-public/public\sumulas.html.backup_20251125_HHMMSS
✓ HTML gerado: penal-public/public\sumulas.html

================================================================================
✓ CONCLUÍDO COM SUCESSO!
================================================================================
```

### 7. Verificar

Abra `penal-public/public\sumulas.html` no navegador e procure pela Súmula 720!

---

## ⚡ Atalho Rápido

Crie um arquivo `atualizar_sumulas.bat` com:

```batch
@echo off
cd "C:\Apps\Resumos Direito\resumosDireito"
python Scripts/gerar_sumulas_html.py
pause
```

Depois, basta clicar duas vezes nele para atualizar! 🚀
