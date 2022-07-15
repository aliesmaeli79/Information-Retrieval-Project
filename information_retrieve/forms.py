from django import forms
from .models import FileUploadModel


class KeywordSearchForm(forms.Form):
	keyword = forms.CharField(max_length=150, label='', required=False)



class UploadFileForm(forms.ModelForm):
	class Meta:
		model = FileUploadModel
		fields = ('file_upload',)

	def __init__(self, *args, **kwargs):
		super(UploadFileForm, self).__init__(*args, **kwargs)
		self.fields['file_upload'].required = False
