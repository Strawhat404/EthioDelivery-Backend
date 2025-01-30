import json
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Payment

# Stripe webhook secret from settings
STRIPE_WEBHOOK_SECRET = settings.STRIPE_WEBHOOK_SECRET

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        return JsonResponse({"error": "Invalid payload"}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({"error": "Invalid signature"}, status=400)

    # Handle different event types
    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        stripe_payment_id = payment_intent["id"]

        # Update Payment model
        try:
            payment = Payment.objects.get(stripe_payment_intent_id=stripe_payment_id)
            payment.status = "SUCCESS"
            payment.save()
        except Payment.DoesNotExist:
            pass

    elif event["type"] == "payment_intent.payment_failed":
        payment_intent = event["data"]["object"]
        stripe_payment_id = payment_intent["id"]

        try:
            payment = Payment.objects.get(stripe_payment_intent_id=stripe_payment_id)
            payment.status = "FAILED"
            payment.save()
        except Payment.DoesNotExist:
            pass

    return JsonResponse({"status": "success"}, status=200)
