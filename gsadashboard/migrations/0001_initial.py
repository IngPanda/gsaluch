# Generated by Django 4.2.3 on 2023-07-08 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('lastName', models.CharField(max_length=200, null=True)),
                ('password', models.CharField(max_length=16)),
                ('position', models.CharField(max_length=200, null=True)),
                ('codeGSA', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idGSA', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('agency', models.CharField(max_length=200)),
                ('agencyCode', models.CharField(max_length=200)),
                ('userEmail', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RFQModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idGSA', models.CharField(max_length=35)),
                ('title', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=50)),
                ('issueTime', models.CharField(max_length=16)),
                ('closeTime', models.CharField(max_length=16)),
                ('cancelTime', models.CharField(max_length=16)),
                ('idOld', models.IntegerField()),
                ('daysOpen', models.IntegerField()),
                ('shipInd', models.IntegerField()),
                ('referenceNum', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('deliveryDays', models.IntegerField()),
                ('leadTime', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=16)),
                ('sourceSought', models.BooleanField()),
                ('extended', models.BooleanField()),
                ('popStartDate', models.CharField(max_length=16)),
                ('popEndDate', models.CharField(max_length=16)),
                ('quoteCount', models.IntegerField()),
                ('overseas', models.BooleanField()),
                ('closedDate', models.CharField(max_length=16)),
                ('closeHour', models.CharField(max_length=5)),
                ('closeHourPMAM', models.CharField(max_length=3)),
                ('valid', models.CharField(max_length=16)),
                ('awardCount', models.IntegerField()),
                ('connectRFQ', models.BooleanField()),
                ('connectAwardableRFQ', models.BooleanField()),
                ('closed', models.BooleanField()),
                ('gwac', models.BooleanField()),
                ('submitted', models.BooleanField()),
                ('saved', models.BooleanField()),
                ('openRFC', models.BooleanField()),
                ('complimentarySins', models.JSONField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gsadashboard.account')),
                ('userOwner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gsadashboard.userowner')),
            ],
        ),
        migrations.CreateModel(
            name='Modifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('versionNumber', models.IntegerField()),
                ('note', models.TextField()),
                ('time', models.CharField(max_length=16)),
                ('rfq', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gsadashboard.rfqmodel')),
            ],
        ),
        migrations.CreateModel(
            name='Attachments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docName', models.CharField(max_length=200)),
                ('docPath', models.CharField(max_length=200)),
                ('docSeqNum', models.IntegerField()),
                ('docType', models.IntegerField()),
                ('docSessionId', models.IntegerField()),
                ('docSessionDate', models.CharField(max_length=16)),
                ('seqNum', models.IntegerField()),
                ('rfq', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gsadashboard.rfqmodel')),
            ],
        ),
    ]
