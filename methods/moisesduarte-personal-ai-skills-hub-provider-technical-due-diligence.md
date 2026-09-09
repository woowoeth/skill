---
name: provider-technical-due-diligence
description: >
  Analisa tecnicamente provedores de pagamentos, Open Finance e infraestrutura
  financeira usando prioritariamente MCP e documentação oficial. Produz análise
  fundamentada, score estimado, riscos e questões em aberto.
---

# Provider Technical Due Diligence

## Objetivo

Avaliar tecnicamente um provedor utilizando suas fontes oficiais e, quando
disponível, seu MCP.

A análise deve determinar:

- modelos de operação disponíveis;
- arquitetura e ciclo de vida das operações;
- idempotência e retries;
- estados e erros;
- comportamento diante de timeouts e resultados indeterminados;
- webhooks;
- conciliação;
- rate limits;
- autenticação e segurança;
- ambientes;
- requisitos Open Finance/BACEN;
- observabilidade e operação.

## Arquivos de referência

Antes de executar a análise, utilizar:

- `references/questionnaire.md` para as dimensões e perguntas da investigação;
- `references/evidence-rules.md` para classificação de evidências e lacunas;
- `references/scoring.md` para notas, pesos, red flags e classificação;
- `references/output-format.md` para estruturar o resultado final.

## Hierarquia de fontes

Priorizar:

1. MCP oficial do provedor;
2. documentação técnica oficial;
3. OpenAPI / Swagger oficial;
4. documentação regulatória oficial referenciada pelo provedor;
5. documentação BACEN / Open Finance;
6. materiais oficiais complementares;
7. informações fornecidas diretamente pelo usuário.

Não utilizar fontes de terceiros para afirmar comportamento da API quando
existir documentação oficial disponível.

## Regras fundamentais

- Priorizar MCP e documentação oficial do provedor.
- Não assumir que uma funcionalidade existe.
- Ausência de documentação não significa ausência de funcionalidade.
- Não inventar endpoints, parâmetros, estados, limites ou garantias.
- Distinguir fatos documentados de inferências.
- Investigar documentação relacionada antes de declarar uma questão como não documentada.
- Não simplesmente percorrer o questionário: cruzar endpoints, entidades, estados,
  erros, webhooks e demais fontes relacionadas.
- Consolidar respostas quando uma descoberta resolver múltiplos questionamentos.
- Gerar questões em aberto apenas para pontos que permanecerem sem resposta após
  a investigação.
- Não confundir retry HTTP, retry de operação, nova operação e retry de webhook.
- Não considerar logs de webhook automaticamente como mecanismo de conciliação.

## Processo

1. Descobrir ferramentas e fontes disponíveis.
2. Identificar produtos e modelos de operação.
3. Mapear entidades, endpoints e ciclos de vida.
4. Executar a investigação descrita em `references/questionnaire.md`.
5. Cruzar as evidências encontradas.
6. Identificar lacunas e inconsistências.
7. Avaliar os critérios conforme `references/scoring.md`.
8. Produzir o resultado conforme `references/output-format.md`.

## Comportamento agentico com MCP

Quando houver MCP disponível:

1. descobrir as ferramentas relevantes;
2. localizar documentação dos produtos;
3. identificar modelos de operação;
4. mapear entidades e fluxos;
5. pesquisar identificadores;
6. pesquisar idempotência;
7. pesquisar estados;
8. pesquisar retries;
9. pesquisar erros;
10. pesquisar timeouts e resultados indeterminados;
11. pesquisar webhooks;
12. pesquisar conciliação;
13. pesquisar polling;
14. pesquisar rate limits;
15. pesquisar autenticação;
16. pesquisar ambientes;
17. pesquisar requisitos regulatórios;
18. pesquisar observabilidade;
19. cruzar resultados;
20. buscar inconsistências;
21. investigar lacunas encontradas;
22. preencher o questionário;
23. calcular score e confiança;
24. identificar red flags;
25. consolidar lacunas;
26. gerar somente as questões que permaneceram realmente em aberto.

Não encerrar a análise após encontrar apenas uma página que pareça responder à questão.

Não utilizar o MCP apenas como busca textual. Explorar relações entre:

- produtos;
- entidades;
- endpoints;
- schemas;
- estados;
- erros;
- eventos;
- limites.

## Princípio principal

Determinar, com base em evidências, se a integração pode ser construída e
operada de forma:

- determinística;
- idempotente;
- recuperável;
- conciliável;
- segura;
- observável;
- escalável;
- testável.

O resultado deve deixar claro:

1. o que sabemos;
2. como sabemos;
3. o que apenas podemos inferir;
4. o que não conseguimos determinar;
5. quais riscos existem;
6. quais questões permanecem em aberto;
7. quais dessas questões podem alterar o score ou a decisão técnica.

## Modos de uso

### Análise individual

É o modo padrão da skill.

A skill analisa um único provedor utilizando todo o crivo técnico definido, produzindo:

- análise fundamentada;
- score técnico;
- nível de confiança;
- riscos e red flags;
- lacunas de documentação;
- questões em aberto.

Exemplo:

> Analise a Pluggy utilizando a skill `provider-technical-due-diligence` e o MCP oficial do provedor.

### Análise comparativa

Quando solicitado explicitamente, a skill pode aplicar o mesmo crivo a dois provedores e produzir uma comparação entre eles.

Cada provedor deve ser analisado individualmente utilizando os mesmos critérios, pesos e regras de evidência. A comparação é feita somente após as duas análises.

Exemplo:

> Compare Pluggy e Iniciador utilizando a skill `provider-technical-due-diligence` e os MCPs oficiais dos dois provedores.

O resultado comparativo deve priorizar leitura rápida e objetiva, podendo utilizar várias tabelas curtas em vez de uma única tabela extensa.

Sugestão de estrutura:

#### Visão geral

| Indicador | Provedor A | Provedor B |
|---|---:|---:|
| Score técnico | 82/100 | 76/100 |
| Confiança | 88% | 72% |
| Red flags | 0 | 1 |
| Questões críticas em aberto | 2 | 5 |
| Classificação | Aprovado com ressalvas | Aprovação condicionada |

#### Operação e confiabilidade

| Dimensão | Provedor A | Provedor B |
|---|---:|---:|
| Modelos de operação | 4/5 | 5/5 |
| Idempotência | 5/5 | 3/5 |
| Timeouts e respostas indeterminadas | 4/5 | 3/5 |
| Conciliação | 5/5 | 3/5 |

#### Integração e eventos

| Dimensão | Provedor A | Provedor B |
|---|---:|---:|
| Webhooks | 4/5 | 5/5 |
| Polling e consultas | 4/5 | 4/5 |
| Rate limits | 3/5 | 4/5 |
| Observabilidade | 4/5 | 3/5 |

#### Segurança e ambientes

| Dimensão | Provedor A | Provedor B |
|---|---:|---:|
| Autenticação e segurança | 4/5 | 4/5 |
| Sandbox / homologação / produção | 4/5 | 3/5 |
| Open Finance / regulatório | 4/5 | 4/5 |
| Qualidade da documentação | 5/5 | 3/5 |

#### Diferenças relevantes

| Tema | Melhor posicionado | Motivo |
|---|---|---|
| Idempotência | Provedor A | Fluxo mais claro e melhor documentado |
| Webhooks | Provedor B | Melhor cobertura de eventos |
| Conciliação | Provedor A | Mecanismos de recuperação mais completos |
| Rate limits | Provedor B | Limites mais favoráveis ou melhor documentados |

A comparação deve destacar somente diferenças materialmente relevantes e evitar repetir todo o conteúdo das análises individuais.

O modo comparativo não altera nem simplifica o modo individual.

Exemplo:

> Compare Pluggy e Iniciador utilizando a skill `provider-technical-due-diligence` e os MCPs oficiais dos dois provedores.
