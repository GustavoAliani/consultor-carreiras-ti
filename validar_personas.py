"""Fase 4: roda as personas no motor de inferência e gera docs/validacao_personas.md."""
import sys
from pathlib import Path

from personas import PERSONAS
from sistema_especialista import TRILHAS, consultar


def main() -> int:
    linhas = [
        "# Validação com Personas de Teste\n",
        "| Persona | Esperada | Recomendada | Pontos | Margem | Resultado |",
        "|---|---|---|---|---|---|",
    ]
    acertos = 0
    for p in PERSONAS:
        r = consultar(p["respostas"])
        ok = r["trilha"] == p["esperada"]
        acertos += ok
        linhas.append(
            f"| {p['nome']} | {TRILHAS[p['esperada']][0]} | {r['nome']} | "
            f"{r['pontos']} | {r['margem']} | {'✅ Acertou' if ok else '❌ Errou'} |"
        )
        print(f"[{'OK' if ok else 'FALHA'}] {p['nome']}: {r['nome']} ({r['pontos']} pts, margem {r['margem']})")

    resumo = f"\n**Acertos: {acertos}/{len(PERSONAS)}**\n"
    linhas.append(resumo)
    Path("docs").mkdir(exist_ok=True)
    Path("docs/validacao_personas.md").write_text("\n".join(linhas), encoding="utf-8")
    print(resumo)
    return 0 if acertos == len(PERSONAS) else 1


if __name__ == "__main__":
    sys.exit(main())
