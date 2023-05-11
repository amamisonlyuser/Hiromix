from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import secrets
from django.urls import reverse
from django import forms
from django.conf import settings
from django.db import migrations
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count


class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='poll_images', blank=True, null=True)
    video = models.FileField(upload_to='poll_videos', blank=True, null=True)
    
    def user_can_vote(self, user):
        """ 
        Return False if user already voted
        """
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def get_result_dict(self):
        res = []
        for choice in self.choice_set.all():
            d = {}
            d['text'] = choice.choice_text
            d['num_votes'] = choice.get_vote_count()
          

            if not self.get_vote_count:
                d['percentage'] = 0
            else:
                d['percentage'] = (choice.get_vote_count() / self.get_vote_count)*100


           
            
            res.append(d)
        return res
   

    def __str__(self):
        return self.text
 
  
class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    

    def __str__(self):
        return self.choice_text

    def get_vote_count(self):
     return self.vote_set.count()
    
    


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    

    def __str__(self):
        return f'{self.poll.text[:15]} - {self.choice.choice_text[:15]} - {self.user.username}'
    
    
    def classify_poll_results(poll_id):
        # Get all votes for the given poll, and annotate each choice with the number of votes
        votes = Vote.objects.filter(poll_id=poll_id).select_related('user', 'choice')
        choices = Choice.objects.filter(poll_id=poll_id).annotate(num_votes=Count('vote')).order_by('-num_votes')

        # Get the choices with the most votes (winners) and the rest (losers)
        max_votes = choices.first().num_votes
        winners = [choice for choice in choices if choice.num_votes == max_votes]
        losers = [choice for choice in choices if choice not in winners]

        # Get the users who voted for each choice
        winner_users = [vote.user.username for vote in votes if vote.choice in winners]
        loser_users = [vote.user.username for vote in votes if vote.choice in losers]

        # Return the winners, losers, and users who voted for each choice
        return winners, losers, winner_users, loser_users
    


       


class Comment(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='pollcomments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE ,blank=True, null=True)
    def __str__(self):
        return f'{self.user.username} - {self.poll.text}'
    
  