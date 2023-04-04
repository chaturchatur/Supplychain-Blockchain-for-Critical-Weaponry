# Generated by Django 3.2.9 on 2021-12-07 04:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('indent', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='indent',
            name='owner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]