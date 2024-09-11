from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from . models import UserDetails,Equipment,Requests_Apply
from datetime import datetime

from .forms import EquipementForm
import re


def indexpage(request):
    return render(request, 'index.html')

def loginpage(request):
    return render(request,'login.html')



def handellogin(request):
    
    if request.method=="POST":
     
        loginusername=request.POST['username']
        loginpassword=request.POST['password']

        user=authenticate(username= loginusername, password= loginpassword)

        if user is not None:
            obj=UserDetails.objects.get(username=loginusername)
            Post = obj.post

            if  Post=='Rental Manager':
                login(request, user)
                messages.success(request,"Successfully Logged In  as Rental Manager")
                return redirect('rentalmanagerpage')
            
            elif(Post=='Customer'):
                login(request, user)
                messages.success(request,"Successfully Logged In as Customer")
                return redirect('customerpage')
        else:
            messages.error(request,"Invalid User. Please check the username and password" )
            return redirect("loginpage")
    


def registerpage(request):  
    return render(request, "register.html")

def handleregister(request):

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    

    if request.method == 'POST':

        alluser=UserDetails.objects.all()
        a=len(alluser)
        l=[int(i.user_id) for i  in alluser]
        while(a in l):
            a+=1

       
        Username = request.POST['username']
        Email = request.POST['email']
        Password=request.POST['password']
        Village= request.POST['village']
        Taluka= request.POST['taluka']
        District= request.POST['district']
        phoneno=request.POST['phoneno']
        Post=request.POST['post']

        if not Username.isalnum():
            messages.error(request,'Error. Username Should only contain letters and numbers.')
            return redirect('registerpage')

        if(re.fullmatch(regex, Email)):
            pass
        else:
            messages.error(request,'Invalid Email')
            return redirect('registerpage')
        
        allusers=User.objects.all()

        for i in allusers:
            if(i.username==Username):
                messages.error(request,"User already exists")
                return redirect('registerpage')
            
        myuser = User.objects.create_user(Username, Email, Password)
        myuser.save()

        newuser=UserDetails(username=Username, email=Email,password=Password,taluka=Taluka,district=District,village=Village,phone_no=phoneno,user_id=a,post=Post)
        newuser.save()

        messages.success(request,"Your account has been successfully created")
        return redirect('loginpage')
    
    else:
        return HttpResponse('<h1>404-Error</h1>')
    

def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('indexpage')


def customerpage(request):
    if request.user.is_authenticated:
        allequipments = Equipment.objects.all()
        name = request.user.username
        return render(request,'customer.html',{'name':name,'allequipments':allequipments}) 
    
    return redirect('indexpage')


def rentalmanagerpage(request):

    if request.user.is_authenticated:

        req= Requests_Apply.objects.filter(equipmentholder_name=request.user.username,request_status='Pending')
        his= Requests_Apply.objects.filter(equipmentholder_name=request.user.username,request_status='Accepted')
        
        name = request.user.username
        params={}
        params['requests']=req
        params['history']=his
        params['name'] = name

        return render(request,'rentalmanager.html',params)      

    else :
        return redirect('indexpage')


def addequipment(request):

    if request.user.is_authenticated:
        return render(request,'addequipment.html')
    
    else :
        return redirect('indexpage')



def add(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            Equipmentname=request.POST['equipmentname']
            Description=request.POST['description']
            Rent=request.POST['rent']
            Old=request.POST['old']

            Img1=request.FILES['img1']
            Img2=request.FILES['img2']
            

            allequipments=Equipment.objects.all()
            l=[i.equipment_id for i in allequipments]
            print(l)
            a=len(allequipments)
            while(a in l):
                a+=1
                
            equipmentholder=UserDetails.objects.get(username=request.user.username)
            eq=Equipment(username=request.user.username,password=request.user.password,village=equipmentholder.village,taluka=equipmentholder.taluka,district=equipmentholder.district,rent=Rent,image1=Img1,image2=Img2,equipmentname=Equipmentname,old=Old,description=Description,equipment_id=a,phone_no=equipmentholder.phone_no,equipmentholder_id=equipmentholder.user_id)
            eq.save()
            messages.success(request,"Equipmet added successfully ")
            return redirect('addequipment')
    else :
        return redirect('indexpage')


def editequipment(request):

    if request.user.is_authenticated:
        allequipments=Equipment.objects.filter(username=request.user.username)
        params={}
        params['allequipments']=allequipments
        return render(request,'editequipment.html',params)
    else :
        return redirect('indexpage')

def delete(request,slug):
    if request.user.is_authenticated:
        print(slug)
        eq=Equipment.objects.filter(equipment_id=int(slug))
        eq.delete()
        return redirect('editequipment')
    return redirect('indexpage')

def edit(request,slug):  
       eq=Equipment.objects.get(equipment_id=int(slug))

       if request.method == 'POST':
           form = EquipementForm(request.POST,instance=eq) 
           if form.is_valid():     
               form.save()
               return redirect('editequipment')
       else:
            form = EquipementForm(instance=eq)
       return render(request,'edit.html',{'form': form,'eq':eq})

def equipmentdetail(request, equipment_id):
 
    equipment = get_object_or_404(Equipment, equipment_id=equipment_id)
    return render(request, 'detailequipement.html', {'equipment': equipment})


def apply(request,slug):

    if request.user.is_authenticated:
        print(slug)
        takedate=request.POST['take']
        givedate=request.POST['give']

        takedate=takedate.split('-')
        givedate=givedate.split('-')

        takedate='/'.join(takedate)
        givedate='/'.join(givedate)

        print(takedate)
        print(givedate)

        d1 = datetime.strptime(takedate, "%Y/%m/%d")
        d2 = datetime.strptime(givedate, "%Y/%m/%d")

        
        delta = d2 - d1
        totaldays=int(delta.days)

        already=Requests_Apply.objects.filter(customer_name=request.user.username,
                                              equipment_id=int(slug))

        print(len(already))

        if len(already)==0 :
    
            equ=Equipment.objects.get(equipment_id=int(slug))
            totalrent=equ.rent*totaldays

            customer=UserDetails.objects.get(username=request.user.username)
            req=Requests_Apply(customer_name=request.user,
            customer_village=customer.village,customer_taluka=customer.taluka,
            customer_district=customer.district,customer_phone=customer.phone_no,
            equipment_name=equ.equipmentname,equipment_id=int(slug),
            equipmentholder_phone_no=equ.phone_no,equipmentholder_name=equ.username,
            equipmentholder_village=equ.village,equipmentholder_taluka=equ.taluka,
            equipmentholder_district=equ.district,rent=equ.rent,take_date=takedate,
            give_date=givedate,total_rent=totalrent,customer_id=customer.user_id,
            equipmentholder_id=equ.equipmentholder_id)
            req.save()
            messages.success(request,"Request added successfully ")
            return redirect('requests')
        
    else :
        return redirect('indexpage')


def requests(request):

    if request.user.is_authenticated:
        req=Requests_Apply.objects.filter(customer_name=request.user.username)
        params={}
        params['requests']=req
        return render(request,'requests.html',params) 
    
    else :
        return redirect('indexpage')


def accept_request(request,slug):

    if request.user.is_authenticated:

        slug=slug.split(',')
        slug=[int(i) for i in slug]

        equ1=Equipment.objects.filter(equipment_id=slug[0])

        req=Requests_Apply.objects.get(equipment_id=slug[0],customer_id=slug[1],
        request_status='Pending')
        all_req=Requests_Apply.objects.filter(equipment_id=slug[0])

        for i in all_req:
            if(i!=req):
                i.delete()
        req.request_status='Accepted'
        equ1.delete()
        req.save()
        
        return redirect('rentalmanagerpage')
    
    else :
        return redirect('indexpage')
    
def denied_request(request,slug):
    
    if request.user.is_authenticated:
        slug=slug.split(',')
        slug=[int(i) for i in slug]
        print(slug)
        req=Requests_Apply.objects.filter(equipment_id=slug[0],customer_id=slug[1])
        print(req)
        req.delete()
        return redirect('rentalmanagerpage')
    
    else :
        return redirect('indexpage')
    
    
def searchpage(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
           name=request.POST['search']
           eq = Equipment.objects.filter(equipmentname__istartswith=name).order_by('old')
           return render(request,'searchpage.html',{'name':eq}) 
               
    return render(request,'searchpage.html')