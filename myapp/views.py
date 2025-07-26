from django.shortcuts import render,get_object_or_404

# Create your views here.
from .models import Course,enrolement,Content,Contact,ContentVedio,Progress
from django.http import request
from django.views.generic.edit import CreateView
from django.views.generic import ListView,DetailView,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import logout


def home(request):
    return render(request,'myapp/index.html')


class coursemainview:
    model=Course
    
class coursecreate_view(coursemainview,CreateView):
    template_name='myapp/course.html'
    success_url=reverse_lazy('courselist')
    fields=['course_name','slug','course_discription']
    
    
class CourseListView(coursemainview,ListView):
    template_name = "myapp/resume.html"
    context_object_name='courses'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['enrolled_courses'] = Course.objects.filter(enrolement__user=self.request.user)
        else:
            context['enrolled_courses'] = []
        return context

class CourseContentDetailView(LoginRequiredMixin, DetailView):
    model = Content
    template_name = 'myapp/mother.html'
    context_object_name = 'selected_content'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_slug = self.kwargs.get('course_slug')
        course = get_object_or_404(Course, slug=course_slug)
        context['course'] = course
        context['contents'] = course.content_set.all()
        context['videos'] = ContentVedio.objects.filter(content=self.object)
        return context
    
class ContactView(CreateView):
    model = Contact
    template_name = 'myapp/contact.html'
    fields = ['full_name', 'email', 'phone_number', 'message']
    success_url = reverse_lazy('home')
    

class enrollmentview(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        course_slug = kwargs.get('course_slug')
        course = get_object_or_404(Course, slug=course_slug)
        enrollment, created = enrolement.objects.get_or_create(user=request.user, course=course)
        if created:
            message = "You have successfully enrolled in the course."
        else:
            message = "You are already enrolled in this course."
        return redirect('courselist')  # Redirect to course list after enrolling

    def get(self, request, *args, **kwargs):
        return redirect('courselist')
    
'''class enrollmentlistview(LoginRequiredMixin, ListView):
    model = enrolement
    template_name = 'myapp/enrollment_list.html'
    context_object_name = 'enrollments'

    def get_queryset(self):
        return enrolement.objects.filter(user=self.request.user)'''
class authmainview:
    model=User
    
class registerview(authmainview,CreateView):
    template_name='myapp/register.html'
    form_class = UserCreationForm
    context_object_name = 'form'
    success_url = reverse_lazy('home')

    
class UserLogin(authmainview,LoginView):
    template_name='myapp/login.html' 
    fields = ['username', 'password']
    

class LogoutViewAllow(View):
    def get(self, request):
        logout(request)
        return redirect('/login/')


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'myapp/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrolled_courses = Course.objects.filter(enrolement__user=self.request.user)
        progress_list = []
        for course in enrolled_courses:
            total = course.content_set.count()
            completed = Progress.objects.filter(
                user=self.request.user, course=course, completed=True
            ).count()
            percent = int((completed / total) * 100) if total > 0 else 0
            progress_list.append({
                'course': course,
                'completed': completed,
                'total': total,
                'percent': percent,
            })
        context['progress_list'] = progress_list
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'myapp/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

