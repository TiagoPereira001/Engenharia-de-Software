"""Regras dos pedidos.

A API só recebe e devolve dados; as regras ficam aqui, para se poderem
testar sem passar pelo HTTP (ver wiki/04-arquitetura/arquitetura.md).
"""

import re

from django.db import transaction
from django.db.models import Count, Q

from .models import Estado, MudancaEstado, Origem, Pedido, Voto

# Transições permitidas, iguais ao diagrama de estados (wiki/05-modelacao/estados-e-atividades.md).
TRANSICOES = {
    Estado.NOVO: {Estado.EM_ANALISE},
    Estado.EM_ANALISE: {Estado.APROVADO, Estado.REJEITADO},
    Estado.APROVADO: {Estado.EM_DESENVOLVIMENTO},
    Estado.EM_DESENVOLVIMENTO: {Estado.EM_REVISAO},
    Estado.EM_REVISAO: {Estado.EM_DESENVOLVIMENTO, Estado.CONCLUIDO},
    Estado.REJEITADO: set(),
    Estado.CONCLUIDO: set(),
}


class RegraViolada(Exception):
    """Pedido de mudança que as regras do produto não deixam fazer."""


@transaction.atomic
def criar_pedido(*, autor, titulo, descricao, categoria, origem=Origem.SISTEMA):
    # Só quem gere pedidos pode registar um pedido que chegou por outro caminho.
    if not autor.gere_pedidos:
        origem = Origem.SISTEMA
    pedido = Pedido.objects.create(
        autor=autor, titulo=titulo.strip(), descricao=descricao.strip(), categoria=categoria, origem=origem
    )
    MudancaEstado.objects.create(pedido=pedido, de="", para=Estado.NOVO, autor=autor)
    return pedido


@transaction.atomic
def mudar_estado(*, pedido, para, autor, motivo=""):
    if para not in TRANSICOES[Estado(pedido.estado)]:
        raise RegraViolada(f"Não se pode passar de {pedido.get_estado_display()} para {Estado(para).label}.")
    if para == Estado.REJEITADO and not motivo.strip():
        raise RegraViolada("Para rejeitar um pedido é preciso escrever o motivo.")
    MudancaEstado.objects.create(pedido=pedido, de=pedido.estado, para=para, motivo=motivo.strip(), autor=autor)
    pedido.estado = para
    pedido.save(update_fields=["estado", "atualizado_em"])
    return pedido


def alternar_voto(*, pedido, utilizador):
    """Vota, ou retira o voto se já tinha votado. Devolve se ficou com voto."""
    apagados, _ = Voto.objects.filter(pedido=pedido, utilizador=utilizador).delete()
    if apagados:
        return False
    Voto.objects.get_or_create(pedido=pedido, utilizador=utilizador)
    return True


def _raizes(texto):
    """Palavras com 4 ou mais letras, cortadas a 6 para 'exportar' apanhar 'exportação'."""
    palavras = re.findall(r"\w+", texto.lower())
    return {p[:6] for p in palavras if len(p) >= 4}


def procurar_parecidos(texto, limite=5):
    """Primeira versão: procura pedidos com as mesmas palavras no título ou na descrição.

    Quando a base de dados passar a PostgreSQL, isto troca por semelhança por trigramas.
    """
    raizes = _raizes(texto)
    if not raizes:
        return []
    filtro = Q()
    for r in raizes:
        filtro |= Q(titulo__icontains=r) | Q(descricao__icontains=r)
    candidatos = Pedido.objects.exclude(estado=Estado.REJEITADO).filter(filtro).annotate(total_votos=Count("votos"))

    def pontos(p):
        return len(raizes & _raizes(p.titulo)) * 2 + len(raizes & _raizes(p.descricao))

    return sorted(candidatos, key=lambda p: (-pontos(p), -p.total_votos))[:limite]
