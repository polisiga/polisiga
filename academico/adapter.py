from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.forms import ValidationError



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


