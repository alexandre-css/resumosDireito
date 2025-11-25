# 📚 ResumosDireito - Sistema de Súmulas

Sistema completo de gerenciamento de súmulas jurídicas com interface web e geração automática de HTML.

---

## 📁 Estrutura do Projeto

```
resumosDireito/
├── 📄 index.html              # Página inicial
├── 📄 sumulas.html            # Página de súmulas penais
├── 📄 honorarios.html         # Calculadora de honorários
├──
├── 🔧 editor.bat              # Inicia editor web (PRINCIPAL)
├── 🔧 gerar_html.bat          # Gera HTML das súmulas
│
├── 📁 Data/                   # Arquivos JSON das súmulas
│   ├── stf.json              # 77 súmulas do STF
│   ├── stj.json              # 99 súmulas do STJ
│   └── eca.json              # 9 súmulas do ECA
│
├── 📁 Scripts/                # Scripts Python principais
│   ├── 1_extrair_sumulas.py  # Extrai HTML → JSON
│   ├── 2_gerar_html.py       # Gera JSON → HTML
│   └── 3_servidor_editor.py  # Servidor web do editor
│
├── 📁 docs/                   # Documentação
│   ├── GUIA_SUMULAS.md       # Guia completo
│   ├── LEIA-ME_SUMULAS.md    # Resumo rápido
│   ├── EXEMPLO_ADICIONAR_SUMULA.md
│   └── SISTEMA_PRONTO.md
│
├── 📁 backup/                 # Backups automáticos
└── 📁 utils/                  # Scripts auxiliares antigos
```

---

## 🚀 Como Usar

### 1️⃣ **Editar Súmulas (RECOMENDADO)**

Clique duplo em: **`editor.bat`**

Isso abre uma interface web completa onde você pode:

-   ✏️ Editar súmulas existentes
-   ➕ Adicionar novas súmulas
-   🗑️ Excluir súmulas
-   🚀 Gerar HTML com um clique

**URL:** http://localhost:8080

---

### 2️⃣ **Editar Manualmente (Avançado)**

1. Abra `Data/stf.json` (ou stj/eca)
2. Edite o JSON
3. Execute: **`gerar_html.bat`**

---

## 📝 Formato do JSON

```json
{
    "numero": 701,
    "titulo": "Tema da Súmula",
    "texto": "Texto completo da súmula.",
    "cor": "blue",
    "vinculante": false,
    "chips": ["ALTERADA"],
    "nota": "Observação opcional"
}
```

---

## 🎨 Cores e Categorias

### Categorias Principais:

-   🔴 **Vermelho** - Júri
-   🟠 **Laranja** - Execução Penal
-   🟢 **Verde** - Crimes Geral
-   🔷 **Teal** - Processual
-   💙 **Índigo** - Prescrição
-   🟣 **Roxo** - Competência
-   🌸 **Rosa** - Aplicação da Pena
-   🌹 **Rosa-forte** - Perdão Judicial

### Mais 15 categorias adicionais disponíveis!

Veja todas as cores no editor ou em `docs/GUIA_SUMULAS.md`

---

## 🏷️ Chips Disponíveis

-   **VINCULANTE** (amarelo) - Súmulas vinculantes do STF
-   **ALTERADA** (azul) - Súmula foi alterada
-   **SUPERADA EM PARTE** (laranja) - Parcialmente superada

---

## ⚙️ Scripts Disponíveis

| Script                 | Descrição                        |
| ---------------------- | -------------------------------- |
| `editor.bat`           | Inicia editor web interativo     |
| `gerar_html.bat`       | Gera HTML das súmulas            |
| `1_extrair_sumulas.py` | Extrai súmulas do HTML para JSON |
| `2_gerar_html.py`      | Gera HTML a partir dos JSONs     |
| `3_servidor_editor.py` | Servidor web do editor           |

---

## 📚 Documentação

Consulte a pasta **`docs/`** para guias detalhados:

-   **GUIA_SUMULAS.md** - Documentação completa
-   **LEIA-ME_SUMULAS.md** - Guia rápido
-   **EXEMPLO_ADICIONAR_SUMULA.md** - Tutorial passo-a-passo

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
