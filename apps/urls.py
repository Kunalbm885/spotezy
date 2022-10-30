from os import name
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from . import views



from django.contrib.auth.views import LogoutView , LoginView


urlpatterns = [
    # path('google-login/', views.google_login, name="google_login"),



    # path('accounts/' , include('allauth.urls')),
    path("",views.Homepage,name="homepage"),

    path("request",views.handlerequest,name="handlerequest"),
    path("response/",views.handleresponse,name="handleresponse"),

    #-------------------------------USER--------------------------------------#
    # path("userreg",views.regCust,name="regCust"),
    path("user_login/",views.LoginAuthentication,name="UserLogin"),
    path("userdashboard/",views.userdash,name="userdashboard"),
    path("order_summary-page/<pk>",views.orders,name="order_summary"),
    path("Events/<idd>",views.show_eventdetails_booknow,name="show_eventdetails_booknow"),



    #-------------------------------BIZZZ--------------------------------------#
    path("business_contactus/",views.TaketoBcontactus,name="biz_contactus_pg"),
    path("business_login/",views.BizLogin,name="BusinessLogin"),
    path("business-reg/",views.curator_Reg,name="curator_Reg"),
    path("dashboard/create-event",views.Dashboard_form1,name="Dashboard-form1-page"),
    path("Create-Event/ticketing-2/<pk>/",views.Dashboard_form2,name="Dashboard-form2-page"),
    path("Created-Events/<pk>",views.Created_Events,name="Created_Events"),
    path("publish-Event/<pk>/<fk>",views.Publish_Event,name="Publish_Event"),
    path("view-Event/<eveid>/<bizuid>",views.View_Event,name="View_Event"),
    path("<pk>/<id>",views.Delete_ticket,name="delete_ticket"),
    path("del/<pk>/",views.Delete_Event,name="delete_event"),
    path("<pk>/",views.Update_ticket,name="updatetickets"),
    path("",views.logoutcreator,name="logoutcreator"),



    #-------------------------------SOCIAL AUTHENTICATION-------------------------------------#
    path('accounts/' ,include('allauth.urls')),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

