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
        return render(request,'error_authentication.html',{'error':"You must be a faculty to access this page"})
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
        return render(request,'error_authentication.html',{'error':"You must be a faculty to access this page"})

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
        return render(request,'error_authentication.html',{'error':"You must be a faculty to access this page"})
    course = ""
    try:
        course = models.Course.objects.get(course_name = cn, semester = sem, year = ye, profs = faculty_object)
    except:
        return render(request,'error_faculty.html',{'fac':faculty_object ,'error':"Please enter a valid course URL"})
    

    applications = models.Application.objects.filter(course = course)
    emails_accepted_array = models.Application.objects.values_list('student__ldap_id',flat = True).filter(course = course, status = "Accepted")
    emails_accepted =""
    for i in emails_accepted_array:
        emails_accepted+=i+"@iitb.ac.in,"

    if emails_accepted!="":
        emails_accepted = emails_accepted[:-1]
    
    emails_rejected_array = models.Application.objects.values_list('student__ldap_id',flat = True).filter(course = course, status = "Rejected")
    emails_rejected =""
    for i in emails_rejected_array:
        emails_rejected+=i+"@iitb.ac.in,"

    if emails_rejected!="":
        emails_rejected = emails_rejected[:-1]
    
    emails_on_hold_array = models.Application.objects.values_list('student__ldap_id',flat = True).filter(course = course, status = "On Hold")
    emails_on_hold =""
    for i in emails_on_hold_array:
        emails_on_hold+=i+"@iitb.ac.in,"

    if emails_on_hold!="":
        emails_on_hold = emails_on_hold[:-1]
    
    emails_waitlist_array = models.Application.objects.values_list('student__ldap_id',flat = True).filter(course = course, status = "Waitlist")
    emails_waitlist =""
    for i in emails_waitlist_array:
        emails_waitlist+=i+"@iitb.ac.in,"

    if emails_waitlist!="":
        emails_waitlist = emails_waitlist[:-1]
    

    return render(request,'applications.html',{'applications':applications,'course':course,'accepted':emails_accepted,'rejected':emails_rejected,'hold':emails_on_hold,'waitlist':emails_waitlist})



    
def editCourse(request,cn,sem,ye):
    if not request.user.is_authenticated:
        return redirect('home')
    faculty_object = ""
    try:
        faculty_object = models.FacultyUser.objects.get(user = request.user)
    except:
        return render(request,'error_authentication.html',{'error':"You must be a faculty to access this page"})
    course = ""
    try:
        course = models.Course.objects.get(course_name = cn, semester = sem, year = ye, profs = faculty_object)
    except:
        return render(request,'error_faculty.html',{'fac':faculty_object ,'error':"Please enter a valid course URL/You are not a course professor for "+ cn +" "+sem+" "+ye+". Please ask the course professor to add you as one."})
    if request.method == "POST":
        form = forms_faculty.PostForm_NewCouse(request.POST,instance = course)
        if form.is_valid():
            post = form.save()
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('faculty_applications',cn = cn,sem = sem,ye = ye)
    else:
        form = forms_faculty.PostForm_NewCouse(instance = course)
    return render(request,'addcourse.html',{form:'form'})

def student_profile(request,cn,sem,ye,ldap_stud):
    if not request.user.is_authenticated:
        return redirect('home')
    faculty_object = ""
    try:
        faculty_object = models.FacultyUser.objects.get(user = request.user)
        print("Got faculty object.")
    except:
        return render(request,'error_authentication.html',{'error':"You must be a faculty to access this page"})
    course = ""
    try:
        course = models.Course.objects.get(course_name = cn, semester = sem, year = ye, profs = faculty_object)
        print("Got faculty object.")
    except:
        return render(request,'error_faculty.html',{'fac':faculty_object ,'error':"No such Course " + cn+" "+ sem + " " + ye+"\nPlease enter a valid course URL"})
    try:
        student_object = models.StudentUser.objects.get(ldap_id = ldap_stud)
        print("Got student object.")

    except:
        return render(request,'error_faculty.html',{'fac':faculty_object ,'error':"No such student"})
    
    
    try:
        application = models.Application.objects.get(course = course,student = student_object)
        print("got application object")
    except:
        return render(request,'error_faculty.html',{'fac':faculty_object ,'error':"No such student application"})

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