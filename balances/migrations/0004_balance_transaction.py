# Generated by Django 4.0.3 on 2022-04-08 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balances', '0003_alter_payment_balance_alter_topup_balance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='transaction',
            field=models.CharField(default='TRANSFER', max_length=10),
            preserve_default=False,
        ),
    ]
