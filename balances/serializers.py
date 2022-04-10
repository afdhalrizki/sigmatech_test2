from pkg_resources import require
from rest_framework import serializers
from .models import Balance, TopUp, Payment, Transfer
from members.models import User

from .tasks import transfer_on_the_background

class TopUpSerializer(serializers.Serializer):
    amount_top_up = serializers.IntegerField(required=True)

    def create(self, validated_data):
        user = User.objects.get(id=validated_data['user_id'])
        latest_balance = Balance.objects.filter(member=user).latest('created_date')
        b = Balance(id=None, member=user, credit=validated_data['amount_top_up'], balance=latest_balance.balance+validated_data['amount_top_up'], transaction='TOPUP')
        b.save()

        to = TopUp.objects.create(
            amount_top_up=validated_data['amount_top_up'],
            status='SUCCESS',
            transaction_type='CREDIT',
            balance_before=latest_balance.balance,
            balance_after=b.balance,
            balance=b
        )

        to.save()

        return to


class PaymentSerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True)
    remarks = serializers.CharField(required=True)
    
    def validate(self, attrs):

        user = User.objects.get(id=self.context['user_id'])
        
        latest_balance = Balance.objects.filter(member=user).latest('created_date')

        if attrs['amount'] > latest_balance.balance:
            raise serializers.ValidationError({'message': 'Balance is not enough'})

        return attrs

    def create(self, validated_data):

        user = User.objects.get(id=validated_data['user_id'])

        latest_balance = Balance.objects.filter(member=user).latest('created_date')
        b = Balance(id=None, member=user, debit=validated_data['amount'], balance=latest_balance.balance-validated_data['amount'], transaction='PAYMENT')
        b.save()

        p = Payment.objects.create(
            amount=validated_data['amount'],
            remarks=validated_data['remarks'],
            status='SUCCESS',
            transaction_type='DEBIT',
            balance_before=latest_balance.balance,
            balance_after=b.balance,
            balance=b
        )
    
        p.save()

        return p

class TransferSerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True)
    remarks = serializers.CharField(required=True)
    target_user = serializers.CharField(required=True)

    def validate(self, attrs):

        user = User.objects.get(id=self.context['user_id'])
        
        latest_balance = Balance.objects.filter(member=user).latest('created_date')

        if attrs['amount'] > latest_balance.balance:
            raise serializers.ValidationError({'message': 'Balance is not enough'})

        return attrs
    
    def create(self, validated_data):
        transfer_on_the_background.delay(validated_data)
        return {'message': 'Transfer request has been made'}

    # def create(self, validated_data):

    #     user = User.objects.get(id=validated_data['user_id'])

    #     target_user = User.objects.get(phone_number=validated_data['target_user'])

    #     latest_balance1 = Balance.objects.filter(member=user).latest('created_date')
    #     b1 = Balance(id=None, member=user, debit=validated_data['amount'], balance=latest_balance1.balance-validated_data['amount'], transaction='TRANSFER')
    #     b1.save()

    #     latest_balance2 = Balance.objects.filter(member=target_user).latest('created_date')
    #     b2 = Balance(id=None, member=target_user, credit=validated_data['amount'], balance=latest_balance2.balance+validated_data['amount'], transaction='TRANSFER')
    #     b2.save()
        
    #     # Pengirim Transfer
    #     t1 = Transfer.objects.create(
    #         amount=validated_data['amount'],
    #         remarks=validated_data['remarks'],
    #         status='SUCCESS',
    #         transaction_type='DEBIT',
    #         balance_before=latest_balance1.balance,
    #         balance_after=b1.balance,
    #         target_user = target_user,
    #         balance=b1
    #     )
    
    #     t1.save()

    #     # Penerima Transfer
    #     t2 = Transfer.objects.create(
    #         amount=validated_data['amount'],
    #         remarks=validated_data['remarks'],
    #         status='SUCCESS',
    #         transaction_type='CREDIT',
    #         balance_before=latest_balance2.balance,
    #         balance_after=b2.balance,
    #         target_user = user,
    #         balance=b2
    #     )

    #     t2.save()

    #     return t1