# code
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from order import models as order
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from smshandler import twilio_core
 
 
@receiver(post_save, sender=order.OrderModel)
def send_order_email(sender, instance, created, **kwargs):
    if created:
        twilio_core.TwilioSMSHandler('test ksks ', '+13156108162', '+9108920563723').send()
        
        
        # # prepare email data
        # subject = 'Order Confirmation'
        # to = [instance.user.email]
        # context = {'order': instance}

        # # render email template
        # body = render_to_string('email.order_confirm.html', context)

        # # create and send email message
        # email_message = EmailMessage(subject, body, to=to)
        # email_message.send()