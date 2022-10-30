from dataclasses import field
from re import A
from django import forms 
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import AllUsers
  
    # class UploadImageForm(forms.ModelForm): 
    
    #     class Meta: 
    #         model = Event_detail 
    #         fields = ['Event_img','Event_Name','Description'] 

    #         # ,'organizer','category','startdate','starttime','city','fulladdress','Description','tnc'

class AllUsersCreationform(UserCreationForm):
    class Meta(UserCreationForm):
        model = AllUsers
        fields = ('email',)


class AllUsersChangeform(UserChangeForm):
    class Meta:
        model = AllUsers
        fields = ('email',)
