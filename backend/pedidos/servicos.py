"""Regras dos pedidos.

A API só recebe e devolve dados; as regras ficam aqui, para se poderem
testar sem passar pelo HTTP (ver wiki/04-arquitetura/arquitetura.md).
"""

import re

from django.db import transaction
from django.db.models import Count, Q

from contas.models import Papel

from .models import Estado, Etiqueta, MudancaEstado, Origem, Pedido, Voto

GESTAO = {Papel.PRODUCT_MANAGER, Papel.PRODUCT_OWNER}

# Cada passagem do diagrama de estados e quem a pode fazer (wiki/05-modelacao/estados-e-atividades.md).
# O product manager faz a triagem, o programador leva o trabalho até à revisão e o Product Owner aceita.
QUEM_PODE = {
    (Estado.NOVO, Estado.EM_ANALISE): GESTAO,
    (Estado.EM_ANALISE, Estado.APROVADO): GESTAO,
    (Estado.EM_ANALISE, Estado.REJEITADO): GESTAO,
    (Estado.APROVADO, Estado.EM_DESENVOLVIMENTO): {Papel.PROGRAMADOR, Papel.PRODUCT_OWNER},
    (Estado.EM_DESENVOLVIMENTO, Estado.EM_REVISAO): {Papel.PROGRAMADOR},
    (Estado.EM_REVISAO, Estado.EM_DESENVOLVIMENTO): {Papel.PROGRAMADOR, Papel.PRODUCT_OWNER},
    (Estado.EM_REVISAO, Estado.CONCLUIDO): {Papel.PRODUCT_OWNER},
}

# Transições permitidas, tiradas da tabela de cima para não haver duas listas a manter.
TRANSICOES = {estado: {para for (de, para) in QUEM_PODE if de == estado} for estado in Estado}


class RegraViolada(Exception):
    """Pedido de mudança que as regras do produto não deixam fazer."""


class SemPermissao(Exception):
    """A mudança existe, mas o papel de quem a pede não a pode fazer."""


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


def estados_seguintes(pedido, utilizador):
    """Para onde este utilizador pode levar o pedido agora. O ecrã usa isto para mostrar os botões."""
    if not utilizador.is_authenticated:
        return []
    return [para for (de, para), papeis in QUEM_PODE.items() if de == pedido.estado and utilizador.papel in papeis]


@transaction.atomic
def mudar_estado(*, pedido, para, autor, motivo=""):
    if para not in TRANSICOES[Estado(pedido.estado)]:
        raise RegraViolada(f"Não se pode passar de {pedido.get_estado_display()} para {Estado(para).label}.")
    if autor.papel not in QUEM_PODE[(pedido.estado, para)]:
        raise SemPermissao(f"O teu papel não pode passar um pedido para {Estado(para).label}.")
    if para == Estado.REJEITADO and not motivo.strip():
        raise RegraViolada("Para rejeitar um pedido é preciso escrever o motivo.")
    MudancaEstado.objects.create(pedido=pedido, de=pedido.estado, para=para, motivo=motivo.strip(), autor=autor)
    pedido.estado = para
    pedido.save(update_fields=["estado", "atualizado_em"])
    return pedido


def _nomes_de_etiquetas(nomes):
    """Minúsculas, sem espaços a mais e sem repetidos, pela ordem em que vieram."""
    vistos = []
    for nome in nomes:
        nome = " ".join(nome.split()).lower()[:30]
        if nome and nome not in vistos:
            vistos.append(nome)
    return vistos


@transaction.atomic
def classificar(*, pedido, autor, categoria=None, etiquetas=None):
    """Muda a categoria e as etiquetas de um pedido (US-02). Só quem gere pedidos."""
    if not autor.gere_pedidos:
        raise SemPermissao("Só o product manager ou o Product Owner classificam pedidos.")
    if categoria is not None:
        pedido.categoria = categoria
        pedido.save(update_fields=["categoria", "atualizado_em"])
    if etiquetas is not None:
        pedido.etiquetas.set([Etiqueta.objects.get_or_create(nome=n)[0] for n in _nomes_de_etiquetas(etiquetas)])
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
