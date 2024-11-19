# Generated by Django 4.2.13 on 2024-11-11 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('unit_cost', models.FloatField()),
                ('totalCost', models.FloatField(blank=True, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('processor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
