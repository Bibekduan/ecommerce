# Generated by Django 4.2 on 2023-10-13 05:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='tags',
        ),
        migrations.AlterField(
            model_name='category',
            name='cid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=22, max_length=30, prefix='cat', unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='Pid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=22, max_length=30, prefix='', unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=22, max_length=34, prefix='sku', unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]