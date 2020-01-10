from django import forms

from student_faculty.models import Course,FacultyUser,Application

class PostForm_NewCouse(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('course_name','course_details','eligibility_criteria','department','deadline','duration','question1','question2','question3','question4','question5','year','semester')
        '''
        course_name=models.CharField(('Course Name'),max_length=40)
	    profs=models.ManyToManyField(FacultyUser)
	    course_details=models.CharField(('Course Details'),max_length=1000,blank=True)
	    eligibility_criteria=models.CharField(('Eligibility'),max_length=500,blank=True)
	    department=models.CharField(('Department'),max_length=50,choices=DEPT_CHOICES)
	    deadline=models.DateField(default=date.today()+timedelta(days=7),blank=False,)
	    duration=models.CharField(default='Full Semester',choices=DURATION_CHOICES,max_length=10)
	    extra_questions=models.CharField(max_length=1500)
	    year=models.IntegerField(blank=False)
	    semester=models.PositiveSmallIntegerField(blank=False,choices=SEM_OPTIONS)
        '''


class Application(forms.ModelForm):

    class Meta:
        model = Application
        fields = ['status','waitlist_num']


class AddProf(forms.Form):
    ldap_id = forms.CharField(label='LDAP ID', max_length=100,required = True)
        



