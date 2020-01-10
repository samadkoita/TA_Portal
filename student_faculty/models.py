from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import date,datetime,timedelta
from student_faculty.choices import *
from uuid import uuid4
from django.contrib.auth.models import User
'''
class MyUser(AbstractUser):
	username = models.CharField(('username'), max_length=30, unique = True)
	email = models.EmailField(('email address'),blank=True)
	first_name =  models.CharField(('First name'),max_length=30,blank = True)
	last_name = models.CharField(('Last name'),max_length=30,blank = True)

	USERNAME_FIELD = 'username'
'''
class StudentUser(models.Model):
# add additional fields in here
    class Meta:
    	db_table="Student Users"


    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50, blank=True)
    user = models.OneToOneField(User, related_name='student_user', on_delete=models.CASCADE, null=True, blank=True)
    ldap_id = models.CharField(max_length=50, null=True, blank=True)
    roll_no=models.CharField(('Roll Number'),max_length=9,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    year_of_study=models.PositiveSmallIntegerField(('Year Of Study'),null=True, blank=True,choices=YEAR)
    contact_no=models.CharField(('Phone'),max_length=12,null=True, blank=True)
    cpi=models.FloatField(('CPI'),null=True, blank=True)
    selected_yet=models.BooleanField(default=False,null=True, blank=True)

    department = models.CharField(max_length=30, null=True, blank=True)
    department_name = models.CharField(max_length=200, null=True, blank=True)
    degree = models.CharField(max_length=200, null=True, blank=True)
    degree_name = models.CharField(max_length=200, null=True, blank=True)
    join_year = models.CharField(max_length=5, null=True, blank=True)
    graduation_year = models.CharField(max_length=5, null=True, blank=True)
    def __str__(self):
    	return self.ldap_id
'''
    def save(self, *args, **kwargs):
    	self.cpi = round(self.cpi, 2)
    	super(StudentUser, self).save(*args, **kwargs)
'''

	
def contact_default():
    return {"firstname": "Web",
            "lastname":"Nominee"}


class FacultyUser(models.Model):
# add additional fields in here


	class Meta:
		db_table="Faculty Users"
	user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, null=True, blank=True)
	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	ldap_id = models.CharField(max_length=50, null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	department = models.CharField(max_length=30, null=True, blank=True)
	department_name = models.CharField(max_length=200, null=True, blank=True)	#contact_no=models.CharField(('Phone'),max_length=12)
	def __str__(self):
		return self.ldap_id

class Course(models.Model):
	#id created by defualt
	class Meta:
		unique_together=(('course_name','year','semester'),)
		db_table="Courses"

	course_name=models.CharField(('Course Name'),max_length=40)
	profs=models.ManyToManyField(FacultyUser)
	course_details=models.CharField(('Course Details'),max_length=1000,blank=True)
	eligibility_criteria=models.CharField(('Eligibility'),max_length=500,blank=True)
	department = models.CharField(max_length=30, null=True, blank=True,choices=DEPT_CHOICES)
	department_name = models.CharField(max_length=200, null=True, blank=True)
	deadline=models.DateField(default=date.today()+timedelta(days=7),blank=False,)
	duration=models.CharField(default='Full Semester',choices=DURATION_CHOICES,max_length=20)
	question1=models.CharField(max_length=500,blank=True,null=True,default=None)
	question2=models.CharField(max_length=500,blank=True,null=True,default=None)
	question3=models.CharField(max_length=500,blank=True,null=True,default=None)
	question4=models.CharField(max_length=500,blank=True,null=True,default=None)
	question5=models.CharField(max_length=500,blank=True,null=True,default=None)
	year=models.IntegerField(blank=False)
	semester=models.PositiveSmallIntegerField(blank=False,choices=SEM_OPTIONS)

class Application(models.Model):
	class Meta:
		unique_together=(('course','student'),)
		db_table="Applications"
	course=models.ForeignKey(Course,on_delete=models.CASCADE)
	student=models.ForeignKey(StudentUser,on_delete=models.CASCADE)
	status=models.CharField(max_length=100,choices=STUDENT_STATUS,default='On Hold')
	grade=models.PositiveSmallIntegerField(('Grade'),choices=GRADE)
	answer1=models.TextField(null=True,blank=True,default=None)
	answer2=models.TextField(null=True,blank=True,default=None)
	answer3=models.TextField(null=True,blank=True,default=None)
	answer4=models.TextField(null=True,blank=True,default=None)
	answer5=models.TextField(null=True,blank=True,default=None)	# to be used only is status is waitlist
	# to be used only is status is waitlist
	waitlist_num=models.IntegerField(('Waitlist Number'),blank=True,null=True)
	created_or_modified=models.DateTimeField(('Last Modified'),auto_now=True)
	def save(self,*args,**kwargs):
		if self.status!="Waitlist":
			self.waitlist_num=None
		super(Application,self).save(*args,**kwargs)


#This will store the 
class StudentFeedback(models.Model):
	course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='student_feedback_course')
	student=models.ForeignKey(StudentUser,on_delete=models.CASCADE,related_name='student_feedback_student')
	#replace field with actual attributes to put
	field1=models.IntegerField(('Field1- Replace with actual parameter'),choices=RATINGS)
	field2=models.IntegerField(('Field2'),choices=RATINGS)
	field3=models.IntegerField(('Field3'),choices=RATINGS)
	comments=models.CharField(('Comments'),max_length=1000)

