import pandas as pd
import streamlit as st

from sistema_especialista import PERGUNTAS, consultar

st.set_page_config(page_title="Consultor de Carreiras em TI", page_icon="🧭", layout="centered")

st.title("🧭 Consultor Inteligente de Carreiras em TI")
st.write(
    "Responda às perguntas abaixo e o sistema especialista vai recomendar, entre 10 trilhas, "
    "a que mais combina com o seu perfil — explicando quais regras levaram à decisão."
)
st.divider()


def perguntar(chave):
    p = PERGUNTAS[chave]
    return st.selectbox(
        p["pergunta"],
        options=list(p["opcoes"]),
        format_func=p["opcoes"].get,
        index=None,
        placeholder="Selecione uma opção...",
        key=chave,
    )


respostas = {}
for chave in ("matematica", "atuacao", "ferramenta", "entrega"):
    respostas[chave] = perguntar(chave)

# Perguntas dinâmicas: só aparecem quando a resposta anterior é ambígua.
if respostas["atuacao"] == "dados_brutos":
    st.info("Trabalhar com dados pode levar a mais de uma trilha. Vamos refinar:")
    respostas["dados_foco"] = perguntar("dados_foco")
if respostas["atuacao"] in ("algoritmos_logicos", "layouts_visuais"):
    respostas["plataforma"] = perguntar("plataforma")

faltando = [k for k, v in respostas.items() if v is None]

if st.button("Descobrir minha trilha", type="primary", disabled=bool(faltando)):
    r = consultar(respostas)

    st.success(f"Trilha recomendada: **{r['nome']}**")
    st.write(r["descricao"])

    col1, col2 = st.columns(2)
    col1.metric("Pontuação da trilha", r["pontos"])
    col2.metric("Vantagem sobre a 2ª colocada", r["margem"])

    st.subheader("Por que essa recomendação?")
    for m in r["motivos"]:
        sinal = f"+{m['pontos']}" if m["pontos"] > 0 else str(m["pontos"])
        st.markdown(f"- **{m['regra']}** ({sinal} pts): {m['motivo']}")

    st.subheader("Ranking das 10 trilhas")
    df = pd.DataFrame(r["ranking"], columns=["Trilha", "Pontos"]).set_index("Trilha")
    st.bar_chart(df)

    with st.expander("Ver todas as regras disparadas"):
        tabela = pd.DataFrame(r["disparos"])[["regra", "trilha", "pontos", "motivo"]]
        st.dataframe(tabela, hide_index=True)
elif faltando:
    st.caption("Responda todas as perguntas para liberar a recomendação.")
