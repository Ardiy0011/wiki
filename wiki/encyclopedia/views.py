from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django import forms

from django.urls import reverse
from . import util

import markdown2
from markdown2 import Markdown

import re
import secrets
"""
for random selection
"""

class NewEntrypageform (forms.Form):
    title= forms.CharField(label = "Title", widget=forms.TextInput(attrs={'class': 'form-control col-md-4 col=lg-4'}))
    content= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-11 col-lg-11','rows': 8}))
    edit= forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def indexpage(request):
    if request.method == "POST":
        indexpage = util.get_entrypage()
        if indexpage:
            return render (request, "encyclopedia/indexpage.html", {
                "entries": indexpage
            })
        else:
            return render(request, "encyclopedia/nonexistingpage.html",{
                
            })
    else:
        return render(request, "encyclopedia/indexpage.html",{
            "entries" :util.list_entries()
                
            })
"""
return and render the indexpage and at the same time link it to or give  the list within index.html to the data base in util
"""
def Home(request):
    return render(request, "encyclopedia/indexpage.html", {
        "entries": util.list_entries()
    })
def entrypage(request, entrypage):
    """ this is the entry page/ starting page function"""
    entryPages = util.get_entrypage(entrypage)
    markdowner = Markdown()
    if entryPages is not None:
        return render(request, "encyclopedia/entrypage.html", {
           "entrypage":markdowner.convert(entryPages), 
           "entrypageTitle" : entrypage
       })
    else:
        return render(request, "encyclopedia/nonexistingpage.html", {
           "entrypageTitle": entrypage
               
         
    })

def newEntrypage(request):
    """this is the new entrypage Method"""
    if request.method == "POST":
        form= NewEntrypageform (request.POST)
        if form.is_valid():
           title = form.cleaned_data ["title"]
           content = form.cleaned_data ["content"]
           if(util.get_entrypage(title) is False or form.cleaned_data ["edit"] is True):
                util.save_entrypage(title,content)
                return HttpResponseRedirect(reverse ("entrypage",kwargs={'entrypage': title}))

           else:
                return render(request, "encyclopedia/newEntrypage.html",{
                "form": form,
                "existing": True,
                "entrypage": title
                })

        else:
            return render (request, "encyclopedia/newEntrypage.html",{
            "form": form,
            "existing": False
            })

    else:
        return render(request, "encyclopedia/newEntrypage.html",{
            "form": NewEntrypageform(),
        "existing": False
            })

def editpage(request, entrypage):
    entryPages = util.get_entrypage(entrypage)
    if entryPages is False:
        return render(request, "encyclopedia/nonexistingpage.html",{
            "entrypageTitle": entrypage
         
        })

    else:
        form = NewEntrypageform()
        form.fields["title"].initial = entrypage
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entryPages
        form.fields["edit"].initial= True
        return render(request, "encyclopedia/newEntrypage.html",{

            "form": form,
            "edit": form.fields["edit"].initial,
            "entrypageTitle": form.fields["title"].initial
        })
        
def randompage(request):
    entries = util.list_entries()
    randomentrypage = secrets.choice(entries)
    return HttpResponseRedirect(reverse ("entrypage",kwargs= {'entrypage': randomentrypage}))
    

def usersearch(request):
    searchinput = request.GET.get('q','')
    if(util.get_entrypage(searchinput) is not None):
        return HttpResponseRedirect(reverse("entrypage", kwargs= {'entrypage': searchinput }))

    
    else:
        subStringEntries = []
        for entrypage in util.list_entries():
            if searchinput.upper() in entrypage.upper(): 
                    subStringEntries.append(entrypage)
        return render(request, "encyclopedia/indexpage.html" ,{
        "entries": subStringEntries,
        "usersearch": True,
        "searchinput": searchinput

        })
