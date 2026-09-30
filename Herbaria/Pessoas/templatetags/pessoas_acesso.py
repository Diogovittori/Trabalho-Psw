from django import template

from Pessoas.acesso import pode_gerenciar_pessoas

register = template.Library()
register.filter("pode_gerenciar_pessoas", pode_gerenciar_pessoas)
