from django.contrib import admin

# Register your models here.
from .models import Course,enrolement,Content,ContentVedio,Contact,Progress


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display=['course_name','slug','course_discription','created_at']
    prepopulated_fields={'slug': ('course_name',)}


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display=['course','slug','title','body','created_at']
    prepopulated_fields={'slug':('title',)}
    
@admin.register(ContentVedio)
class VedioAdmin(admin.ModelAdmin):
    list_display=['course','content','slug','vedio_title','vedio_url','created_at']
    prepopulated_fields={'slug':('vedio_title',)}
    
    
@admin.register(enrolement)
class EnrolAdmin(admin.ModelAdmin):
    list_display=['user','course','created_at']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display=['full_name','email','phone_number','message']
@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display=['user','course','content','completed']