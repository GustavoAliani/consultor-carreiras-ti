# 🧭 Consultor Inteligente de Carreiras em TI

Sistema Especialista baseado em regras (Python + **Experta** + **Streamlit**) que entrevista o usuário e recomenda
a trilha de carreira em TI mais adequada entre 10 opções, justificando a decisão com as regras disparadas.

- **Disciplina:** Inteligência Artificial — Ciência da Computação
- **Instituição:** UNIPAC Barbacena
- **Professor:** Felipe Roncalli de Paula Carneiro

## Trilhas cobertas

Back-end · Front-end & UI/UX · Ciência de Dados e ML · Engenharia de Dados · Cibersegurança · DevOps & SRE ·
Computação em Nuvem · Mobile · QA · Gestão de Produtos

## Instalação e execução

Requer Python 3.10 ou superior.

```bash
git clone <URL-DO-SEU-REPOSITORIO>
cd consultor-carreiras-ti

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

O navegador abrirá em `http://localhost:8501`.

> **Nota sobre o Experta:** a versão publicada do Experta fixa `frozendict==1.2`, que não compila em
> Python 3.12+. Por isso o `requirements.txt` usa `frozendict` atual, e o arquivo `sistema_especialista.py`
> aplica uma pequena compatibilidade (`collections.Mapping`). Se `pip install experta` falhar na sua máquina, use
> `pip install -r requirements.txt` (já resolve).

## Validação com personas (Fase 4)

```bash
python validar_personas.py
```

Roda 13 personas (as 4 do enunciado, as demais trilhas e casos de desambiguação) e gera
`docs/validacao_personas.md`. Resultado atual: **13/13 acertos**.

## Estrutura do projeto

```
├── app.py                    # Interface Streamlit (entrevista dinâmica + justificativa)
├── sistema_especialista.py   # Base de conhecimento: Facts, regras @Rule e motor de inferência
├── personas.py               # Personas de teste
├── validar_personas.py       # Validação automática das personas
├── requirements.txt
└── docs/
    ├── matriz_decisao.md     # Fase 1: matriz de decisão e tabela das regras
    └── validacao_personas.md # Resultado da validação (gerado)
```

## Como funciona

1. **Entrevista dinâmica:** 4 perguntas fixas (matemática, atuação diária, ferramenta, entrega de valor) e 2 perguntas
   que só aparecem quando há ambiguidade (`dados_foco` para dados; `plataforma` para algoritmos/layouts).
2. **Fatos:** as respostas viram um `Fact` (`Perfil`) declarado na memória de trabalho do Experta.
3. **Regras (encadeamento para frente):** 29 regras `@Rule` do tipo SE–ENTÃO cruzam as dimensões e somam pontos às
   trilhas; algumas penalizam trilhas concorrentes (ex.: R09 Front × Mobile; R13 Ciência × Engenharia de Dados).
4. **Decisão:** a regra R30 (`salience=-100`) dispara por último e escolhe a trilha de maior pontuação.
5. **Justificativa transparente:** a tela mostra a trilha recomendada, as regras que a sustentam (com pontos),
   o ranking das 10 trilhas e a lista completa de regras disparadas.

A tabela completa de regras está em [`docs/matriz_decisao.md`](docs/matriz_decisao.md).

## Publicando no GitHub

```bash
git init
git add .
git commit -m "Consultor Inteligente de Carreiras em TI"
git branch -M main
git remote add origin https://github.com/<seu-usuario>/<seu-repositorio>.git
git push -u origin main
```
