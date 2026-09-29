from django.db import migrations


def corrigir_nomes(apps, schema_editor):
    Planta = apps.get_model("plantas", "Planta")
    # Pares invertidos confirmados no banco existente. Não inferir pelo formato
    # do nome nem trocar todas as linhas: registros corretos devem ser preservados.
    pares = (
        ("Girassol", "Helianthus annuus"),
        ("Orquídea", "Phalaenopsis amabilis"),
        ("Rosa", "Rosa × hybrida"),
    )
    for popular, cientifico in pares:
        Planta.objects.using(schema_editor.connection.alias).filter(
            nome_popular=cientifico, nome_cientifico=popular
        ).update(nome_popular=popular, nome_cientifico=cientifico)


class Migration(migrations.Migration):
    dependencies = [("plantas", "0008_remove_planta_status")]

    # Reverter o esquema não deve reintroduzir dados incorretos.
    operations = [migrations.RunPython(corrigir_nomes, migrations.RunPython.noop)]
