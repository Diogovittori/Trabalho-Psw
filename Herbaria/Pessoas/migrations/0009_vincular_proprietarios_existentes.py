from django.db import migrations


def vincular_proprietarios(apps, schema_editor):
    alias = schema_editor.connection.alias
    Group = apps.get_model("auth", "Group")
    User = apps.get_model("auth", "User")
    grupo = Group.objects.using(alias).get(name="proprietario")
    for usuario in User.objects.using(alias).filter(groups__name="Proprietário").iterator():
        usuario.groups.add(grupo)


class Migration(migrations.Migration):
    dependencies = [("pessoas", "0008_grupo_proprietario")]
    operations = [migrations.RunPython(vincular_proprietarios, migrations.RunPython.noop)]
