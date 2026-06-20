# Respostas — Conversa com o Professor (10/06)

## 1. Área de aplicação

Jornalismo / Geração Automática de Títulos de Notícias.

O sistema recebe o corpo de um artigo jornalístico e gera automaticamente um título para ele — sem título original, sem supervisão humana. A frase mais central identificada pelo TextRank serve de base para o título gerado.

- **Redações:** acelerar o processo editorial gerando sugestões de título para jornalistas
- **Newsletters:** titular automaticamente artigos curados sem título próprio
- **Indexação de acervos:** gerar títulos para documentos digitalizados sem cabeçalho

---

## 2. Problema a resolver

Escrever um bom título de notícia exige identificar a informação mais central do texto — tarefa que consome tempo do jornalista e que pode ser automatizada.

O problema técnico é: dado o corpo de um artigo, **qual é a frase que melhor o representa?** Essa frase, possivelmente ajustada por uma heurística de comprimento, se torna o título gerado. O sistema opera sem supervisão — não precisa de pares (artigo, título) para treinar.

---

## 3. Input — dados de entrada

- **Formato:** textos em formato livre (strings / arquivos `.txt`)
- **Tipo:** dados reais — artigos de notícias de datasets públicos (ex: CNN/DailyMail, CSTNews)
- Dados fictícios gerados por LLM poderão ser usados como complemento para casos de teste

---

## 4. Modelagem do grafo

| Elemento | Descrição |
|---|---|
| **Vértices** | Cada frase do texto |
| **Arestas** | Conexão entre duas frases semanticamente relacionadas |
| **Peso** | Número de palavras em comum após remoção de stopwords e stemming, normalizado pelo tamanho das frases |
| **Tipo** | Grafo não-direcionado e ponderado |

Arestas com peso abaixo de um limiar são descartadas para evitar um grafo denso demais.

**Algoritmo principal:** TextRank (variante do PageRank) — ranqueia as frases por importância com base na estrutura do grafo. A frase com maior score é candidata ao título, passando pela heurística de comprimento antes da saída final.

**Fluxo:** Texto → Frases → Stopwords + Stem → Palavras Comuns → Grafo → TextRank → Heurística → Título

---

## 5. Outra estrutura de dados

- **Heap (fila de prioridade):** usada para extrair eficientemente as K frases com maior score após rodar o TextRank — O(log n) por extração
- **Tabela hash (dicionário):** armazena o conjunto de palavras de cada frase (após stopwords e stemming) para calcular a interseção eficientemente
- **Matriz de adjacência (vetor de vetores):** representação interna do grafo de similaridade

---

## 6. Output

Um **título gerado automaticamente** — a frase mais central do artigo, processada pela heurística de comprimento.

**Exemplo:**

*Input (corpo do artigo):*
> "O Brasil registrou recorde de exportações em maio. O agronegócio liderou os resultados, com destaque para a soja e o milho. A balança comercial fechou com superávit de R$ 12 bilhões. Analistas apontam o câmbio favorável como fator principal. O setor industrial também apresentou crescimento moderado."

*Output (título gerado):*
> "Balança comercial fecha com superávit de R$ 12 bilhões em maio"

### Heurística de comprimento

| Caso | Condição | Ação |
|---|---|---|
| Curta demais | ≤ 5 palavras | Mini TextRank sobre top-3 frases → nova candidata |
| Ideal | 5–20 palavras | Usar frase diretamente como título |
| Longa demais | > 20 palavras | Truncar no 1º separador natural (vírgula ou ponto e vírgula) |
