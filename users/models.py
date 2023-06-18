from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.exceptions import ObjectDoesNotExist
import os
from datetime import datetime

from .image_save_utils import user_profile_directory_path     
# from .storage import OverwriteStorage
from django.utils import timezone


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    # If an user is deleted, the correponding model will be deleted, too.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    avatar = models.ImageField(default='default_avatar.png', upload_to='profile_images') #, storage=OverwriteStorage()) #upload_to=user_directory_path, #upload_to='profile_images', # storage=OverwriteStorage()
    bio = models.TextField()
    bio2 = models.TextField(default=None, blank=True, null=True)

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)       


# class Prediction
class ImagePrediction(models.Model):
    """ 
    This entity represent disease prediction, it has four attributes:
        id: primary key (implicit)
        user_id: foreign key, linked to User entity
        category: type of medical image, default: x_ray
        url: link of medical image, currently saved in local, later: saved to datalake
        timestamp
        date_key
    """
    # from django.conf import settings
    user = models.ForeignKey(User, on_delete=models.CASCADE) #settings.AUTH_USER_MODEL  ???
    category = models.TextField(default=None, blank=True, null=True)
    # input_url = models.URLField(default=None, blank=True, null=True) #image url
    # output_url = models.URLField(default=None, blank=True, null=True) 
    input_image = models.ImageField(default='default.jpg', upload_to="input_images") 
    output_image = models.ImageField(default='output_image_default.jpg', upload_to="output_images") 
    
    timestamp = models.DateTimeField(editable=False)
    date_key = models.IntegerField(default=None, blank=True, null=True)
    
    # https://stackoverflow.com/questions/8016412/in-django-do-models-have-a-default-timestamp-field
    # created_at = models.DateField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    # Result of AI model's prediction.
    status = models.TextField(default="In progress", blank=True, null=True)
    
    # https://stackoverflow.com/questions/22157437/model-field-based-on-other-fields
    def save(self, *args, **kwargs):

        self.timestamp = timezone.now()        
        self.date_key = int(self.timestamp.strftime("%Y%m%d"))
        
        super(ImagePrediction, self).save(*args, **kwargs) # Call the "real" save() method.
    
    def __str__(self):
        return self.input_image.url
    
    # https://books.agiliq.com/projects/django-orm-cookbook/en/latest/table_name.html
    class Meta:
        db_table = "users_image_prediction"
    
class DiseasePrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(editable=False)
    date_key = models.IntegerField(default=None, blank=True, null=True)
    image_prediction = models.ForeignKey(ImagePrediction, on_delete=models.CASCADE)
    disease = models.CharField(max_length=100, null=True, blank=True)
    location_xyxy = models.CharField(max_length=100, null=True, blank=True)
    score = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True) #null=True, blank=True, default = 0
    # https://groups.google.com/g/django-users/c/YggIgNhde1g/m/bXPixH6eeJEJ
    
    def save(self, *args, **kwargs):
        self.timestamp = timezone.now()        
        self.date_key = int(self.timestamp.strftime("%Y%m%d"))
        
        super(DiseasePrediction, self).save(*args, **kwargs) # Call the "real" save() method.
        
    def __str__(self):
        return str(self.user.id) + " " + self.image_prediction.output_image.url + " " + self.disease 
    
    class Meta:
        db_table = "users_disease_prediction"
    
class DummyModel(models.Model):
    x = models.IntegerField(default=0)
    x_image = models.ImageField(default='default.jpg', upload_to="input_images") #, storage=OverwriteStorage()) #upload_to=user_directory_path, #upload_to='profile_images', # storage=OverwriteStorage()

    def __str__(self):
        return str(self.x)
    