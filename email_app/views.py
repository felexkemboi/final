from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from . models import User, Message
from . forms import userForm, messageForm

# Function called when the user is expected to sign up
def index(request):
    request.session.flush()
    if request.method == "POST":

        #get the data posted by the user when signs in. Includes  username,firstname
        data = request.POST.copy()

        #check if the password confirmations are the same.If not cancel the whole process and redirect the user to signin again 
        if data['password1'] != data['password2']:
            return render(request, 'index.html', {'errors': 'Both passwords field did not match. Try again!'})
        data['password1'] = make_password(data['password1'])
        data['password2'] = make_password(data['password2'])

        #use the data to fill the form forwaded
        form =userForm(data)

        # check if the form is valid then save the data to the database 
        if form.is_valid():
            form.save(commit=True)
            #create  a session of the loggedin user
            request.session['logged_in'] = {'username': request.POST['username'], 'email': request.POST['email']}
            #redirect the user to the inbox
            return redirect('inbox')
        else:
            #incase there is an error,cancel the process and redirect the user  to signin page
            return render(request, 'index.html', {'errors': form.errors})
    return render(request, 'index.html', {'start': 'start'})


#Function called when the user signs in 
def signin(request):
    #reset the session details
    request.session.flush()
    if request.method == "POST":
        form = User.objects.filter(username=request.POST['username']).exists()
        #go ahead if the user picked exists,then authenticate the user
        if form:
            user = User.objects.filter(username=request.POST['username'])[0]

            if check_password(request.POST['password'], user.password1):
                request.session['logged_in'] = {'username': request.POST['username'], 'email': user.email}
                return redirect('inbox')
        return render(request, 'signin.html', {'errors': 'Invalid username or password'})
    return render(request, 'signin.html', {'start': 'start'})


def inbox(request):
    #check if the user is loggged in else return them to the index
    if 'logged_in' in request.session:
        #get the messages belonging to this user 
        messages = Message.objects.filter(To=request.session['logged_in']['email']).order_by('-id')
        return render(request, 'inbox.html', {'messages':messages})
    else:
        return redirect('index')



#Logout view
def logout(request):
    if 'logged_in' in request.session:
        request.session.flush()
    return redirect('signin')

#View message  function
def message_view(request, id):
    if 'logged_in' in request.session:
        message = Message.objects.get(id=id)

        if request.method == "POST":
            form = messageForm({'To':message.From, 'From':message.To, 'subject':message.subject,
                                'body':request.POST['body']})
            if form.is_valid():
                form.save(commit=True)
                return render(request, 'message_view.html', {'message': message, 'success': 'Reply sent successfully!'})
            else:
                return render(request, 'message_view.html', {'message': message, 'errors': form.errors})

        return render(request, 'message_view.html', {'message': message, 'start':'start'})
    else:
        return redirect('index')


#Message view
def message_view2(request, id):
    if 'logged_in' in request.session:
        message = Message.objects.get(id=id)
        if request.method == "POST":
            form = messageForm({'To':message.To, 'From':message.From, 'subject':message.subject,
                                'body':request.POST['body']})
            if form.is_valid():
                form.save(commit=True)
                return render(request, 'message_view.html', {'message': message, 'success': 'Reply sent successfully!'})
            else:
                return render(request, 'message_view.html', {'message': message, 'errors': form.errors})

        return render(request, 'message_view2.html', {'message': message, 'start':'start'})
    else:
        return redirect('index')

#this method calls the pop up showing when the user sends a message
def sent(request):
    if 'logged_in' in request.session:
        messages = Message.objects.filter(From=request.session['logged_in']['email']).order_by('-id')
        return render(request, 'sent.html',{'messages':messages})
    else:
        return redirect('index')

#function called when creating a new email
def compose(request):
    #only possible to be done by loged in users,else redirected to the login page
    if 'logged_in' in request.session:
        if request.method == "POST":
            form = messageForm(request.POST)

            #form must be valid
            if form.is_valid():
                form.save(commit=True)
                return render(request, 'compose.html', {'message':' Email sent successfully!'})
            else:
                return render(request, 'compose.html', {'errors': form.errors})
        #return the user to create new email incase of errors
        return render(request, 'compose.html', {'start': 'start'})
    else:
        #if not logged in,redirect the user to login afresh 
        return redirect('index')
