from django.shortcuts import render,redirect
from . import models 
from django.utils import timezone

# Create your views here.
class trialcourse():
    def __init__(self,d1,d2,d3):
        # initializing instance variable
        self.course_name=d1
        self.semester = d2
        self.year = d3


from . import forms_faculty
def home(request):
    if not request.FacultyUser.is_authenticated:
        return redirect('home')
    faculty = request.FacultyUser.username
    
    courses = models.Course.objects.filter(profs = request.FacultyUser)
    #Tester Code
    #To test w/o login, please comment out the rest of the code above, and test the following
    # faculty = "Saoaposjdsp"

    # x1 = trialcourse('MA105','Spring','2020')
    # x2 = trialcourse('MA106','Autumn','2020')
    # courses = [x1,x2]
    return render(request,'home.html',{'fac':faculty,
                                        'courses':courses})



def addcourse(request):
    if not request.FacultyUser.is_authenticated:
        return redirect('home')
            #To test w/o login, please comment out the rest of the code above, and test the following

    if request.method == "POST":
        form = forms_faculty.PostForm_NewCouse(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('faculty_home')


    else:
        form = forms_faculty.PostForm_NewCouse()
    return render(request, 'addcourse.html', {'form': form})