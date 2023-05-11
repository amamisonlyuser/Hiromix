from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from .models import Poll, Choice, Vote ,Comment 
from .forms import PollAddForm, EditPollForm, ChoiceAddForm ,CommentForm
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import redis
import json
from django.core.cache import cache
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone
from datetime import datetime
from django.views.decorators.csrf import csrf_protect
import asyncio
from asgiref.sync import sync_to_async
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from polls.models import Comment
from django.utils import timezone
from datetime import datetime
from asgiref.sync import sync_to_async


from channels.generic.websocket import AsyncWebsocketConsumer
import json

from channels.generic.websocket import AsyncWebsocketConsumer
import json

from django.db.models import Count





def polls_list(request):
    all_polls = Poll.objects.all()
    search_term = ''
    if 'name' in request.GET:
        all_polls = all_polls.order_by('text')

    if 'date' in request.GET:
        all_polls = all_polls.order_by('pub_date')

    if 'vote' in request.GET:
        all_polls = all_polls.annotate(Count('vote')).order_by('vote__count')

    if 'search' in request.GET:
        search_term = request.GET['search']
        all_polls = all_polls.filter(text__icontains=search_term)

    paginator = Paginator(all_polls, 100)  # Show 6 contacts per page
    page = request.GET.get('page')
    polls = paginator.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    print(params)
    context = {
        'polls': polls,
        'params': params,
        'search_term': search_term,
    }
    return render(request, 'polls/polls_list.html', context)


@login_required()
def list_by_user(request):
    all_polls = Poll.objects.filter(owner=request.user)
    paginator = Paginator(all_polls, 7)  # Show 7 contacts per page

    page = request.GET.get('page')
    polls = paginator.get_page(page)

    context = {
        'polls': polls,
    }
    return render(request, 'polls/polls_list.html', context)


@login_required()


def polls_add(request):
    if request.method == 'POST':
        form = PollAddForm(request.POST, request.FILES)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.owner = request.user
            poll.save()

            # handle image upload for the poll
            if form.cleaned_data['image']:
                image = form.cleaned_data['image']
                # create the directory to store images if it doesn't exist
                if not os.path.exists(settings.MEDIA_ROOT):
                    os.makedirs(settings.MEDIA_ROOT)
                # save the uploaded image file to the media directory
                with open(os.path.join(settings.MEDIA_ROOT, image.name), 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                # save the image url to the poll object
                poll.image = image.name

            # handle video upload for the poll
            if form.cleaned_data['video']:
                video = form.cleaned_data['video']
                # create the directory to store videos if it doesn't exist
                if not os.path.exists(settings.MEDIA_ROOT):
                    os.makedirs(settings.MEDIA_ROOT)
                # save the uploaded video file to the media directory
                with open(os.path.join(settings.MEDIA_ROOT, video.name), 'wb+') as destination:
                    for chunk in video.chunks():
                        destination.write(chunk)
                # save the video url to the poll object
                poll.video = video.name

            # create choice objects
            choice1 = Choice(poll=poll, choice_text=form.cleaned_data['choice1'])
            choice1.save()

            choice2 = Choice(poll=poll, choice_text=form.cleaned_data['choice2'])
            choice2.save()

            poll.save()

            return redirect('polls:list')
    else:
        form = PollAddForm()
    context = {
        'form': form,
    }
    return render(request, 'polls/add_poll.html', context)


@login_required
def polls_edit(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')

    if request.method == 'POST':
        form = EditPollForm(request.POST, instance=poll)
        if form.is_valid:
            form.save()
            messages.success(request, "Poll Updated successfully.",
                             extra_tags='alert alert-success alert-dismissible fade show')
            return redirect("polls:list")

    else:
        form = EditPollForm(instance=poll)

    return render(request, "polls/poll_edit.html", {'form': form, 'poll': poll})


@login_required
def polls_delete(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    poll.delete()
    messages.success(request, "Poll Deleted successfully.",
                     extra_tags='alert alert-success alert-dismissible fade show')
    return redirect("polls:list")


@login_required
def add_choice(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                request, "Choice added successfully.", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:edit', poll.id)
    else:
        form = ChoiceAddForm()
    context = {
        'form': form,
    }
    return render(request, 'polls/add_choice.html', context)
 

@login_required
def choice_edit(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.owner:
        return redirect('home')

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST, instance=choice)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                request, "Choice Updated successfully.", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:edit', poll.id)
    else:
        form = ChoiceAddForm(instance=choice)
    context = {
        'form': form,
        'edit_choice': True,
        'choice': choice,
    }
    return render(request, 'polls/add_choice.html', context)


@login_required
def choice_delete(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.owner:
        return redirect('home')
    choice.delete()
    messages.success(
        request, "Choice Deleted successfully.", extra_tags='alert alert-success alert-dismissible fade show')
    return redirect('polls:edit', poll.id) 



@login_required
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST.get('choice')
    comments = []
    winners, losers, winner_users, loser_users =Vote.classify_poll_results(poll_id)
    context = {
        'winners': winners,
        'losers': losers,
        'winner_users': winner_users,
        'loser_users': loser_users,
      }    
    if choice_id:
            if not poll.user_can_vote(request.user):
                messages.error(
                    request, "You already voted this poll!", extra_tags='alert alert-warning alert-dismissible fade show'
                )
            else:
                choice = Choice.objects.get(id=choice_id)
                vote = Vote(user=request.user, poll=poll, choice=choice)
                
                vote.save()
                messages.success(request, "Your vote has been recorded!", extra_tags='alert alert-success alert-dismissible fade show')
    if poll:
        comments = Comment.objects.filter(poll=poll)    
    else:
        poll = Poll(pk=poll_id)
        poll.save()
        
    return render(request, 'polls/poll_result.html', {'poll': poll, 'comments': comments , 'context':context} )
        
        


@login_required
def endpoll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return render(request, 'polls/poll_result.html')


    if poll.active is True:
        poll.active = False
        poll.save()
        return render(request, 'polls/poll_result.html', {'poll': poll} )
    else:
        return render(request, 'polls/poll_result.html', {'poll': poll})
    


@login_required
def comments(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    comments = Comment.objects.filter(poll=poll)
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            comment = Comment.objects.create(
                poll=poll,
                user=request.user,
                text=comment_text,
            )
            return redirect('polls:vote', poll_id=poll_id)
    elif request.method == 'DELETE':
        comment_id = request.GET.get('comment_id')
        if comment_id:
            comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
            comment.delete()
            return JsonResponse({'status': 'success'})
    return render(request, 'polls/poll_result.html', {'poll': poll, 'comments': comments})


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:
        comment.delete()
        return redirect('polls:vote', poll_id=comment.poll.id)
    else:
        return render(request, '403.html', status=403)


