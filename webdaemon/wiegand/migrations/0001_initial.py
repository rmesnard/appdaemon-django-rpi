# Generated by Django 2.2.3 on 2019-07-23 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_text', models.CharField(max_length=100)),
                ('info_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_text', models.CharField(max_length=100)),
                ('last_use_date', models.DateTimeField(verbose_name='last use')),
                ('expire_date', models.DateTimeField(verbose_name='expiration date')),
                ('state_text', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_text', models.CharField(max_length=100)),
                ('last_use_date', models.DateTimeField(verbose_name='last use')),
                ('model_text', models.CharField(max_length=8)),
                ('state_text', models.CharField(max_length=20)),
                ('error_counter_int', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_text', models.CharField(max_length=100)),
                ('last_use_date', models.DateTimeField(verbose_name='last use')),
                ('state_text', models.CharField(max_length=20)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wiegand.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid_text', models.CharField(max_length=100)),
                ('name_text', models.CharField(max_length=100)),
                ('last_use_date', models.DateTimeField(verbose_name='last use')),
                ('state_text', models.CharField(max_length=20)),
                ('associated_pin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wiegand.Pin')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wiegand.User')),
            ],
        ),
        migrations.AddField(
            model_name='pin',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wiegand.User'),
        ),
    ]
