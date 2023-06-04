from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, UpdateConditionPredictionForm, DummyForm
from .models import DummyModel, ConditionPrediction

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

# @login_required
# def prediction(request):   
#     context = {"hello": "This is Tran"}
#     # dummy_form = {"first_value": 10}
    
#     if request.method == 'POST':
#         dummy_form = DummyForm(request.POST)
        
#         if dummy_form.is_valid():
#             dummy_form.save()
#             messages.success(request, "update dummy form successful")
#             return redirect(to='users-condition-prediction')
    
#     else:
#         context['dummy_form'] = DummyForm()
#     return render(request, 'users/prediction.html', context=context)

from django.contrib.auth.mixins import LoginRequiredMixin
class ConditionPredictionView(LoginRequiredMixin, View):
    def get(self, request):
        dummy_list = DummyModel.objects.all();
        # print(dummy_list)
        # condition_prediction_list = ConditionPrediction.objects.count();
        
        # condition_prediction_list = {"hello"}
        # print(condition_prediction_list)
        
        context = {'dummy_list': dummy_list} # 'condition_prediction_list' : condition_prediction_list
        return render(request, 'users/prediction.html', context=context)
    
    
# We use reverse_lazy() because we are in "constructor attribute" code
# that is run before urls.py is completely loaded
class ConditionPredictionCreate(LoginRequiredMixin, View):
    template = 'users/prediction_form.html'
    successful_url = reverse_lazy('condition_prediction_all')
    
    def get(self, request):
        form = DummyForm()
        ctx = {'form': form}
        return render(request, self.template, ctx)
    
    def post(self, request):
        form = DummyForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)
        
        dummy = form.save()
        return redirect(self.successful_url)
    
    
# the get/post/validate/store flow
class ConditionPredictionUpdate(LoginRequiredMixin, View):
    model = DummyModel
    success_url = reverse_lazy('condition_prediction_all')
    template = 'users/prediction_form.html'

    def get(self, request, pk):
        dummy_item = get_object_or_404(self.model, pk=pk)
        form = DummyForm(instance=dummy_item)
        
        ctx = {'form': form, "dummy_item": dummy_item}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        dummy_item = get_object_or_404(self.model, pk=pk)
        # print("dummy_item:", dummy_item.__dict__)
        
        # print("request.POST:", request.POST)
        # print("request.FILES:", request.FILES)
        
        form = DummyForm(request.POST, request.FILES, instance=dummy_item)
        
        if not form.is_valid():
            print("This form is not valid")
            ctx = {'form': form}
            return render(request, self.template, ctx)
        
        # print("form:", form)
        # print("form['x_image']:", form["x_image"].__dict__)
        # print("form:", form.__dict__)

        form.save()
        return redirect(self.success_url)


class ConditionPredictionDelete(LoginRequiredMixin, View):
    model = DummyModel
    success_url = reverse_lazy('condition_prediction_all')
    template = 'users/prediction_confirm_delete.html'
    
    def get(self, request, pk):
        dummy_item = get_object_or_404(self.model, pk=pk)
        form = DummyForm(instance=dummy_item)
        ctx = {'dummy_item': dummy_item}
        return render(request, self.template, ctx)
    
    def post(self, request, pk):
        dummy_item = get_object_or_404(self.model, pk=pk)
        dummy_item.delete()
        return redirect(self.success_url)

        

