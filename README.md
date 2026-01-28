# 📚 ResumosDireito - Sistema Profissional de Súmulas e Temas

Sistema completo de gerenciamento de súmulas e temas jurídicos com interface web moderna, editor unificado e integração Git.

[![Version](https://img.shields.io/badge/version-2.0-blue.svg)](https://github.com/alexandre-css/resumosDireito)
[![License](https://img.shields.io/badge/license-Copyleft-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)](https://www.python.org/)

---

## ✨ Funcionalidades Principais

- 📋 **Súmulas**: STF (77), STJ (99), ECA (9)
- 🎯 **Temas**: Repercussão Geral (STF) e Repetitivos (STJ)
- 🎨 **Interface Moderna**: Design responsivo com Tailwind CSS
- 🔄 **Editor Unificado**: Gerencie súmulas e temas em uma única interface
- 🚀 **Git Integration**: Commit e push direto do editor
- 📱 **Responsivo**: Funciona em desktop, tablet e mobile
- 🔍 **Busca Avançada**: Pesquisa inteligente com filtros
- 📦 **Categorização**: Sistema de cores e categorias customizáveis
- 📝 **Campo "Modulação de Efeitos"**: Com suporte a quebras de parágrafo

---

## 📁 Estrutura do Projeto (v2.0)

```
resumosDireito/
├── 📄 README.md                    # Este arquivo
├── 📄 ESTRUTURA_PROJETO.md         # Documentação da estrutura
├── 📄 .gitignore                   # Arquivos ignorados
├── 🚀 editor_unificado.bat         # ⭐ PRINCIPAL - Editor completo
│
├── 📂 public/                      # Páginas HTML públicas
│   ├── index.html                  # Página inicial
│   ├── penal.html                  # Seção penal
│   ├── civil.html                  # Seção civil
│   ├── sumulas.html                # Visualização de súmulas
│   ├── temas.html                  # Visualização de temas
│   ├── acordao.html                # Modelo de acórdão
│   └── honorarios.html             # Calculadora de honorários
│
├── 📂 Data/                        # Dados JSON
│   ├── categorias_cores.json       # Configuração de cores
│   ├── stf.json, stj.json, eca.json # Súmulas
│   └── temas_stf.json, temas_stj.json # Temas
│
├── 📂 Scripts/                     # Scripts Python organizados
│   ├── 📂 generators/              # Geradores de HTML
│   ├── 📂 editors/                 # Servidores de edição
│   ├── 📂 extractors/              # Extratores de dados
│   └── 📂 utils/                   # Utilitários diversos
│
├── 📂 automation/                  # Automação (.bat)
├── 📂 docs/                        # Documentação completa
└── 📂 backup/                      # Backups automáticos
```

📖 **Documentação completa da estrutura**: [ESTRUTURA_PROJETO.md](ESTRUTURA_PROJETO.md)

---

## 🚀 Início Rápido

### **Modo Mais Fácil - Editor Unificado**

1. **Clique duplo em**: `editor_unificado.bat`
2. Aguarde os 3 servidores iniciarem
3. O navegador abrirá automaticamente em `http://localhost:8000`
4. Use as abas para alternar entre **Súmulas** e **Temas**
5. Edite, gere HTML e faça commit/push - tudo em uma interface!

### **Funcionalidades do Editor:**
- ✏️ **Edição completa** de súmulas e temas
- 📋 **Abas integradas** para alternar entre conteúdos
- 🔄 **Gerar HTML** de ambos com um clique
- 🚀 **Commit & Push Git** direto da interface
- 🎨 **Categorização visual** com cores
- 📝 **Campo de modulação de efeitos** com quebras de parágrafo

---

## 📖 Documentação

### **Guias Principais:**
- 📘 [ESTRUTURA_PROJETO.md](ESTRUTURA_PROJETO.md) - Organização e arquitetura
- 📗 [EDITOR_UNIFICADO.md](docs/EDITOR_UNIFICADO.md) - Editor completo
- 📙 [GUIA_SUMULAS.md](docs/GUIA_SUMULAS.md) - Documentação de súmulas
- 📕 [CONFIGURAR_CATEGORIAS.md](docs/CONFIGURAR_CATEGORIAS.md) - Sistema de cores

### **Recursos Adicionais:**
- [EXEMPLO_ADICIONAR_SUMULA.md](docs/EXEMPLO_ADICIONAR_SUMULA.md)
- [RECURSOS_EDITOR.md](docs/RECURSOS_EDITOR.md)
- [SISTEMA_PRONTO.md](docs/SISTEMA_PRONTO.md)

---

## 🛠️ Tecnologias

- **Frontend**: HTML5, Tailwind CSS, JavaScript vanilla
- **Backend**: Python 3.8+
- **Dados**: JSON
- **Versionamento**: Git
- **Automação**: Batch scripts (.bat)

---

## 🎨 Cores e Categorias

### **Categorias Principais:**
- 🔴 Vermelho - Júri
- 🟠 Laranja - Execução Penal  
- 🟢 Verde - Crimes Geral
- 🔷 Teal - Processual
- 💙 Índigo - Prescrição
- 🟣 Roxo - Competência
- 🌸 Rosa - Aplicação da Pena

**+ 15 cores adicionais disponíveis!**

---

## 📋 Formato dos Dados

### **Súmula:**
```json
{
    "numero": 701,
    "titulo": "Tema da Súmula",
    "texto": "Texto completo da súmula.",
    "cor": "blue",
    "vinculante": false,
    "chips": ["ALTERADA"],
    "modulacao_efeitos": "Informações sobre modulação (opcional)",
    "nota": "Comentário adicional (opcional)"
}
```

### **Tema:**
```json
{
    "numero": 1234,
    "titulo": "Título do Tema",
    "tese": "Tese fixada pelo tribunal.",
    "cor": "indigo",
    "chips": [],
    "modulacao_efeitos": "Modulação de efeitos (opcional)",
    "comentario": "Observações (opcional)"
}
```

---

## 🔧 Scripts e Automação

### **Arquivos .bat (Automação):**
- `editor_unificado.bat` - ⭐ Editor completo (RECOMENDADO)
- `gerar_html.bat` - Gera todos os HTMLs
- `automation/editor_sumulas.bat` - Apenas súmulas
- `automation/editor_temas.bat` - Apenas temas

### **Scripts Python:**

#### **Geradores** (`Scripts/generators/`)
- `1_gerar_html_sumulas.py` - Gera HTML de súmulas
- `1_gerar_html_temas.py` - Gera HTML de temas

#### **Editores** (`Scripts/editors/`)
- `2_servidor_sumulas.py` - Servidor de edição de súmulas
- `2_servidor_temas.py` - Servidor de edição de temas
- `3_servidor_unificado.py` - Servidor do editor unificado

#### **Utilitários** (`Scripts/utils/`)
- `analise_completa.py` - Análise do sistema
- `atualizar_textos.py` - Atualização em massa
- `corrigir_sumulas.py` - Correções automáticas

---

## 🔄 Workflow Recomendado

1. Execute `editor_unificado.bat`
2. Edite súmulas ou temas no navegador
3. Clique em **"Gerar HTML"** para atualizar visualização
4. Clique em **"Commit & Push"** para enviar ao GitHub
5. ✨ Deploy automático (se configurado)

---

## 🚀 Reorganização do Projeto

### **Primeira vez após atualização?**

Execute (apenas uma vez):
```batch
reorganizar_projeto.bat
```

Isso irá:
1. Criar nova estrutura de diretórios
2. Mover arquivos para locais corretos
3. Atualizar referências automaticamente

---

## 🔄 Backup Automático

Toda vez que você gera o HTML, um backup automático é criado em **`backup/`**

---

## 💡 Dicas

✅ Use o **editor web** para facilitar
✅ Backups são automáticos
✅ JSONs são versionados no Git
✅ Arquivos organizados por função

---

## 🆘 Suporte

Dúvidas? Consulte `docs/GUIA_SUMULAS.md`

---

**Desenvolvido com ❤️ para ResumosDireito**
Resumos de Direito interativos
