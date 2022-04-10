from celery import shared_task
from .models import Balance, Transfer
from members.models import User


@shared_task(bind=True)
def test_func(param):
    return 'The tasks executed with the following parameter: "%s" '

@shared_task(bind=True)
def transfer_on_the_background(self, validated_data):
    print("masuk")
    user = User.objects.get(id=validated_data['user_id'])

    target_user = User.objects.get(phone_number=validated_data['target_user'])

    latest_balance1 = Balance.objects.filter(member=user).latest('created_date')
    b1 = Balance(id=None, member=user, debit=validated_data['amount'], balance=latest_balance1.balance-validated_data['amount'], transaction='TRANSFER')
    b1.save()

    latest_balance2 = Balance.objects.filter(member=target_user).latest('created_date')
    b2 = Balance(id=None, member=target_user, credit=validated_data['amount'], balance=latest_balance2.balance+validated_data['amount'], transaction='TRANSFER')
    b2.save()
    
    # Pengirim Transfer
    t1 = Transfer.objects.create(
        amount=validated_data['amount'],
        remarks=validated_data['remarks'],
        status='SUCCESS',
        transaction_type='DEBIT',
        balance_before=latest_balance1.balance,
        balance_after=b1.balance,
        target_user = target_user,
        balance=b1
    )

    t1.save()

    # Penerima Transfer
    t2 = Transfer.objects.create(
        amount=validated_data['amount'],
        remarks=validated_data['remarks'],
        status='SUCCESS',
        transaction_type='CREDIT',
        balance_before=latest_balance2.balance,
        balance_after=b2.balance,
        target_user = user,
        balance=b2
    )

    t2.save()

    return "Transfer Succeed"
