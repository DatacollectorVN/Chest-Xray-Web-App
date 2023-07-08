import os
import json
import requests 

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, ImagePredictionForm
from .models import ImagePrediction, DiseasePrediction, Profile, Traffic

from .azure_dl.config.config_reader import config_reader
from .azure_dl.connectors.azure_dl import initialize_storage_account


class HomeView(View):
    """ 
    Logic for home page - home.html
    """
    
    def get(self, request):
        # Tracking number of traffics
        if request.user.is_authenticated:
            new_traffic = Traffic(user=request.user)
            new_traffic.save()
        
        return render(request, 'users/home.html')

def test(request):
    """
    Logic for test page - test.html
    """
    return render(request, 'users/test.html')

def news_1(request):    
    """ 
    News 1 on home page - news_1.html
    """
    return render(request, 'users/news_1.html')

def news_2(request):    
    """ 
    News 2 on home page - news_2.html
    """
    return render(request, 'users/news_2.html')

def news_3(request):
    """ 
    News 3 on home page - news_3.html
    """    
    return render(request, 'users/news_3.html')


class RegisterView(View):
    """ 
    Logic for register page - register.html
    """
    
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    """ 
    Logic for login page - login.html
    """
    
    form_class = LoginForm

    def form_valid(self, form):
        # add here to append into Azure Data Lake

        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
    


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Logic for password reset page - password_reset.html
    """
    
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    """
    Logic for changing password page - change_password.html
    """
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


class ProfileView(LoginRequiredMixin, View):
    """ 
    Logic for profile page - profile.html 
    """
    
    def get(self, request):
        """ 
        Get user's profile information from database and display as form
        Download user's avatar from datalake if it is not available in user's storage, and save the avatar to media/profile_images/avatar_{user_id}.{ext}
        Return profile.html template with profile's information and avatar.
        """
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
        
        profile_item = Profile.objects.filter(user_id=request.user.id)[0]        
        profile_avatar_file_path = os.path.join(settings.MEDIA_ROOT, profile_item.avatar.__str__())
        
        # If profile_avatar is already in local storage.
        if os.path.exists(profile_avatar_file_path):
            # Yes: Upload to view -> html
            print("Profile avatar exists locally, not download from datalake.")
            pass
        else:  # If profile_avatar is not in local storage.
            print("Profile avatar not exists locally, download from datalake.")

            config_path = os.path.join(settings.BASE_DIR, "users", "config_dl_vm", "config_dl_vm.json")
            with open(config_path) as config_file:
                config_data = json.load(config_file)
                
            # Download from cloud AI model API to local storage.
            service_client = initialize_storage_account(config_reader.azure_storage['azure_storage_account_name']
                ,  config_reader.azure_storage['azure_storage_account_key']
            )
            
            file_system_client = service_client.get_file_system_client(file_system= config_data["user_avatar_file_system_name"])
            
            # datalake file path
            datalake_profile_avatar_file_path =  profile_item.avatar.__str__()
            profile_avatar_file_client = file_system_client.get_file_client(file_path = datalake_profile_avatar_file_path)
        
            # print("datalake_profile_avatar_file_path:", datalake_profile_avatar_file_path)
            
            profile_avatar_path = profile_avatar_file_path  #profile_images/avatar_4.jpg  #"/home/Chest-Xray-Web-App/test2.jpeg" # "/mnt/d/Chest-Xray-Web-App/users/azure_dl/test2.jpeg" #/home/Chest-Xray-Web-App
            with open(profile_avatar_path,'wb') as local_file:
                download= profile_avatar_file_client.download_file()
                downloaded_bytes = download.readall()
                local_file.write(downloaded_bytes)
            
            # Upload to view -> html
            pass
        
        return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})
    
    
    def post(self, request):
        """ 
        Get user's profile information from the front end and load into forms.
        Validate forms and return old forms if the forms' information is not valid.   
        
        Rename and move the avatar image to media/profile_images/avatar_{user_id}.{ext}
        Upload avatar image to Azure Datalake at user-avatar/profile_images/avatar_{user_id}.{ext}
        Redirect to profile.html (get method)
        """
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if (not user_form.is_valid()) or (not profile_form.is_valid()):
            ctx = {'user_form': user_form, 'profile_form': profile_form}
            return render(request, 'users/profile.html', ctx)
        
        user_form.save()
        profile_object = profile_form.save()
        
        profile_avatar_file_name = os.path.basename(profile_object.avatar.url)
        profile_avatar_file_ext = os.path.splitext(profile_avatar_file_name)[1]
        
        profile_avatar_old_file_path = os.path.join(settings.MEDIA_ROOT, profile_object.avatar.__str__())
        profile_avatar_new_file_path = os.path.join(settings.MEDIA_ROOT, "profile_images", f"avatar_{profile_object.user_id}" + profile_avatar_file_ext)
        profile_avatar_new_internal_file_path = os.path.join("profile_images", f"avatar_{profile_object.user_id}" + profile_avatar_file_ext)
        os.replace(profile_avatar_old_file_path, profile_avatar_new_file_path)
        
        profile_object.avatar = profile_avatar_new_internal_file_path
        profile_object.save()
        
        ############### Upload image to Azure Datalake ###################################################
        config_path = os.path.join(settings.BASE_DIR, "users", "config_dl_vm", "config_dl_vm.json")
        with open(config_path) as config_file:
            config_data = json.load(config_file) 
        
        service_client = initialize_storage_account(config_reader.azure_storage['azure_storage_account_name']
            ,  config_reader.azure_storage['azure_storage_account_key']
        )

        file_system_client = service_client.get_file_system_client(file_system=config_data["user_avatar_file_system_name"])   
        directory_client = service_client.get_directory_client(file_system_client.file_system_name, config_data["avatar_folder_path"]) # "chest_xray"
        
        image_path = os.path.join(settings.MEDIA_ROOT, profile_object.avatar.__str__())
        image_name = os.path.basename(image_path) 
        with open(image_path, "rb") as file: #"/home/Chest-Xray-Web-App/test2.jpeg"
            file_system_client = directory_client.create_file(image_name) #"test2.jpeg"
            file_system_client.upload_data(file,  overwrite=True)
                
        messages.success(request, 'Your profile is updated successfully')
        return redirect(to='users-profile')
        

class ImagePredictionView(LoginRequiredMixin, View):
    """ 
    Logic for prediction history page - prediction.html 
    """

    def get(self, request):
        """ 
        Load list of image predictions from users_image_prediction table in database. 
        For each image_prediction, check if the input image is avaiable in local storage. 
        If not, download that image from datalake at prediction/input_images/input_image_{image_prediction_id}_{user_id}.{ext}
        Downloaded input images are located in media/input_images/input_image_{image_prediction_id}_{user_id}.{ext}
        Return prediction.html template with associated information.
        """        
        image_prediction_list = ImagePrediction.objects.filter(user_id=request.user.id)
        
        # Pagination section
        paginator = Paginator(image_prediction_list, 4) # Show 5 image prediction per page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        # Download section
        config_path = os.path.join(settings.BASE_DIR, "users", "config_dl_vm", "config_dl_vm.json")
        with open(config_path) as config_file:
            config_data = json.load(config_file)
        
        # Download from cloud AI model API to local storage.
        service_client = initialize_storage_account(config_reader.azure_storage['azure_storage_account_name']
            ,  config_reader.azure_storage['azure_storage_account_key']
        )
        
        file_system_client = service_client.get_file_system_client(file_system= config_data["file_system_name"])
        
        for image_prediction_item in page_obj: #image_prediction_list:
            input_image_file_path = os.path.join(settings.MEDIA_ROOT, image_prediction_item.input_image.__str__()) # /mnt/d/Chest-Xray-Web-App/media/input_images/input_image_10_1.jpg
            
            # If input_image is already in local storage.
            if os.path.exists(input_image_file_path):
                # Yes: Upload to view -> html
                print("Input image exists locally, not download from datalake.", input_image_file_path)
                pass
            else: # If input_image not in local storage:
                print("Input image not exists locally, download from datalake.", input_image_file_path)
                
                # datalake file path
                datalake_input_image_file_path =  image_prediction_item.input_image.__str__()
                input_image_file_client = file_system_client.get_file_client(file_path = datalake_input_image_file_path)
                
                # output_path = os.path.join("/home/nathan/project/ChestXray-Model-API/app/", "images_1.jpeg")
                input_path = input_image_file_path #"/home/Chest-Xray-Web-App/test2.jpeg" # "/mnt/d/Chest-Xray-Web-App/users/azure_dl/test2.jpeg" #/home/Chest-Xray-Web-App
                with open(input_path,'wb') as local_file:
                    download= input_image_file_client.download_file()
                    downloaded_bytes = download.readall()
                    local_file.write(downloaded_bytes)
                
                # Upload to view -> html
                pass
            
            

        
        context = {'image_prediction_list': image_prediction_list, 'page_obj': page_obj} 
        return render(request, 'users/prediction.html', context=context)
    
    
class ImagePredictionSubmitSuccess(LoginRequiredMixin, View):
    """ 
    Logic for image prediction submission success page - prediction_submit_success.html 
    """
    def get(self, request):
        """ 
        Return prediction_submit_success.html 
        """
        return render(request, 'users/prediction_submit_success.html')
    
# We use reverse_lazy() because we are in "constructor attribute" code
# that is run before urls.py is completely loaded
class ImagePredictionCreate(LoginRequiredMixin, View):
    """ 
    Logic for image prediction create page - prediction_form.html
    Usage: handle logic when user upload input image to datalake for AI prediction.
    """
    template = 'users/prediction_form.html'
    successful_url = reverse_lazy('image_prediction_submit_success') #'image_prediction_all')
    
    def get(self, request):       
        """ 
        Create a form for input image and modality type and send it to front end.
        """
        image_prediction_form = ImagePredictionForm()
        ctx = {'image_prediction_form': image_prediction_form}
        return render(request, self.template, ctx)
    
    def post(self, request): 
        """
        Get input image and modality from the front end and load it into image_prediction_form. 
        Validate the form and return an empty form if the form's information is invalid.
        Resave image to media/input_images/input_image_{image_prediction_id}_{user_id}.{ext}
        Upload input_image to Azure Datalake.
        Send post request to AI Virtual Machine for AI inference on input image.
        Redirect user to image_prediction_submit_success to confirm successful submission. 
        """
        image_prediction_form = ImagePredictionForm(request.POST, request.FILES)
        
        if (not image_prediction_form.is_valid()): 
            ctx = {'image_prediction_form': image_prediction_form}
            return render(request, self.template, ctx)
        
        image_prediction_object = image_prediction_form.save(commit=False) #form.save(commit=False) 
        image_prediction_object.user = request.user
        image_prediction_object.save()
        # image_prediction_object = image_prediction_form.save()
        
        ############### Resave image files ###################################################
        image_prediction_file_name = os.path.basename(image_prediction_object.input_image.url)
        image_prediction_file_ext = os.path.splitext(image_prediction_file_name)[1]
        
        image_prediction_old_file_path = os.path.join(settings.MEDIA_ROOT, image_prediction_object.input_image.__str__())
        image_prediction_new_file_path = os.path.join(settings.MEDIA_ROOT, "input_images", f"input_image_{image_prediction_object.id}_{image_prediction_object.user_id}" + image_prediction_file_ext)
        image_prediction_new_internal_file_path = os.path.join("input_images", f"input_image_{image_prediction_object.id}_{image_prediction_object.user_id}" + image_prediction_file_ext)
        os.replace(image_prediction_old_file_path, image_prediction_new_file_path)
        
        image_prediction_object.input_image = image_prediction_new_internal_file_path
        image_prediction_object.save()
        ############### Upload image to Azure Datalake ###################################################
        
        config_path = os.path.join(settings.BASE_DIR, "users", "config_dl_vm", "config_dl_vm.json")
        with open(config_path) as config_file:
            config_data = json.load(config_file) 
        
        service_client = initialize_storage_account(config_reader.azure_storage['azure_storage_account_name']
            ,  config_reader.azure_storage['azure_storage_account_key']
        )

        file_system_client = service_client.get_file_system_client(file_system=config_data["file_system_name"])   
        directory_client = service_client.get_directory_client(file_system_client.file_system_name, config_data["input_folder_path"]) # "chest_xray"
        
        image_path = os.path.join(settings.MEDIA_ROOT, image_prediction_object.input_image.__str__())
        image_name = os.path.basename(image_path) 
        with open(image_path, "rb") as file: 
            file_system_client = directory_client.create_file(image_name) 
            file_system_client.upload_data(file,  overwrite=True)
            
        ########################################### send post request to AI VM ###############################################
        url = config_data["url"]         
        r = requests.post(url, json={ "file_system_name": config_data["file_system_name"], "file_path": image_prediction_object.input_image.__str__(), "output_folder_path": config_data["output_folder_path"]}) 
    
        # print(f"Status Code: {r.status_code}, Response: {r.json()}")            
        return redirect(self.successful_url)
    
# the get/post/validate/store flow
class ImagePredictionUpdate(LoginRequiredMixin, View):
    """ 
    Logic for image prediction view page - prediction_view.html
    Usage: handle logic when user click on an image_prediction_item on prediction.html to view the prediction's result. 
    """
    image_prediction_model = ImagePrediction
    disease_prediction_model = DiseasePrediction
    template = 'users/prediction_view.html'

    def get(self, request, pk):
        """ 
        Get lastest predictions (diseases' name and output image) of the input_image in the clicked image_prediction_item
        Check if input image and output image exist locally. If not, download those images from datalake.
            media/input_images/input_image_{image_prediction_id}_{user_id}.{ext}
            media/output_images/output_image_{image_prediction_id}_{user_id}.{ext}
        Return template prediction_view.html with associated input_image, output_image, and disease's name.
        """
        image_prediction_item = get_object_or_404(self.image_prediction_model, pk=pk)
        lastest_timestamp = DiseasePrediction.objects.filter(image_prediction_id=image_prediction_item.id).order_by('-timestamp')[0].timestamp
        disease_prediction_list = DiseasePrediction.objects.filter(image_prediction_id=image_prediction_item.id, timestamp = lastest_timestamp) #.values()
        disease_dict = {}        
        
        num_disease_found = 0
        for disease_prediction_item in disease_prediction_list:
            disease_name = disease_prediction_item.disease
            if disease_name:
                num_disease_found += 1
                if disease_name not in disease_dict:
                    disease_dict[disease_name] = []
                    disease_dict[disease_name].append(float(disease_prediction_item.score) *100.0)
                else:
                    disease_dict[disease_name].append(float(disease_prediction_item.score) *100.0)

        # num_disease_found = len(disease_prediction_list)

        input_image_file_path = os.path.join(settings.MEDIA_ROOT, image_prediction_item.input_image.__str__())
        output_image_file_path = os.path.join(settings.MEDIA_ROOT, image_prediction_item.output_image.__str__()) 
        
        # If output_image is already in local storage.
        if os.path.exists(input_image_file_path):
            # Yes: Upload to view -> html
            print("Input image exists locally, not download from datalake.")
            pass
        else: # If output_image not in local storage:
            print("Input image not exists locally, download from datalake.")
            
            config_path = os.path.join(settings.BASE_DIR, "users", "config_dl_vm", "config_dl_vm.json")
            with open(config_path) as config_file:
                config_data = json.load(config_file)
            
            # Download from cloud AI model API to local storage.
            service_client = initialize_storage_account(config_reader.azure_storage['azure_storage_account_name']
                ,  config_reader.azure_storage['azure_storage_account_key']
            )
            file_system_client = service_client.get_file_system_client(file_system= config_data["file_system_name"])
            
            # datalake file path
            datalake_input_image_file_path =  image_prediction_item.input_image.__str__()
            input_image_file_client = file_system_client.get_file_client(file_path = datalake_input_image_file_path)
            
            input_path = input_image_file_path 
            with open(input_path,'wb') as local_file:
                download= input_image_file_client.download_file()
                downloaded_bytes = download.readall()
                local_file.write(downloaded_bytes)
            
            # Upload to view -> html
            pass
           
        # If output_image is already in local storage.
        if os.path.exists(output_image_file_path):
            # Yes: Upload to view -> html
            print("Output image exists locally, not download from datalake.")
            pass
        else: # If output_image not in local storage:
            print("Output image not exists locally, download from datalake.")
            
            config_path = os.path.join(settings.BASE_DIR, "users", "config_dl_vm", "config_dl_vm.json")
            with open(config_path) as config_file:
                config_data = json.load(config_file)
            
            # Download from cloud AI model API to local storage.
            service_client = initialize_storage_account(config_reader.azure_storage['azure_storage_account_name']
                ,  config_reader.azure_storage['azure_storage_account_key']
            )
            file_system_client = service_client.get_file_system_client(file_system= config_data["file_system_name"])
            
            # datalake file path
            datalake_output_image_file_path =  image_prediction_item.output_image.__str__()
            output_image_file_client = file_system_client.get_file_client(file_path = datalake_output_image_file_path)
            
            output_path = output_image_file_path 
            with open(output_path,'wb') as local_file:
                download= output_image_file_client.download_file()
                downloaded_bytes = download.readall()
                local_file.write(downloaded_bytes)
            
            # Upload to view -> html
            pass
        
        ctx = {"image_prediction_item": image_prediction_item, "disease_prediction_list": disease_prediction_list, "disease_dict": disease_dict, "num_disease_found": num_disease_found}
        return render(request, self.template, ctx)


class ImagePredictionDelete(LoginRequiredMixin, View):
    """ 
    Logic for image prediction delete page - prediction_confirm_delete.html
    Usage: handle logic when user click delete on an image_prediction_item on prediction.html. 
    """
    model = ImagePrediction
    success_url = reverse_lazy('image_prediction_all')
    template = 'users/prediction_confirm_delete.html'
    
    def get(self, request, pk):
        """ 
        Get that image_prediction_item from users_image_prediction table in database. 
        Return prediction_confirm_delete with associated data
        """
        image_prediction_item = get_object_or_404(self.model, pk=pk)
        image_prediction_form = ImagePredictionForm(instance=image_prediction_item)
        ctx = {'image_prediction_item': image_prediction_item}
        return render(request, self.template, ctx)
    
    def post(self, request, pk):
        """ 
        Get that image_prediction_item from users_image_prediction table in database. 
        Delete the image_prediction_item.
        Redirect to prediction history page. 
        """
        image_prediction_item = get_object_or_404(self.model, pk=pk)
        image_prediction_item.delete()
        return redirect(self.success_url)

        

