from django.shortcuts import render,redirect
from student_faculty import models 
from django.utils import timezone
from django.http import HttpResponse



def homepage(request):
    if not request.user.is_authenticated:
        return redirect('home')
    student_object = ""
    try:
        student_object = models.StudentUser.objects.get(user = request.user)
    except:
        return HttpResponse("Error-> No such student")

    return render(request,'home_student.html',{'student':student_object})

