class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) 

    avatar = models.ImageField(default='default.jpg', upload_to="") #
    bio = models.TextField()
    bio2 = models.TextField(default=None, blank=True, null=True)

    def save(self, *args, **kwargs): 
        super().save(*args, **kwargs)

        # If the avatar field have some avatar
        if self.avatar: 
            super().save(*args, **kwargs)
            
            # If there is an avatar in the model
            if self.avatar:                 
                # filename = f"profile_{self.user.id}_{self.avatar.name}" 
                # upload_to_azure_storage(self.avatar.file, filename)
                # print(type(self.avatar.file))
                
                upload_to_local_storage(self.avatar.path, user_id=self.user.id)
                # This function should convert the avatar filename to avatar.{extension}, then save the file to directory media/profile_images/user_id_{user_id}/
                # self.avatar.path, 
                # user_id=self.user.id
                
            
def upload_to_local_storage(filepath, user_id):   
    # read in image from filepath
    img = Image.open(filepath)
    
    # create or get directory media/profile_images/user_id_{user_id}/
    # Create saved directory if not exist
    saved_directory = "media/profile_images/user_id_{user_id}".format(user_id=user_id)
    if (os.path.exists(saved_directory)):
        pass
    else:
        os.mkdir(saved_directory)
        
               
    file_name = os.path.basename(filepath)
    file_extension = os.path.splitext(file_name)[1]
    
    # convert the avatar filename to avatar.{extension}
    file_path = "media/profile_images/user_id_{user_id}/avatar{extension}".format(
        user_id= user_id,
        extension= file_extension,
    ).lower() #/mnt/d/Chest-Xray-Web-App/media/profile_images/user_id_5/avatar.jpg
    
    # save image to the new file_path
    if img.height > 100 or img.width > 100:
        MAX_SIZE = (100, 100)
        img.thumbnail(MAX_SIZE)
    img.save(file_path)