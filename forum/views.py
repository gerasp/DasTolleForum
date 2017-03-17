from django.contrib import messages
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from .models import *
from .forms import *

topics_per_page = 7
threads_per_page = 7
messages_per_page = 10

# Create your views here.

def index(request):
    active_users = UserProfile.objects.order_by("no_of_messages").reverse()[0:5]
    last_users = UserProfile.objects.order_by("user__date_joined").reverse()[0:5]
    last_threads = Thread.objects.order_by("date_created").reverse()[0:10]

    return render(request, 'welcome.html', {'active_users':active_users,'last_users':last_users, 'last_threads':last_threads})

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            email = cleaned_data.get('email')
            user_model = User.objects.create_user(username=username, password=password, email=email)
            user_model.groups.add(Group.objects.get(name="NormalUser"))
            user_model.save()
            user_profile = UserProfile(user=user_model)
            user_profile.save()

            messages.success(request, 'Account successfully created. Please try to login')
            return HttpResponseRedirect('/welcome')
    else:
        form = UserForm()
    return render(request, 'form.html', {'form': form,'title': 'Registration page'})

@login_required()
def change_avatar(request):
    if request.method == 'POST':
        form = AvatarChangeForm(request.POST, request.FILES,
                                instance=UserProfile.objects.get(user = request.user))
        if form.is_valid():
            form.save()
            messages.success(request, 'Avatar from ' + request.user.username + ' successfully changed')
            return HttpResponseRedirect('/welcome')
    else:
        form = AvatarChangeForm(instance=UserProfile.objects.get(user = request.user))

    return render(request, 'form.html', {'form': form,'title': 'Change avatar of '+request.user.username})

def show_topics(request):
    # takes all topics and show them
    topics = Topic.objects.all()
    paginator = Paginator(topics, topics_per_page)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        topics = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        topics = paginator.page(paginator.num_pages)
    return render(request, 'topics.html', {'topics': topics})

@login_required()
def add_or_edit_topic(request,pk = None):
    # if the topic exists, edit it, if not create it
    if pk:
        topic = Topic.objects.get(pk=pk)
    else:
        topic = Topic()

    if request.method == 'GET':
        form = TopicForm(instance=topic)
    else:
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            if (pk):
                messages.success(request, 'Topic ' + topic.name + ' updated')
            else:
                messages.success(request, 'Topic ' + topic.name + ' created')
            return HttpResponseRedirect('/topics')
        else:
            messages.error(request, 'Error in form')
            return HttpResponseRedirect('/topics')

    if pk:
        return render(request, 'form.html', {'form': form, 'title': 'Edit topic '+ topic.name})
    else:
        return render(request, 'form.html', {'form': form, 'title': 'Add a new topic to the forum'})

@login_required()
def remove_topic(request, pk):
    topic = Topic.objects.get(pk=pk)
    topic.delete()
    messages.success(request, 'Topic ' + topic.name + ' deleted')
    return HttpResponseRedirect('/topics')

def show_threads(request, pk):
    topic = Topic.objects.get(pk=pk)
    threads = Thread.objects.filter(topic=topic)
    paginator = Paginator(threads, threads_per_page)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        threads = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        threads = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        threads = paginator.page(paginator.num_pages)
    return render(request, 'threads.html', {'threads': threads, 'topic':topic})

@login_required()
def add_or_edit_thread(request,pk, pk2 = None):
    topic = Topic.objects.get(pk=pk)

    if pk2:
        thread = Thread.objects.get(pk=pk2)
    else:
        thread = Thread(topic=topic)

    if request.method == 'GET':
        form = ThreadForm(instance=thread)
    else:
        form = ThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            if (pk2):
                messages.success(request, 'Thread ' + thread.title + ' updated')
            else:
                topic.no_of_threads += 1
                topic.save()
                messages.success(request, 'Thread ' + thread.title + ' created')
            return HttpResponseRedirect('/{}/threads'.format(pk))
        else:
            messages.error(request, 'Error in form')
            return HttpResponseRedirect('/{}/threads'.format(pk))

    if pk2:
        return render(request, 'form.html', {'form': form, 'title': 'Edit thread "'+ thread.title + '"'})
    else:
        return render(request, 'form.html', {'form': form, 'title': 'Add a new thread to the topic "' + topic.name + '"'})

@login_required()
def remove_thread(request, pk, pk2):
    topic = Topic.objects.get(pk=pk)
    thread = Thread.objects.get(pk=pk2)
    thread.delete()
    topic.no_of_threads -= 1
    topic.save()
    messages.success(request, 'Thread ' + thread.title + ' deleted')
    return HttpResponseRedirect('/{}/threads'.format(pk))

@login_required()
def show_messages(request,pk, pk2):
    topic = Topic.objects.get(pk = pk)
    thread = Thread.objects.get(pk = pk2)
    forum_messages = Message.objects.filter(thread=thread)
    user = UserProfile.objects.get(user=request.user)

    if request.method == 'GET':
        form = MessageForm()
    else:
        form = MessageForm(request.POST)
        if form.is_valid():
            message = Message.objects.create(thread=thread, user=user, title=form.cleaned_data['title'], content=form.cleaned_data['content'])
            thread.no_of_messages += 1
            thread.save()
            user.no_of_messages += 1
            user.save()
            messages.success(request, 'Your message ' + message.title + ' was published')
            return HttpResponseRedirect('/{}/{}/messages'.format(pk,pk2))
        else:
            messages.error(request, 'Error in form')
            return HttpResponseRedirect('/{}/{}/messages'.format(pk, pk2))
    return render(request, 'messages.html', {'form': form ,'forum_messages': forum_messages, 'thread': thread, 'topic': topic, 'user_profile':user})

def search(request):

    keywords = request.GET['q'].replace('+',' ')
    results = Thread.objects.filter(title__contains=keywords).order_by('no_of_messages')
    paginator = Paginator(results, threads_per_page)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results = paginator.page(paginator.num_pages)
    return render(request, 'search.html', {'results': results, 'keywords':keywords})
