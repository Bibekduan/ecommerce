# Generated by Django 4.2 on 2023-10-14 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews', to='base.product'),
        ),
    ]