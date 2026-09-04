---
name: biasi-email-triage
description: Classificar e-mails recebidos pela Biasi Engenharia antes de entrarem no fluxo comercial. Usar ao receber assunto, remetente, corpo, anexos e links de um e-mail para decidir se é um cliente/solicitante pedindo orçamento ou proposta à Biasi, se é apenas uma possível oportunidade que exige revisão humana, se é cotação enviada por fornecedor ou se é outro tipo de e-mail. Extrair sinais mínimos para roteamento no n8n/Biasi Hub, identificar anexos e links de projeto sem analisar tecnicamente os projetos nesta etapa e distinguir perfil da empresa, papel na obra e papel contratual quando essas relações estiverem explicitamente evidenciadas.
---

# Biasi Email Triage

## Objetivo

Atuar como a primeira barreira do fluxo de e-mail. Classificar a mensagem com alta precisão antes de qualquer análise de projeto, resposta ao cliente ou criação de oportunidade comercial.

Não analisar tecnicamente PDF, DWG, imagem ou projeto nesta etapa. Apenas reconhecer que esses elementos existem e preparar o roteamento.

## Fluxo obrigatório

1. Ler remetente, assunto, corpo do e-mail, histórico disponível, nomes/tipos de anexos e URLs informadas.
2. Determinar a intenção principal do e-mail usando as regras de `references/classification-rules.md`.
3. Identificar anexos por tipo e links que provavelmente apontam para arquivos/projetos.
4. Quando o e-mail trouxer evidência sobre participantes do empreendimento, distinguir perfil da empresa, papel na obra e papel contratual conforme `references/client-relationship-rules.md`. Não transformar essas três dimensões em um único `tipo_cliente`.
5. Definir a ação de fluxo:
   - `PROSSEGUIR_ANALISE` somente para `ORCAMENTO_CLIENTE`.
   - `REVISAR_MANUALMENTE` para `POSSIVEL_ORCAMENTO`.
   - `ENCERRAR_FLUXO` para `COTACAO_FORNECEDOR` e `NAO_ORCAMENTO`.
6. Se houver link de projeto/arquivos externos, marcar `precisa_validar_download=true`. O fluxo deve aguardar o usuário confirmar no Biasi Hub que os arquivos foram baixados/disponibilizados antes da análise técnica completa.
7. Retornar somente JSON válido conforme `references/output-schema.md`. Não adicionar explicações fora do JSON.

## Regras críticas

- Classificar pela intenção real, não apenas por palavras-chave.
- Não considerar todo e-mail com a palavra "orçamento" como solicitação de orçamento de cliente.
- Distinguir cliente pedindo preço/proposta à Biasi de fornecedor enviando sua própria cotação para a Biasi.
- Não confundir quem envia ou intermedeia o e-mail com quem é cliente final, proprietário do ativo ou contratante da Biasi.
- Considerar respostas e encaminhamentos: usar o conteúdo disponível do histórico quando ele deixar clara a intenção original.
- Se houver evidência insuficiente ou conflitante, usar `POSSIVEL_ORCAMENTO`; não forçar decisão positiva.
- Não inventar cliente, empresa, obra, local, prazo, disciplina, valor, escopo, papel na obra, perfil empresarial, papel contratual ou conteúdo de anexo.
- Quando um campo não estiver explícito, usar `null`, `[]` ou `false` conforme o tipo.
- Não escrever resposta ao remetente.
- Não criar oportunidade no Hub nesta etapa; apenas fornecer dados para o próximo nó.
- Não abrir nem interpretar tecnicamente o conteúdo de anexos nesta Skill. Se o conteúdo já vier fornecido no input, ainda assim limitar a saída à triagem de e-mail.

## Sinais úteis a extrair

Extrair apenas quando houver evidência no e-mail:

- nome do remetente;
- e-mail do remetente;
- empresa/cliente;
- assunto;
- pedido principal em uma frase curta;
- obra/projeto citado;
- cidade/local citado;
- prazo citado;
- disciplinas citadas;
- anexos por nome e extensão;
- links presentes;
- evidências textuais curtas que justificam a classificação.

## Leitura de referências

Ler `references/classification-rules.md` para regras de decisão, falsos positivos e exemplos.

Ler `references/client-relationship-rules.md` quando houver necessidade de distinguir natureza da empresa, papel na obra ou posição contratual.

Ler `references/output-schema.md` para o contrato JSON obrigatório.
