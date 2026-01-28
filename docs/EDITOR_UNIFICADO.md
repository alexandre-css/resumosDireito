# 📝 Editor Unificado - Súmulas e Temas

Editor completo com integração Git para gerenciar súmulas e temas em uma única interface.

## 🚀 Como Usar

### Opção 1: Arquivo .bat (Recomendado)

Simplesmente execute:

```
editor_unificado.bat
```

Isso irá:

- Iniciar o editor de súmulas (porta 8001)
- Iniciar o editor de temas (porta 8002)
- Iniciar o editor unificado (porta 8000)
- Abrir automaticamente no navegador

### Opção 2: Manual

Execute em terminais separados:

**Terminal 1 - Editor de Súmulas:**

```bash
python Scripts/3_servidor_editor.py
```

**Terminal 2 - Editor de Temas:**

```bash
python Scripts/4_servidor_editor_temas.py
```

**Terminal 3 - Editor Unificado:**

```bash
python Scripts/5_editor_unificado.py
```

Acesse: http://localhost:8000

## ✨ Funcionalidades

### 📋 Abas Integradas

- **SÚMULAS**: Editar súmulas do STF, STJ e ECA
- **TEMAS**: Editar temas de repercussão geral e repetitivos

### 🎨 Recursos

- ✅ Alternar entre súmulas e temas em abas
- ✅ Edição completa de todos os campos
- ✅ Campo "Modulação de Efeitos" com quebra de parágrafo
- ✅ Gerar HTML de ambos com um único clique
- ✅ **Commit & Push Git** direto do editor

### 🚀 Git Integration

O botão **"Commit & Push"** automaticamente:

1. ✓ Verifica se há mudanças
2. ✓ Adiciona todos os arquivos (`git add .`)
3. ✓ Faz commit com mensagem automática
4. ✓ Envia para o GitHub (`git push`)

**Mensagem de commit padrão:**

```
Atualização de súmulas e temas - [data/hora]
```

## 📊 Estrutura

```
Scripts/
├── 3_servidor_editor.py       → Editor de Súmulas (porta 8001)
├── 4_servidor_editor_temas.py → Editor de Temas (porta 8002)
└── 5_editor_unificado.py      → Editor Unificado (porta 8000)

editor_unificado.bat           → Inicia tudo automaticamente
```

## 🔧 Portas Utilizadas

| Serviço          | Porta | URL                   |
| ---------------- | ----- | --------------------- |
| Editor Unificado | 8000  | http://localhost:8000 |
| Editor Súmulas   | 8001  | http://localhost:8001 |
| Editor Temas     | 8002  | http://localhost:8002 |

## 💡 Dicas

- Use o **Editor Unificado** para ter tudo em um único lugar
- O botão **"Gerar HTML"** atualiza ambos os arquivos HTML
- O botão **"Commit & Push"** só aparece se o Git estiver configurado
- Todas as edições são salvas automaticamente nos arquivos JSON

## ⚠️ Requisitos

- Python 3.x
- Git configurado no sistema
- Repositório Git inicializado no projeto

## 🎯 Workflow Recomendado

1. Execute `editor_unificado.bat`
2. Edite súmulas ou temas conforme necessário
3. Clique em **"Gerar HTML"** para atualizar os HTMLs
4. Clique em **"Commit & Push"** para enviar ao GitHub
5. ✨ Pronto! Mudanças publicadas automaticamente

---

**Produzido por Alexandre Claudino Simas Santos**  
Secretário Jurídico - Gabinete do Desembargador Alexandre Morais da Rosa  
Tribunal de Justiça de Santa Catarina  
Copyleft (ↄ) 2025
