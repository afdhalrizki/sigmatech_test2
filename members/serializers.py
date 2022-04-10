from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from balances.models import Balance, TopUp
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Import django packages
from django.utils.translation import gettext_lazy as _

class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all(), message="Phone Number already registered")]
        )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('phone_number', 'password', 'confirm_password','first_name', 'last_name', 'address')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            phone_number=validated_data['phone_number'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            address=validated_data['address'],
        )

        user.set_password(validated_data['password'])
        user.save()

        # initialize first balance
        b = Balance(id=None, member=user, balance=0, transaction='TOPUP')
        b.save()

        to = TopUp.objects.create(
            id=None,
            amount_top_up=0,
            status='SUCCESS',
            transaction_type='CREDIT',
            balance_before=b.balance,
            balance_after=b.balance+0,
            balance=b
        )

        to.save()

        return user

class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    address = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('user_id', 'first_name', 'last_name', 'address', 'updated_date')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'address': {'required': True},
        }
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': _("Phone number and pin doesn't match.")
    }