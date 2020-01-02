from django import forms
from student_faculty.models import Course,StudentUser,Application

class PostForm_EditDetails(forms.ModelForm):
	
	class Meta:
		model = StudentUser
		fields = ('cpi','year_of_study')
		'''
		cpi=models.FloatField(('CPI'),null=True, blank=True)
		year_of_study=models.CharField(('Year Of Study'),max_length=1,null=True, blank=True)
        '''


from django.views.generic.edit import UpdateView

# class PostForm_EditCourse(UpdateView):
#     model = Course
#     fields = ('course_name','course_details','profs','eligibility_criteria','department','deadline','duration','extra_questions','year','semester')

class AddApplication(forms.ModelForm):

    class Meta:
        model = Application
        fields = ['grade','answers_to_questions']