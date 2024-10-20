from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Refunds, RefundItems
from order.models import Orders, OrderItem
from payment.models import Payment
from .serializers import RefundSerializer, RefundStatusUpdateSerializer
from django.utils import timezone
from accounts.models import UserAccount
from django.db import transaction
from rest_framework.exceptions import AuthenticationFailed
from accounts.token_authentication import CustomTokenAuthentication
# from .permissions import IsAdminOrHasRefundPermission




class RefundRequestView(generics.CreateAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RefundSerializer


    # def post(self, request, *args, **kwargs):
    #     user = self.request.user
    #     if not user:
    #         raise AuthenticationFailed('User not Found.')
 
    #     order_id = request.data.get('order')
    #     reason = request.data.get('reason')
    #     amount = request.data.get('amount')

    #     try:
    #         order = Orders.objects.get(order_id=order_id, user=user)
    #     except Orders.DoesNotExist:
    #         return Response({'error': 'Order not found or not associated with this user.'}, status=status.HTTP_404_NOT_FOUND)

    #     # Check if a refund request already exists for this order
    #     if Refund.objects.filter(order=order).exists():
    #         return Response({'message': 'You have already sent a request for a refund for this order.'}, status=status.HTTP_400_BAD_REQUEST)
        
    #     refund = Refund.objects.create(
    #         order=order,
    #         reason=reason,
    #         amount=amount,
    #         status='PENDING',
    #         requested_by=user
    #     )

    #     serializer = RefundSerializer(refund)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def post(self, request, *args, **kwargs):
        user = self.request.user
        if not user:
            raise AuthenticationFailed('User not Found.')

        order_id = request.data.get('order')
        print(order_id)

        reason = request.data.get('reason')
        amount = request.data.get('amount')
        transaction_id = request.data.get('transaction')
        # transaction_id = transaction_id.data.get('transaction_id')
        print(transaction_id)
        refund_items_data = request.data.get('refund_items', [])


        try:
            order = Orders.objects.get(order_id=order_id, user=user)
        except Orders.DoesNotExist:
            return Response({'error': 'Order not found or not associated with this user.'}, status=status.HTTP_404_NOT_FOUND)

      
        try:
            payment = Payment.objects.get( order=order, transaction_id=transaction_id)
            print(payment)
        except Payment.DoesNotExist:
            return Response({'error': 'Transaction not found or not associated with this user.'}, status=status.HTTP_404_NOT_FOUND)

        if Refunds.objects.filter(order=order, transaction_id=payment).exists():
            return Response({'message': 'You have already sent a request for a refund for this order and transaction.'}, status=status.HTTP_400_BAD_REQUEST)

        refund = Refunds.objects.create(
            order=order,
            transaction_id=payment,

            reason=reason,
            amount=amount,
            status='PENDING',
            requested_by=user,
        )

        for item_data in refund_items_data:
            order_item_id = item_data['order_item']
            quantity = item_data['quantity']
            try:
                order_item = OrderItem.objects.get(id=order_item_id, order=order)
            except OrderItem.DoesNotExist:
                return Response({'error': f'Order item {order_item_id} not found or not associated with this order.'}, status=status.HTTP_404_NOT_FOUND)
            RefundItems.objects.create(refund=refund, order_item=order_item, quantity=quantity)

        serializer = RefundSerializer(refund)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RefundRequestUpdateView(generics.UpdateAPIView):
    authentication_classes = [CustomTokenAuthentication]

    serializer_class = RefundSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Refunds.objects.filter(requested_by=user)

    def put(self, request, *args, **kwargs):
        refund = self.get_object()
        serializer = self.get_serializer(refund, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class RefundProcessView(generics.UpdateAPIView):
    authentication_classes = [CustomTokenAuthentication]

    serializer_class = RefundStatusUpdateSerializer
    permission_classes = [IsAdminUser]
    queryset = Refunds.objects.all()

    
    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        refund = self.get_object()
        if refund.status != 'PENDING':
            return Response({'error': 'Refund has already been processed.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(refund, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data['status'] == 'APPROVED':
            order_items = OrderItem.objects.filter(order=refund.order)

            # Adjust stock levels
            for item in order_items:
                product = item.product
                product.stock += item.quantity
                product.save()


            
            # Subtract shipping cost from refund amount
            refund_amount = refund.amount - refund.order.shipping_cost.rate

            # Update financial records
            refund.order.total_amount -= refund_amount
            refund.order.grand_total -= refund.amount
            refund.order.save()

            refund.processed_at = timezone.now()
            refund.processed_by = request.user
            refund.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

