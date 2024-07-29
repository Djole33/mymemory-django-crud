from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from .models import Word, Guess
from .forms import WordForm
from django.http import HttpRequest, HttpResponse

# Create your views here.

class HomeView(ListView):
    model = Word
    template_name = 'index.html'
    def dispatch(self, request, *args, **kwargs):
        # Clear guesses from the session when visiting the home screen
        if 'guesses' in request.session:
            del request.session['guesses']
        return super().dispatch(request, *args, **kwargs)

class WordsView(ListView):
    model = Word
    template_name = 'words-list.html'
    def dispatch(self, request, *args, **kwargs):
        # Clear guesses from the session when visiting the words list
        if 'guesses' in request.session:
            del request.session['guesses']
        return super().dispatch(request, *args, **kwargs)

def guess_view(request: HttpRequest) -> HttpResponse:
    # Use session to store guesses across requests
    if 'guesses' not in request.session:
        request.session['guesses'] = []

    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            # Append the valid guess to the session list
            guess = form.cleaned_data['guess']
            request.session['guesses'].append(guess)
            request.session.modified = True  # Mark session as modified to save changes
            return redirect('/recall')
    else:
        form = WordForm()

    # Retrieve guesses from session
    guesses = request.session['guesses']
    
    return render(request, 'recall.html', {'form': form, 'guesses': guesses})

def delete_guess(request: HttpRequest) -> HttpResponse:
    # Check if guesses exist in session
    if 'guesses' in request.session and request.session['guesses']:
        # Remove the last guess from the session list
        request.session['guesses'].pop()
        request.session.modified = True  # Mark session as modified to save changes

    return redirect('/recall')

def results(request: HttpRequest) -> HttpResponse:
    words = Word.objects.all()
    # Check if guesses exist in session
    guesses = request.session['guesses']
    return render(request, 'results.html', {'guesses': guesses, 'words': words})
