
from email.policy import default
from re import L
from django.contrib.auth.models import User
from django.db import models
import uuid
from ckeditor.fields import RichTextField

from django.contrib.auth.models import AbstractBaseUser ,AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import AllUsersManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone




class AllUsers(AbstractBaseUser , PermissionsMixin):
    email = models.EmailField(_('email address') , unique=True)
    is_active =models.BooleanField(default=True)
    is_staff =models.BooleanField(default=False)
    is_customer =models.BooleanField(default=False)
    is_organizer =models.BooleanField(default=False)

    is_superuser =models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS= []

    objects = AllUsersManager()

    def __str__(self):
        return self.email


# Create your models here.
class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True , default=uuid.uuid4 ,editable=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract :True



class Customer_Data(BaseModel):
    user = models.OneToOneField(AllUsers ,on_delete=models.CASCADE )
    Name = models.CharField(max_length=50)
    Mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.Name



class Booking_Detail(BaseModel):
    Booked_by = models.ForeignKey("AllUsers" ,on_delete=models.CASCADE )
    Event_Id = models.CharField(max_length=80)
    Event_Name = models.CharField(max_length=100)
    Total_amount = models.CharField(max_length=80)
    Order_id = models.CharField(max_length=80)
    Spot_id = models.CharField(max_length=20 , default="SPOT_ID")
    Tx_id_PG = models.CharField(max_length=20 , default="CASHFREE_REF_ID")

    def __str__(self):
        return self.Event_Name    

class Ordered_Tickets_Detail(BaseModel):
    Booking_id = models.ForeignKey("Booking_Detail", on_delete=models.CASCADE)    
    TicketName = models.CharField(max_length=80)
    Total_Ticket = models.CharField(max_length=100)
    Total_Ticket_Price = models.CharField(max_length=80)

    def __str__(self):
        return self.TicketName    





# ***********************************************************************************************************************************











class Business_Data(BaseModel):
    user = models.OneToOneField(AllUsers ,on_delete=models.CASCADE )
    Business_Name = models.CharField(max_length=50)
    Contact = models.CharField(max_length=40)
    Registered_As = models.CharField(max_length=20 , default="")
    

    def __str__(self):
        return self.Business_Name





class Event_detail(BaseModel):
    Event_img = models.ImageField(upload_to='images/')
    Event_Name = models.CharField(max_length=100 , default='')
    Is_Carousel = models.CharField(max_length=10 , default='')
    Organizer = models.CharField(max_length=200 , default='')
    Category = models.CharField(max_length=100, default='')
    Startdate = models.CharField(max_length=10, default='')
    Starttime = models.CharField(max_length=10, default='')
    Endtime = models.CharField(max_length=10, default='')
    orgtype = models.CharField(max_length=10, default='')
    Age = models.CharField(max_length=4, default='18+') 
    Language = models.CharField(max_length=50, default='Hinglish')
    City = models.CharField(max_length=100, default='')
    Fulladdress = models.CharField(max_length=500, default='')
    Description = RichTextField(blank=True ,null=True)
    TnC = RichTextField(blank=True ,null=True ,max_length=3500, default='')
    Status = models.CharField(max_length=800, default='Unpublished',null=True)


    @property
    def uuiid(self):
        return self.Organizer.uid



class Event_Ticket(BaseModel):
    Ticket_type = models.CharField(max_length=150 , default='')
    Description = models.TextField(max_length=150 , default='')
    Created_by = models.CharField(max_length=200 , default='')
    Price = models.CharField(max_length=10, default='')
    Expected_Quantity = models.CharField(max_length=10, default='')
    Expiry_Date = models.CharField(max_length=10, default='')
    Expiry_Time = models.CharField(max_length=10, default='')
    Additional_data = models.CharField(max_length=150,null=True,blank=True, default='')
   
    
    def __str__(self):
        return self.Created_by



