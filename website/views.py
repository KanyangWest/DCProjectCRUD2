from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record, Note


def home(request):
	records = Record.objects.all()

	#Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		#Authenticate
		user = authenticate(request, username = username, password = password)
		if user is not None:
			login(request, user)
			messages.success(request,"You have been logged in!")
			return redirect('home')
		else:
			messages.success(request, "There was an error logging in, please try again")
			return redirect('home')
	return render(request, 'home.html', {'records': records})


def logout_user(request):
	logout(request)
	messages.success(request, "You successfully logged out.")
	return redirect('home')


def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, "You have successfully registered!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look up records
        customer_record = Record.objects.get(id=pk)
        notes = Note.objects.filter(record=customer_record)
        return render(request, 'record.html', {'customer_record': customer_record, 'notes': notes})
    else:
        messages.success(request, "You must be logged in to view the page!")
        return redirect('home')



def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = Record.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record deleted successfully")
		return redirect('home')
	else:
		messages.success(request, "You must logged in to delete it.")
		return redirect('home')


def add_record(request):
    if request.user.is_authenticated:
        form = AddRecordForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                record = form.save(commit=False)
                record.user = request.user
                record.save()
                messages.success(request, "Record Added")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.error(request, "You must be logged in")
        return redirect('home')


def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance = current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record has updated")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
			messages.success(request, "You must be logged in")
			return redirect('home')


def create_note(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            record = Record.objects.get(id=pk)
            note = Note.objects.create(record=record, title=title, content=content)
            messages.success(request, 'Note added successfully.')
            return redirect('record', pk=pk)  # Redirect to create_note view for the same record
        
        customer_record = Record.objects.get(id=pk)
        notes = Note.objects.filter(record=customer_record)
        return render(request, 'create_note.html', {'customer_record': customer_record, 'notes': notes})
    
    else:
        messages.error(request, 'You must be logged in to add a note.')
        return redirect('home')



def update_note(request, note_id):
    if request.user.is_authenticated:
        note = Note.objects.get(id=note_id)
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            record_id = note.record.id
            note.title = title
            note.content = content
            note.save()
            messages.success(request, 'Note updated successfully.')
            return redirect('record', pk=record_id)
        return render(request, 'update_note.html', {'note': note})
    else:
        messages.error(request, 'You must be logged in to update a note.')
        return redirect('home')


def delete_note(request, note_id):
    if request.user.is_authenticated:
        note = Note.objects.get(id=note_id)
        record_id = note.record.id
        note.delete()
        messages.success(request, 'Note deleted successfully.')
        return redirect('record', pk=record_id)
    else:
        messages.error(request, 'You must be logged in to delete a note.')
        return redirect('home')