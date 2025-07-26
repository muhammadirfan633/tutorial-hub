from django.db import models
from django.contrib.auth.models import User
from urllib.parse import urlparse, parse_qs

# Create your models here.

class CommonModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    slug=models.SlugField(unique=True,auto_created=True)
    
    class Meta:
        abstract=True


class Course(CommonModel):
    course_name=models.CharField(unique=True,max_length=25)
    course_discription=models.CharField(max_length=100)
    
    def __str__(self):
        return self.course_name


class Content(CommonModel):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    body=models.TextField()

    def __str__(self):
        return self.course.course_name


class ContentVedio(CommonModel):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    content=models.ForeignKey(Content,on_delete=models.CASCADE)
    vedio_title=models.CharField(max_length=50)
    vedio_url=models.URLField()
    def clean(self):
        # Extract the video ID from various YouTube URL formats
        url = self.vedio_url
        parsed = urlparse(url)
        video_id = None
        if 'youtube.com' in parsed.netloc:
            qs = parse_qs(parsed.query)
            video_id = qs.get('v', [None])[0]
        elif 'youtu.be' in parsed.netloc:
            video_id = parsed.path.lstrip('/')
        if video_id:
            self.vedio_url = f'https://www.youtube.com/watch?v={video_id}'

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

   
    
class enrolement(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together=('user','course')
    def __str__(self):
        return self.user.username
    
class Contact(models.Model):
    full_name=models.CharField(max_length=100)
    email=models.EmailField()
    phone_number=models.CharField(null=True,blank=True)
    message=models.TextField()


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'course', 'content')

    def __str__(self):
        return f"{self.user.username} - {self.course.course_name} - {self.content.title}"