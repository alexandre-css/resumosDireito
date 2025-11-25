# ⚙️ Guia de Configuração de Categorias

## 📝 O que é?

Sistema que permite você **editar o nome das categorias** de cada cor, personalizando completamente o sistema de organização das súmulas.

---

## 🚀 Como Usar

### Método 1: Pelo Editor (Recomendado)

1. Execute **`editor.bat`**
2. Clique no botão **"⚙️ Configurar Categorias"** (canto superior direito)
3. Edite os nomes das categorias
4. Clique em **"💾 Salvar Configurações"**
5. Reinicie o editor para ver as mudanças

### Método 2: Atalho Direto

1. Clique duplo em **`configurar_categorias.bat`**
    - ⚠️ Certifique-se de que o editor está rodando!
2. Edite as categorias
3. Salve
4. Reinicie o editor

### Método 3: Edição Manual

1. Abra **`Data/categorias_cores.json`**
2. Edite o JSON:
    ```json
    {
      "red": "Seu Nome de Categoria",
      "blue": "Outra Categoria",
      ...
    }
    ```
3. Salve o arquivo
4. Reinicie o editor

---

## 🎨 Cores Disponíveis

Total: **21 cores** configuráveis

| Cor | Código    | Padrão                |
| --- | --------- | --------------------- |
| 🔴  | `red`     | Júri                  |
| 🟠  | `orange`  | Execução Penal        |
| 🟢  | `green`   | Crimes Geral          |
| 🔷  | `teal`    | Processual            |
| 💙  | `indigo`  | Prescrição            |
| 🟣  | `purple`  | Competência           |
| 🌸  | `pink`    | Aplicação da Pena     |
| 🌹  | `rose`    | Perdão Judicial       |
| 🔵  | `blue`    | Outros                |
| 💠  | `cyan`    | Recursos              |
| 🟢  | `lime`    | Ação Penal            |
| 🟡  | `amber`   | Medidas Cautelares    |
| 💚  | `emerald` | Crimes Contra Ordem   |
| 🟣  | `violet`  | Nulidades             |
| 🌺  | `fuchsia` | Suspensão Condicional |
| ☁️  | `sky`     | Garantias             |
| 🟡  | `yellow`  | Prova                 |
| ⚫  | `slate`   | Especial              |
| ⚫  | `zinc`    | Transação             |
| 🟤  | `stone`   | Crimes Tributários    |
| ⚫  | `gray`    | Diversos              |

---

## 💡 Exemplos de Uso

### Exemplo 1: Adaptar para Direito Civil

```json
{
    "red": "Obrigações",
    "blue": "Contratos",
    "green": "Família",
    "purple": "Sucessões",
    "orange": "Responsabilidade Civil"
}
```

### Exemplo 2: Direito Trabalhista

```json
{
    "red": "CLT",
    "blue": "Acidente de Trabalho",
    "green": "Rescisão",
    "purple": "Jornada",
    "orange": "FGTS"
}
```

### Exemplo 3: Direito Administrativo

```json
{
    "red": "Licitações",
    "blue": "Servidores",
    "green": "Contratos Administrativos",
    "purple": "Responsabilidade",
    "orange": "Processo Administrativo"
}
```

---

## 🔄 Restaurar Padrão

Na página de configuração, clique em **"🔄 Restaurar Padrão"** para voltar aos nomes originais.

---

## ⚠️ Importante

-   ✅ As alterações são salvas em **`Data/categorias_cores.json`**
-   ✅ Você precisa **reiniciar o editor** para ver as mudanças
-   ✅ O arquivo JSON é versionado no Git
-   ✅ Backup recomendado antes de grandes alterações

---

## 🎯 Fluxo Completo

```
1. Abrir Editor (editor.bat)
   ↓
2. Clicar em "⚙️ Configurar Categorias"
   ↓
3. Editar nomes das categorias
   ↓
4. Salvar
   ↓
5. Fechar editor (Ctrl+C)
   ↓
6. Abrir editor novamente
   ↓
7. ✅ Dropdown mostra novas categorias!
```

---

## 📁 Arquivos Envolvidos

-   **`Data/categorias_cores.json`** - Arquivo de configuração
-   **`Scripts/3_servidor_editor.py`** - Servidor (carrega categorias)
-   **`configurar_categorias.bat`** - Atalho rápido
-   **`editor.bat`** - Editor principal

---

## 🆘 Problemas?

### Categorias não aparecem no editor

-   **Solução:** Reinicie o editor (feche e abra novamente)

### Botão "Configurar" não funciona

-   **Solução:** Certifique-se que o editor está rodando

### Arquivo não salva

-   **Solução:** Verifique permissões da pasta `Data/`

---

**Personalize seu sistema de súmulas! 🎨**
