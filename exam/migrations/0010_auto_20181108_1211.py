# Generated by Django 2.0.7 on 2018-11-08 03:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0009_auto_20181108_1210'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answerimage',
            old_name='o',
            new_name='o_id',
        ),
        migrations.RenameField(
            model_name='answerimage',
            old_name='t',
            new_name='t_id',
        ),
        migrations.RenameField(
            model_name='answerimage',
            old_name='u',
            new_name='u_id',
        ),
    ]
