from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.exceptions import ObjectDoesNotExist
import os
from datetime import datetime

from .image_save_utils import user_profile_directory_path     
from .storage import OverwriteStorage


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    # If an user is deleted, the correponding model will be deleted, too.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    avatar = models.ImageField(default='default.jpg', upload_to=user_profile_directory_path) #, storage=OverwriteStorage()) #upload_to=user_directory_path, #upload_to='profile_images', # storage=OverwriteStorage()
    bio = models.TextField()
    bio2 = models.TextField(default=None, blank=True, null=True)

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        # Note: this class run save method first, then run upload_to function
        # To do: read in image
        
    #     # https://stackoverflow.com/questions/9522759/imagefield-overwrite-image-file-with-same-name
        # https://docs.djangoproject.com/en/4.2/topics/files/
        
        # try:
        #     this = Profile.objects.get(id=self.id)
        #     print("##########")
        #     print("this.avatar:", this.avatar)
        #     print("this.avatar.path:", this.avatar.path)
        #     print("this.avatar.name:", this.avatar.name)
        #     print("this.avatar.file:", this.avatar.file)
            
        #     print("self.avatar:", self.avatar)
        #     print("self.avatar.path:", self.avatar.path)
        #     print("self.avatar.name:", self.avatar.name)
        #     print("self.avatar.file:", self.avatar.file)
        #     print("##########")
            
        #     image = Image.open(self.avatar.path)
        #     image.save(this.avatar.path)
        #     print("image saved")
        
        # self.avatar.save(name="avatar.jpg", content=self.avatar.file, save=True)
        
        # except: pass
        # super(Profile, self).save(*args, **kwargs)
        
        
        # Userful links:
        # https://docs.djangoproject.com/en/4.2/topics/files/
        # https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.FileField.upload_to
        # https://stackoverflow.com/questions/1308386/programmatically-saving-image-to-django-imagefield
        
        ####################################
        super().save()

        # img = Image.open(self.avatar.path)

        # if img.height > 100 or img.width > 100:
        #     new_img = (100, 100)
        #     img.thumbnail(new_img)
        #     img.save(self.avatar.path)
            
        #####################################
            
    #     #     # print("this:", this)
    #     #     # print("this:", this.__dict__)
            # print("this.avatar:", this.avatar) # this.avatar: profile_images/user_id_5/avatar_PwdE6YS.jpg
            # print("self.avatar:", self.avatar) # self.avatar: live_voquangtran28101999.jpg
            
            # this_avatar_path = this.avatar.path
            
            # if this.avatar:
            #     this.avatar.save(self.avatar.file)
            #     self.avatar.save(
            #         name= os.path.basename(self.avatar.path),
                    
            #         )
                
            #     (
            # os.path.basename(self.url),
            # File(open(result[0], 'rb'))
            # )
                
            # if this.avatar == self.avatar:
                # this.avatar.delete()

        
    #     # https://stackoverflow.com/questions/31666309/replacing-a-file-while-uploading-in-django/31669165#31669165
    #     # try:
    #     #     this = Profile.objects.get(id=self.id)
    #     #     if this.avatar:
    #     #         os.remove(this.avatar.path)
    #     # except ObjectDoesNotExist:
    #     #     pass
    #     # print("self.avatar.path", self.avatar.path)
    #     # filename = os.path.basename(self.avatar.path)
    #     # print("user_directory_path:", user_directory_path(self, filename=filename))
        
    #     # img = Image.open(self.avatar.path)
    #     # # print(self.avatar.__dict__)
    #     # # print(self.avatar.path)

    #     # if img.height > 100 or img.width > 100:
    #     #     MAX_SIZE = (100, 100)
    #     #     img.thumbnail(MAX_SIZE) # image thumbnail rotate raw image horizontally?
    #     #     # print(self.avatar.path)
            
    #     #     # # Process self.avatar.path
    #     #     # # /media/profile_images/user_id_5/avatar_NyeAJ2e.JPG
    #     #     # raw_path = self.avatar.path
    #     #     # dir_name = os.path.dirname(raw_path)
    #     #     # file_name = os.path.basename(raw_path)
    #     #     # file_extension = os.path.splitext(file_name)[1]
            
    #     #     # avatar_path = os.path.join(dir_name, "avatar" + file_extension).lower()
    #     #     # print("path:", avatar_path) #/mnt/d/Chest-Xray-Web-App/media/profile_images/user_id_5/avatar.jpg
    #     #     # img.save(avatar_path)
    #     #     img.save(self.avatar.path)
            
        
    #     # Two step:
    #         # 1) save file without change file name
    #         # 2) resize file then save file.

# class Prediction
class Prediction(models.Model):
    """ 
    This entity represent disease prediction, it has four attributes:
        id: primary key (implicit)
        user_id: foreign key, linked to User entity
        category: type of medical image, default: x_ray
        url: link of medical image, currently saved in local, later: saved to datalake
        timestamp
        date_key
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.TextField(default=None, blank=True, null=True)
    # input_url = models.ImageField(default='default.jpg', upload_to="input_images") 
    # output_url = models.ImageField(default='default.jpg', upload_to="output_images") 
    input_url = models.URLField(default=None, blank=True, null=True) #image url
    output_url = models.URLField(default=None, blank=True, null=True) 
    
    timestamp = models.DateTimeField(auto_now_add=True)
    date_key = models.IntegerField(default=None, blank=True, null=True) #??? Ask Nhan again.
    
    # https://stackoverflow.com/questions/8016412/in-django-do-models-have-a-default-timestamp-field
    # created_at = models.DateField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    # Result of AI model's prediction.
    result = models.TextField(default=None, blank=True, null=True)
    
    # https://stackoverflow.com/questions/22157437/model-field-based-on-other-fields
    def save(self, *args, **kwargs):
        self.date_key = int(datetime.fromtimestamp(self.timestamp).strftime('%d%m%Y'))
        super(Prediction, self).save(*args, **kwargs) # Call the "real" save() method.
    
    def __str__(self):
        return self.user.username
    
    # https://books.agiliq.com/projects/django-orm-cookbook/en/latest/table_name.html
    # class Meta:
    #     db_table = "user_prediction"
    

# class Prediction
class ConditionPrediction(models.Model):
    """ 
    This entity represent disease prediction, it has four attributes:
        id: primary key (implicit)
        user_id: foreign key, linked to User entity
        category: type of medical image, default: x_ray
        url: link of medical image, currently saved in local, later: saved to datalake
        timestamp
        date_key
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.TextField(default=None, blank=True, null=True)
    # input_url = models.URLField(default=None, blank=True, null=True) #image url
    # output_url = models.URLField(default=None, blank=True, null=True) 
    input_image = models.ImageField(default='default.jpg', upload_to="input_images") 
    output_image = models.ImageField(default='default.jpg', upload_to="output_images") 
    
    timestamp = models.DateTimeField(auto_now_add=True)
    date_key = models.IntegerField(default=None, blank=True, null=True)
    
    # https://stackoverflow.com/questions/8016412/in-django-do-models-have-a-default-timestamp-field
    # created_at = models.DateField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    # Result of AI model's prediction.
    result = models.TextField(default=None, blank=True, null=True)
    
    # https://stackoverflow.com/questions/22157437/model-field-based-on-other-fields
    def save(self, *args, **kwargs):
        self.date_key = int(datetime.fromtimestamp(self.timestamp).strftime('%d%m%Y'))
        super(Prediction, self).save(*args, **kwargs) # Call the "real" save() method.
    
    def __str__(self):
        return self.user.username
    
    # https://books.agiliq.com/projects/django-orm-cookbook/en/latest/table_name.html
    class Meta:
        db_table = "user_condition_prediction"
    
    
class DummyModel(models.Model):
    x = models.IntegerField(default=0)
    x_image = models.ImageField(default='default.jpg', upload_to="input_images") #, storage=OverwriteStorage()) #upload_to=user_directory_path, #upload_to='profile_images', # storage=OverwriteStorage()

    def __str__(self):
        return str(self.x)
    