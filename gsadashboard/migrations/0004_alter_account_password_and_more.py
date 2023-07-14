# Generated by Django 4.2.3 on 2023-07-11 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gsadashboard', '0003_alter_account_codegsa_alter_account_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='password',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='attachments',
            name='docSessionDate',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='modifications',
            name='time',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='rfqmodel',
            name='cancelTime',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='rfqmodel',
            name='closeTime',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='rfqmodel',
            name='closedDate',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='rfqmodel',
            name='issueTime',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='rfqmodel',
            name='leadTime',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='rfqmodel',
            name='password',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='rfqmodel',
            name='popEndDate',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='rfqmodel',
            name='popStartDate',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='rfqmodel',
            name='valid',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
