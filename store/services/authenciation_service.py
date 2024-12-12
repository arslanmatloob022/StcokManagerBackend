from datetime import  timedelta
from hashlib import sha256
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
import requests
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.conf import settings
import time
from django.core.exceptions import ObjectDoesNotExist
import base64
from rest_framework.exceptions import ValidationError

from store.models import CustomUser
class AuthenticationService:

    @staticmethod
    def login(email, password, is_superuser):
        if is_superuser:
            user: CustomUser = CustomUser.objects.filter(email=email, is_superuser=True).first()
        else:
            #check not for superuser
            user: CustomUser = CustomUser.objects.filter(email=email, is_superuser=False).first()
            if not user:
                raise AuthenticationFailed('Only company users login allowed')
            
        #check if user not active
        if user is None or not user.is_active:
            raise AuthenticationFailed('User not active ')
        if user is None or not user.check_password(password):
            raise AuthenticationFailed('Invalid email or password')

        # if user.unblock_date is not None and user.unblock_date > timezone.now():
        #     raise PermissionDenied(f'You were blocked')

        access_token = str(AccessToken.for_user(user))
        refresh_token = str(RefreshToken.for_user(user))

        return access_token, refresh_token, user
    
    @staticmethod
    def login_other_profile(email):
        
        user: CustomUser = CustomUser.objects.filter(email=email).first()

        if user is None or not user.is_active:
            print('before login')
            raise AuthenticationFailed('User not active ')
        print('after login')

        # if user.unblock_date is not None and user.unblock_date > timezone.now():
        #     raise PermissionDenied(f'You were blocked')

        access_token = str(AccessToken.for_user(user))
        refresh_token = str(RefreshToken.for_user(user))

        return access_token, refresh_token, user

    @staticmethod
    def change_password(user: CustomUser, password):
        subject = 'Success! Your password has been changed'
        msg_html = 'common/change_password.html'

        user.set_password(password)
        user.save()
        # send_html_email_message.delay(user_id=user.id, subject=subject, msg_html=msg_html)
    