from django.db import migrations


def configurar_grupo(apps, schema_editor):
    alias = schema_editor.connection.alias
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")
    content_type, _ = ContentType.objects.using(alias).get_or_create(app_label="pessoas", model="pessoa")
    grupo, _ = Group.objects.using(alias).get_or_create(name="proprietario")
    for acao, nome in (("add", "Can add pessoa"), ("view", "Can view pessoa"),
                       ("change", "Can change pessoa"), ("delete", "Can delete pessoa")):
        permissao, _ = Permission.objects.using(alias).get_or_create(
            content_type=content_type, codename=f"{acao}_pessoa", defaults={"name": nome},
        )
        grupo.permissions.add(permissao)


class Migration(migrations.Migration):
    dependencies = [
        ("pessoas", "0007_remove_pessoa_sexo"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]
    operations = [migrations.RunPython(configurar_grupo, migrations.RunPython.noop)]
