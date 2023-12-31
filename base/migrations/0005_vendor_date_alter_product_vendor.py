# Generated by Django 4.2 on 2023-10-13 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_product_category_alter_vendor_vid'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='base.vendor'),
        ),
    ]
