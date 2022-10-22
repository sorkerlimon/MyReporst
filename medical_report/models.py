from email.policy import default
from operator import mod
from tkinter import image_types
from django.db import models

# Create your models here.
from users.models import Profile
import uuid
from django.utils.timezone import now  


### Image Added
class Imageadd(models.Model):
    image_owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    # date = models.CharField(max_length=255, blank="True")
    uploaddate = models.DateField(default=now)
    testdate = models.DateField(max_length=8,blank=True,null=True)
    image = models.ImageField(default='default.jpg',upload_to='blood/')
    image_id = models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    
    

    
    def __str__(self):
        return str(self.image_id)
        
# image Type
class Imagetype(models.Model):
    image_owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    imageid = models.ForeignKey(Imageadd, null=True,blank=True,on_delete=models.CASCADE)
    image_type = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{str(self.image_owner)} : {self.image_type}'


# white blood 
class Totallcount(models.Model):
    image_owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    imageid = models.ForeignKey(Imageadd, null=True,blank=True,on_delete=models.CASCADE)
    wbc = models.FloatField(null=True, blank=True)
    rbc = models.FloatField(null=True, blank=True)
    plt = models.FloatField(null=True, blank=True)
    hbg = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(default=now)
    
    def __str__(self):
        return f'{str(self.image_owner)} totall count'

class Absoluteleukocytecount(models.Model):
    image_owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    imageid = models.ForeignKey(Imageadd, null=True,blank=True,on_delete=models.CASCADE)
    neutrophil = models.FloatField(null=True, blank=True)
    lymphocyte = models.FloatField(null=True, blank=True)
    monocyte = models.FloatField(null=True, blank=True)
    eosinophil = models.FloatField(null=True, blank=True)
    basophil = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(default=now)
    
    def __str__(self):
        return f'{str(self.image_owner)} absolute leukocyte count'


class Differentialleukocytecount(models.Model):
    image_owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    imageid = models.ForeignKey(Imageadd, null=True,blank=True,on_delete=models.CASCADE)
    neutrophil2 = models.FloatField(null=True, blank=True)
    lymphocyte2 = models.FloatField(null=True, blank=True)
    monocyte2 = models.FloatField(null=True, blank=True)
    eosinophil2 = models.FloatField(null=True, blank=True)
    basophil2 = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(default=now)
    
    def __str__(self):
        return f'{str(self.image_owner)} defferential leukocyte count'


class Redcellindices(models.Model):
    image_owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    imageid = models.ForeignKey(Imageadd, null=True,blank=True,on_delete=models.CASCADE)
    pcv = models.FloatField(null=True, blank=True)
    mcv = models.FloatField(null=True, blank=True)
    mch = models.FloatField(null=True, blank=True)
    mchc = models.FloatField(null=True, blank=True)
    rdw = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(default=now)
    
    def __str__(self):
        return f'{str(self.image_owner)} red cell indices'


class Pltpanel(models.Model):
    image_owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    imageid = models.ForeignKey(Imageadd, null=True,blank=True,on_delete=models.CASCADE)
    pct = models.FloatField(null=True, blank=True)
    mpv = models.FloatField(null=True, blank=True)
    pdw = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(default=now)
    
    def __str__(self):
        return f'{str(self.image_owner)} plt panel'
    

class Esrcount(models.Model):
    image_owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    imageid = models.ForeignKey(Imageadd, null=True,blank=True,on_delete=models.CASCADE)
    esr = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(default=now)
    
    def __str__(self):
        return f'{str(self.image_owner)} esr count'


class Hba1c(models.Model):
    image_owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    imageid = models.ForeignKey(Imageadd, null=True,blank=True,on_delete=models.CASCADE)
    hba1c = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(default=now)
    
    def __str__(self):
        return f'{str(self.image_owner)} hba1c count'