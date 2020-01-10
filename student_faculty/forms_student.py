from django import forms
from student_faculty.models import Course,StudentUser,Application

class PostForm_EditDetails(forms.ModelForm):
	
	class Meta:
		model = StudentUser
		fields = ('cpi','year_of_study')
		'''
		cpi=models.FloatField(('CPI'),null=True, blank=True)
		year_of_study=models.PositiveSmallIntegerField(('Year Of Study'),null=True, blank=True,choices=YEAR)
        '''


from django.views.generic.edit import UpdateView

# class PostForm_EditCourse(UpdateView):
#     model = Course
#     fields = ('course_name','course_details','profs','eligibility_criteria','department','deadline','duration','extra_questions','year','semester')

class AddApplication(forms.ModelForm):
	class Meta:
		model = Application
		fields = ['grade','answer1','answer2','answer3','answer4','answer5']

	def __init__(self, *args, **kwargs):
		super(AddApplication, self).__init__(*args, **kwargs)
		if self.instance and (self.instance.course.question5 is None or self.instance.course.question5==""):
			print("cs")
			del self.fields["answer5"]
		if self.instance and (self.instance.course.question4 is None or self.instance.course.question4==""):
			print("cs")
			del self.fields["answer4"]
		if self.instance and (self.instance.course.question3 is None or self.instance.course.question3==""):
			print("cs")
			del self.fields["answer3"]
		if self.instance and (self.instance.course.question2 is None or self.instance.course.question2==""):
			print("cs")
			del self.fields["answer2"]
		if self.instance and (self.instance.course.question1 is None or self.instance.course.question1==""):
			print("cs")
			del self.fields["answer1"]