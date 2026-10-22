"""Personas de teste (Fase 4). Cada uma traz a trilha esperada."""
from sistema_especialista import BACKEND, CLOUD, DE, DEVOPS, DS, FRONTEND, MOBILE, PM, QA, SEC

PERSONAS = [
    # --- As 4 personas sugeridas no enunciado ---
    {"nome": "Carla (perfil analítico)", "esperada": DS, "respostas": {
        "matematica": "alta", "atuacao": "dados_brutos", "ferramenta": "python",
        "entrega": "insights_dados", "dados_foco": "modelagem"}},
    {"nome": "Elisa (perfil infra/segurança)", "esperada": SEC, "respostas": {
        "matematica": "media", "atuacao": "seguranca", "ferramenta": "linux_redes",
        "entrega": "seguranca"}},
    {"nome": "Beto (perfil visual/front-end)", "esperada": FRONTEND, "respostas": {
        "matematica": "baixa", "atuacao": "layouts_visuais", "ferramenta": "javascript",
        "entrega": "produto_usuario", "plataforma": "web_desktop"}},
    {"nome": "João (perfil negócios/produto)", "esperada": PM, "respostas": {
        "matematica": "baixa", "atuacao": "priorizar_negocio", "ferramenta": "nenhuma",
        "entrega": "estrategia_produto"}},
    # --- Cobertura das demais trilhas ---
    {"nome": "Ana (back-end)", "esperada": BACKEND, "respostas": {
        "matematica": "media", "atuacao": "servidores_apis", "ferramenta": "sql",
        "entrega": "produto_usuario"}},
    {"nome": "Diego (engenheiro de dados)", "esperada": DE, "respostas": {
        "matematica": "media", "atuacao": "dados_brutos", "ferramenta": "sql",
        "entrega": "infraestrutura", "dados_foco": "pipelines"}},
    {"nome": "Fábio (DevOps)", "esperada": DEVOPS, "respostas": {
        "matematica": "media", "atuacao": "automacao_deploy", "ferramenta": "linux_redes",
        "entrega": "infraestrutura"}},
    {"nome": "Gabi (arquiteta cloud)", "esperada": CLOUD, "respostas": {
        "matematica": "media", "atuacao": "planejar_infra", "ferramenta": "linux_redes",
        "entrega": "infraestrutura"}},
    {"nome": "Hugo (mobile)", "esperada": MOBILE, "respostas": {
        "matematica": "baixa", "atuacao": "apps_celular", "ferramenta": "javascript",
        "entrega": "produto_usuario"}},
    {"nome": "Iara (QA)", "esperada": QA, "respostas": {
        "matematica": "media", "atuacao": "testar_qualidade", "ferramenta": "python",
        "entrega": "qualidade"}},
    # --- Casos de desambiguação ---
    {"nome": "Marcos (dados + modelos, deve ser Cientista de Dados)", "esperada": DS, "respostas": {
        "matematica": "alta", "atuacao": "dados_brutos", "ferramenta": "python",
        "entrega": "insights_dados", "dados_foco": "modelagem"}},
    {"nome": "Nina (dados + pipelines, deve ser Engenheira de Dados)", "esperada": DE, "respostas": {
        "matematica": "alta", "atuacao": "dados_brutos", "ferramenta": "python",
        "entrega": "infraestrutura", "dados_foco": "pipelines"}},
    {"nome": "Rui (layouts visuais para celular, deve ser Mobile)", "esperada": MOBILE, "respostas": {
        "matematica": "baixa", "atuacao": "layouts_visuais", "ferramenta": "javascript",
        "entrega": "produto_usuario", "plataforma": "mobile"}},
]
