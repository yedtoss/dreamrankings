from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

from models import Member
import models
import helper

import datetime

import subprocess
import models
from django.conf import settings


def show_old_ratings(request, challenge_type, date):
    date = helper.get_date(date)
    return show_ratings(request, date=date, challenge_type=challenge_type)


def show_ratings_no_picture(request, challenge_type='Development', date=datetime.date.today()):
    date = helper.get_date(date)
    helper.get_members_result(challenge_type=challenge_type)
    members = Member.objects.filter(date=date, challenge_type=challenge_type).order_by('-mu', '-sigma')
    data = {
        "contestType": challenge_type,
        "updated_on": date,
        "text_updated_date": date.isoformat(),
        "base_url": "http://" + request.get_host(),
        "google_plus_url": "http://" + request.get_host() + "/ratings/" + challenge_type + "/" + date.isoformat()
    }
    context = {"members": members, "data": data}
    #return HttpResponse("Working")
    return render(request, 'ranktc/view_rankings.html', context)


def show_ratings(request, challenge_type=None, date=datetime.date.today()):
    date = helper.get_date(date)
    if not challenge_type:
        challenge_type = 'Development'
    #today = datetime.date.today()
    response = show_ratings_no_picture(request, date=date, challenge_type=challenge_type)
    m = models.RatingsPicture.objects.filter(date=date, challenge_type=challenge_type)

    base_url = "http://" + request.get_host()

    if m.count() > 0 and not m[0].picture_done:
        cmd = ['webkit2png',
               '-o', settings.RATING_IMG + "/" + challenge_type + "_" + date.isoformat()
               ,base_url + '/ratings_no_picture/' + challenge_type + "/" + date.isoformat()]
        subprocess.Popen(cmd)
        #subprocess.Popen(cmd).wait()

    return response

def show_home(request):
    date= '2015'
    data = {
        'num_architecture_rated': Member.objects.filter(challenge_type='Architecture').values('handle').distinct().count(),
        'num_assembly_rated': Member.objects.filter( challenge_type='Assembly Competition').values('handle').distinct().count(),
        'num_development_rated': Member.objects.filter(challenge_type='Development').values('handle').distinct().count(),
        'num_design_rated': Member.objects.filter(challenge_type='Design').values('handle').distinct().count(),
        'num_first2finish_rated': Member.objects.filter(challenge_type='First2Finish').values('handle').distinct().count(),
        'num_code_rated': Member.objects.filter(challenge_type='Code').values('handle').distinct().count(),
        'is_home': True
    }
    context = {

        "data":data

    }

    return render(request, 'ranktc/home.html', context)


