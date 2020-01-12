from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Poll, Choice, Voter, Contestant
from django.http import JsonResponse

# Create your views here.


def home(request):
    latest_poll_list = Poll.objects.order_by('-start_date')[:5]
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'VotingApp/home.html', context)


def detail(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404("Poll does not exist")
    return render(request, 'VotingApp/detail.html', {'poll': poll})


def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'VotingApp/results.html', {'poll': poll})


def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if Voter.objects.filter(poll_id=poll_id, user_id=request.user.id).exists():
        return render(request, 'VotingApp/detail.html', {
            'poll': poll,
            'error_message': "Sorry, but you have already voted.",
        })
    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'VotingApp/detail.html', {
            'poll': poll,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        v = Voter(user=request.user, poll=poll)
        v.save()
        return HttpResponseRedirect(reverse('VotingApp:results', args=(poll.id,)))


@login_required
def contestant_view(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    if Contestant.objects.filter(poll_id=poll_id, user_id=request.user.id, approved=True).exists():
        messages.add_message(request, messages.WARNING,
                             'You are already a contestant', extra_tags='danger')
        return redirect('VotingApp:home')
    elif Contestant.objects.filter(poll_id=poll_id, user_id=request.user.id, approved=False).exists():
        messages.add_message(request, messages.WARNING,
                             'You have not been approved', extra_tags='danger')
        return redirect('VotingApp:home')

    c = Contestant(poll=poll, user=request.user, approved=False)
    c.save()
    return redirect('VotingApp:home')


def resultsData(request,obj):
    votedata=[]

    poll = Poll.objects.get(id=obj)
    votes = poll.choice_set.all()

    for i in votes:
        votedata.append({i.contestant.user.full_name:i.votes})

    print(votedata)
    return JsonResponse(votedata,safe=False)