from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(response, id):
    ls = ToDoList.objects.get(id=id)
    
    if(response.method == "POST"):
        if(response.POST.get("save")):
            for item in ls.item_set.all():
                if(response.POST.get("d" + str(item.id))):                 ## Update name change
                    item.text = response.POST.get("d" + str(item.id))
                    
                if(response.POST.get("e" + str(item.id)) == "Completed"):  ## Update complete status
                    item.complete = True
                else:
                    item.complete = False
                item.save()
        elif(response.POST.get("newItem")):
            txt = response.POST.get("new")
            if(len(txt) > 2):
                ls.item_set.create(text=txt, complete=False)
            
        elif(response.POST.get("delete")):                                 ## Delete items
            for item in ls.item_set.all():
                if(response.POST.get("c" + str(item.id)) == "clicked"):
                    item.delete()
    
    return render(response, "main/list.html", {"ls": ls})

def home(response):
    return render(response, "main/home.html")

@login_required
def create(request):
    if(request.method == "POST"):
        form = CreateNewList(request.POST)
        
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n, user=request.user)
            t.save()
        return HttpResponseRedirect(f"/{t.id}")
    else:
        form = CreateNewList()
    return render(request, "main/create.html", {"form": form})

@login_required
def view(request):
    todolist = ToDoList.objects.all().filter(user=request.user)
    return render(request, "main/view.html", {"todolist": todolist})