"""Regras do product backlog, dos sprints e das equipas (US-10, US-11 e US-13).

A ordem do backlog é a ordem do Product Owner, que vive no módulo Priorização:
aqui só se lê, não se repete (wiki/04-arquitetura/desenho.md).
"""

from django.db import transaction

from contas.models import Papel
from pedidos.models import Estado
from pedidos.servicos import RegraViolada, SemPermissao

from .models import EstadoSprint, ItemBacklog, Sprint

# No quadro do sprint, uma coluna por estado (ecrã 07).
COLUNAS = [Estado.APROVADO, Estado.EM_DESENVOLVIMENTO, Estado.EM_REVISAO, Estado.CONCLUIDO]


def _so_product_owner(autor, acao):
    if autor.papel != Papel.PRODUCT_OWNER:
        raise SemPermissao(f"Só o Product Owner pode {acao}.")


def esforco_de(item):
    estimativa = getattr(item.pedido, "estimativa", None)
    return estimativa.esforco if estimativa else None


def _posicao_de(item):
    estimativa = getattr(item.pedido, "estimativa", None)
    return estimativa.posicao if estimativa and estimativa.posicao else float("inf")


def _itens():
    return ItemBacklog.objects.select_related("pedido__estimativa", "pedido__categoria", "equipa", "sprint")


@transaction.atomic
def acrescentar_ao_backlog(*, pedido, autor):
    """Um pedido aprovado entra no product backlog (US-10)."""
    _so_product_owner(autor, "acrescentar pedidos ao backlog")
    if pedido.estado != Estado.APROVADO:
        raise RegraViolada("Só os pedidos aprovados entram no product backlog.")
    return ItemBacklog.objects.get_or_create(pedido=pedido)[0]


def product_backlog():
    """O que falta fazer e ainda não está em nenhum sprint, pela ordem do Product Owner."""
    itens = _itens().filter(sprint__isnull=True).exclude(pedido__estado__in=[Estado.CONCLUIDO, Estado.REJEITADO])
    return sorted(itens, key=lambda i: (_posicao_de(i), i.acrescentado_em))


def pronto_para_sprint(item):
    """Devolve (pode entrar, porquê não). Um item só entra no sprint se tiver estimativa (US-11)."""
    if esforco_de(item) is None:
        return False, "sem estimativa: não pode entrar"
    return True, ""


@transaction.atomic
def criar_sprint(*, autor, nome, objetivo, inicio, fim, capacidade):
    _so_product_owner(autor, "criar sprints")
    if fim <= inicio:
        raise RegraViolada("O sprint tem de acabar depois de começar.")
    if not objetivo.strip():
        raise RegraViolada("O sprint precisa de um objetivo.")
    return Sprint.objects.create(
        nome=nome.strip(), objetivo=objetivo.strip(), inicio=inicio, fim=fim, capacidade=capacidade
    )


def pontos(sprint):
    return sum(esforco_de(i) or 0 for i in _itens().filter(sprint=sprint))


def aviso_capacidade(sprint):
    usados = pontos(sprint)
    if usados > sprint.capacidade:
        return f"O sprint tem {usados} pontos e a capacidade é {sprint.capacidade}."
    return ""


@transaction.atomic
def por_no_sprint(*, item, sprint, autor):
    """Passa um item do product backlog para o sprint. Devolve o aviso de capacidade, se houver."""
    _so_product_owner(autor, "planear o sprint")
    if sprint.estado == EstadoSprint.FECHADO:
        raise RegraViolada("O sprint já está fechado.")
    pode, motivo = pronto_para_sprint(item)
    if not pode:
        raise RegraViolada(f"Este pedido não pode entrar no sprint: {motivo}.")
    item.sprint = sprint
    item.save(update_fields=["sprint"])
    return aviso_capacidade(sprint)


@transaction.atomic
def tirar_do_sprint(*, item, autor):
    _so_product_owner(autor, "planear o sprint")
    item.sprint = None
    item.save(update_fields=["sprint"])


@transaction.atomic
def comecar_sprint(*, sprint, autor):
    _so_product_owner(autor, "começar o sprint")
    if Sprint.objects.filter(estado=EstadoSprint.EM_CURSO).exclude(pk=sprint.pk).exists():
        raise RegraViolada("Já há um sprint em curso. Fecha-o antes de começar outro.")
    if sprint.estado != EstadoSprint.PLANEADO:
        raise RegraViolada("Só se começa um sprint planeado.")
    sprint.estado = EstadoSprint.EM_CURSO
    sprint.save(update_fields=["estado"])
    return sprint


@transaction.atomic
def fechar_sprint(*, sprint, autor):
    """Fecha o sprint. O que não ficou concluído volta ao product backlog (US-11). Devolve quantos voltaram."""
    _so_product_owner(autor, "fechar o sprint")
    if sprint.estado == EstadoSprint.FECHADO:
        raise RegraViolada("O sprint já está fechado.")
    voltam = _itens().filter(sprint=sprint).exclude(pedido__estado=Estado.CONCLUIDO)
    quantos = voltam.update(sprint=None)
    sprint.estado = EstadoSprint.FECHADO
    sprint.save(update_fields=["estado"])
    return quantos


def quadro(sprint, equipa=None):
    """Itens do sprint por coluna de estado (ecrã 07). Pode filtrar-se por equipa (US-13)."""
    itens = _itens().filter(sprint=sprint)
    if equipa:
        itens = itens.filter(equipa_id=equipa)
    colunas = {estado: [] for estado in COLUNAS}
    for item in itens:
        if item.pedido.estado in colunas:
            colunas[item.pedido.estado].append(item)
    return colunas


@transaction.atomic
def atribuir_equipa(*, item, equipa, autor):
    """O gestor de projeto (ou o Product Owner) diz que equipa faz o trabalho (US-13)."""
    if autor.papel not in (Papel.GESTOR_PROJETO, Papel.PRODUCT_OWNER):
        raise SemPermissao("Só o gestor de projeto ou o Product Owner atribuem trabalho a equipas.")
    item.equipa = equipa
    item.save(update_fields=["equipa"])
    return item
