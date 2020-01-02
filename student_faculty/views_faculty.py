from django.shortcuts import render,redirect
from student_faculty import models 
from django.utils import timezone
from django.http import HttpResponse

# Create your views here.
class trialcourse():
    def __init__(self,d1,d2,d3):
        # initializing instance variable
        self.course_name=d1
        self.semester = d2
        self.year = d3


from student_faculty import forms_faculty
def home(request):
    if not request.user.is_authenticated:
        return redirect('home')
    faculty_object = ""
    try:
        faculty_object = models.FacultyUser.objects.get(user = request.user)
    except:
        return HttpResponse("Error")
    faculty = faculty_object.ldap_id
    courses = models.Course.objects.filter(profs__ldap_id = faculty_object.ldap_id)
    # #Tester Code
    #To test w/o login, please comment out the rest of the code above, and test the following
    # faculty = "Saoaposjdsp"

    # x1 = trialcourse('MA105','Spring','2020')
    # x2 = trialcourse('MA106','Autumn','2020')
    # courses = [x1,x2]
    return render(request,'home.html',{'fac':faculty,
                                        'courses':courses})



def addcourse(request):
    if not request.user.is_authenticated:
        return redirect('home')
    faculty_object = ""
    try:
        faculty_object = models.FacultyUser.objects.get(user = request.user)
    except:
        return HttpResponse("Error")

    if request.method == "POST":
        form = forms_faculty.PostForm_NewCouse(request.POST)
        if form.is_valid():
            post = form.save()
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('faculty_home')


    else:
        form = forms_faculty.PostForm_NewCouse()
    return render(request, 'addcourse.html', {'form': form})



def ListApplicants(request,cn,sem,ye):
    if not request.user.is_authenticated:
        return redirect('home')
    faculty_object = ""
    try:
        faculty_object = models.FacultyUser.objects.get(user = request.user)
    except:
        return HttpResponse("Error -> Not a faculty")
    course = ""
    try:
        course = models.Course.objects.get(course_name = cn, semester = sem, year = ye, profs = faculty_object)
    except:
        return HttpResponse("Error - > No such Course" + cn+" "+ sem + " " + ye)
    

    applications = models.Application.objects.filter(course = course)

    return render(request,'applications.html',{'applications':applications,'course':course})



    
def editCourse(request,cn,sem,ye):
    if not request.user.is_authenticated:
        return redirect('home')
    faculty_object = ""
    try:
        faculty_object = models.FacultyUser.objects.get(user = request.user)
    except:
        return HttpResponse("Error -> Not a faculty member")
    course = ""
    try:
        course = models.Course.objects.get(course_name = cn, semester = sem, year = ye, profs = faculty_object)
    except:
        return HttpResponse("Error - > No such Course" + cn+" "+ sem + " " + ye)
    form = forms_faculty.PostForm_EditCourse(request.POST or None, instance=course)
    if form.is_valid():
        form.save()
        return redirect('faculty_home')
    

    