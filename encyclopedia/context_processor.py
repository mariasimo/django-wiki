from .views import SearchForm
from . import util
from random import randint

def search_form(request):
    entries = util.list_entries()
    return {
        'form': SearchForm,
        'random': entries[randint(0, len(entries) - 1)]
    }
