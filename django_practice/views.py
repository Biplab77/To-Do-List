from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from django.utils import timezone

#Local Imports
from .models import ToDoItem, ToDoEvent
from .forms import LoginForm, AddTaskForm, UpdateTaskForm, AddEventForm

def index(request):
	todoitem_list = ToDoItem.objects.filter(user_id=request.user.id)
	todoevent_list = ToDoEvent.objects.filter(user_id=request.user.id)
	context = { 
		'todoitem_list': todoitem_list,
        'todoevent_list': todoevent_list,
		'user': request.user
	}
	return render(request, "todolist/index.html", context)


def todoitem(request, todoitem_id):
	todoitem = get_object_or_404(ToDoItem, pk=todoitem_id)
	return render(request, "todolist/todoitem.html", model_to_dict(todoitem))

def todoevent(request, todoevent_id):
    todoevent = get_object_or_404(ToDoEvent, pk=todoevent_id)
    return render(request, "todolist/todoevent.html", model_to_dict(todoevent))

def register(request):

	users = User.objects.all()
	is_user_registered = False
	context = {
		"is_user_registered": is_user_registered
	}
	for indiv_user in users:
		if indiv_user.username == "johndoe":
			is_user_registered = True
			break

	if is_user_registered == False:
		user = User()
		user.username = "johndoe"
		user.first_name = "John"
		user.last_name = "Doe"
		user.email = "john@mail.com"
		user.set_password("john1234")
		user.is_staff = False
		user.is_active = True

		user.save()

		context = {
			"first_name": user.first_name,
			"last_name": user.last_name
		}
	return render(request, "todolist/register.html", context)

def change_password(request):

	is_user_authenticated = False

	user = authenticate(username="johndoe", password="john1234")
	print(user)

	if user is not None:
		authenticated_user  = User.objects.get(username="johndoe")
		authenticated_user.set_password("johndoe1")
		authenticated_user.save()
		is_user_authenticated = True
	context ={
		"is_user_authenticated": is_user_authenticated
	}
	return render(request, "todolist/change_password.html", context)

def login_view(request):
		context = {}

		if request.method == 'POST':
				form = LoginForm(request.POST)

				if form.is_valid() == False:
					form = LoginForm()
				else:
					username = form.cleaned_data['username']
					password = form.cleaned_data['password']
					user = authenticate(username=username, password=password)
					context={
						"username" : username,
						"password" : password
					}

					if user is not None:
							login(request, user)
							return redirect("todolist:index")
					else:
						context = {
							"error" : True
						}

		return render(request, "todolist/login.html", context)

def logout_view(request):
	logout(request)
	return redirect("todolist:index")

def add_task(request):

    context = {}

    if request.method == 'POST':

        form = AddTaskForm(request.POST)

        if form.is_valid() == False:

            form = AddTaskForm()

        else:

            task_name = form.cleaned_data['task_name']
            description = form.cleaned_data['description']

            # Checks the database if a task already exists
            # By default the "filter" method searches for records that are case insensitive
            duplicates = ToDoItem.objects.filter(task_name=task_name)

            # if todoitem does not contain any duplicates
            if not duplicates:

                # Creates an object based on the "ToDoItem" model and saves the record in the database
                ToDoItem.objects.create(task_name=task_name, description=description, date_created=timezone.now(), user_id=request.user.id)
                return redirect("todolist:index")

            else:

                context = {
                    "error": True
                }

    return render(request, "todolist/add_task.html", context) 

def update_task(request, todoitem_id):

    # Returns a queryset
    todoitem = ToDoItem.objects.filter(pk=todoitem_id)

    context = {
        "user": request.user,
        "todoitem_id": todoitem_id,
        # Accessing the first element is necessary because the "ToDoItem.objects.filter()" method returns a queryset
        "task_name": todoitem[0].task_name,
        "description": todoitem[0].description,
        "status": todoitem[0].status
    }

    if request.method == 'POST':

        form = UpdateTaskForm(request.POST)

        if form.is_valid() == False:

            form = UpdateTaskForm()

        else:

            task_name = form.cleaned_data['task_name']
            description = form.cleaned_data['description']
            status = form.cleaned_data['status']

            if todoitem:

                todoitem[0].task_name = task_name
                todoitem[0].description = description
                todoitem[0].status = status

                todoitem[0].save()
                return redirect("todolist:index")

            else:

                context = {
                    "error": True
                }

    return render(request, "todolist/update_task.html", context)

def delete_task(request, todoitem_id):

    todoitem = ToDoItem.objects.filter(pk=todoitem_id).delete()
    return redirect("todolist:index")

def add_event(request):

    context = {}

    if request.method == 'POST':
        
        form = AddEventForm(request.POST)

        if form.is_valid() == False:

            form = AddEventForm()

        else:

            event_name = form.cleaned_data['event_name']
            description = form.cleaned_data['description']
            print(event_name, description)

            duplicates = ToDoEvent.objects.filter(event_name=event_name)

            if not duplicates:

                ToDoEvent.objects.create(event_name=event_name, description=description, event_date=timezone.now(), user_id=request.user.id)
                return redirect("todolist:index")

            else:

                context = {
                    "error": True
                }

    return render(request, "todolist/add_event.html", context)

