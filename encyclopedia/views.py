from django.shortcuts import render

from . import util
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
import random
class SearchEntryForm(forms.Form):
    form = forms.CharField(label = "Search Entry")

class NewEntry(forms.Form):
    pass

#entry = ["HTML", 'CSS', 'Django', 'Python']
def index(request):
    if "entry" not in request.session:
        request.session['entry'] = ["HTML", 'CSS', 'Django', 'Python']
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form" : SearchEntryForm()
    })

def title(request, title):
    markdowner = Markdown()
    if util.get_entry(title) != None:
        content = markdowner.convert(util.get_entry(title)) 
        return render(request, "encyclopedia/title.html", 
        {
            "content" : content,
            "title" : title
        })
    else:
        return render(request, "encyclopedia/wrong_page.html")

def create_page(request):
    return render(request, "encyclopedia/new_page.html")

def search(request):
    if request.method == "POST":
        form = SearchEntryForm(request.POST)
        if form.is_valid():
            return render(request, "encyclopedia/wrong_page.html")
    elif request.method == 'GET':
        query = request.GET.get('q')
        if util.get_entry(query):
            return HttpResponseRedirect(reverse("encyclopedia:title", kwargs = {"title": query}))
        else:
            list_of_result = [existed_query for existed_query in util.list_entries() if query in existed_query ] 
            return render(request, "encyclopedia/search_result.html", {'list_result': list_of_result})      


def creating(request):
    if request.method == "POST":
        new_entry = NewEntry(request.POST)
        if new_entry.is_valid():
            title = request.POST.get("title")
            content = request.POST.get("content")
            if title in request.session['entry']:
                return render(request, "encyclopedia/query_existed.html")
            else:
                request.session['entry'].append(title)
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("encyclopedia:title", kwargs={"title": title}))
    else:
        return HttpResponse("request method is Get, please type in the textarea again")


def random_list(request):
    entry = random.choice(request.session['entry'])
    return HttpResponseRedirect(reverse("encyclopedia:title", kwargs= {'title': entry}))

def edit(request, title):
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit_page.html", {
        'title': title,
        'content': content
    })

def after_edit(request, title):
    if request.method == "POST":
        new_entry = NewEntry(request.POST)
        if new_entry.is_valid():
            content = request.POST.get("edited_content")
            util.save_entry(title, content)
    return HttpResponseRedirect(reverse("encyclopedia:title", kwargs={"title": title}))

