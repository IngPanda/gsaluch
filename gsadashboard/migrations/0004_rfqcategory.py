# Generated by Django 4.2.3 on 2023-07-19 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gsadashboard', '0003_remove_rfqmodel_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='RFQCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gsadashboard.category')),
                ('rfq', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gsadashboard.rfqmodel')),
            ],
        ),
    ]
