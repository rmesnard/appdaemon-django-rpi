# Generated by Django 2.2.3 on 2019-07-31 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wiegand', '0005_auto_20190729_1228'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_text', models.CharField(max_length=100)),
                ('type_status', models.CharField(choices=[('H', 'HomeAssistant'), ('M', 'MQTT'), ('A', 'API')], max_length=1)),
                ('payload', models.CharField(max_length=200)),
                ('topic', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_text', models.CharField(max_length=100)),
                ('iftype', models.CharField(choices=[('T', 'Tag used'), ('P', 'PIN used'), ('S', 'Status'), ('N', 'Not Status')], max_length=1)),
                ('ifchain', models.CharField(choices=[('A', 'IF'), ('A', 'AND'), ('O', 'OR')], max_length=1)),
                ('status_trigger_value', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_text', models.CharField(max_length=100)),
                ('type_status', models.CharField(choices=[('H', 'HomeAssistant'), ('M', 'MQTT'), ('A', 'API')], max_length=1)),
                ('last_udate_date', models.DateTimeField(blank=True, null=True, verbose_name='last update')),
                ('value_text', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='tag',
            name='associated_pin',
        ),
        migrations.AddField(
            model_name='pin',
            name='valid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tag',
            name='expire_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='expiration date'),
        ),
        migrations.AddField(
            model_name='tag',
            name='valid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='pin',
            name='last_use_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last use'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='last_use_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last use'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='last_use_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last use'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_use_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last use'),
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_text', models.CharField(max_length=100)),
                ('last_use_date', models.DateTimeField(blank=True, null=True, verbose_name='last use')),
                ('enabled', models.BooleanField(default=True)),
                ('actions', models.ManyToManyField(to='wiegand.Action')),
                ('conditions', models.ManyToManyField(to='wiegand.Condition')),
            ],
        ),
        migrations.AddField(
            model_name='condition',
            name='associated_pin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wiegand.Tag'),
        ),
        migrations.AddField(
            model_name='condition',
            name='associated_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wiegand.Status'),
        ),
        migrations.AddField(
            model_name='condition',
            name='associated_tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wiegand.Pin'),
        ),
    ]