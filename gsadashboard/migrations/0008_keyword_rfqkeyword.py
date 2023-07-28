# Generated by Django 4.2.3 on 2023-07-27 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gsadashboard', '0007_category_activesearch'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('icon', models.CharField(max_length=35, null=True)),
                ('activeSearch', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RFQKeyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gsadashboard.keyword')),
                ('rfq', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gsadashboard.rfqmodel')),
            ],
        ),
    ]
