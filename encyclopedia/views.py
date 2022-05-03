from django.shortcuts import render, redirect
from django import forms

from . import util

class SearchForm(forms.Form):
    q=forms.CharField(max_length=100,label="Search encyclopedia")

class NewEntryForm(forms.Form):
    title=forms.CharField(max_length=144,label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':15}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content=util.get_entry(title)

    if content is not None:
        return render(request, "encyclopedia/entry.html", {
            "content": util.markdown_to_html(content),
            "title": title
        })

    return render(request, "encyclopedia/error.html")
     

def search(request):
    entries = util.list_entries()

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data['q'].upper()
            upper_entries = [entry.upper() for entry in entries]

            if query in upper_entries:
                return redirect('entry', title=query)
            else: 
                filtered_entries = [entry for entry in entries if query.upper() in entry.upper()]

                return render(request, "encyclopedia/results.html", {
                    'title': f"Search Results ({len(filtered_entries)})",
                    'form': form,
                    'entries': filtered_entries
                })

    return render(request, "encyclopedia/results.html", {
        'entries': entries,
        'title': 'All Entries'
    })
        

def new(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)

        if form.is_valid():
            # list unpacking
            title, content = form.cleaned_data.values()
            upper_entries = [entry.upper() for entry in util.list_entries()]

            if title.upper() in upper_entries:
                return render(request, 'encyclopedia/new.html', {
                    'newEntryForm': form,
                    'errorMessage': "An entry with this title already exists"
                })
            else:
                util.save_entry(title, content)
                return redirect('index')

    return render(request, 'encyclopedia/new.html', {
        'newEntryForm': NewEntryForm
    })


def edit(request, title):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)

        if form.is_valid():
            title, content = form.cleaned_data.values()
            util.save_entry(title, content)
            return redirect('entry', title)

    entry=util.get_entry(title)
    form = NewEntryForm({'title': title, 'content': entry})

    return render(request, 'encyclopedia/new.html', {
        'title': f"Edit {title}",
        'newEntryForm': form,
        'editMode': True
    })