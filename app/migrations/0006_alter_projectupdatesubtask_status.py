# Generated by Django 4.2.13 on 2024-11-28 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_projectupdate_enddate_projectupdate_startdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectupdatesubtask',
            name='status',
            field=models.CharField(blank=True, default='ongoing', max_length=100, null=True),
        ),
    ]