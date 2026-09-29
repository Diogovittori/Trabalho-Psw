from django import forms, template
from django.forms import CheckboxInput, CheckboxSelectMultiple, RadioSelect
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

register = template.Library()


def _field_classes(field):
    widget = field.field.widget
    if isinstance(widget, (CheckboxInput, CheckboxSelectMultiple, RadioSelect)):
        return ["form-check-input"]
    return ["form-control"]


def _render_field(field):
    classes = _field_classes(field)
    if field.errors:
        classes.append("is-invalid")

    if field.is_hidden:
        return str(field)
    attrs = {"class": " ".join(classes)}
    described_by = []
    if field.help_text:
        described_by.append(f"{field.auto_id}_helptext")
    if field.errors:
        described_by.append(f"{field.auto_id}_errors")
        attrs["aria-invalid"] = "true"
    if described_by:
        attrs["aria-describedby"] = " ".join(described_by)
    return render_to_string("Plantas/componentes/campo.html", {
        "field": field,
        "widget": field.as_widget(attrs=attrs),
        "grupo": isinstance(field.field.widget, (CheckboxSelectMultiple, RadioSelect)),
    })


@register.filter
def bootstrap_field(field):
    return mark_safe(_render_field(field))


@register.filter
def bootstrap_form(form):
    html = render_to_string("Plantas/componentes/erros_formulario.html", {"form": form})
    html += "".join(_render_field(field) for field in form)
    return mark_safe(html)


@register.filter
def imagem_url(value):
    if not value:
        return ""
    if hasattr(value, "url"):
        return value.url
    return value


@register.simple_tag(takes_context=True)
def url_listagem(context):
    request = context.get("request")
    if request is not None and getattr(request, "resolver_match", None) is not None:
        url_name = request.resolver_match.url_name
        if url_name.startswith("categoria_"):
            return reverse("plantas:categoria_listar")
        if url_name.startswith("planta_"):
            return reverse("plantas:planta_listar")
        if url_name.startswith("cuidado_"):
            return reverse("plantas:cuidado_listar")
        if url_name.startswith("fotografia_"):
            return reverse("plantas:fotografia_listar")
    return reverse("plantas:planta_listar")
