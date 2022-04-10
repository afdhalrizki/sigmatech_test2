from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import TopUpSerializer, PaymentSerializer, TransferSerializer

from members.models import User
from .models import Balance, TopUp, Payment, Transfer

class TopUpView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TopUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentSerializer

    def post(self, request):
        serializer = self.serializer_class(
                                            data=request.data,
                                            context={'user_id': request.user.id}
                                        )
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransferView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransferSerializer

    def post(self, request):
        serializer = self.serializer_class(
                                            data=request.data,
                                            context={'user_id': request.user.id}
                                          )
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)
            return Response({'message': 'Transfer request has been made'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # def post(self, request):
    #     serializer = self.serializer_class(
    #                                         data=request.data,
    #                                         context={'user_id': request.user.id}
    #                                     )
    #     if serializer.is_valid():
    #         serializer.save(user_id=request.user.id)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        balance = Balance.objects.filter(member=user).order_by('-created_date')
        transactions_list = []
        for b in balance:
            if b.transaction == 'TOPUP':
                to = TopUp.objects.get(balance_id=b.id)
                topup = {'top_up_id': to.top_up_id,
                         'status': to.status,
                         'user_id': user.user_id,
                         'transaction_type': to.transaction_type, 
                         'amount': to.amount_top_up,
                         'remarks': to.remarks,
                         'balance_before': to.balance_before,
                         'balance_after': to.balance_after,
                         'created_date': to.created_date,
                        }
                transactions_list.append(topup)
            elif b.transaction == 'PAYMENT':
                pay = Payment.objects.get(balance_id=b.id)
                payment = {
                            'payment_id': pay.payment_id,
                            'status': pay.status,
                            'user_id': user.user_id,
                            'transaction_type': pay.transaction_type,
                            'amount': pay.amount,
                            'remarks': pay.remarks,
                            'balance_before': pay.balance_before,
                            'balance_after': pay.balance_after,
                            'created_date': pay.created_date,
                          }
                transactions_list.append(payment)
            elif b.transaction == 'TRANSFER':
                trf = Transfer.objects.get(balance_id=b.id)
                target_user = User.objects.get(id=trf.target_user_id)
                transfer = {
                                'transfer_id': trf.transfer_id,
                                'status': trf.status,
                                'user_id': target_user.user_id,
                                'transaction_type': trf.transaction_type,
                                'amount': trf.amount,
                                'remarks': trf.remarks,
                                'balance_before': trf.balance_before,
                                'balance_after': trf.balance_after,
                                'created_date': trf.created_date,
                            }
                transactions_list.append(transfer)
                
        return Response(transactions_list)
