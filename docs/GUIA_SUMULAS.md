# 📋 Sistema de Gerenciamento de Súmulas

Sistema simples para adicionar, editar e remover súmulas sem mexer diretamente no HTML.

---

## 🎯 Como Funciona

1. **Súmulas são armazenadas em arquivos JSON** (fácil de editar)
2. **Um script Python gera o HTML automaticamente** dos JSONs
3. **Você só precisa editar os JSONs e rodar o script!**

---

## 📁 Estrutura de Arquivos

```
Data/
├── stf.json       # Súmulas do STF
├── stj.json       # Súmulas do STJ (Penal)
└── eca.json       # Súmulas do STJ (ECA)

Scripts/
├── gerar_sumulas_html.py           # Gera HTML dos JSONs
└── extrair_sumulas_para_json.py    # Converte HTML para JSON
```

---

## ✏️ Como Adicionar uma Nova Súmula

### Passo 1: Editar o JSON

Abra o arquivo JSON do tribunal desejado (exemplo: `Data/stj.json`):

```json
{
    "tribunal": "STJ",
    "total": 99,
    "sumulas": [
        {
            "numero": 701,
            "titulo": "Novo Tema",
            "texto": "Texto completo da súmula aqui.",
            "cor": "blue",
            "vinculante": false,
            "chips": []
        }
    ]
}
```

### Passo 2: Adicionar a Nova Súmula

Adicione um novo objeto no array `sumulas`:

```json
{
    "numero": 702,
    "titulo": "Título da Nova Súmula",
    "texto": "Texto completo da nova súmula.",
    "cor": "green",
    "vinculante": false,
    "chips": []
}
```

### Passo 3: Gerar o HTML

No terminal:

```bash
cd "C:\Apps\Resumos Direito\resumosDireito"
python Scripts/gerar_sumulas_html.py
```

Pronto! O HTML foi atualizado automaticamente! ✓

---

## 🎨 Campos do JSON

### Campos Obrigatórios:

| Campo    | Tipo   | Descrição            | Exemplo           |
| -------- | ------ | -------------------- | ----------------- |
| `numero` | number | Número da súmula     | `701`             |
| `titulo` | string | Título/tema resumido | `"Confissão"`     |
| `texto`  | string | Texto completo       | `"O réu pode..."` |

### Campos Opcionais:

| Campo        | Tipo    | Padrão   | Descrição               | Exemplo                                 |
| ------------ | ------- | -------- | ----------------------- | --------------------------------------- |
| `cor`        | string  | `"blue"` | Cor do card             | `"red"`, `"green"`, `"purple"`          |
| `vinculante` | boolean | `false`  | Se é vinculante (STF)   | `true`                                  |
| `chips`      | array   | `[]`     | Etiquetas               | `["ALTERADA"]`, `["SUPERADA EM PARTE"]` |
| `nota`       | string  | -        | Nota explicativa abaixo | `"Lei 14.843/2024..."`                  |

---

## 🎨 Cores Disponíveis

-   `red`, `blue`, `green`, `purple`, `pink`, `indigo`
-   `yellow`, `orange`, `teal`, `cyan`, `lime`, `emerald`
-   `violet`, `fuchsia`, `rose`, `sky`, `amber`, `gray`

---

## 🏷️ Chips Disponíveis

| Chip                | Cor     | Uso                          |
| ------------------- | ------- | ---------------------------- |
| `VINCULANTE`        | Amarelo | Súmulas vinculantes (STF)    |
| `ALTERADA`          | Azul    | Súmula foi alterada          |
| `SUPERADA EM PARTE` | Laranja | Súmula parcialmente superada |

---

## 📝 Exemplos Práticos

### Exemplo 1: Súmula Simples

```json
{
    "numero": 700,
    "titulo": "Prescrição",
    "texto": "A prescrição regula-se pela pena concretizada.",
    "cor": "blue",
    "vinculante": false,
    "chips": []
}
```

### Exemplo 2: Súmula Vinculante (STF)

```json
{
    "numero": 70,
    "titulo": "Algemas",
    "texto": "Só é lícito o uso de algemas em caso de resistência...",
    "cor": "red",
    "vinculante": true,
    "chips": ["VINCULANTE"]
}
```

### Exemplo 3: Súmula com Nota

```json
{
    "numero": 439,
    "titulo": "Exame Criminológico",
    "texto": "Admite-se o exame criminológico pelas peculiaridades...",
    "cor": "blue",
    "vinculante": false,
    "chips": ["SUPERADA EM PARTE"],
    "nota": "A Lei 14.843/2024 tornou obrigatório o exame criminológico."
}
```

### Exemplo 4: Súmula Alterada

```json
{
    "numero": 545,
    "titulo": "Confissão",
    "texto": "A confissão do autor possibilita a atenuação...",
    "cor": "red",
    "vinculante": false,
    "chips": ["ALTERADA"]
}
```

---

## 🔧 Comandos Úteis

### Gerar HTML das Súmulas

```bash
python Scripts/gerar_sumulas_html.py
```

### Extrair Súmulas do HTML para JSON

```bash
python Scripts/extrair_sumulas_para_json.py
```

---

## ⚠️ Dicas Importantes

1. **Sempre faça backup** antes de gerar o HTML (o script já faz isso automaticamente)
2. **Mantenha a ordem crescente** dos números no JSON (não obrigatório, mas ajuda)
3. **Use aspas duplas** no JSON, não aspas simples
4. **Não esqueça vírgulas** entre objetos do array
5. **Teste localmente** antes de fazer commit

---

## 🆘 Solução de Problemas

### Erro: "JSON inválido"

-   Verifique se todas as vírgulas estão corretas
-   Verifique se as aspas são duplas (`"`)
-   Use um validador JSON online

### Súmula não aparece

-   Verifique se o número está correto
-   Rode o script novamente
-   Verifique se salvou o JSON

### Cores não aparecem

-   Use apenas cores da lista de cores disponíveis
-   Cores customizadas precisam estar no Tailwind CSS

---

## 📞 Fluxo de Trabalho Recomendado

1. ✏️ **Editar JSON** → Adicionar/modificar súmula
2. 💾 **Salvar** → Salvar arquivo JSON
3. ▶️ **Rodar Script** → `python Scripts/gerar_sumulas_html.py`
4. 👀 **Revisar** → Abrir `penal-sumulas.html` no navegador
5. ✅ **Commit** → Se estiver OK, fazer commit no Git

---

## 🎓 Notas Finais

-   O sistema mantém backup automático do HTML anterior
-   Os JSONs são versionados no Git (histórico completo)
-   É possível reverter qualquer mudança facilmente
-   A estrutura é escalável para adicionar novos tribunais

**Qualquer dúvida, consulte este guia ou entre em contato!** 🚀
