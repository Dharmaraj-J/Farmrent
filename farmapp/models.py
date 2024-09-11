from django.db import models

# Create your models here.

class UserDetails(models.Model):

    s_no=models.AutoField
    user_id=models.IntegerField(null=True)
   
    username=models.CharField(max_length=75,default="")
    password=models.CharField(max_length=75,default="")
    email=models.CharField(max_length=75,default="")
    village=models.CharField(max_length=75,default="")
    taluka=models.CharField(max_length=75,default="")
    district=models.CharField(max_length=75,default="")
    phone_no=models.IntegerField(null=True)

    post = models.CharField(max_length=75,default="")
    
    def __str__(self):
        return self.username


class Equipment(models.Model):

    s_no=models.AutoField
    equipmentholder_id=models.IntegerField(null=True)
    equipment_id=models.IntegerField(null=True)


    username=models.CharField(max_length=75,default="")
    password=models.CharField(max_length=75,default="")
   
    phone_no=models.IntegerField(null=True)
    village=models.CharField(max_length=75,default="")
    taluka=models.CharField(max_length=75,default="")
    district=models.CharField(max_length=75,default="")

    
    description=models.TextField(default="")
    old=models.IntegerField(null=True)
    equipmentname=models.CharField(max_length=75,default="")
    rent=models.IntegerField()
    
    image1= models.ImageField(upload_to="constructapp/images",default="")

    image2= models.ImageField(upload_to="constructapp/images",default="")

    def __str__(self):
        return self.username



class Requests_Apply(models.Model):

    customer_name=models.CharField(max_length=75,default="")
    customer_id=models.IntegerField(null=True)
    customer_village=models.CharField(max_length=75,default="")
    customer_taluka=models.CharField(max_length=75,default="")
    customer_district=models.CharField(max_length=75,default="")
    customer_phone=models.CharField(max_length=75,default="")

    equipment_name=models.CharField(max_length=75,default="")
    equipment_id=models.IntegerField(null=True)
    equipmentholder_phone_no=models.IntegerField(null=True)
    equipmentholder_id=models.IntegerField(null=True)
    equipmentholder_name=models.CharField(max_length=75,default="")
    equipmentholder_village=models.CharField(max_length=75,default="")
    equipmentholder_taluka=models.CharField(max_length=75,default="")
    equipmentholder_district=models.CharField(max_length=75,default="")

    rent=models.IntegerField(null=True)
    take_date=models.CharField(max_length=75,default="")
    give_date=models.CharField(max_length=75,default="")
    total_rent=models.IntegerField(null=True)

    request_status=models.CharField(max_length=75,default="Pending")

    def __str__(self):
        return self.customer_name
