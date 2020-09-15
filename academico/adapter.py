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
        if email_domain(sociallogin.user.email) not in allowed_signup_domains:
            return False
        return super(SocialAccountAdapter, self).is_open_for_signup(request, sociallogin)



# class RestrictEmailAdapter(DefaultSocialAccountAdapter):
#     def clean_email(self,email):
#         RestrictedList = ['guillermitus@gmail.com']
#         print(RestrictedList)
#         if email in RestrictedList:
#             raise ValidationError('You are restricted from registering. Please contact admin.')
#         return email