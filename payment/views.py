
from accounts.token_authentication import CustomTokenAuthentication
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Payment
from order.models import Orders
from cart.models import Carts
from .serializers import PaymentSerializer, CardInformationSerializer
from rest_framework.exceptions import AuthenticationFailed
import uuid
import stripe
import requests
from sslcommerz_lib import SSLCOMMERZ

from django.conf import settings
from django.shortcuts import render, redirect



# Stripe settings
stripe.api_key = settings.STRIPE_SECRET_KEY
# stripe.api_key = settings.STRIPE_PUBLISHABLE_KEY


# Create your views here.
from django.views.generic import TemplateView

class PaymentFormView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        order_id = self.request.data.get('order')
        method = self.request.data.get('payment_method')

        try:
            order = Orders.objects.get(order_id=order_id, user=user)
        except Orders.DoesNotExist:
            raise ValidationError("Order not found or does not belong to this user.")

        transaction_id = str(uuid.uuid4())
        amount = order.grand_total

        if method == 'stripe':
            return redirect('create-checkout-session')   
        elif method == 'cash_on_delivery':
            cod_response = self.cod_payment({})
            if cod_response['status'] == status.HTTP_200_OK:
                payment_status = 'pending'
            else:
                raise ValidationError("COD payment initiation failed")
            
            serializer.save(user=user, order=order, transaction_id=transaction_id, payment_status=payment_status, amount=amount)
        elif method == 'ssl_ecommerce':
            payment_status = 'pending'
        elif method == 'bkash':
            payment_status = 'pending'
        else:
            raise ValidationError("Invalid payment method.")

    # def create_stripe_checkout_session(self, order, user, serializer):
    #     amount_in_cents = int(order.grand_total * 100)
    #     try:
    #         checkout_session = stripe.checkout.Session.create(
    #             payment_method_types=['card'],
    #             line_items=[
    #                 {
    #                     'price_data': {
    #                         'currency': 'usd',
    #                         'product_data': {
    #                             'name': f'Order {order.order_id}',
    #                         },
    #                         'unit_amount': amount_in_cents,
    #                     },
    #                     'quantity': 1,
    #                 },
    #             ],
    #             mode='payment',
    #             success_url=self.request.build_absolute_uri('/api/payments/success') + '?session_id={CHECKOUT_SESSION_ID}',
    #             cancel_url=self.request.build_absolute_uri('/api/payments/cancel') + '?session_id={CHECKOUT_SESSION_ID}',
    #         )

    #         serializer.save(
    #             user=user,
    #             order=order,
    #             transaction_id=checkout_session.id,
    #             payment_status='pending',
    #             amount=order.grand_total
    #         )

    #         return Response({'checkout_url': checkout_session.url}, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         raise ValidationError(str(e))

    def cod_payment(self, data):
        return {
            'message': 'Cash on Delivery payment initiated',
            'status': status.HTTP_200_OK,
            'redirect_url': self.request.build_absolute_uri('/api/payments/success')
        }

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = "Payment successfully made."
        return response




   
class PaymentCreateViewAPI(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    authentication_classes = [CustomTokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        order_id = self.request.data.get('order')
        method = self.request.data.get('payment_method')

        try:
            order = Orders.objects.get(order_id=order_id, user=user)
        except Orders.DoesNotExist:
            raise ValidationError("Order not found or does not belong to this user.")

        transaction_id = str(uuid.uuid4())
        amount = order.grand_total
        amount_in_cents = int(order.grand_total * 100)

        if method == 'stripe':
            stripe_data = self.request.data.get('stripe')
            stripe_serializer = CardInformationSerializer(data=stripe_data)
            if stripe_serializer.is_valid():
                card_details = {
                    "number": stripe_serializer.validated_data['card_number'],
                    "exp_month": stripe_serializer.validated_data['expiry_month'],
                    "exp_year": stripe_serializer.validated_data['expiry_year'],
                    "cvc": stripe_serializer.validated_data['cvc'],
                }
                try:
                    payment_intent = stripe.PaymentIntent.create(
                        amount=amount_in_cents,
                        currency='usd',
                        payment_method_data={"type": "card", "card": card_details},
                        confirm=True,
                        metadata={'order_id': order_id},
                        return_url='http://127.0.0.1:8000/api/payments/success', 
                    )
                    transaction_id = payment_intent.id
                    payment_status = 'completed' if payment_intent.status == 'succeeded' else 'failed'
                except stripe.error.CardError as e:
                    raise ValidationError(e.user_message)
                except stripe.error.StripeError as e:
                    raise ValidationError(f"Stripe error: {e.user_message}")
                except Exception as e:
                    raise ValidationError(f"Payment error: {str(e)}")

                serializer.save(user=user, order=order, transaction_id=transaction_id, payment_status=payment_status, amount=order.grand_total)
                return Response({'message': 'Payment successfully made.', 'payment_status': payment_status}, status=status.HTTP_200_OK)
            else:
                raise ValidationError(stripe_serializer.errors)




        elif method == 'cash_on_delivery':

            cod_response = self.cod_payment({})
            if cod_response['status'] == status.HTTP_200_OK:
                payment_status = 'pending'
            else:
                raise ValidationError("COD payment initiation failed")
            
            serializer.save(user=user, order=order, transaction_id=transaction_id, payment_status=payment_status, amount=amount)
            
            
            

        elif method == 'ssl_ecommerce':
            # Implement SSL E-commerce integration here
            payment_status = 'pending'
        elif method == 'bkash':
            # Implement Bkash integration here
            payment_status = 'pending'
        else:
            raise ValidationError("Invalid payment method.")

        # serializer.save(user=user, order=order, transaction_id=transaction_id, payment_status=payment_status, amount=amount)

    def cod_payment(self, data):
        # Implement your Cash on Delivery logic here
        return {
            'message': 'Cash on Delivery payment initiated',
            'status': status.HTTP_200_OK,
            'redirect_url': 'http://127.0.0.1:8000/api/payments/success' # Assuming SUCCESS_URL is defined in your settings
        }

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = "Payment successfully made."
        return response
    

class CreateCheckoutSessionStripeView(views.APIView):
    authentication_classes = [CustomTokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]
        
    # def post(self, request, *args, **kwargs):
    #     user = request.user
    #     if not user:
    #         raise AuthenticationFailed('Unauthenticated user.')
        
    #     order_id = request.data.get('order')
    #     try:
    #         order = Orders.objects.get(order_id=order_id, user=user)
    #         price = order.grand_total
    #         # quantity = order.cart.cartitems.quantity
    #     except Orders.DoesNotExist:
    #         raise ValidationError("Order not found or does not belong to this user.")
        
    #     transaction_id = str(uuid.uuid4())
        
    #     try:
    #         checkout_session = stripe.checkout.Session.create(
    #             payment_method_types=['card'],
    #             line_items=[
    #                 {
    #                     'price_data': {
    #                         'currency': 'usd',
    #                         'product_data': {
    #                             'name': 'Order {}'.format(order_id),
    #                         },
    #                         'unit_amount': int(price) ,
    #                     },
    #                     'quantity': 1,
    #                 },
    #             ],
    #             mode='payment',
    #             success_url=request.build_absolute_uri('/api/payments/success') + '?session_id={CHECKOUT_SESSION_ID}',
    #             cancel_url=request.build_absolute_uri('/api/payments/cancel') +'?session_id={CHECKOUT_SESSION_ID}',
    #         )
            
    #         # Save the initial payment info
    #         Payment.objects.create(
    #             user=user,
    #             order=order,
    #             transaction_id=transaction_id,
    #             payment_status='pending',
    #             amount=order.grand_total
    #         )
            
    #     except Exception as e:
    #         raise ValidationError(str(e))

    #     return Response({'checkout_url': checkout_session.url}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user:
            raise AuthenticationFailed('Unauthenticated user.')

        # order_id = request.data.get('order')
        order_id = request.data.get('order')
        method = request.data.get('payment_method')
        if method != 'stripe':
            raise ValidationError("Invalid payment method.")
        try:
            order = Orders.objects.get(order_id=order_id, user=user)
            price = order.grand_total
        except Orders.DoesNotExist:
            raise ValidationError("Order not found or does not belong to this user.")

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': f'Order {order_id}',
                            },
                            'unit_amount': int(price),
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri('/api/payments/success') + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri('/api/payments/cancel') + '?session_id={CHECKOUT_SESSION_ID}',
            )

            # Save the initial payment info
            Payment.objects.create(
                user=user,
                order=order,
                transaction_id=checkout_session.id,  # Use Stripe session ID as transaction_id
                payment_status='pending',
                amount=order.grand_total,
                payment_method='stripe'

            )

        except Exception as e:
            raise ValidationError(str(e))

        return Response({'checkout_url': checkout_session.url}, status=status.HTTP_200_OK)

        

class PaymentStatusUpdateView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Payment.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.user != request.user:
            raise ValidationError("You do not have permission to update this payment.")

        # Confirm the payment intent if the method is Stripe
        if instance.method == 'stripe':
            intent_id = instance.transaction_id
            try:
                intent = stripe.PaymentIntent.retrieve(intent_id)
                if intent.status == 'succeeded':
                    instance.payment_status = 'completed'
                elif intent.status == 'requires_payment_method':
                    instance.payment_status = 'failed'
            except stripe.error.StripeError as e:
                raise ValidationError(f"Stripe error: {e.user_message}")


        instance.save()
        serializer = self.get_serializer(instance, partial=partial)
        return Response(serializer.data)



class PaymentSuccessView(views.APIView):
    authentication_classes = [CustomTokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if not session_id:
            raise ValidationError("No session ID provided.")
        
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)
            
            # Retrieve the payment object using the Stripe session ID
            payment = Payment.objects.get(transaction_id=session_id)
            
            payment.payment_status = 'completed' if payment_intent.status == 'succeeded' else 'failed'
            # payment.payment_method = 'stripe'
            payment.save()
        except Payment.DoesNotExist:
            raise ValidationError("Payment matching query does not exist.")
        except Exception as e:
            raise ValidationError(f"An error occurred: {str(e)}")

        return Response({'message': 'Payment was successful!'}, status=status.HTTP_200_OK)

class PaymentCancelView(views.APIView):
    authentication_classes = [CustomTokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if not session_id:
            raise ValidationError("No session ID provided.")
        
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            payment = Payment.objects.get(transaction_id=session.payment_intent)
            payment.payment_status = 'cancelled'
            payment.save()
        except Exception as e:
            raise ValidationError(f"An error occurred: {str(e)}")

        return render(request, 'payment_cancel.html')



# class CreateSSLCommerzSessionView(views.APIView):
#     authentication_classes = [CustomTokenAuthentication]
    
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         user = self.request.user
#         order_id = request.data.get('order')
#         try:
#             order = Orders.objects.get(order_id=order_id, user=user)
#         except Orders.DoesNotExist:
#             raise ValidationError("Order not found or does not belong to this user.")

#         payment_method = request.data.get('payment_method')
#         if payment_method != 'sslcommerz':
#             raise ValidationError("Invalid payment method.")

#         amount = order.grand_total

#         # SSLCommerz parameters
#         post_data = {
#             'store_id': settings.SSL_COMMERZ_STORE_ID,
#             'store_passwd': settings.SSL_COMMERZ_STORE_PASSWORD,
#             'total_amount': amount,
#             'currency': 'BDT',
#             'tran_id': order_id,
#             'success_url': request.build_absolute_uri('/api/ssl-payments/success/'),
#             'fail_url': request.build_absolute_uri('/api/ssl-payments/fail/'),
#             'cancel_url': request.build_absolute_uri('/api/ssl-payments/cancel/'),
#             'cus_name': user.username,
#             'cus_email': user.email,
#             'cus_add1': 'dhaka',
#             'cus_phone': user.phone,
#         }
        

#         response = requests.post('https://sandbox.sslcommerz.com/gwprocess/v3/api.php', data=post_data, timeout=15)
#         response_data = response.json()
#         # response = createSession(post_data)
# #       return Response({'gateway_url': response['GatewayPageURL']}, status=status.HTTP_200_OK)
#         print("SSLCommerz Response Data:", response_data)



#         if response_data['status'] == 'SUCCESS':
#             Payment.objects.create(
#                 user=user,
#                 order=order,
#                 transaction_id=response_data.get('tran_id'),
#                 payment_status='pending',
#                 amount=amount,
#                 payment_method=payment_method

#             )
#             # serializer.save(user=user,
#             #     order=order,
#             #     transaction_id=response_data['tran_id'],
#             #     payment_status='pending',
#             #     amount=amount,
#             #     payment_method='sslcommerz')
            
#             return Response({'gateway_url': response_data['GatewayPageURL']}, status=status.HTTP_200_OK)

#         else:
#             raise ValidationError("Failed to initiate payment with SSLCommerz.")

class CreateSSLCommerzSessionView(views.APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        order_id = request.data.get('order')

        # Validate the order
        try:
            order = Orders.objects.get(order_id=order_id, user=user)
        except Orders.DoesNotExist:
            raise ValidationError("Order not found or does not belong to this user.")
        
        method = request.data.get('payment_method')
        if method != 'sslcommerz':
            raise ValidationError("Invalid payment method.")

        amount = order.grand_total

        # SSLCommerz parameters
        post_data = {
            'total_amount': amount,
            'currency': 'BDT',
            'tran_id': f"SSLCOMMERZ_{order_id}",  # Unique transaction ID
            'success_url': request.build_absolute_uri('/api/ssl-payments/success/'),
            'fail_url': request.build_absolute_uri('/api/ssl-payments/fail/'),
            'cancel_url': request.build_absolute_uri('/api/ssl-payments/cancel/'),
            'cus_name': user.username,
            'cus_email': user.email,
            'cus_add1': 'Dhaka',  # Corrected city name
            'cus_phone': user.phone,
            'cus_city': 'Dhaka',  # Corrected city name
            'cus_country': 'Bangladesh',  # Corrected country name
            'shipping_method': 'NO',
            'product_name': 'Test Product',  # Changed product name
            'product_category': 'Test Category',
            'product_profile': 'general'
        }

        sslcz = SSLCOMMERZ({
            'store_id': settings.SSL_COMMERZ_STORE_ID,
            'store_pass': settings.SSL_COMMERZ_STORE_PASSWORD,
            'issandbox': settings.SSL_COMMERZ_SANDBOX  # Set to False for production
        })

        response = sslcz.createSession(post_data)

        if response.GET.get['status'] == 'SUCCESS':
            Payment.objects.create(
                user=user,
                order=order,
                transaction_id=response.get('tran_id'),
                payment_status='pending',
                amount=amount,
                payment_method=method
            )
            return Response({'gateway_url': response['GatewayPageURL']}, status=status.HTTP_200_OK)
        else:
            error_message = response.get('failedreason', 'Failed to initiate payment with SSLCommerz.')
            raise ValidationError(error_message)
        

class SSLCommerzSuccessView(views.APIView):
    # authentication_classes = [CustomTokenAuthentication]

    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        transaction_id = request.GET.get('tran_id')
        if not transaction_id:
            raise ValidationError("Transaction ID not provided.")
        
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
            payment.payment_status = 'completed'
            payment.save()
        except Payment.DoesNotExist:
            raise ValidationError("Payment not found.")

        return Response({'message': 'Payment was successful!'}, status=status.HTTP_200_OK)
    
class SSLCommerzFailView(views.APIView):
    # authentication_classes = [CustomTokenAuthentication]

    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        transaction_id = request.GET.get('tran_id')
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
            payment.payment_status = 'failed'
            payment.save()
        except Payment.DoesNotExist:
            raise ValidationError("Payment not found.")

        return Response({'message': 'Payment failed.'}, status=status.HTTP_200_OK)

class SSLCommerzCancelView(views.APIView):
    # authentication_classes = [CustomTokenAuthentication]

    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        transaction_id = request.GET.get('tran_id')
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
            payment.payment_status = 'cancelled'
            payment.save()
        except Payment.DoesNotExist:
            raise ValidationError("Payment not found.")

        return Response({'message': 'Payment was cancelled.'}, status=status.HTTP_200_OK)
    


class SSLCommerzIPNView(views.APIView):
    authentication_classes = [CustomTokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        transaction_id = request.data.get('tran_id')
        val_id = request.data.get('val_id')

        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
            # Verify the payment
            verification_response = requests.post('https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php', data={
                'val_id': val_id,
                # 'store_id': settings.SSL_COMMERZ_STORE_ID,
                # 'store_passwd': settings.SSL_COMMERZ_STORE_PASSWORD,
                'store_id': 'testbox', 
                'store_pass': 'qwerty',
                'issandbox': settings.SSL_COMMERZ_SANDBOX
            })
            verification_data = verification_response.json()
            
            if verification_data['status'] == 'VALID':
                payment.payment_status = 'completed'
            else:
                payment.payment_status = 'failed'
            
            payment.save()
        except Payment.DoesNotExist:
            raise ValidationError("Payment not found.")

        return Response({'message': 'IPN received'}, status=status.HTTP_200_OK)

