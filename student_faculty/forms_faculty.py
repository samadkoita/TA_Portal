from django import forms

from student_faculty.models import Course,FacultyUser,Application

class PostForm_NewCouse(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('course_name','course_details','profs','eligibility_criteria','department','deadline','duration','extra_questions','year','semester')
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


from django.views.generic.edit import UpdateView

class PostForm_EditCourse(UpdateView):
    model = Course
    fields = ('course_name','course_details','profs','eligibility_criteria','department','deadline','duration','extra_questions','year','semester')
