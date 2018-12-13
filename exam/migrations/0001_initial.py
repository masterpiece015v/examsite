# Generated by Django 2.0.7 on 2018-10-15 02:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_id', models.CharField(max_length=100)),
                ('a_date', models.DateTimeField()),
                ('a_ipa', models.CharField(max_length=100)),
                ('a_page', models.CharField(max_length=100)),
                ('a_state', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Auth',
            fields=[
                ('auth_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('auth_kind', models.CharField(max_length=10)),
                ('auth_value', models.CharField(max_length=100)),
                ('auth_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Classify',
            fields=[
                ('c_id', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('l_id', models.CharField(max_length=2)),
                ('l_name', models.CharField(max_length=40)),
                ('m_id', models.CharField(max_length=2)),
                ('m_name', models.CharField(max_length=40)),
                ('s_id', models.CharField(max_length=2)),
                ('s_name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='LittleTest',
            fields=[
                ('t_key', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('t_id', models.CharField(max_length=4)),
                ('t_num', models.CharField(max_length=4)),
                ('t_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Org',
            fields=[
                ('o_id', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('o_name', models.CharField(max_length=40)),
                ('l_num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('q_id', models.CharField(max_length=9, primary_key=True, serialize=False)),
                ('q_test', models.CharField(max_length=2)),
                ('q_period', models.CharField(max_length=5)),
                ('q_num', models.CharField(max_length=2)),
                ('q_title', models.CharField(max_length=100)),
                ('q_answer', models.CharField(max_length=1)),
                ('c', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Classify')),
            ],
        ),
        migrations.CreateModel(
            name='ResultTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r_answer', models.CharField(max_length=1)),
                ('r_date', models.DateTimeField()),
                ('t', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.LittleTest')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('u_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('u_email', models.EmailField(max_length=100)),
                ('u_pass', models.CharField(max_length=20)),
                ('u_name', models.CharField(max_length=40)),
                ('u_admin', models.BooleanField(default=False)),
                ('u_enable', models.BooleanField(default=True)),
                ('u_hidden', models.BooleanField(default=False)),
                ('u_date', models.DateField()),
                ('o', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Org')),
            ],
        ),
        migrations.AddField(
            model_name='resulttest',
            name='u',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.User'),
        ),
        migrations.AddField(
            model_name='littletest',
            name='o',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Org'),
        ),
        migrations.AddField(
            model_name='littletest',
            name='q',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Question'),
        ),
    ]
