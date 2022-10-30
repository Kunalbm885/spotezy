from django.shortcuts import redirect, render, reverse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages as msg
from datetime import datetime, timedelta, time, date

# from website.apps.models import Booking_Detail
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from apps.models import Customer_Data, Business_Data, Event_detail, Event_Ticket, AllUsers,Booking_Detail
# from django.contrib.auth.models import AllUsers

from django.utils.crypto import get_random_string
from random import randint
from django.contrib.auth.models import User, auth
from .decorators import *
from django.contrib.auth.models import Group

from .tasks import *

from django.db import IntegrityError
import uuid

from django.views.decorators.csrf import csrf_exempt

import hashlib
import hmac
import base64


def Homepage(request):
    if request.method == "POST":
        u = AllUsers
        print(u)
        username = request.POST['personname']
        useremail = request.POST['username']
        usernumber = request.POST['mobilenumber']
        userpass = request.POST['password']

        u = AllUsers.objects.create_user(
            email=useremail, password=userpass, is_customer="True")
        group = Group.objects.get(name='customer')
        u.groups.add(group)
        u.save()

        customer_c = Customer_Data.objects.create(
            user=u, Name=username, Mobile=usernumber)
        customer_c.save()
        return redirect('userdashboard')

    carousel = Event_detail.objects.all().filter(Is_Carousel="Yes")
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")

    Eventcards = Event_detail.objects.all().filter(Startdate__gte=d1, orgtype="Event")
    Clubcards = Event_detail.objects.all().filter(
        Startdate__gt=d1, orgtype="Club").count()

    return render(request, "homepage.html", {'Eventcards': Eventcards, 'Clubcards': Clubcards, 'carousel': carousel})


def show_eventdetails_booknow(request, idd):

    event_details = Event_detail.objects.all().filter(uid=idd)
    ticket = Event_Ticket.objects.all().filter(Created_by=idd)
    return render(request, "Users/eventdetailpg.html", {'event': event_details, 'tickets': ticket})


# User Section below >>>>>>>>>>>............................................................................................................


@unauthenticated_user
def LoginAuthentication(request):
    if request.method == "POST":
        username = request.POST['uemail']
        password = request.POST['upass']

        user = authenticate(
            email=username, password=password, is_customer="True")
        if user is not None:
            auth.login(request, user)
            return redirect('userdashboard')
        else:
            msg.info(request, 'Invalid Username or Password')
            return redirect('userdashboard')
    else:
        return render(request, "account/login.html",)


def TaketoRegistration(request):
    username = request.POST['Uname']
    useremail = request.POST['Uemail']
    usernumber = request.POST['Umob']
    userpass = request.POST['Upass']
    usercpass = request.POST['Ucpass']

    user = Customer_Data.objects.filter(Email=useremail)

    if user:
        message = "User is already Registered"
        return render(request, "Users/login.html")
    else:
        if userpass == usercpass:
            newcustomer = Customer_Data.objects.create(
                Name=username, Email=useremail, Password=userpass, Mobile=usernumber)
            message = "Teacher Is Successfully Registered !"
            return render(request, "Users/login.html", {'msg1': message})
        else:
            message = "Password did not Matched !"

    return render(request, "Users/login.html", {'msg2': message})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="UserLogin")
@allowed_users(allowed_roles=['customer'])
def userdash(request):
    carousel = Event_detail.objects.all().filter(Is_Carousel="Yes")
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    current_user = request.user
    name = Customer_Data.objects.all().filter(user=current_user)
    for i in name:
        usernamee = i.Name
    Eventcards = Event_detail.objects.all().filter(Startdate__gte=d1, orgtype="Event")
    Clubcards = Event_detail.objects.all().filter(
        Startdate__gt=d1, orgtype="Club").count()

    return render(request, "Users/userhomepage.html", {'Eventcards': Eventcards, 'Clubcards': Clubcards, 'carousel': carousel, 'u': usernamee})




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="UserLogin")
@allowed_users(allowed_roles=['customer'])
def orders(request, pk):
    event_details = Event_detail.objects.all().filter(uid=pk)

    current_user = request.user
    print(current_user.email)
    name = Customer_Data.objects.all().filter(user=current_user)
    for i in name:
        usernamee = i.Name
        phone = i.Mobile

    if request.method == "POST":
        uid = list(request.POST['uids'].split(","))
        name = list(str(request.POST['ticket_type']).split(","))
        price = list(request.POST['price'].split(","))
        number = list(request.POST['total_numbers'].split(","))
        print(number)

        namelist = []
        pricelist = []
        numberlist = []
        more = 0
        total = 0

        for i in range(len(uid)):
            if number[i] != "0":
                cost = int(number[i])*int(price[i])
                pricelist.append(cost)
                namelist.append(name[i])
                numberlist.append(number[i])
                total += cost
                if price[i] >= "2000":
                    more += 150*int(number[i])
                else:
                    more += 100*int(number[i])

        all_list = zip(namelist, numberlist, pricelist)
        percent9 = (9*int(more))/100
        additional = 2*int(percent9)
        booking_fees = int(more) + int(additional)
        final = int(total) + int(booking_fees)

        main_id = uuid.uuid4()
        di = str(randint(100, 9999))
        di2 = str(randint(100, 999))
        order_id = "Spot@"+di+get_random_string(1)+di2+get_random_string(2)

        context = {
            'main_id': main_id,
            'ord_id': order_id,
            'final_amt': final,
            'booking_fees': booking_fees,
            'percent9': percent9,
            'all_list': all_list,
            'u': usernamee,
            'event': event_details,
            'con': more,
            'email': current_user.email,
            'phone': phone,
        }
        request.session['spot_id'] = context['ord_id']
        request.session['email'] = context['email']
        request.session['event_id'] = pk
        request.session['phone'] = context['phone']

    return render(request, "Users/order_summary.html", context)




secretKey = "TESTbb80ff9d3d2450b72d817b0727a95cc06234f1bb"

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="UserLogin")
@allowed_users(allowed_roles=['customer'])
def handlerequest(request):
    if request.method == "POST":
        mode = "TEST"  # <-------Change to TEST for test server, PROD for production
        postData = {
            "appId": "204434e28173cb6cfb60e28fb4434402",
            "orderId": request.POST['orderId'],

            "orderAmount": request.POST['orderAmount'],
            "orderCurrency": request.POST['orderCurrency'],
            "orderNote": request.POST['orderNote'],
            "customerName": request.POST['customerName'],
            "customerPhone": request.POST['customerPhone'],
            "customerEmail": request.POST['customerEmail'],
            "returnUrl": request.POST['returnUrl'],
            "notifyUrl": request.POST['notifyUrl'],
        }

 
        extData ={
                "Eventid" :request.POST['eventid'],
                "Event_Name" :request.POST['evename'],
                "orderNote":request.POST['orderNote'],
                "amount" : request.POST['orderAmount'],
                "email": request.POST['customerEmail'],
        }

        sortedKeys = sorted(postData)
        signatureData = ""
        for key in sortedKeys:
            signatureData += key+postData[key]
        message = signatureData.encode('utf-8')
        secret = secretKey.encode('utf-8')
        signature = base64.b64encode(
            hmac.new(secret, message, digestmod=hashlib.sha256).digest()).decode('utf-8')

        if mode == 'PROD':
            url = "https://www.cashfree.com/checkout/post/submit"
        else:
            url = "https://test.cashfree.com/billpay/checkout/post/submit"
        return render(request, 'Users/request.html', {'postData': postData, 'signature': signature, 'url': url,})


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="UserLogin")
@allowed_users(allowed_roles=['customer'])
def handleresponse(request):

    if request.method == "POST":
        postData = {
            "orderId": request.POST.get('orderId'),
            "orderAmount": request.POST.get('orderAmount'),
            "referenceId": request.POST.get('referenceId'),
            "txStatus": request.POST.get('txStatus'),
            "paymentMode": request.POST.get('paymentMode'),
            "txMsg": request.POST.get('txMsg'),
            "signature": request.POST.get('signature'),
            "txTime": request.POST.get('txTime')
        }
        # customerName =  request.POST.get('customerName'),
        # customerPhone =  request.POST.get('customerPhone'),
        # customerEmail = request.POST.get('customerEmail'),
        # print(request.POST.get('customerEmail'))

        extra_data = {
            "spot_id" : request.session['spot_id'],
            "event_id" : request.session['event_id'],
            "email_id":request.session['email'],     
            "phone":request.session['phone'],     
        }
        


        signature = request.POST.get('signature')
        status = request.POST.get('txStatus')
        print(status)

        signatureData = ""
        signatureData = postData['orderId'] + postData['orderAmount'] + postData['referenceId'] + \
            postData['txStatus'] + postData['paymentMode'] + \
            postData['txMsg'] + postData['txTime']

        message = signatureData.encode('utf-8')
        secret = secretKey.encode('utf-8')
        computedsignature = base64.b64encode(
            hmac.new(secret, message, digestmod=hashlib.sha256).digest()).decode('utf-8')

        print(computedsignature)


        if signature == computedsignature :
            if status == "SUCCESS" :

                booking_details = Booking_Detail.objects.create(
                Booked_by=AllUsers.objects.get(email = extra_data['email_id']), Event_Id=extra_data['event_id'], Event_Name=Event_detail.objects.get(uid=extra_data['event_id']).Event_Name, Total_amount=postData['orderAmount'],Order_id =postData['orderId'] ,Spot_id=extra_data['spot_id'],Tx_id_PG=postData['referenceId'])

                booking_details.save()

                test_func.delay()




            else:
                print("FAILED")


        else:
            print("NO")




    return render(request, 'Users/response.html', {'postData': postData, 'computedsignature': computedsignature , 'extra_data':extra_data})




# Curators Section below >>>>>>>>>>>...........................................................................................................
# Curators Section below >>>>>>>>>>>...........................................................................................................
# Curators Section below >>>>>>>>>>>...........................................................................................................
# Curators Section below >>>>>>>>>>>...........................................................................................................
# Curators Section below >>>>>>>>>>>...........................................................................................................
# Curators Section below >>>>>>>>>>>...........................................................................................................
# Curators Section below >>>>>>>>>>>...........................................................................................................
# Curators Section below >>>>>>>>>>>...........................................................................................................
# Curators Section below >>>>>>>>>>>...........................................................................................................
# Curators Section below >>>>>>>>>>>...........................................................................................................


def curator_Reg(request):
    try:

        if request.method == "POST":
            u = AllUsers
            print(u)
            curatorbizname = request.POST['name']
            curatoremail = request.POST['bizemail']
            curatornumber = request.POST['number']
            curatorType = request.POST['type']
            curatorpass = request.POST['bizpass']

            u = AllUsers.objects.create_user(
                email=curatoremail, password=curatorpass, is_organizer="True")
            group = Group.objects.get(name='organizer')
            u.groups.add(group)
            u.save()
            curator_c = Business_Data.objects.create(
                user=u, Business_Name=curatorbizname, Contact=curatornumber, Registered_As=curatorType)
            curator_c.save()
            messages.info(request, 'User -Created')

            return redirect("curator_Reg")

    except IntegrityError:

        messages.info(request, 'User Alredy Exist With THis email-id')
        return redirect("curator_Reg")

    return render(request, "Biz/reg.html")


def BizLogin(request):
    if request.method == "POST":
        username = request.POST['mailinput']
        password = request.POST['passinput']

        user = authenticate(email=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('Dashboard-form1-page')
        else:
            messages.info(request, 'Invalid Email OR Password')
            return redirect('Dashboard-form1-page')
    else:
        return render(request, "Biz/login.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="BusinessLogin")
@allowed_users(allowed_roles=['organizer'])
def Dashboard_form1(request):
    today = date.today()
    current_user = request.user.id
    print(current_user)
    uid_of_curator = Business_Data.objects.all().filter(user=current_user)
    print(uid_of_curator)
    for i in uid_of_curator:
        pk = i.uid
        bizname = i.Business_Name
        type = i.Registered_As

        if request.method == "POST":
            product_details = Event_detail()
            name = request.POST['Event_Name']
            product_details.Event_Name = request.POST['Event_Name']
            product_details.Organizer = pk
            product_details.Category = request.POST['category']
            product_details.orgtype = request.POST['orgtype']
            product_details.Startdate = request.POST['startdate']
            Startdate = request.POST['startdate']
            Starttime = request.POST['starttime']
            product_details.Starttime = request.POST['starttime']
            product_details.Endtime = request.POST['endtime']
            product_details.Age = request.POST['age']
            product_details.Language = request.POST['lang']
            product_details.City = request.POST['city']
            product_details.Fulladdress = request.POST['fulladdress']
            product_details.Description = request.POST['Description']
            product_details.TnC = request.POST['tnc']

            if len(request.FILES) != 0:
                product_details.Event_img = request.FILES.get('Event_img')

            product_details.save()
            abc = Event_detail.objects.all().filter(Organizer=pk, Event_Name=name,
                                                    Startdate=Startdate, Starttime=Starttime)
            for i in abc:
                uuuuid = str(i.uid)
            return redirect('Dashboard-form2-page', pk=uuuuid)

    return render(request, "Biz/Dashboard.html", {'bizuid': pk, 'bizname': bizname, 'type': type})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="BusinessLogin")
@allowed_users(allowed_roles=['organizer'])
def Dashboard_form2(request, pk):
    get_event_details = Event_detail.objects.all().filter(uid=pk)
    for i in get_event_details:
        bizuid = i.Organizer
    display = Event_Ticket.objects.all().filter(Created_by=pk)
    if request.method == "POST":
        t = Event_Ticket()
        creator = request.POST['created_by']
        t.Created_by = request.POST['created_by']
        t.Ticket_type = request.POST['tictype']
        t.Description = request.POST['shortdes']
        t.Price = request.POST['price']
        t.Expected_Quantity = request.POST['quantity']
        t.Expiry_Date = request.POST['expdate']
        t.Expiry_Time = request.POST['exp']
        t.Additional_data = request.POST['additional_info']

        t.save()

        display = Event_Ticket.objects.all().filter(Created_by=creator)

        get_event_details = Event_detail.objects.all().filter(uid=creator)
        return render(request, "Biz/ticket_info.html", {'eve': get_event_details, 'display': display, 'eventid': pk, 'bizuid': bizuid})
    return render(request, "Biz/ticket_info.html", {'eve': get_event_details, 'display': display, 'eventid': pk, 'bizuid': bizuid})


def Delete_ticket(request, pk, id):
    ticket = Event_Ticket.objects.get(uid=id)
    ticket.delete()
    return redirect('Dashboard-form2-page', pk=pk)


def Delete_Event(request, pk):
    event = Event_detail.objects.all().filter(uid=pk)
    for i in event:
        bizuid = i.Organizer
        bi = bizuid
    Event = Event_detail.objects.get(uid=pk)
    ticket = Event_Ticket.objects.all().filter(Created_by=pk)
    ticket.delete()
    Event.delete()
    return redirect('Created_Events', pk=bi)


def Update_ticket(request, pk):
    if request.method == "POST":
        ticid = request.POST['tickid']
        update = Event_Ticket.objects.get(Created_by=pk, uid=ticid)
        update.Ticket_type = request.POST['tickname']
        update.Description = request.POST['shdes']
        update.Price = request.POST['price']
        update.Expected_Quantity = request.POST['quantityy']
        update.Expiry_Date = request.POST['expdddate']
        update.Expiry_Time = request.POST['exptime']
        update.Additional_data = request.POST['additional']
        update.save()
    return redirect('Dashboard-form2-page', pk=pk)


def logoutcreator(request):
    logout(request)
    return redirect('homepage')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="BusinessLogin")
@allowed_users(allowed_roles=['organizer'])
def Created_Events(request, pk):
    print(pk)
    Created_Events = Event_detail.objects.all().filter(Organizer=pk)
    return render(request, "Biz/created-event.html", {'bizuid': pk, 'created': Created_Events})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="BusinessLogin")
@allowed_users(allowed_roles=['organizer'])
def View_Event(request, eveid, bizuid):
    event = Event_detail.objects.all().filter(uid=eveid)
    for e in event:
        biz_id = e.Organizer
    return render(request, "Biz/view-event.html", {'eventinfo': event, 'biz_id': biz_id})

    

def Publish_Event(request, pk, fk):
    pub = "Published"
    publish_this_event = Event_detail.objects.all().filter(uid=fk)
    for i in publish_this_event:
        i.Status = pub
        i.save()
    return redirect('Created_Events', pk=pk)




def TaketoBcontactus(request):
    if request.method == 'POST':
        name = request.POST.get('full_name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        msg = request.POST.get('msg')

        data = {
            'Name': name,
            'Mobile_Number': mobile,
            'Email': email,
            'Subject': subject,
            'Description': msg,
        }

        message = ''' 
       
        FULL NAME  : {}
        CONTACT DETAILS  : {}
        EMAIL ADDRESS  : {}

        DESCRIPTION  : {} 
        '''.format(data['Name'], data['Mobile_Number'], data['Email'], data['Description'])

        send_mail(data['Subject'], message,
                  "support@spotezy.in", ['support@spotezy.in'])

        message = "Thanks for contacting us! We will be in touch with you shortly."

        return render(request, "Biz/bizenquiry.html", {'msg': message})

    else:

        return render(request, "Biz/bizenquiry.html")
