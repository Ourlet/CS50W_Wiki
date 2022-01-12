from re import template
from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
import random as random_module

markdowner=Markdown()

from . import util

def convert_to_HTLM(title):
    entry = util.get_entry(title)
    html = markdowner.convert(entry) if entry else None
    return html

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entryPage = util.get_entry(title)
    if entryPage == None:
        return render(request, 'encyclopedia/notFound.html', {
            "entry" : title
            })
    else:
        return render(request, 'encyclopedia/entryPage.html', {
        "entryTitle" : title,
        "page" : convert_to_HTLM(title)
        })

def search(request):
    if request.method == "GET":
        input = request.GET.get('searched')
        page = convert_to_HTLM(input)
        entries = util.list_entries()
        search_pages = []
        entry = util.get_entry(input)

        if entry:
            return render(request, 'encyclopedia/entryPage.html', {
                    "entryTitle" : input,
                    "page" : page
                    })
        
        for entry in entries:
            if input.upper() in entry.upper():
                search_pages.append(entry)

            if search_pages != []:
                return render(request, 'encyclopedia/results.html',{
                    "entries": search_pages,
                    "searched": input
                })

        else:
            return render(request, "encyclopedia/notFound.html",{
                "entry": input
                })
        
def create(request):
    return render(request, "encyclopedia/create.html", {})

def save(request):
    if request.method == "POST":
        entries = util.list_entries()
        title = request.POST.get('title')
        content = request.POST.get('content')
        existingEntry = False

        for entry in entries:
            if title.upper() == entry.upper():
                existingEntry = True
        
        if existingEntry:
            return render(request, "encyclopedia/existingEntry.html", {
                "entry": title
            })

        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('entry-page', kwargs={
                "title": title
            }))

def edit(request):
    if request.method == "POST":
        input_title = request.POST.get('title')
        input_content = util.get_entry(input_title)
    
        return render(request, "encyclopedia/edit.html", {
            "content": input_content,
            "title": input_title,
        })

def saveEdit(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title, content)
            
        page = convert_to_HTLM(title)
        
        return render(request, "encyclopedia/entryPage.html", {
            "entryTitle": title,
            "page": page
            })

def random(request):
    entries = util.list_entries()
    randomPage = random_module.choice(entries)
    page = convert_to_HTLM(randomPage)

    return render(request, "encyclopedia/entryPage.html", {
        "entryTitle": randomPage,
        "page": page
    })
