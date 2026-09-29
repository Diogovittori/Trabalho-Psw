import re
from pathlib import Path

from django import forms
from django.conf import settings
from django.contrib.staticfiles import finders
from django.template.loader import render_to_string
from django.test import SimpleTestCase

from .templatetags.herbaria_ui import bootstrap_form


class IntegracaoTemaTests(SimpleTestCase):
    def test_dependencias_css_locais_existem(self):
        raiz = Path(settings.BASE_DIR) / "Plantas/static/Plantas"
        for css in raiz.rglob("*.css"):
            for ref in re.findall(r"url\([\"']?([^\)\"']+)", css.read_text(encoding="utf-8")):
                if ref.startswith(("http:", "https:", "//", "data:")):
                    continue
                caminho = ref.split("?")[0].split("#")[0]
                if caminho:
                    with self.subTest(css=css.name, recurso=ref):
                        self.assertTrue((css.parent / caminho).is_file())

    def test_template_base_resolve_estaticos_e_ordena_dependencias(self):
        html = render_to_string("Plantas/base.html")
        for caminho in re.findall(r'(?:src|href)="/static/([^\"]+)"', html):
            self.assertIsNotNone(finders.find(caminho.split("?")[0]), caminho)
        scripts = ["jquery-2.2.4.min.js", "popper.min.js", "bootstrap.min.js", "plugins.js", "herbaria.js"]
        posicoes = [html.index(script) for script in scripts]
        self.assertEqual(posicoes, sorted(posicoes))

    def test_estilizacao_preserva_campos_erros_e_valores(self):
        class Formulario(forms.Form):
            nome = forms.CharField()
            data = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
            tipos = forms.MultipleChoiceField(
                choices=[("regar", "Regar"), ("adubar", "Adubar")],
                widget=forms.CheckboxSelectMultiple,
            )
        form = Formulario({"nome": "Roseira", "data": "invalida", "tipos": ["regar", "adubar"]})
        self.assertFalse(form.is_valid())
        html = bootstrap_form(form)
        self.assertIn('name="nome"', html)
        self.assertIn('value="Roseira"', html)
        self.assertIn('class="form-control is-invalid"', html)
        self.assertEqual(html.count(' checked'), 2)
        self.assertIn('class="errorlist"', html)
