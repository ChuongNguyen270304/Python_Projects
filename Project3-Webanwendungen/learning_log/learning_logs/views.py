from django.shortcuts import render

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    """The home page of Learning Log."""
    return render(request, 'learning_logs/index.html')
@login_required
def topics(request):
    """Show all topics."""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)
def topic(request, topic_id):
    """Show a single topic and all its entries"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # Keine Daten übermittelt; es wird ein leeres Formular erstellt.
        form = TopicForm()
    else:
        # Daten übermittelt; Daten werden verarbeitet.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')
    # Zeigt ein leeres oder ein als ungültig erkanntes Formular an.
    context = {'form' : form}
    return render(request, 'learning_logs/new_topic.html', context)
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # Keine Daten übermittelt; es wird ein leeres Formular erstellt.
        form = EntryForm()
    else:
        # Daten übermittelt; Daten werden verarbeitet.
        form= EntryForm(data=request.POST)
        if form.is_valid():
            new_entry= form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    # Zeigt ein leeres oder ein als ungültig erkanntes Formular an.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # Ursprüngliche Anforderung; das mit dem jetztigen Eintrag vorab 
        # ausgefüllte Formular wird erstellt.
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
