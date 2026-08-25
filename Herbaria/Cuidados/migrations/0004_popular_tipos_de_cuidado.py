from django.db import migrations


TIPOS_DE_CUIDADO = (
    ("regar_muito", "Regar muito"),
    ("regar_pouco", "Regar pouco"),
    ("regar_moderadamente", "Regar moderadamente"),
    ("adubar", "Adubar"),
    ("podar", "Podar"),
    ("local_iluminado", "Colocar em local iluminado"),
    ("luz_direta", "Colocar sob luz direta"),
    ("local_sombreado", "Colocar em local sombreado"),
    ("controlar_pragas", "Controlar pragas"),
    ("trocar_substrato", "Trocar o substrato"),
)


def criar_tipos_de_cuidado(apps, schema_editor):
    TipoDeCuidado = apps.get_model("cuidados", "TipoDeCuidado")
    for codigo, nome in TIPOS_DE_CUIDADO:
        TipoDeCuidado.objects.get_or_create(codigo=codigo, defaults={"nome": nome})


class Migration(migrations.Migration):
    dependencies = [("cuidados", "0003_tipodecuidado_remove_cuidados_tipo_cuidados_tipo")]

    operations = [migrations.RunPython(criar_tipos_de_cuidado, migrations.RunPython.noop)]