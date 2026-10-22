"""
Consultor Inteligente de Carreiras em TI — Sistema Especialista baseado em Regras.

Base de conhecimento (Experta) com encadeamento para frente:
  1. O usuário responde a uma entrevista -> viram um Fact `Perfil`.
  2. As regras (R01..R29) casam com o Perfil e acumulam pontos para as trilhas,
     registrando o motivo de cada disparo (justificativa transparente).
  3. A regra final (R30, salience baixa) escolhe a trilha vencedora.
"""
import collections
import collections.abc

# Compatibilidade: o Experta antigo usa collections.Mapping (removido no Python 3.10+).
for _nome in ("Mapping", "MutableMapping", "Sequence", "Iterable", "Callable"):
    if not hasattr(collections, _nome):
        setattr(collections, _nome, getattr(collections.abc, _nome))

from experta import Fact, KnowledgeEngine, P, Rule  # noqa: E402

# ----------------------------------------------------------------------------
# Trilhas
# ----------------------------------------------------------------------------
BACKEND, FRONTEND, DS, DE, SEC, DEVOPS, CLOUD, MOBILE, QA, PM = (
    "backend", "frontend", "ciencia_dados", "eng_dados", "ciberseguranca",
    "devops", "nuvem", "mobile", "qa", "produtos",
)

TRILHAS = {
    BACKEND: ("Desenvolvimento Back-end",
              "Lógica de servidores, construção de APIs, regras de negócio e bancos de dados."),
    FRONTEND: ("Desenvolvimento Front-end & UI/UX",
               "Interfaces web responsivas, experiência do usuário e frameworks reativos."),
    DS: ("Ciência de Dados e Machine Learning",
         "Estatística, modelagem preditiva, análise de grandes massas de dados e inteligência artificial."),
    DE: ("Engenharia de Dados",
         "Arquitetura de dados, pipelines (ETL/ELT) e infraestrutura para Data Lakes."),
    SEC: ("Cibersegurança (Security / Pentesting)",
          "Defesa cibernética, análise de vulnerabilidades, criptografia e redes seguras."),
    DEVOPS: ("DevOps & SRE",
             "Automação de processos, integração e entrega contínua (CI/CD) e contêineres."),
    CLOUD: ("Computação em Nuvem (Cloud Architecture)",
            "Planejamento, migração e gestão de infraestruturas escaláveis (AWS/Azure/GCP)."),
    MOBILE: ("Desenvolvimento Mobile",
             "Ecossistema de dispositivos móveis (nativo ou multiplataforma com Flutter/React Native)."),
    QA: ("Engenharia de Qualidade e Testes (QA)",
         "Testes automatizados, confiabilidade de software e processos de qualidade."),
    PM: ("Gestão de Produtos (Product Management)",
         "Ponte entre negócio, design e desenvolvimento, metodologias ágeis e priorização de produto."),
}

# ----------------------------------------------------------------------------
# Entrevista (perguntas e opções)
# ----------------------------------------------------------------------------
PERGUNTAS = {
    "matematica": {
        "pergunta": "Qual é a sua afinidade com matemática e estatística?",
        "opcoes": {"baixa": "Baixa", "media": "Média", "alta": "Alta"},
    },
    "atuacao": {
        "pergunta": "O que você mais gostaria de fazer no dia a dia de trabalho?",
        "opcoes": {
            "algoritmos_logicos": "Escrever algoritmos e resolver problemas lógicos",
            "layouts_visuais": "Criar layouts e interfaces visuais",
            "servidores_apis": "Lidar com servidores, APIs e bancos de dados",
            "dados_brutos": "Analisar dados brutos",
            "seguranca": "Garantir segurança e buscar vulnerabilidades",
            "automacao_deploy": "Automatizar builds, testes e deploys",
            "planejar_infra": "Planejar e dimensionar infraestrutura escalável",
            "apps_celular": "Construir aplicativos para celular",
            "testar_qualidade": "Testar software e garantir qualidade",
            "priorizar_negocio": "Conversar com clientes e priorizar o que será construído",
        },
    },
    "ferramenta": {
        "pergunta": "Qual linguagem/ferramenta você domina melhor hoje?",
        "opcoes": {
            "python": "Python",
            "javascript": "JavaScript",
            "sql": "SQL / bancos de dados",
            "linux_redes": "Linux / Redes",
            "nenhuma": "Nenhuma / Iniciante",
        },
    },
    "entrega": {
        "pergunta": "Que tipo de entrega de valor mais te motiva?",
        "opcoes": {
            "produto_usuario": "O produto final usado pelo usuário",
            "infraestrutura": "A infraestrutura que sustenta o sistema",
            "seguranca": "A segurança contra invasões",
            "insights_dados": "Insights e previsões geradas a partir de dados",
            "qualidade": "A confiabilidade e a qualidade do software",
            "estrategia_produto": "A estratégia: decidir o que e por que construir",
        },
    },
    # Perguntas dinâmicas (só aparecem quando a resposta anterior é ambígua)
    "dados_foco": {
        "pergunta": "Trabalhando com dados, você prefere...",
        "opcoes": {
            "modelagem": "Treinar modelos preditivos e estatísticos",
            "pipelines": "Construir pipelines e a infraestrutura que movimenta os dados",
        },
    },
    "plataforma": {
        "pergunta": "Em qual plataforma você prefere ver o seu trabalho rodando?",
        "opcoes": {
            "web_desktop": "Web / Desktop",
            "mobile": "Celular (Android/iOS)",
            "indiferente": "Tanto faz",
        },
    },
}


def normalizar(respostas: dict) -> dict:
    """Completa respostas das perguntas dinâmicas com valores neutros."""
    perfil = dict(respostas)
    perfil.setdefault("dados_foco", "nao_se_aplica")
    perfil.setdefault("plataforma", "indiferente")
    if perfil["atuacao"] == "apps_celular":
        perfil["plataforma"] = "mobile"
    return perfil


# ----------------------------------------------------------------------------
# Fatos e motor de inferência
# ----------------------------------------------------------------------------
class Perfil(Fact):
    """Respostas do usuário (matematica, atuacao, ferramenta, entrega, dados_foco, plataforma)."""


def em(*valores):
    return P(lambda x: x in valores)


def diferente(valor):
    return P(lambda x: x != valor)


class ConsultorCarreiras(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.pontos = {t: 0 for t in TRILHAS}
        self.disparos = []
        self.vencedora = None

    def _add(self, regra, trilha, pontos, motivo):
        self.pontos[trilha] += pontos
        self.disparos.append(
            {"regra": regra, "trilha": trilha, "pontos": pontos, "motivo": motivo}
        )

    # ---------------- Back-end ----------------
    @Rule(Perfil(atuacao="servidores_apis"))
    def r01(self):
        self._add("R01", BACKEND, 4, "Você prefere lidar com servidores, APIs e bancos de dados.")

    @Rule(Perfil(ferramenta="sql", atuacao=em("algoritmos_logicos", "servidores_apis")))
    def r02(self):
        self._add("R02", BACKEND, 3, "SQL combinado com lógica/regras de negócio é a base do back-end.")

    @Rule(Perfil(atuacao="algoritmos_logicos", ferramenta=em("python", "javascript"),
                 matematica=em("baixa", "media"), plataforma=diferente("mobile")))
    def r03(self):
        self._add("R03", BACKEND, 3,
                  "Gosta de algoritmos em linguagem de uso geral, sem exigir matemática avançada.")

    # ---------------- Front-end ----------------
    @Rule(Perfil(atuacao="layouts_visuais"))
    def r04(self):
        self._add("R04", FRONTEND, 4, "Você gosta de criar layouts e interfaces visuais.")

    @Rule(Perfil(atuacao="layouts_visuais", entrega="produto_usuario"))
    def r05(self):
        self._add("R05", FRONTEND, 2, "Quer ver o produto final nas mãos do usuário (experiência de uso).")

    @Rule(Perfil(atuacao="layouts_visuais", ferramenta="javascript"))
    def r06(self):
        self._add("R06", FRONTEND, 2, "JavaScript + interfaces visuais aponta para frameworks reativos.")

    # ---------------- Mobile ----------------
    @Rule(Perfil(atuacao="apps_celular"))
    def r07(self):
        self._add("R07", MOBILE, 5, "Você quer construir aplicativos para celular.")

    @Rule(Perfil(plataforma="mobile", atuacao=em("layouts_visuais", "algoritmos_logicos", "apps_celular")))
    def r08(self):
        self._add("R08", MOBILE, 5, "Prefere ver o seu trabalho rodando em dispositivos móveis.")

    @Rule(Perfil(plataforma="mobile", atuacao=em("layouts_visuais", "algoritmos_logicos")))
    def r09(self):
        self._add("R09", FRONTEND, -4,
                  "Foco em celular reduz a aderência ao Front-end web (desambigua Front-end x Mobile).")

    # ---------------- Ciência de Dados ----------------
    @Rule(Perfil(atuacao="dados_brutos", dados_foco="modelagem"))
    def r10(self):
        self._add("R10", DS, 5, "Gosta de analisar dados para treinar modelos preditivos.")

    @Rule(Perfil(matematica="alta", entrega="insights_dados"))
    def r11(self):
        self._add("R11", DS, 3, "Alta afinidade matemática + motivação por insights e previsões.")

    @Rule(Perfil(matematica="alta", atuacao="dados_brutos"))
    def r12(self):
        self._add("R12", DS, 2, "Estatística forte aplicada a dados brutos é o núcleo de Data Science.")

    @Rule(Perfil(matematica="baixa", atuacao="dados_brutos"))
    def r13(self):
        self._add("R13", DS, -3,
                  "Baixa afinidade matemática reduz a aderência a Ciência de Dados/ML.")
        self._add("R13", DE, 2,
                  "Trabalho com dados sem exigir estatística avançada combina mais com Engenharia de Dados.")

    # ---------------- Engenharia de Dados ----------------
    @Rule(Perfil(atuacao="dados_brutos", dados_foco="pipelines"))
    def r14(self):
        self._add("R14", DE, 5, "Prefere construir pipelines e a infraestrutura que movimenta os dados.")

    @Rule(Perfil(atuacao="dados_brutos", ferramenta="sql"))
    def r15(self):
        self._add("R15", DE, 2, "SQL é ferramenta central em processos ETL/ELT.")

    @Rule(Perfil(atuacao="dados_brutos", entrega="infraestrutura"))
    def r16(self):
        self._add("R16", DE, 3, "Quer entregar a infraestrutura que sustenta os dados (Data Lakes).")

    # ---------------- Cibersegurança ----------------
    @Rule(Perfil(atuacao="seguranca"))
    def r17(self):
        self._add("R17", SEC, 5, "Você gosta de garantir segurança e analisar vulnerabilidades.")

    @Rule(Perfil(entrega="seguranca"))
    def r18(self):
        self._add("R18", SEC, 4, "A proteção contra invasões é o valor que mais te motiva a entregar.")

    @Rule(Perfil(ferramenta="linux_redes", entrega="seguranca"))
    def r19(self):
        self._add("R19", SEC, 3, "Domínio de Linux/Redes é base para defesa e pentesting.")

    # ---------------- DevOps & SRE ----------------
    @Rule(Perfil(atuacao="automacao_deploy"))
    def r20(self):
        self._add("R20", DEVOPS, 5, "Você gosta de automatizar builds, testes e deploys (CI/CD).")

    @Rule(Perfil(atuacao="automacao_deploy", ferramenta="linux_redes"))
    def r21(self):
        self._add("R21", DEVOPS, 3, "Linux + automação é a base de contêineres e pipelines CI/CD.")

    # ---------------- Computação em Nuvem ----------------
    @Rule(Perfil(atuacao="planejar_infra"))
    def r22(self):
        self._add("R22", CLOUD, 5, "Você gosta de planejar infraestruturas escaláveis.")

    @Rule(Perfil(atuacao="planejar_infra", entrega="infraestrutura"))
    def r23(self):
        self._add("R23", CLOUD, 3,
                  "Planejamento + entrega de infraestrutura aponta para arquitetura em nuvem (AWS/Azure/GCP).")

    # ---------------- QA ----------------
    @Rule(Perfil(atuacao="testar_qualidade"))
    def r24(self):
        self._add("R24", QA, 5, "Você gosta de testar software e garantir qualidade.")

    @Rule(Perfil(entrega="qualidade"))
    def r25(self):
        self._add("R25", QA, 4, "A confiabilidade do software é o valor que mais te motiva.")

    @Rule(Perfil(entrega="qualidade", ferramenta=em("python", "javascript")))
    def r26(self):
        self._add("R26", QA, 2, "Programação aplicada a testes automatizados.")

    # ---------------- Gestão de Produtos ----------------
    @Rule(Perfil(atuacao="priorizar_negocio"))
    def r27(self):
        self._add("R27", PM, 5, "Você gosta de conversar com clientes e priorizar o que será construído.")

    @Rule(Perfil(entrega="estrategia_produto"))
    def r28(self):
        self._add("R28", PM, 4, "Decidir o que e por que construir é o que mais te motiva.")

    @Rule(Perfil(ferramenta="nenhuma", entrega="estrategia_produto", matematica=em("baixa", "media")))
    def r29(self):
        self._add("R29", PM, 2,
                  "Perfil de negócios: a trilha não exige domínio técnico profundo de início.")

    # ---------------- Decisão final ----------------
    @Rule(Perfil(), salience=-100)
    def r30_decisao(self):
        regras_por_trilha = {t: 0 for t in TRILHAS}
        for d in self.disparos:
            if d["pontos"] > 0:
                regras_por_trilha[d["trilha"]] += 1
        ordem = list(TRILHAS)
        ranking = sorted(
            TRILHAS,
            key=lambda t: (-self.pontos[t], -regras_por_trilha[t], ordem.index(t)),
        )
        self.vencedora = ranking[0]


def consultar(respostas: dict) -> dict:
    """Executa a entrevista no motor de inferência e devolve a recomendação justificada."""
    perfil = normalizar(respostas)
    motor = ConsultorCarreiras()
    motor.reset()
    motor.declare(Perfil(**perfil))
    motor.run()

    vencedora = motor.vencedora
    ranking = sorted(motor.pontos.items(), key=lambda kv: -kv[1])
    segunda = next(kv for kv in ranking if kv[0] != vencedora)
    motivos = [d for d in motor.disparos if d["trilha"] == vencedora]
    return {
        "trilha": vencedora,
        "nome": TRILHAS[vencedora][0],
        "descricao": TRILHAS[vencedora][1],
        "pontos": motor.pontos[vencedora],
        "segunda": segunda[0],
        "margem": motor.pontos[vencedora] - segunda[1],
        "motivos": motivos,
        "ranking": [(TRILHAS[t][0], p) for t, p in ranking],
        "disparos": motor.disparos,
        "perfil": perfil,
    }
