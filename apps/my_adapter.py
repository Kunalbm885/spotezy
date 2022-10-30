from django.contrib.auth.models import User
from apps.models import Customer_Data, Business_Data, Event_detail, Event_Ticket, AllUsers

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import Group








class MySocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):

        if sociallogin.is_existing:
            print("EXIST")
            return

        if 'email' not in sociallogin.account.extra_data:
            messages.error(request, 'email is not provided')
            raise ImmediateHttpResponse(redirect('/accounts/login'))

        try:
            user = AllUsers.objects.get(email=sociallogin.account.user.email)
            if user:
                print("WE GOT.........")

        
        except AllUsers.DoesNotExist:
            print("NOT FOUND ................")

            email = sociallogin.account.extra_data['email']
            name = sociallogin.account.extra_data['name']
            print("NAME" + name)

            user = AllUsers.objects.create_user(email=email , password="", is_customer="True")
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            sociallogin.connect(request, user)  # linking account
            user.set_password(None)  # optional, so user can't login with password
            user.save()
            customer_c = Customer_Data.objects.create(
            user=user, Name=name, Mobile="")
            customer_c.save()
            print("NOT FOUND ................")


