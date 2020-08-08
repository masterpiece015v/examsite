# Generated by Django 3.0.6 on 2020-07-31 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0005_question_q_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionJs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q_id', models.CharField(max_length=10)),
                ('q_period', models.CharField(max_length=6)),
                ('q_subject', models.CharField(max_length=2)),
                ('q_num', models.CharField(max_length=2)),
                ('q_title', models.CharField(max_length=20)),
                ('q_content', models.CharField(max_length=80)),
            ],
        ),
    ]
