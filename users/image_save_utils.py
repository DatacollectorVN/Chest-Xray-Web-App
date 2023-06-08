import os

def set_avatar_filename_format(instance, filename):
    """
    file format setting
    e.g)
        {username}.{extension}
        avatar.png/ avatar.jpg
    """
    return "avatar{extension}".format(
        extension=os.path.splitext(filename)[1],
    )


def user_profile_directory_path(instance, filename):
    """
    https://gist.github.com/LeoHeo/5131362006bd2ee9b693b3e29692c42f
    image upload directory setting
    e.g)
        "profile_images/user_id_{user_id}/{filename}"
        profile_images/user_id_1/avatar.png
    """
    # print("upload_to first")
    
    # Create saved directory if not exist
    saved_directory = "media/profile_images/user_id_{user_id}".format(user_id=instance.user.id)
    if (os.path.exists(saved_directory)):
        pass
    else:
        os.mkdir(saved_directory)
    
    # # Create saved path for image
    path = "profile_images/user_id_{user_id}/{filename}".format(
        user_id=instance.user.id,
        filename=set_avatar_filename_format(instance, filename),
    ).lower() #/mnt/d/Chest-Xray-Web-App/media/profile_images/user_id_5/avatar.jpg
    
    # If the file avatar.jpg already exist in that directory, delete it. 
    if os.path.exists(path):
        os.remove(path)

    print("path:", path) # path: profile_images/user_id_5/avatar.jpg
    return path
    
    # print(saved_directory)
    # return saved_directory
    
    # If profile_images/user_id_5/avatar.jpg exist -> delete
    # Then save the new image with the same name


""" 
# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    # If an user is deleted, the correponding model will be deleted, too.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    avatar = models.ImageField(default='default.jpg', upload_to= user_profile_directory_path) #upload_to='profile_images'
    bio = models.TextField()
    bio2 = models.TextField(default=None, blank=True, null=True)
"""