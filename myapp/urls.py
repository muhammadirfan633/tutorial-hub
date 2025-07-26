from django.urls import path
from .views import coursecreate_view,home,CourseListView,CourseContentDetailView,ContactView,registerview,UserLogin,LogoutViewAllow,enrollmentview,UserDetailView,UserUpdateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',home,name='home'),
    path('create_course/',coursecreate_view.as_view(),name='create_course'),
    path('courselist/',CourseListView.as_view(),name='courselist'),
    path('courses/<slug:course_slug>/<slug:slug>/',CourseContentDetailView.as_view(),name='course-content-detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('register/', registerview.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', LogoutViewAllow.as_view(), name='logout'),
    path('enrollment/<slug:course_slug>/', enrollmentview.as_view(), name='enrollment'),
    #path('videos/', VideoListView.as_view(), name='videos'),
    path('profile/', UserDetailView.as_view(), name='profile'),
    path('profile/edit/', UserUpdateView.as_view(), name='profile-edit'),


]
