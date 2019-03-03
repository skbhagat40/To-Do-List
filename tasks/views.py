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
from django.contrib.auth import authenticate
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
        return Tasks.objects.all()

    
class DetailView(generic.DetailView):
    template_name = 'tasks/detail.html'
    model = Tasks
    context_object_name = 'task'


class CreateTask(generic.CreateView):
    template_name = 'tasks/forms.html'
    model = Tasks
    fields = ['TaskName','Description','DueDate','priority']

    
class UpdateTask(generic.UpdateView):
    template_name = 'tasks/forms.html'
    model = Tasks
    fields = ['TaskName','Description','DueDate','priority']

    
class DeleteTask(generic.DeleteView):
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
    form_class = AuthenticationForm
    success_url = reverse_lazy('tasks:homepage')
    def form_valid(self,form):
        user = AuthenticationForm(data = self.request.POST)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            return HttpResponseRedirect(reverse('tasks:homepage'))
        else:
            return super(LoginView,self).form_valid(form)


class RegisterView(generic.CreateView):
    template_name = 'tasks/register.html'
    success_url = reverse_lazy('tasks:homepage')
    #context_object_name = 'register_object'
    model = User
    fields = ['username','password','email','first_name','last_name']

