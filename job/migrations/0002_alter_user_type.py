# Generated by Django 4.2 on 2023-05-09 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('Com', 'Company'), ('Reg', 'Regular')], default='Reg', max_length=3),
        ),
    ]