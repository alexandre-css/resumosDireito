# 🎯 RESUMO RÁPIDO - Sistema de Súmulas

## Para Adicionar/Editar Súmulas:

### 1️⃣ Edite o JSON

-   **STF**: Abra `Data/stf.json`
-   **STJ**: Abra `Data/stj.json`
-   **ECA**: Abra `Data/eca.json`

### 2️⃣ Adicione a súmula

```json
{
    "numero": 999,
    "titulo": "Título",
    "texto": "Texto completo da súmula.",
    "cor": "blue",
    "vinculante": false,
    "chips": []
}
```

### 3️⃣ Atualize o HTML

**Opção A - Clique duplo:**

-   Clique em `atualizar_sumulas.bat`

**Opção B - Terminal:**

```bash
python Scripts/gerar_sumulas_html.py
```

## ✅ Pronto!

---

## 📚 Documentação Completa

Consulte **`GUIA_SUMULAS.md`** para documentação detalhada.

Consulte **`EXEMPLO_ADICIONAR_SUMULA.md`** para um exemplo passo-a-passo.

---

## 🎨 Campos Principais

| Campo    | Exemplo             | Obrigatório        |
| -------- | ------------------- | ------------------ |
| `numero` | `701`               | ✅                 |
| `titulo` | `"Prescrição"`      | ✅                 |
| `texto`  | `"A prescrição..."` | ✅                 |
| `cor`    | `"blue"`            | ❌ (padrão: blue)  |
| `chips`  | `["ALTERADA"]`      | ❌ (padrão: vazio) |
| `nota`   | `"Lei 14.843..."`   | ❌                 |

---

## 🏷️ Chips Disponíveis

-   `VINCULANTE` (amarelo)
-   `ALTERADA` (azul)
-   `SUPERADA EM PARTE` (laranja)

---

## ⚠️ Importante

-   O script cria backup automático do HTML
-   Súmulas são ordenadas por número automaticamente
-   Use aspas duplas (`"`) no JSON
