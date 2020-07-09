# Generated by Django 3.0.6 on 2020-07-09 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_compquestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionPm',
            fields=[
                ('q_id', models.CharField(max_length=9, primary_key=True, serialize=False)),
                ('q_test', models.CharField(max_length=2)),
                ('q_period', models.CharField(max_length=5)),
                ('q_num', models.IntegerField()),
                ('q_classify', models.CharField(max_length=20)),
                ('q_title', models.CharField(max_length=40)),
            ],
        ),
    ]