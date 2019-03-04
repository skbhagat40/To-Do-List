from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.views import generic
from .models import Tasks
from django.urls import reverse,reverse_lazy
from django.forms import DateInput
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,logout,login
from .forms import LoginForm
from django import forms
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
#def home(request):
#    return render(request,'tasks/home.html')


class IndexView(generic.ListView):
# adding authentication
    def get(self, request):
        is_logged_in = request.user.is_authenticated

        if not is_logged_in :
            url = reverse_lazy('tasks:login')
            return HttpResponseRedirect(url)
        else:
            return super(IndexView,self).get(self.request)
        
    template_name = 'tasks/home.html'
    context_object_name = 'all_tasks'
    
    def get_queryset(self):
        return Tasks.objects.filter(user=self.request.user)

    
class DetailView(generic.DetailView,LoginRequiredMixin):
    template_name = 'tasks/detail.html'
    model = Tasks
    context_object_name = 'task'

    '''def get_object(self, queryset=None):
        obj = super(DetailView, self).get_object(queryset=queryset)
        if obj.user != self.request.user:
            raise Http404()
        return obj'''
    
    def get_queryset(self):
        queryset = super(DetailView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class CreateTask(generic.CreateView,LoginRequiredMixin):
    template_name = 'tasks/forms.html'
    model = Tasks
    fields = ['TaskName','Description','DueDate','priority']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)


class UpdateTask(generic.UpdateView,LoginRequiredMixin):
    template_name = 'tasks/forms.html'
    model = Tasks
    fields = ['TaskName','Description','DueDate','priority']

    
class DeleteTask(generic.DeleteView,LoginRequiredMixin):
    model = Tasks
    success_url = reverse_lazy('tasks:homepage')

    def get_success_url(self):
        return DeleteTask.success_url

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(DeleteTask, self).post(request, *args, **kwargs)

        
class LoginView(generic.edit.FormView):
    template_name = 'tasks/login.html'
    #context_object_name = 'login_object'
    form_class = LoginForm
    success_url = reverse_lazy('tasks:homepage')
                
    def form_valid(self,form):
        #user = AuthenticationForm(data = self.request.POST)
        Username = form.cleaned_data['Username']
        Password = form.cleaned_data['Password']
        user = authenticate(self.request,username=Username,password=Password)
        if user is not None:
            login(self.request,user)
            return HttpResponseRedirect(reverse('tasks:homepage'))
        else:
 
            return super(LoginView,self).form_valid(form)

class RegisterView(generic.CreateView):
    template_name = 'tasks/register.html'
    success_url = reverse_lazy('tasks:homepage')
    #context_object_name = 'register_object'
    model = User
    fields = ['username','password','email','first_name','last_name']

    '''def form_valid(self,form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        return super(RegisterView,self).form_valid(form)'''
    def get_form(self,form_class=None):
            form = super(RegisterView,self).get_form(form_class)
            form.fields['password'].widget = forms.PasswordInput()
            return form
        
    def form_valid(self,form):
        #form = self.form_class(request.POST) #form to take values from the request method
    
        if form.is_valid():
            user = form.save(commit = False)
            username = form.cleaned_data['username'] # else would have used request.POST.get('var1')
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return redirect('tasks:homepage')
        else:
            return render(self.request,'tasks/register.html',{'form':form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('tasks:homepage'))
