# Generated by Django 4.2.3 on 2023-08-17 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gsadashboard', '0015_categorybyrfq_rfq_delete_rfqcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorybyrfq',
            name='alreadyExists',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='categorybyrfq',
            name='hideInEbuy',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='categorybyrfq',
            name='valid',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
