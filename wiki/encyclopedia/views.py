from django import forms
from django.shortcuts import render
from django.utils.safestring import mark_safe
from . import util
import urllib.request
import requests
import random

class NewSearch(forms.Form):
    se = forms.CharField(label="Search:")
class NewPage(forms.Form):
    title = forms.CharField(label="Page Title:")
    content = forms.CharField(widget=forms.Textarea,label="Content:")
    # (attrs={'rows':10, 'cols':10})
def index(request):
    entries = util.list_entries()
    y = False
    x = []
    if request.method == "POST":
        form = NewSearch(request.POST)
        if form.is_valid():
            result = form.cleaned_data["se"]
        if result.lower() in (names.lower() for names in entries):
            return render(request, "encyclopedia/entries.html", {
                "entry":util.get_entry(result)
                })
        else:
            for entry in entries:
                if result.lower() in entry.lower():
                    x.append(entry)
                    y = True
            if y==False:
                x = []
            return render(request, "encyclopedia/search.html",{
                "entries": x,
                "len": len(x)
                })
    else:
        return render(request, "encyclopedia/index.html",{
            "entries": util.list_entries()
            })
def entries(request,name):
    entry = util.get_entry(name)
    if name == "random":
        if len(util.list_entries()) == 0:
            Random = "Sorry"
            entry = ""
            error = "#No Entries\n[Create a new page](/wiki/new) to visit a random page."
        else:
            Random = random.choice(util.list_entries())
            entry = util.get_entry(Random) 
            error = ""
        return render(request,"encyclopedia/entries.html",{
            "name": Random,
            "entry": entry,
            "error": error   
            })
        print (util.get_entry(Random))
    elif name != "new":
        if entry == None:
            entry = "#Sorry \n *The requested URL doesn't exist! Please, check your spelling.*"
        return render(request,"encyclopedia/entries.html",{
            "name": name,
            "entry": entry
            })
    else: 
        if request.method == "POST":
            form = NewPage(request.POST)
            if form.is_valid():
                title = form.cleaned_data["title"]
                content = form.cleaned_data["content"]
            else:
                return render (request,"encyclopedia/new.html",{
                    "new":form,
                    "editmode":False,
                    "name":"new"
                    })
            if title not in util.list_entries():
                util.save_entry(title,content)
                return render (request, "encyclopedia/entries.html",{
                "name":title,
                "entry":util.get_entry(title)
                })
            else:
                return render (request,"encyclopedia/new.html",{
                    "new":form,
                    "error": "You are redirected here because the title already exists.",
                    "editmode":False
                    })
        else:
            return render (request, "encyclopedia/new.html",{
                "new": NewPage()
                })
def edit(request,name,mode):
    entry = util.get_entry(name)
    error = ""
    if name.lower() not in (names.lower() for names in util.list_entries()):
                entry = ""
                error = "#"+name+"\n Sorry the entry name: " + "**"+name+"** does not exist.\n\n Should you want to create it, click [here](/wiki/new)."
    if entry == None or not (mode == "edited" or mode == "edit"):
            entry = ""  
            error =  "#Sorry \n *The requested URL doesn't exist! Please, check your spelling.*"
    if mode == "edit":
        if request.method == "POST":
            # if request.form["submited"] == "Edit":
            if 'Edit' in request.POST:
                return render(request,"encyclopedia/new.html",{
                    "new": NewPage(initial = {'title':name,'content':entry}),
                    "editmode":True,
                    "name":name,
                    "mode":"edited",

                    })
            else:
                util.delete(name)
                return render(request,"encyclopedia/index.html",{
                    "entries":util.list_entries
                    })
        else:
            return render (request, "encyclopedia/entries.html",{
                "name":name,
                "entry":entry,
                "error":error
                })
    elif mode == "edited":
        if request.method == "POST":
            form = NewPage(request.POST)
            if form.is_valid():
                title = form.cleaned_data["title"]
                content = form.cleaned_data["content"]
            else:
                return render (request,"encyclopedia/new.html",{
                    "new":form,
                    "editmode":True,
                    "name":name,
                    "mode":mode
                    })
            util.save_entry(title,content)
            return render (request, "encyclopedia/entries.html",{
                "name":title,
                "entry":util.get_entry(title),
                "error":error
                })
        else:
            return render (request, "encyclopedia/entries.html",{
                "name":name,
                "entry":entry,
                "error":error
                })
    else:
        return render(request,"encyclopedia/entries.html",{
            "name": name,
            "entry": entry,
            "error":error
            })