"""Regras da priorização (US-06 e US-09).

Só o Product Owner muda a ordem e o impacto. O esforço também o pode estimar
o programador, que é quem vai fazer o trabalho (casos de uso do Diogo).
"""

from django.db import transaction
from django.db.models import Count

from contas.models import Papel
from pedidos.models import Estado, Pedido
from pedidos.servicos import SemPermissao

from .models import ESFORCOS, AlteracaoOrdem, Estimativa, Impacto

# Os pedidos que entram na priorização: os que estão a ser analisados e os já aprovados.
ESTADOS_A_PRIORIZAR = [Estado.EM_ANALISE, Estado.APROVADO]

ORDENS = ["manual", "impacto", "esforco", "relacao", "votos"]


class EstimativaInvalida(Exception):
    """Valor fora da escala documentada."""


def _estimativa(pedido):
    return Estimativa.objects.get_or_create(pedido=pedido)[0]


@transaction.atomic
def estimar(*, pedido, autor, impacto=None, esforco=None):
    """Grava o impacto e/ou o esforço de um pedido. None quer dizer 'não mexer'."""
    if impacto is not None and autor.papel != Papel.PRODUCT_OWNER:
        raise SemPermissao("Só o Product Owner estima o impacto.")
    if esforco is not None and autor.papel not in (Papel.PRODUCT_OWNER, Papel.PROGRAMADOR):
        raise SemPermissao("Só o Product Owner ou um programador estimam o esforço.")
    if impacto is not None and impacto not in Impacto.values:
        raise EstimativaInvalida("O impacto é 1 (baixo), 2 (médio) ou 3 (alto).")
    if esforco is not None and esforco not in ESFORCOS:
        raise EstimativaInvalida(f"O esforço é um destes valores em pontos: {', '.join(map(str, ESFORCOS))}.")
    estimativa = _estimativa(pedido)
    if impacto is not None:
        estimativa.impacto = impacto
    if esforco is not None:
        estimativa.esforco = esforco
    estimativa.save()
    return estimativa


@transaction.atomic
def ordenar(*, autor, ids, razao="", aceitou_sugestao_ia=False):
    """O Product Owner põe os pedidos pela ordem que quer. Fica registado quem, quando e porquê."""
    if autor.papel != Papel.PRODUCT_OWNER:
        raise SemPermissao("Só o Product Owner muda a ordem dos pedidos.")
    ids = list(dict.fromkeys(ids))
    validos = set(Pedido.objects.filter(id__in=ids, estado__in=ESTADOS_A_PRIORIZAR).values_list("id", flat=True))
    if validos != set(ids):
        raise EstimativaInvalida("Só se ordenam pedidos em análise ou aprovados.")
    # Quem não está na lista nova perde o lugar e passa para o fim.
    Estimativa.objects.exclude(pedido_id__in=ids).update(posicao=None)
    for posicao, pedido_id in enumerate(ids, start=1):
        Estimativa.objects.update_or_create(pedido_id=pedido_id, defaults={"posicao": posicao})
    return AlteracaoOrdem.objects.create(
        autor=autor, razao=razao.strip(), ordem=ids, aceitou_sugestao_ia=aceitou_sugestao_ia
    )


def _chave(ordem):
    """Como se ordena a lista. Os pedidos sem valor ficam sempre no fim."""
    fim = float("inf")
    chaves = {
        "manual": lambda p: (p.posicao or fim, -p.total_votos),
        "impacto": lambda p: (-(p.impacto or 0), p.posicao or fim),
        "esforco": lambda p: (p.esforco or fim, p.posicao or fim),
        "relacao": lambda p: (-(p.relacao or 0), p.posicao or fim),
        "votos": lambda p: (-p.total_votos, p.posicao or fim),
    }
    return chaves[ordem if ordem in chaves else "manual"]


def lista(ordem="manual", capacidade=None):
    """Os pedidos a priorizar, pela ordem pedida.

    A ordem do Product Owner diz o que entra primeiro no sprint. Se a capacidade for dada,
    soma o esforço dos pedidos já ordenados e marca os que passam da capacidade (US-06).
    """
    pedidos = list(
        Pedido.objects.filter(estado__in=ESTADOS_A_PRIORIZAR)
        .select_related("estimativa")
        .annotate(total_votos=Count("votos"))
    )
    for p in pedidos:
        estimativa = getattr(p, "estimativa", None)
        p.impacto = estimativa.impacto if estimativa else None
        p.esforco = estimativa.esforco if estimativa else None
        p.posicao = estimativa.posicao if estimativa else None
        p.relacao = estimativa.relacao if estimativa else None
    pedidos.sort(key=_chave(ordem))

    acumulado = 0
    for p in sorted(pedidos, key=_chave("manual")):
        if p.posicao is not None:
            acumulado += p.esforco or 0
        p.fora_da_capacidade = capacidade is not None and p.posicao is not None and acumulado > capacidade

    aviso = ""
    if capacidade is not None and acumulado > capacidade:
        aviso = (
            f"A ordem que definiste soma {acumulado} pontos e a capacidade do sprint é {capacidade}. "
            "Os pedidos marcados já não cabem."
        )
    return pedidos, aviso
