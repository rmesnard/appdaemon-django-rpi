# Generated by Django 2.2.3 on 2019-07-29 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiegand', '0003_auto_20190723_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pin',
            name='expire_date',
            field=models.DateTimeField(blank=True, verbose_name='expiration date'),
        ),
    ]