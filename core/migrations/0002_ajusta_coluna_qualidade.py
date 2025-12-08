from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]


    operations = [
        migrations.AddField(
            model_name='registrosono',
            name='qualidade_sono',
            field=models.IntegerField(default=3),
        ),
    ]
