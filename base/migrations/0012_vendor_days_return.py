# Generated by Django 4.2 on 2023-10-13 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_alter_product_life'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='days_return',
            field=models.CharField(blank=True, default='100', max_length=100, null=True),
        ),
    ]
