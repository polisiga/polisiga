from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.forms import ValidationError

from allauth.account.signals import user_logged_in
from django.dispatch import receiver

from django.core.exceptions import ObjectDoesNotExist

from .models import Docente

from django.contrib.auth.models import Group

@receiver(user_logged_in)
def login_callback(sender, **kwargs):
    print("User logged in!")

    try:
        docente = Docente.objects.get(email=kwargs['user'].email)
    except ObjectDoesNotExist:
        pass
    else:
        
        docente.user = kwargs['user']
        try:
            grupo_docente = Group.objects.get(name='docente')
        except ObjectDoesNotExist:
            pass
        else:
            grupo_docente.user_set.add(kwargs['user'])
        docente.save()
    finally:
        pass





def email_domain(email):
    """Extracts the domain from an email address.

    Warning: this is simplified and you may want a true email address parser.
    """
    return email.split('@')[-1]


# Note: this would be better in settings.py
allowed_signup_domains = [
    'pol.una.py',
    'fpuna.edu.py',
]


class SocialAccountAdapter(DefaultSocialAccountAdapter):


    def is_open_for_signup(self, request, sociallogin):
        """
        Si el usuario tiene los dominios pol.una.py o fpuna.edu.py
        se registra dentro del sistema, luego este usuario se debe
        enlazar con el objeto Docente y dar los permisos correspondiente.
        """

        if email_domain(sociallogin.user.email) not in allowed_signup_domains:
            return False
        return super(SocialAccountAdapter, self).is_open_for_signup(request, sociallogin)


