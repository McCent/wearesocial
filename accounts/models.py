from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from paypal.standard.forms import PayPalPaymentsForm
from wearesocial import settings
import uuid



class AccountUserManager (UserManager):
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        creates and saves a User with the given username, email and password
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        user = self.model(username=email, email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    """
    now that we've abstracted this class we can add any number of custom attribute to our user class
    in later units we'll be adding things like payment details
    """

    stripe_id = models.CharField(max_length=40, default='')
    subscription_end = models.DateTimeField(default=timezone.now())

    objects = AccountUserManager()

class Product(models.Model):
    name = models.CharField(max_length=254, default='')
    descritpion = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    @property
    def paypal_form(self):
        paypal_dict= {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": self.price,
            "currency_code": "USD",
            "item_name": self.name,
            "invoice": "%s-%s"% (self.pk, uuid.uuid4()),
            "notify_url": settings.PAYPAL_NOTIFY_URL,
            "return_url": "%s/paypal-return/" % settings.SITE_URL,
            "cancel_return": "%s/paypal-cancel/" % settings.SITE_URL,
        }

        return PayPalPaymentsForm(initial=paypal_dict)