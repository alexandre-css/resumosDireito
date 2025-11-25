# 📂 Estrutura Organizada do Projeto

```
📦 resumosDireito/
│
├── 🌐 PÁGINAS WEB
│   ├── index.html ...................... Página inicial do site
│   ├── sumulas.html .................... Página de súmulas penais
│   └── honorarios.html ................. Calculadora de honorários
│
├── ⚡ EXECUTÁVEIS PRINCIPAIS
│   ├── editor.bat ...................... [PRINCIPAL] Editor web de súmulas
│   └── gerar_html.bat .................. Regenera HTML das súmulas
│
├── 📊 DADOS (JSON)
│   └── Data/
│       ├── stf.json .................... 77 Súmulas do STF
│       ├── stj.json .................... 99 Súmulas do STJ
│       └── eca.json .................... 9 Súmulas ECA/STJ
│
├── 🐍 SCRIPTS PYTHON
│   └── Scripts/
│       ├── 1_extrair_sumulas.py ........ Extrai HTML → JSON
│       ├── 2_gerar_html.py ............. Gera JSON → HTML
│       └── 3_servidor_editor.py ........ Servidor web do editor
│
├── 📖 DOCUMENTAÇÃO
│   └── docs/
│       ├── GUIA_SUMULAS.md ............. Documentação completa
│       ├── LEIA-ME_SUMULAS.md .......... Guia rápido de uso
│       ├── EXEMPLO_ADICIONAR_SUMULA.md . Tutorial passo-a-passo
│       └── SISTEMA_PRONTO.md ........... Visão geral do sistema
│
├── 💾 BACKUPS AUTOMÁTICOS
│   └── backup/
│       ├── sumulas.html.backup_*..... Backups do HTML
│       └── Súmulas/ ................... Arquivos TXT originais
│
├── 🔧 UTILITÁRIOS (Antigos/Auxiliares)
│   └── utils/
│       ├── analise_completa.py
│       ├── atualizar_textos.py
│       ├── comentarios_stf.py
│       ├── comparar_sumulas.py
│       └── ... (outros scripts auxiliares)
│
├── 📄 ARQUIVOS DE CONFIGURAÇÃO
│   ├── README.md ....................... Este arquivo
│   ├── .gitignore
│   └── .venv/ .......................... Ambiente virtual Python
```

---

## 🎯 Fluxo de Trabalho Principal

```
┌─────────────────┐
│  editor.bat     │ ← CLIQUE AQUI para editar súmulas
└────────┬────────┘
         │
         ├─> Abre navegador em http://localhost:8080
         │
         ├─> Editar súmulas visualmente
         │   ├─ Adicionar nova
         │   ├─ Editar existente
         │   └─ Excluir
         │
         ├─> Salva automaticamente em Data/*.json
         │
         ├─> Botão "Gerar HTML" executa:
         │   └─> Scripts/2_gerar_html.py
         │       ├─ Cria backup/sumulas.html.backup_*
         │       └─ Gera novo sumulas.html
         │
         └─> ✅ Pronto!
```

---

## 📚 Quando Usar Cada Arquivo

### Uso Diário

-   **`editor.bat`** → Sempre! Interface completa para tudo

### Uso Avançado

-   **`gerar_html.bat`** → Se editou JSON manualmente
-   **`1_extrair_sumulas.py`** → Extrair de HTML antigo
-   **`2_gerar_html.py`** → Gerar HTML (usado pelo editor)

### Consulta

-   **`docs/LEIA-ME_SUMULAS.md`** → Referência rápida
-   **`docs/GUIA_SUMULAS.md`** → Documentação completa

---

## ✨ Principais Melhorias da Organização

✅ **Pastas temáticas** (docs, backup, utils)
✅ **Nomes claros** (sumulas.html, editor.bat)
✅ **Scripts numerados** (ordem de execução)
✅ **Backups organizados** (pasta dedicada)
✅ **Documentação centralizada** (pasta docs)
✅ **Arquivos antigos** (movidos para utils)

---

## 🚀 Próximos Passos

1. Use `editor.bat` para editar súmulas
2. Consulte `docs/` quando precisar
3. Backups estão sempre em `backup/`
4. Tudo funciona perfeitamente!

---

**Estrutura limpa e organizada! 🎉**
