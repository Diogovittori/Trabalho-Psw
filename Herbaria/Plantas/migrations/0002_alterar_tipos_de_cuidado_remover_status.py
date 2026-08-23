from django.db import migrations, models


def normalizar_cuidados_existentes(apps, schema_editor):
    Cuidados = apps.get_model("plantas", "Cuidados")
    Cuidados.objects.all().update(tipo="regar_moderadamente")


class Migration(migrations.Migration):
    dependencies = [("plantas", "0001_initial")]

    operations = [
        migrations.RemoveField(model_name="planta", name="status"),
        migrations.AlterField(
            model_name="cuidados",
            name="tipo",
            field=models.CharField(
                choices=[
                    ("regar_muito", "Regar muito"),
                    ("regar_moderadamente", "Regar moderadamente"),
                    ("regar_pouco", "Regar pouco"),
                    ("fertilizar", "Adicionar fertilizante"),
                    ("podar", "Podar regularmente"),
                    ("luz_direta", "Manter sob luz direta"),
                    ("luz_indireta", "Manter em lugar iluminado"),
                    ("sombra", "Manter em local sombreado"),
                    ("controlar_pragas", "Controlar pragas"),
                    ("trocar_substrato", "Trocar o substrato"),
                ],
                max_length=25,
                verbose_name="tipo de cuidado",
            ),
        ),
        migrations.RunPython(
            normalizar_cuidados_existentes, migrations.RunPython.noop
        ),
    ]
