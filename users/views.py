import os

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, ImagePredictionForm
from .models import ImagePrediction

from .azure_dl.config.config_reader import ConfigReader
from .azure_dl.connectors.azure_dl import initialize_storage_account

def home(request):
    return render(request, 'users/home.html')


class RegisterView(View):
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
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

from django.contrib.auth.mixins import LoginRequiredMixin
class ImagePredictionView(LoginRequiredMixin, View):
    def get(self, request):
        image_prediction_list = ImagePrediction.objects.filter(user_id=request.user.id)
        
        # print("image_prediction_list[0]:", image_prediction_list[0])
        # print("image_prediction_list[0].__dict__:", image_prediction_list[0].__dict__)
        
        context = {'image_prediction_list': image_prediction_list} # 'condition_prediction_list' : condition_prediction_list
        return render(request, 'users/prediction.html', context=context)
    
class ImagePredictionSubmitSuccess(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'users/prediction_submit_success.html')
    
# We use reverse_lazy() because we are in "constructor attribute" code
# that is run before urls.py is completely loaded
class ImagePredictionCreate(LoginRequiredMixin, View):
    template = 'users/prediction_form.html'
    successful_url = reverse_lazy('image_prediction_submit_success') #'image_prediction_all')
    
    def get(self, request):
        image_prediction_form = ImagePredictionForm()
        ctx = {'image_prediction_form': image_prediction_form}
        return render(request, self.template, ctx)
    
    def post(self, request): #Working on
        image_prediction_form = ImagePredictionForm(request.POST, request.FILES)
        
        
        if (not image_prediction_form.is_valid()): 
            ctx = {'image_prediction_form': image_prediction_form}
            return render(request, self.template, ctx)
        
        # user_form.save()
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
        # print("image_prediction_old_file_path:",image_prediction_old_file_path)
        # print("image_prediction_new_file_path:", image_prediction_new_file_path)
        os.replace(image_prediction_old_file_path, image_prediction_new_file_path)
        
        image_prediction_object.input_image = image_prediction_new_internal_file_path
        image_prediction_object.save()
        ############### Upload image to Azure Datalake ###################################################
        import json
        with open("/mnt/d/Chest-Xray-Web-App/users/config_dl_vm/config_dl_vm.json") as config_file:
            config_data = json.load(config_file) #???
        
        config_reader = ConfigReader(file_name = config_data["config_dl_file_name"]) # '/home/nathan/project/ChestXray-Model-API/app/config/config.ini'
        service_client = initialize_storage_account(config_reader.azure_storage['azure_storage_account_name']
            ,  config_reader.azure_storage['azure_storage_account_key']
        )

        file_system_client = service_client.get_file_system_client(file_system=config_data["file_system_name"])   
        directory_client = service_client.get_directory_client(file_system_client.file_system_name, config_data["input_folder_path"]) # "chest_xray"
        
        image_path = os.path.join(settings.MEDIA_ROOT, image_prediction_object.input_image.__str__())
        image_name = os.path.basename(image_path) 
        with open(image_path, "rb") as file: #"/home/Chest-Xray-Web-App/test2.jpeg"
            file_system_client = directory_client.create_file(image_name) #"test2.jpeg"
            file_system_client.upload_data(file,  overwrite=True)
            
        ########################################### send post request to AI VM ###############################################
        import requests 

        url = config_data["url"]
        # url = 'https://prod-16.eastus.logic.azure.com:443/workflows/091f774adc5846ebb3f80234f8d84d7e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=ggXbpwfMA2J5MgVkErXbbLz-ANVgEOJ2tgfC4wHk-Ns'         
        r = requests.post(url, json={ "file_system_name": config_data["file_system_name"], "file_path": image_prediction_object.input_image.__str__(), "output_folder_path": config_data["output_folder_path"]}) 
    
        print(f"Status Code: {r.status_code}, Response: {r.json()}")            
        return redirect(self.successful_url)
    
# the get/post/validate/store flow
class ImagePredictionUpdate(LoginRequiredMixin, View):
    model = ImagePrediction
    # success_url = reverse_lazy('image_prediction_all')
    template = 'users/prediction_view.html'

    def get(self, request, pk):
        image_prediction_item = get_object_or_404(self.model, pk=pk)
        # print("image_prediction_item.input_image:", image_prediction_item.input_image) # input_images/input_image_10_1.jpg
        # print("image_prediction_item.output_image:", image_prediction_item.output_image) # output_images/output_image_10_1.jpg
        # print("image_prediction_item.output_image.url:", image_prediction_item.output_image.url) # /media/output_images/output_image_10_1.jpg
        # print("image_prediction_item.output_image.__str__():", image_prediction_item.output_image.__str__())
        output_image_file_path = os.path.join(settings.MEDIA_ROOT, image_prediction_item.output_image.__str__()) # /mnt/d/Chest-Xray-Web-App/media/output_images/output_image_10_1.jpg
        # print("output_image_path:", output_image_path) # True
        # print("os.path.exists(output_image_path):",os.path.exists(output_image_path))
           
        # If output_image is already in local storage.
        if os.path.exists(output_image_file_path):
            # Yes: Upload to view -> html
            print("Output image exists locally, not download from datalake.")
            pass
        else: # If output_image not in local storage:
            print("Output image not exists locally, download from datalake.")
            
            import json
            with open("/mnt/d/Chest-Xray-Web-App/users/config_dl_vm/config_dl_vm.json") as config_file:
                config_data = json.load(config_file)
            
            # Download from cloud AI model API to local storage.
            config_reader = ConfigReader(file_name = config_data["config_dl_file_name"]) # '/home/nathan/project/ChestXray-Model-API/app/config/config.ini'
            service_client = initialize_storage_account(config_reader.azure_storage['azure_storage_account_name']
                ,  config_reader.azure_storage['azure_storage_account_key']
            )
            
            file_system_client = service_client.get_file_system_client(file_system= config_data["file_system_name"])
            # datalake file path
            datalake_file_path =  image_prediction_item.output_image.__str__()
            file_client = file_system_client.get_file_client(file_path = datalake_file_path)
            
            # output_path = os.path.join("/home/nathan/project/ChestXray-Model-API/app/", "images_1.jpeg")
            output_path = output_image_file_path #"/home/Chest-Xray-Web-App/test2.jpeg" # "/mnt/d/Chest-Xray-Web-App/users/azure_dl/test2.jpeg" #/home/Chest-Xray-Web-App
            with open(output_path,'wb') as local_file:
                download= file_client.download_file()
                downloaded_bytes = download.readall()
                local_file.write(downloaded_bytes)
            
            # Upload to view -> html
            pass
        
        # print(image_prediction_item.output_image)
        # print(image_prediction_item.output_image.url)
        
        ctx = {"image_prediction_item": image_prediction_item}
        return render(request, self.template, ctx)


class ImagePredictionDelete(LoginRequiredMixin, View):
    model = ImagePrediction
    success_url = reverse_lazy('image_prediction_all')
    template = 'users/prediction_confirm_delete.html'
    
    def get(self, request, pk):
        image_prediction_item = get_object_or_404(self.model, pk=pk)
        image_prediction_form = ImagePredictionForm(instance=image_prediction_item)
        ctx = {'image_prediction_item': image_prediction_item}
        return render(request, self.template, ctx)
    
    def post(self, request, pk):
        image_prediction_item = get_object_or_404(self.model, pk=pk)
        image_prediction_item.delete()
        return redirect(self.success_url)

        

