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
    if request.method == "POST":
        form = forms_faculty.PostForm_NewCouse(request.POST,instance = course)
        if form.is_valid():
            post = form.save()
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('faculty_home')
    else:
        form = forms_faculty.PostForm_NewCouse(instance = course)
    

def student_profile(request,cn,sem,ye,ldap_stud):
    if not request.user.is_authenticated:
        return redirect('home')
    faculty_object = ""
    try:
        faculty_object = models.FacultyUser.objects.get(user = request.user)
        print("Got faculty object.")
    except:
        return HttpResponse("Error -> Not a faculty member")
    course = ""
    try:
        course = models.Course.objects.get(course_name = cn, semester = sem, year = ye, profs = faculty_object)
        print("Got faculty object.")
    except:
        return HttpResponse("Error - > No such Course " + cn+" "+ sem + " " + ye)
    try:
        student_object = models.StudentUser.objects.get(ldap_id = ldap_stud)
        print("Got student object.")

    except:
        return HttpResponse("Error -> No Such Student")
    
    
    try:
        application = models.Application.objects.get(course = course,student = student_object)
        print("got application object")
    except:
        return HttpResponse("Error -> No such student has filled up the form")

    if request.method == "POST":
        form = forms_faculty.Application(request.POST,instance = application)
        if form.is_valid():
            post = form.save()
            post.save()
            return redirect('faculty_applications',cn = cn,sem = sem, ye = ye)
    else:
        form = forms_faculty.Application(instance = application)
        form.fields['waitlist_num'].label = "Waitlist number. Please fill this only if you are waitlisting someone"


    
    return render(request,'student_profile.html',{'student':student_object,'course':course,'application':application,'form':form})