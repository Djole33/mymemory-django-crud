from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'index.html')

def words_list(request):
    words = ['egg', 'pear', 'car', 'apple', 'house']
    return render(request, 'words-list.html', {'words': words})

def recall(request):
    return render(request, 'recall.html')
