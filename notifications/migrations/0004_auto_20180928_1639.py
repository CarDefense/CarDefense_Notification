# Generated by Django 2.1 on 2018-09-28 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_apiuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmergencyNotifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_id', models.IntegerField()),
                ('title', models.CharField(max_length=10)),
                ('message', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='APIUser',
        ),
        migrations.DeleteModel(
            name='NotificationEmergency',
        ),
    ]