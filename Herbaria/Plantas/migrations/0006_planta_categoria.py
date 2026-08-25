import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("categoria", "0001_initial"),
        ("plantas", "0005_remove_planta_categoria_remove_cuidados_planta_and_more"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name="planta",
                    name="categoria",
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="plantas",
                        to="categoria.categoria",
                        verbose_name="categoria",
                    ),
                ),
            ]
        ),
    ]
