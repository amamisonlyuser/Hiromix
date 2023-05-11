from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from polls.models import Poll, Choice, Vote ,Comment 
from polls.forms import PollAddForm, EditPollForm, ChoiceAddForm ,CommentForm
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




def home(request):
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