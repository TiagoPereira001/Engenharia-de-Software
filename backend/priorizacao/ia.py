"""Sugestão de prioridade assistida por IA (US-08).

O resto do sistema só chama `sugerir`. Por trás há duas formas de fazer a sugestão:

- o Claude (API da Anthropic), quando há uma chave em ANTHROPIC_API_KEY;
- uma regra local, sem rede, que usa os mesmos dados (votos, impacto e esforço).

Se o Claude não responder dentro do tempo limite, recusar ou devolver algo que não
bate certo, usa-se a regra local. Assim a priorização nunca fica parada à espera da IA
(decisão D4 em wiki/04-arquitetura/decisoes.md). A sugestão é sempre só uma sugestão:
nada muda sem o Product Owner aceitar.
"""

import json
import logging
import os
from dataclasses import asdict, dataclass

from django.conf import settings

logger = logging.getLogger(__name__)

NIVEIS = ["alta", "média", "baixa"]

INSTRUCOES = (
    "És o assistente de priorização de uma equipa de produto. Recebes uma lista de pedidos de "
    "funcionalidades em JSON, cada um com id, título, votos dos utilizadores, impacto (1 baixo, "
    "2 médio, 3 alto ou null se não estimado) e esforço em pontos (null se não estimado). "
    "Sugere a prioridade de cada pedido (alta, média ou baixa) e devolve-os pela ordem em que os "
    "farias. Para cada um, escreve a razão numa frase curta em português de Portugal, a partir "
    "dos dados (por exemplo: 'esforço baixo para o valor que traz'). Não inventes dados que não "
    "estão na lista e inclui todos os pedidos recebidos, uma só vez."
)

ESQUEMA = {
    "type": "object",
    "properties": {
        "sugestoes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "pedido_id": {"type": "integer"},
                    "nivel": {"type": "string", "enum": NIVEIS},
                    "razao": {"type": "string"},
                },
                "required": ["pedido_id", "nivel", "razao"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["sugestoes"],
    "additionalProperties": False,
}


@dataclass
class Sugestao:
    pedido_id: int
    nivel: str
    razao: str


class RespostaInvalida(Exception):
    """O serviço de IA respondeu, mas não com o que pedimos."""


def _pontos(item, mais_votos):
    """Valor por ponto de esforço. Sem estimativa, conta como esforço médio (5) e impacto baixo."""
    impacto = item["impacto"] or 1
    votos = item["votos"] / mais_votos if mais_votos else 0
    return (impacto * 2 + votos * 3) / (item["esforco"] or 5)


def _razao_local(item, mais_votos):
    partes = []
    if item["impacto"] == 3:
        partes.append("impacto alto")
    if mais_votos and item["votos"] == mais_votos:
        partes.append("é o pedido com mais votos")
    if item["esforco"] is None:
        partes.append("ainda sem estimativa de esforço")
    elif item["esforco"] <= 2:
        partes.append("esforço baixo para o valor que traz")
    elif item["esforco"] >= 8:
        partes.append("esforço alto")
    if item["impacto"] is None:
        partes.append("impacto por estimar")
    texto = ", ".join(partes) or "valor e esforço médios"
    return texto[0].upper() + texto[1:] + "."


def sugerir_local(itens):
    """Regra local: ordena pelo valor por ponto de esforço e divide em três partes iguais."""
    mais_votos = max((i["votos"] for i in itens), default=0)
    ordenados = sorted(itens, key=lambda i: -_pontos(i, mais_votos))
    terco = max(1, round(len(ordenados) / 3))
    sugestoes = []
    for n, item in enumerate(ordenados):
        nivel = NIVEIS[min(n // terco, 2)]
        sugestoes.append(Sugestao(item["id"], nivel, _razao_local(item, mais_votos)))
    return sugestoes


def _pedir_ao_claude(itens):
    """Pede a sugestão ao Claude com saída estruturada (JSON validado pelo esquema de cima)."""
    import anthropic  # só se importa quando há chave, para a regra local não depender do pacote

    cliente = anthropic.Anthropic(timeout=settings.IA_TEMPO_LIMITE, max_retries=0)
    resposta = cliente.beta.messages.create(
        model=settings.IA_MODELO,
        max_tokens=16000,
        # Se o modelo recusar, a API tenta outro modelo na mesma chamada.
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        output_config={"effort": "low", "format": {"type": "json_schema", "schema": ESQUEMA}},
        system=INSTRUCOES,
        messages=[{"role": "user", "content": json.dumps(itens, ensure_ascii=False)}],
    )
    if resposta.stop_reason != "end_turn":
        raise RespostaInvalida(f"O serviço de IA parou com '{resposta.stop_reason}'.")
    texto = next(bloco.text for bloco in resposta.content if bloco.type == "text")
    return json.loads(texto)["sugestoes"]


def _validar(dados, itens):
    ids = {i["id"] for i in itens}
    sugestoes = [Sugestao(int(d["pedido_id"]), d["nivel"], d["razao"].strip()) for d in dados]
    if {s.pedido_id for s in sugestoes} != ids or len(sugestoes) != len(ids):
        raise RespostaInvalida("A IA não devolveu cada pedido uma vez.")
    if any(s.nivel not in NIVEIS or not s.razao for s in sugestoes):
        raise RespostaInvalida("A IA devolveu uma sugestão sem nível ou sem razão.")
    return sugestoes


def sugerir(itens):
    """Devolve (sugestões pela ordem recomendada, fonte). A fonte é 'ia' ou 'regra local'."""
    if not itens:
        return [], "regra local"
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            return _validar(_pedir_ao_claude(itens), itens), "ia"
        except Exception:  # noqa: BLE001 - qualquer falha da IA leva à regra local
            logger.warning("A sugestão da IA falhou; usei a regra local.", exc_info=True)
    return sugerir_local(itens), "regra local"


def como_dict(sugestao):
    return asdict(sugestao)
