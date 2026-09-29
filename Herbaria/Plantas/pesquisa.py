"""Pesquisa no banco e paginação compartilhadas pelas listagens e busca geral."""
from datetime import datetime
import re
import unicodedata

from django.core.paginator import Paginator
from django.db.models import Q


CAMPOS = {
    "plantas": ("nome_popular", "nome_cientifico", "descricao", "categoria__nome"),
    "fotografias": ("planta__nome_popular", "planta__nome_cientifico", "planta__categoria__nome"),
    "cuidados": ("planta__nome_popular", "planta__nome_cientifico", "tipo__nome", "tipo__codigo", "observacoes"),
    "categorias": ("nome", "descricao"),
}
DATAS = {"plantas": "data_plantio", "fotografias": "data_foto", "cuidados": "data"}


def padrao_texto(palavra):
    """Aceita acentos portugueses e maiúsculas sem executar regex do usuário."""
    variantes = {"a": "[aáàâãä]", "e": "[eéèêë]", "i": "[iíìîï]",
                 "o": "[oóòôõö]", "u": "[uúùûü]", "c": "[cç]", "n": "[nñ]"}
    normalizada = "".join(c for c in unicodedata.normalize("NFD", palavra.casefold())
                          if not unicodedata.combining(c))
    return "".join(variantes.get(c, re.escape(c)) for c in normalizada)


def termo_pesquisa(request):
    return request.GET.get("q", "").strip()[:200]


def filtrar(queryset, entidade, termo):
    if not termo:
        return queryset
    data = None
    for formato in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            data = datetime.strptime(termo, formato).date()
            break
        except ValueError:
            pass
    if data and entidade in DATAS:
        return queryset.filter(**{DATAS[entidade]: data})
    for palavra in termo.split():
        condicao = Q()
        padrao = padrao_texto(palavra)
        for campo in CAMPOS[entidade]:
            condicao |= Q(**{f"{campo}__iregex": padrao})
        queryset = queryset.filter(condicao)
    # A relação N:N dos tipos de cuidado pode produzir a mesma linha mais de uma vez.
    return queryset.distinct()


def contexto_listagem(request, queryset, entidade):
    termo = termo_pesquisa(request)
    pagina = Paginator(filtrar(queryset, entidade, termo), 12).get_page(request.GET.get("page"))
    dicas = {
        "plantas": "Nome popular, científico, descrição, categoria ou data de plantio (dd/mm/aaaa).",
        "fotografias": "Nome da planta, categoria ou data da fotografia (dd/mm/aaaa).",
        "cuidados": "Nome da planta, tipo, observações ou data do cuidado (dd/mm/aaaa).",
        "categorias": "Nome ou descrição da categoria.",
    }
    return {entidade: pagina.object_list, "page_obj": pagina, "q": termo,
            "pesquisa_dica": dicas[entidade]}
