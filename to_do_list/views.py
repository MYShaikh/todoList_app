from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from to_do_list.models import CustomUser, Profile, ListNDesc
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.

class SignUpView(View):
    def get(self,request):
        try:
            print("I am in signup view try")
            messages.success(request,"I am signing up")
            return render(request,"signup.html")
        except Exception as exeptionerror:
            print(exeptionerror, 'error')
            print("I am in signup view except")
            return render(request,"error.html")
        
    def post(self,request):
        try:
            name = request.POST.get('username')
            user_email = request.POST.get('email')
            user_password = request.POST.get('password')
            obj = CustomUser(email = user_email, name = name)
            obj.set_password(user_password)
            obj.save()
            
            context = {'email':obj.email, 'password':obj.password}
            messages.success(request,"sign up successful")
            return redirect('loginview')
        except Exception as exeptionerror:
            print(exeptionerror)
            return render(request,"error.html")
        
class LoginView(View):
    def get(self,request):
        try:
            messages.warning(request,"sucessful, login page open")
            return render(request, "login.html")
        except Exception as exeptionerror:
            print(exeptionerror)
            return render(request, "error.html")
    def post(self,request):
        try:
            user_email = request.POST.get('email')
            user_password = request.POST.get('password')
            if not user_email and not user_password:
                return(request,"error.html")
            if CustomUser.objects.filter(email = user_email).exists():
                print("user name is ",user_email)
                user = authenticate(request, email = user_email, password = user_password)
                print("username is ",user)
                login(request,user)
                if user is not None:
                    print(user.id)
                    # if Profile.objects.filter(user = user).first():
                    #     return redirect("dashboard")
                    return redirect("dashboard")
                else:
                    print("You are not registered, sign up!")
                    messages.error(request, "User Email/Passoword is incorrect, please try again!")
                    return render(request,"signup.html")
            else:
                print("You are not registered, try signing up!")
                return render(request, "signup.html")
        except Exception as exeptionerror:
            print(exeptionerror)
            return render(request,"error.html")
        
class DashboardView(View):
    def get(self, request):
        try:
            messages.success(request, "You are in login!")
            return render(request, "dashboard.html")
        except:
            messages.error(request, "Something went wrong, please try again!")
            return render(request, "loginview")

class TodoView(View):
    def get(self, request):
        try:
            messages.success(request, "Welcome to to-do")
            return render(request, "addtodo.html")
        except:
            messages.error(request, "Something went wrong, please try again!")
            return render(request, "loginview")
    def post(self, request):
        try:
            print(request.user)
            title = request.POST.get("title")
            desc = request.POST.get("desc")
            is_completed = request.POST.get("done", False)
            print(" This is the is_completed ", is_completed)
            obj = ListNDesc(user = request.user, title = title, desc = desc, is_completed = is_completed)
            obj.save()
            context = {"title":obj.title, "desc":obj.desc, "is_completed":obj.is_completed}
            print("list has been saved")
            #return render(request,"success.html",{"obj":obj})
            return redirect("todolist")
        except Exception as exeptionerror:
            print(exeptionerror)
            return render(request,"error.html")
        
class TodolistView(View):
    def get(self,request):
        user = request.user
        obj = ListNDesc.objects.filter(user = user)
        # print("This is it ",{"obj": ListNDesc.objects.filter(user=user)})
        return render(request, "todolist.html", {"obj":obj})
    
    def post(self, request):
        print("we are in todolistview post")
        try:
            user = request.user
        # Handling form submission for the "View" button

            task_id = request.POST.get('task_id')
            is_completed = request.POST.get('is_completed')# Get the task id from the button
            print(task_id)
            print(type(task_id))
            task = get_object_or_404(ListNDesc, id=task_id, user=user)
            print(task)
            if is_completed == 'on':
                task.is_completed = True
            else:
                task.is_completed = False
            task.save()
            return redirect("taskdisplays",task_id)
            
        except Exception as exeptionerror:
            print(exeptionerror)
            return render(request,"error.html")

        
        # Other actions like Edit or Delete can be handled similarly
        #return render(request, "todolist.html", {"obj": ListNDesc.objects.filter(user=user)})
    
    
class TaskView(View):
    def get(self,request,task_id):
        print("we are in taskview get")
        try:
            user = request.user
            #obj = ListNDesc.objects.filter(user = user)
            task = get_object_or_404(ListNDesc, id=task_id, user=user)
            #print("this is task",task)
            dataa = ListNDesc.objects.get(id = task_id)
            print(dataa.title)
            print(dataa.desc)
            #print("task id is ",task_id)
            return render(request, "taskview.html", {"task_id": task, "dataa": dataa})

        except Exception as exeptionerror:
            print(exeptionerror)
            return render(request,"error.html")
        
    def post(self, request):
        print("In the taskview post")
        try:
            user = request.user
            print("In the taskview post")
            if "view_task" in request.POST:
                task_id = request.POST.get('task_id')  # Get the task id from the button
                task = get_object_or_404(ListNDesc, id=task_id, user=user)
                return render(request, "taskview.html", {"task_id":task})
        except Exception as exeptionerror:
            print(exeptionerror)
            return render(request,"error.html")
        
class DeleteTaskView(View):
    def post(self, request, task_id):
        # Get the task object or return 404 if not found
        task = get_object_or_404(ListNDesc, id=task_id, user=request.user)

        # Delete the task
        task.delete()

        # Redirect to the page displaying the tasks (or wherever you'd like)
        return redirect('todolist')
    
class EditTaskView(View):
    def get(self,request,task_id):
        print("We are in ++++++++++++++++++++++++++++++++++++++++++++++++++")
        user = request.user
        # task_id = request.post.get("view_task")
        task = get_object_or_404(ListNDesc, id=task_id, user=user)
        # print("This is it ",{"obj": ListNDesc.objects.filter(user=user)})
        return render(request, "taskedit.html", {"task":task})
    
    def post(self,request, task_id):
        print("we are in todolistview post")
        try:
            print("11111111111111111111")
            user = request.user
        # Handling form submission for the "View" button
            # Get the task id from the button
            print(task_id)
            print(type(task_id))
            task = get_object_or_404(ListNDesc, id=task_id, user=user)
            task.title = request.POST.get('title')
            task.desc = request.POST.get('desc')
            print("77777777777777777777777777777777777777777777777")
            task.save()
            print("88888888888888888888888888888888888")
            print(task)
            return redirect("taskdisplays",task_id)
            
        except Exception as exeptionerror:
            print(exeptionerror)
            return render(request,"error.html")
        
class CompletelistView(View):
    def get(self,request):
        user = request.user
        obj = ListNDesc.objects.filter(user = user)
        # print("This is it ",{"obj": ListNDesc.objects.filter(user=user)})
        return render(request, "completelist.html", {"obj":obj})
    
from django.shortcuts import render
from django.views import View

class ProfileView(View):
    def get(self, request):
        user = request.user
        
        total_tasks = ListNDesc.objects.filter(user=user).count()
        completed_tasks = ListNDesc.objects.filter(user=user, is_completed=True).count()
        due_tasks = ListNDesc.objects.filter(user=user, is_completed=False).count()
        
        context = {
            "user": user,
            "name": user.name,
            "email": user.email,
            "mobile": user.mobile,
            "address": user.address,
            "dob": user.dob,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "due_tasks": due_tasks,
        }
        return render(request, "profile.html", context)
    
    def post(self,request):
        try:
            user = request.user
            profile_image = request.POST.get('profile_img')
        except Exception as exeptionerror:
            print(exeptionerror)
            return render(request,"error.html")
    
