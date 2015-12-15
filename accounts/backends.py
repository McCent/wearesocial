from models import User
import arrow

class SubscriptionEnded(Exception):
    pass

class EmailAuth(object):
    def authenticate(self, email=None, password=None):
        """
        get an instance of User using the supplied email and check its password
        """
        try:
            user = User.objects.get(email=email)

            subscription_not_ended=arrow.now() == arrow.get(user.subscription_end)
            if not subscription_not_ended:
                raise SubscriptionEnded()

            if user.check_password(password):
                return user

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        used by the django authentication system to retrieve an instance of User
        """
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None