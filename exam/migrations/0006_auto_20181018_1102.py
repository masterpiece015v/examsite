# Generated by Django 2.0.7 on 2018-10-18 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0005_auto_20181018_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addlicenserequest',
            name='check',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='u_admin',
            field=models.SmallIntegerField(default=0, max_length=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='u_enable',
            field=models.SmallIntegerField(default=1, max_length=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='u_hidden',
            field=models.SmallIntegerField(default=0, max_length=1),
        ),
    ]
