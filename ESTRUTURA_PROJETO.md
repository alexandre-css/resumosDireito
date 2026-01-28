# 📁 Estrutura do Projeto - ResumosDireito

## 🎯 Princípios de Organização

### 1. **Separação de Responsabilidades**
- Páginas públicas separadas de dados
- Scripts separados por função
- Documentação centralizada

### 2. **Nomenclatura Clara**
- Pastas em minúsculas (exceto Data por compatibilidade)
- Nomes descritivos e autoexplicativos
- Prefixos numéricos para ordem de execução

### 3. **Hierarquia Lógica**
- Nível raiz: apenas arquivos essenciais
- Conteúdo agrupado por tipo e propósito
- Estrutura facilita navegação e manutenção

---

## 📂 Estrutura Atual (Recomendada)

```
resumosDireito/
├── 📄 README.md                    # Documentação principal
├── 📄 .gitignore                   # Arquivos ignorados pelo Git
│
├── 📂 public/                      # ✅ PÁGINAS HTML PÚBLICAS
│   ├── index.html                  # Página inicial
│   ├── penal.html                  # Seção penal
│   ├── civil.html                  # Seção civil
│   ├── sumulas.html                # Visualização de súmulas
│   ├── temas.html                  # Visualização de temas
│   ├── acordao.html                # Modelo de acórdão
│   └── honorarios.html             # Calculadora de honorários
│
├── 📂 Data/                        # ✅ DADOS JSON (mantém nome original)
│   ├── categorias_cores.json       # Configuração de cores
│   ├── stf.json                    # Súmulas STF
│   ├── stj.json                    # Súmulas STJ
│   ├── eca.json                    # Súmulas ECA
│   ├── temas_stf.json              # Temas STF
│   └── temas_stj.json              # Temas STJ
│
├── 📂 Scripts/                     # ✅ SCRIPTS PYTHON
│   ├── 📂 generators/              # Geradores de HTML
│   │   ├── 1_gerar_html_sumulas.py
│   │   └── 1_gerar_html_temas.py
│   │
│   ├── 📂 editors/                 # Servidores de edição
│   │   ├── 2_servidor_sumulas.py
│   │   ├── 2_servidor_temas.py
│   │   └── 3_servidor_unificado.py
│   │
│   ├── 📂 extractors/              # Extratores de dados
│   │   ├── extrair_sumulas.py
│   │   └── extrair_temas.py
│   │
│   └── 📂 utils/                   # Utilitários
│       ├── analise_completa.py
│       ├── atualizar_textos.py
│       └── corrigir_sumulas.py
│
├── 📂 automation/                  # ✅ AUTOMAÇÃO (.BAT)
│   ├── editor_unificado.bat        # Inicia editor unificado
│   ├── editor_sumulas.bat          # Inicia editor de súmulas
│   ├── editor_temas.bat            # Inicia editor de temas
│   ├── gerar_html.bat              # Gera todos os HTMLs
│   └── configurar_categorias.bat   # Configura categorias
│
├── 📂 docs/                        # ✅ DOCUMENTAÇÃO
│   ├── CATEGORIAS_CORES.md
│   ├── CONFIGURAR_CATEGORIAS.md
│   ├── CORES_SUMULAS_POR_TEMA.md
│   ├── EDITOR_UNIFICADO.md
│   ├── EXEMPLO_ADICIONAR_SUMULA.md
│   ├── GUIA_SUMULAS.md
│   ├── LEIA-ME_SUMULAS.md
│   ├── RECURSOS_EDITOR.md
│   └── SISTEMA_PRONTO.md
│
└── 📂 backup/                      # ✅ BACKUPS AUTOMÁTICOS
    ├── sumulas.html.backup_*
    └── temas.html.backup_*
```

---

## 🔄 Plano de Migração (se necessário)

### **Fase 1: Criar Nova Estrutura**
```bash
# Criar diretórios
mkdir public automation

# Criar subdiretórios de scripts
mkdir Scripts\generators Scripts\editors Scripts\extractors
```

### **Fase 2: Mover Arquivos HTML**
```bash
# Mover HTMLs para public/
move *.html public\
move public\README.md .
```

### **Fase 3: Organizar Scripts**
```bash
# Mover para generators/
move Scripts\2_gerar_html.py Scripts\generators\1_gerar_html_sumulas.py
move Scripts\2_gerar_html_temas.py Scripts\generators\1_gerar_html_temas.py

# Mover para editors/
move Scripts\3_servidor_editor.py Scripts\editors\2_servidor_sumulas.py
move Scripts\4_servidor_editor_temas.py Scripts\editors\2_servidor_temas.py
move Scripts\5_editor_unificado.py Scripts\editors\3_servidor_unificado.py

# Mover para extractors/
move Scripts\1_extrair_sumulas.py Scripts\extractors\
move Scripts\1_extrair_temas.py Scripts\extractors\
```

### **Fase 4: Organizar Automação**
```bash
# Mover .bat para automation/
move *.bat automation\
```

### **Fase 5: Atualizar Referências**
- Atualizar caminhos nos scripts Python
- Atualizar caminhos nos arquivos .bat
- Atualizar links nos HTMLs
- Testar todas as funcionalidades

---

## 📋 Checklist de Manutenção

### **Ao Adicionar Novo Arquivo:**
- [ ] HTML público → `public/`
- [ ] Dados JSON → `Data/`
- [ ] Script gerador → `Scripts/generators/`
- [ ] Script editor → `Scripts/editors/`
- [ ] Script utilitário → `Scripts/utils/`
- [ ] Automação .bat → `automation/`
- [ ] Documentação → `docs/`

### **Nomenclatura de Scripts:**
- Prefixo numérico: ordem de execução
- Nome descritivo: função principal
- Sufixo de tipo: `_sumulas`, `_temas`, `_unificado`

### **Exemplo:**
```
1_gerar_html_sumulas.py    # 1 = gerador, nome claro, tipo específico
2_servidor_sumulas.py      # 2 = editor/servidor, nome claro
3_servidor_unificado.py    # 3 = nível superior (unifica 2)
```

---

## 🚀 Benefícios da Estrutura

### **Para Desenvolvedores:**
- ✅ Fácil localização de arquivos
- ✅ Separação clara de responsabilidades
- ✅ Facilita manutenção e expansão
- ✅ Reduz conflitos de merge

### **Para Usuários:**
- ✅ Automação simples via `.bat`
- ✅ HTMLs públicos separados
- ✅ Documentação acessível

### **Para o Projeto:**
- ✅ Aparência profissional
- ✅ Facilita onboarding
- ✅ Preparado para crescimento
- ✅ Segue boas práticas

---

## 📝 Notas Importantes

1. **Pasta `Data/`**: Mantém nome com maiúscula por compatibilidade com scripts existentes
2. **Backups**: Gerados automaticamente pelos scripts, organizados por data
3. **Git**: Arquivos `.bat` e backups podem ser ignorados via `.gitignore`
4. **Documentação**: Centralizada em `docs/`, facilita contribuições

---

**Última atualização:** 28/01/2026  
**Versão:** 2.0  
**Status:** ✅ Estrutura Recomendada Definida
