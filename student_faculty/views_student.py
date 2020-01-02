from django.shortcuts import render,redirect
from student_faculty import models 
from django.utils import timezone
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Course,Application
from django import forms
from student_faculty import forms_student
import datetime

#Done by Samad
class CourseList(ListView):
	template_name="course_list.html"
	model=Course
	queryset=Course.objects.filter(deadline__gte=datetime.date.today())

	
class ApplicationList(ListView):
	template_name="application_list.html"
	model=Application
	queryset=Application.objects.none()
	def get(self,request,*args,**kwargs):

		try:
			student_object = models.StudentUser.objects.get(user=request.user)
		except:
			return HttpResponse("Error-> No such student")
		self.queryset=Application.objects.filter(course__deadline__gte=datetime.date.today(),student = student_object)
		return super(ApplicationList,self).get(request,*args,**kwargs)

#Done By Karan

def editdetails(request):
    if not request.user.is_authenticated:
        return redirect('home')
    student_object = ""
    try:
        student_object = models.StudentUser.objects.get(user = request.user)
    except:
        return HttpResponse("Error")

    if request.method == "POST":
        form = forms_student.PostForm_EditDetails(request.POST,instance=student_object)
        if form.is_valid():
            form.save()
            return redirect('student_profile')
    else:
        form = forms_student.PostForm_EditDetails(instance=student_object)
    return render(request, 'editdetails.html', {'form': form})

#Done By Sumanyu
def homepage(request):
    if not request.user.is_authenticated:
        return redirect('home')
    student_object = ""
    try:
        student_object = models.StudentUser.objects.get(user = request.user)
    except:
        return HttpResponse("Error-> No such student")

    return render(request,'home_student.html',{'student':student_object})



def applications(request,cn,sem,ye):
    if not request.user.is_authenticated:
        return redirect('home')
    student_object = ""
    try:
        student_object = models.StudentUser.objects.get(user = request.user)
    except:
        return HttpResponse("Error")
    course = ""
    try:
        course = models.Course.objects.get(course_name = cn,semester = sem,year = ye)
    except:
        return HttpResponse("Error")
    if course.deadline<datetime.date.today():
        return HttpResponse("Error. You are late!")
    try:
        application = models.Application.objects.get(student = student_object,course = course)
        if request.method == "POST":
            form = forms_student.AddApplication(request.POST,instance = application)
            if form.is_valid():
                post = form.save()
                post.author = request.user
                post.student = student_object
                post.published_date = timezone.now()
                post.save()
                print("B1")
                return redirect('course_list')
        else:
            form = forms_student.AddApplication(instance = application)
            form.fields['answers_to_questions'].label = course.extra_questions
            return render(request, 'student_application.html', {'form': form,'course':course})


    except:
        application=Application(course=course,student=student_object)
        if request.method == "POST":
            form = forms_student.AddApplication(request.POST,instance=application)
            if form.is_valid():
                post = form.save()
                post.author = request.user
                post.student = student_object
                post.published_date = timezone.now()
                post.save()
                print("B2")
                return redirect('course_list')
        else:
            form = forms_student.AddApplication(instance=application)
            form.fields['answers_to_questions'].label = course.extra_questions
            print("B3")

        return render(request, 'student_application.html', {'form': form,'course':course})
