
# Register your models here.
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import AllUsers
from .forms import AllUsersCreationform , AllUsersChangeform




# Register your models here.
class AllUsersAdmin(UserAdmin):
    add_form = AllUsersCreationform
    form = AllUsersChangeform
    models = AllUsers
    list_display= ('email','is_superuser','is_customer','is_organizer','date_joined')
    list_filter= ('email','is_superuser','is_customer','is_organizer')
    fieldsets =(
        (None,{'fields':('email','password',)}),
        ('Permissions',{'fields':('is_staff','is_active','is_customer','is_organizer','is_superuser','groups','user_permissions')}),

    )
    add_fieldsets=(
        (None, {
            'classes':('wide',),
            'fields': ('email' ,'password1','password2','is_staff','is_active','is_superuser')}
        ),
    )

    search_fields = ('email',)
    ordering= ('email',)




admin.site.register(AllUsers ,AllUsersAdmin)









class Customer_DataAdmin(admin.ModelAdmin):
    list_display = ['Name' ,'Mobile','uid','user']
admin.site.register(Customer_Data,Customer_DataAdmin )

class Ordered_Tickets_DetailAdmin(admin.ModelAdmin):
    list_display = ['Booking_id','TicketName','Total_Ticket','Total_Ticket_Price']
admin.site.register(Ordered_Tickets_Detail,Ordered_Tickets_DetailAdmin )

class Booking_DetailAdmin(admin.ModelAdmin):
    list_display = ['uid','Booked_by','Event_Name','Total_amount','Order_id']
admin.site.register(Booking_Detail , Booking_DetailAdmin )





class Business_DataAdmin(admin.ModelAdmin):
    list_display = ['Business_Name','Contact','uid','user','created_at']
admin.site.register(Business_Data,Business_DataAdmin )

class Event_detailAdmin(admin.ModelAdmin):
    list_display = ['Event_Name','uid','created_at','Organizer','Startdate']
admin.site.register(Event_detail,Event_detailAdmin )

class Event_TicketAdmin(admin.ModelAdmin):
    list_display = ['Ticket_type','uid','created_at','Created_by']
admin.site.register(Event_Ticket,Event_TicketAdmin )





