from django.db import migrations


def corrigir_referencia(apps, schema_editor):
    Pessoa = apps.get_model("pessoas", "Pessoa")
    vinculos = Pessoa.plantas.through
    alias = schema_editor.connection.alias
    registros = list(vinculos.objects.using(alias).values("id", "pessoa_id", "planta_id"))
    # A migração 0005 atualizou os valores, mas deixou a FK apontando para o id antigo.
    # Recria somente a tabela intermediária usando a chave atual, preservando cada vínculo.
    schema_editor.delete_model(vinculos)
    schema_editor.create_model(vinculos)
    vinculos.objects.using(alias).bulk_create([vinculos(**registro) for registro in registros])


class Migration(migrations.Migration):
    dependencies = [("pessoas", "0009_vincular_proprietarios_existentes")]
    operations = [migrations.RunPython(corrigir_referencia, migrations.RunPython.noop)]
