# views.py
from django.views.generic import ListView
from django.shortcuts import render, redirect
from .models import Word, Guess
from .forms import WordForm, LevelForm
from django.http import HttpRequest, HttpResponse
from random import shuffle
import logging

logger = logging.getLogger(__name__)

class HomeView(ListView):
    model = Word
    template_name = 'index.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Clear guesses from the session when visiting the home screen
        if 'guesses' in request.session:
            del request.session['guesses']
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = LevelForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = LevelForm(request.POST)
        if form.is_valid():
            level = int(form.cleaned_data['level'])
            request.session['level'] = level
            return redirect('/words-list')
        return render(request, self.template_name, {'form': form})

class WordsView(ListView):
    model = Word
    template_name = 'words-list.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Clear guesses from the session when visiting the words list
        if 'guesses' in request.session:
            del request.session['guesses']
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        # Get the selected level from the session
        level = self.request.session.get('level', 1)
        num_words = level + 1
        
        # Get all words from the database
        queryset = list(super().get_queryset())
        # Shuffle the list of words
        shuffle(queryset)
        # Limit the number of words based on the selected level
        queryset = queryset[:num_words]
        
        # Store the shuffled list in the session
        self.request.session['shuffled_words'] = [word.pk for word in queryset]
        logger.debug(f"Shuffled words saved in session: {self.request.session['shuffled_words']}")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve the selected level from the session
        level = self.request.session.get('level', 1)
        context['level'] = level
        return context

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
    # Check if guesses exist in session
    level = request.session.get('level', {})
    words_to_guess = int(level) + 1
    
    return render(request, 'recall.html', {'form': form, 'guesses': guesses, 'words_to_guess': words_to_guess})

def delete_guess(request: HttpRequest) -> HttpResponse:
    # Check if guesses exist in session
    if 'guesses' in request.session and request.session['guesses']:
        # Remove the last guess from the session list
        request.session['guesses'].pop()
        request.session.modified = True  # Mark session as modified to save changes

    return redirect('/recall')

def results(request: HttpRequest) -> HttpResponse:
    # Retrieve the shuffled list of words from the session
    word_ids = request.session.get('shuffled_words', [])
    words = Word.objects.filter(pk__in=word_ids)
    # Ensure the words are in the same order as they were shuffled
    words = sorted(words, key=lambda word: word_ids.index(word.pk))
    # Check if guesses exist in session
    guesses = request.session.get('guesses', {})
    return render(request, 'results.html', {'guesses': guesses, 'words': words})
