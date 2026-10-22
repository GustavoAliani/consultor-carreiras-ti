# Fase 1 — Matriz de Decisão

## Entrevista

| Dimensão | Pergunta | Valores |
|---|---|---|
| `matematica` | Afinidade com matemática e estatística | baixa, media, alta |
| `atuacao` | Preferência de atuação diária | algoritmos_logicos, layouts_visuais, servidores_apis, dados_brutos, seguranca, automacao_deploy, planejar_infra, apps_celular, testar_qualidade, priorizar_negocio |
| `ferramenta` | Linguagem/ferramenta de maior afinidade | python, javascript, sql, linux_redes, nenhuma |
| `entrega` | Tipo de entrega de valor preferida | produto_usuario, infraestrutura, seguranca, insights_dados, qualidade, estrategia_produto |
| `dados_foco` *(dinâmica: só se atuação = dados_brutos)* | Modelos preditivos ou pipelines? | modelagem, pipelines |
| `plataforma` *(dinâmica: só se atuação = algoritmos_logicos ou layouts_visuais)* | Plataforma preferida | web_desktop, mobile, indiferente |

## Como o motor decide

Cada regra **SE–ENTÃO** que casa com as respostas soma (ou subtrai) pontos para uma trilha e registra o motivo.
A regra R30, de menor prioridade (`salience=-100`), dispara por último e escolhe a trilha com mais pontos.
Desempate: maior número de regras positivas disparadas e, depois, ordem fixa das trilhas.

## Tabela de regras (29 regras de pontuação + 1 de decisão)

| Regra | Trilha | SE (condições) | ENTÃO |
|---|---|---|---|
| R01 | Back-end | atuacao = servidores_apis | +4 |
| R02 | Back-end | ferramenta = sql **E** atuacao ∈ {algoritmos_logicos, servidores_apis} | +3 |
| R03 | Back-end | atuacao = algoritmos_logicos **E** ferramenta ∈ {python, javascript} **E** matematica ∈ {baixa, media} **E** plataforma ≠ mobile | +3 |
| R04 | Front-end & UI/UX | atuacao = layouts_visuais | +4 |
| R05 | Front-end & UI/UX | atuacao = layouts_visuais **E** entrega = produto_usuario | +2 |
| R06 | Front-end & UI/UX | atuacao = layouts_visuais **E** ferramenta = javascript | +2 |
| R07 | Mobile | atuacao = apps_celular | +5 |
| R08 | Mobile | plataforma = mobile **E** atuacao ∈ {layouts_visuais, algoritmos_logicos, apps_celular} | +5 |
| R09 | Front-end & UI/UX | plataforma = mobile **E** atuacao ∈ {layouts_visuais, algoritmos_logicos} | −4 (desambigua Front × Mobile) |
| R10 | Ciência de Dados e ML | atuacao = dados_brutos **E** dados_foco = modelagem | +5 |
| R11 | Ciência de Dados e ML | matematica = alta **E** entrega = insights_dados | +3 |
| R12 | Ciência de Dados e ML | matematica = alta **E** atuacao = dados_brutos | +2 |
| R13 | Ciência de Dados e ML / Eng. de Dados | matematica = baixa **E** atuacao = dados_brutos | DS −3 e DE +2 (desambigua DS × DE) |
| R14 | Engenharia de Dados | atuacao = dados_brutos **E** dados_foco = pipelines | +5 |
| R15 | Engenharia de Dados | atuacao = dados_brutos **E** ferramenta = sql | +2 |
| R16 | Engenharia de Dados | atuacao = dados_brutos **E** entrega = infraestrutura | +3 |
| R17 | Cibersegurança | atuacao = seguranca | +5 |
| R18 | Cibersegurança | entrega = seguranca | +4 |
| R19 | Cibersegurança | ferramenta = linux_redes **E** entrega = seguranca | +3 |
| R20 | DevOps & SRE | atuacao = automacao_deploy | +5 |
| R21 | DevOps & SRE | atuacao = automacao_deploy **E** ferramenta = linux_redes | +3 |
| R22 | Computação em Nuvem | atuacao = planejar_infra | +5 |
| R23 | Computação em Nuvem | atuacao = planejar_infra **E** entrega = infraestrutura | +3 |
| R24 | QA | atuacao = testar_qualidade | +5 |
| R25 | QA | entrega = qualidade | +4 |
| R26 | QA | entrega = qualidade **E** ferramenta ∈ {python, javascript} | +2 |
| R27 | Gestão de Produtos | atuacao = priorizar_negocio | +5 |
| R28 | Gestão de Produtos | entrega = estrategia_produto | +4 |
| R29 | Gestão de Produtos | ferramenta = nenhuma **E** entrega = estrategia_produto **E** matematica ∈ {baixa, media} | +2 |
| R30 | (todas) | Perfil existe (salience −100) | Escolhe a trilha de maior pontuação |

## Matriz: respostas que ativam cada trilha

| Trilha | Atuação | Ferramenta | Entrega | Matemática | Dimensões extras |
|---|---|---|---|---|---|
| Back-end | servidores_apis, algoritmos_logicos | sql, python, javascript | — | baixa/média | plataforma ≠ mobile |
| Front-end & UI/UX | layouts_visuais | javascript | produto_usuario | — | plataforma ≠ mobile |
| Ciência de Dados e ML | dados_brutos | python | insights_dados | **alta** | dados_foco = modelagem |
| Engenharia de Dados | dados_brutos | sql | infraestrutura | qualquer (baixa reforça) | dados_foco = pipelines |
| Cibersegurança | seguranca | linux_redes | seguranca | — | — |
| DevOps & SRE | automacao_deploy | linux_redes | infraestrutura | — | — |
| Computação em Nuvem | planejar_infra | linux_redes | infraestrutura | — | — |
| Mobile | apps_celular, layouts_visuais, algoritmos_logicos | javascript | produto_usuario | — | plataforma = mobile |
| QA | testar_qualidade | python, javascript | qualidade | — | — |
| Gestão de Produtos | priorizar_negocio | nenhuma | estrategia_produto | baixa/média | — |

## Desambiguações principais

- **Ciência de Dados × Engenharia de Dados:** decididas por `dados_foco` (modelagem × pipelines), pela matemática (alta reforça DS; baixa reforça DE em R13) e pela entrega (insights × infraestrutura).
- **Front-end × Mobile:** decididas por `plataforma`; R09 penaliza o Front-end quando o foco é celular.
- **DevOps × Cloud:** decididas pela atuação (automação de entrega × planejamento de infraestrutura).
