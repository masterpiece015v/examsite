# Generated by Django 3.0.6 on 2020-10-29 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0013_questioncbtpmresult_a_datetime'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionBoki',
            fields=[
                ('b_id', models.CharField(max_length=11, primary_key=True, serialize=False)),
                ('b_org', models.CharField(max_length=1)),
                ('b_times', models.CharField(max_length=3)),
                ('b_class', models.CharField(max_length=1)),
                ('b_que1', models.CharField(max_length=1)),
                ('b_que2', models.CharField(max_length=1)),
                ('b_field', models.CharField(max_length=40)),
            ],
        ),
    ]