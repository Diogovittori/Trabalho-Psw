from django.db import migrations, models


def copiar_tipo_existente(apps, schema_editor):
    Cuidados = apps.get_model("plantas", "Cuidados")
    for cuidado in Cuidados.objects.all():
        cuidado.tipo = [cuidado.tipo_antigo]
        cuidado.save(update_fields=["tipo"])


class Migration(migrations.Migration):
    dependencies = [
        ("plantas", "0002_alterar_tipos_de_cuidado_remover_status"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cuidados", old_name="tipo", new_name="tipo_antigo"
        ),
        migrations.AddField(
            model_name="cuidados",
            name="tipo",
            field=models.JSONField(default=list, verbose_name="tipos de cuidado"),
        ),
        migrations.RunPython(copiar_tipo_existente, migrations.RunPython.noop),
        migrations.RemoveField(model_name="cuidados", name="tipo_antigo"),
    ]
