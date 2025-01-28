from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=20)
	password = forms.CharField(label='Password', max_length=20)

class AddTaskForm(forms.Form):
	task_name = forms.CharField(label='Task Name', max_length=50)
	description = forms.CharField(label='Description', max_length=200)

class UpdateTaskForm(forms.Form):
    # If fields are optional, using the "Model.save()" method will not work
    # Using the option "required=False" will allow the field to be optional when updating a record
    # task_name = forms.CharField(label='Task Name', max_length=50, required=False)
    task_name = forms.CharField(label='Task Name', max_length=50)
    description = forms.CharField(label='Description', max_length=200)
    status = forms.CharField(label='Status', max_length=50)

class AddEventForm(forms.Form):
    event_name = forms.CharField(label='Event Name', max_length=50)
    description = forms.CharField(label='Description', max_length=200)

class UpdateEventForm(forms.Form):
    event_name = forms.CharField(label='Event Name', max_length=50)
    description = forms.CharField(label='Description', max_length=200)
    status = forms.CharField(label='Status', max_length=50)