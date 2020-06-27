from django.dispatch import receiver
from django.db.models.signals import post_save
from custom_user.models import Verification, MyUser, ContactUs
from custom_user.tasks import send_verification_email, contact_us
from threading import Thread


@receiver(post_save, sender=MyUser, dispatch_uid='create_token')
def create_token(*args, **kwargs):
    obj = kwargs.get("instance")
    created = kwargs.get("created")
    if created:
        Verification.objects.create(
            user=obj
        )


@receiver(post_save, sender=Verification, dispatch_uid='send_mail_to_user')
def send_mail_to_user(*args, **kwargs):
    obj = kwargs.get("instance")
    created = kwargs.get("created")

    if created:
        link = f"http://localhost:8000/verify/{obj.token}/{obj.user_id}/"
        background_job = Thread(target=send_verification_email, args=(obj.user.email, link))
        background_job.start()


@receiver(post_save, sender=ContactUs, dispatch_uid='contactus')
def contactus(*args, **kwargs):
    obj = kwargs.get("instance")
    created = kwargs.get("created")

    if created:
        link = f"{obj.name} {obj.surname} {obj.message}"
        subject = f"{obj.subject}"
        background_job = Thread(target=contact_us, args=(obj.email, link))
        background_job.start()
