__author__ = 'yedtoss'

import requests

import trueskill

import datetime

import subprocess
import models
from django.conf import settings


def get_past_challenges(challenge_type='Development'):
    """

    :param challenge_type:
    :return:
    """
    payload = {
        'type': 'develop',
        'challengeType': challenge_type,
        'pageIndex': 1,
        'pageSize': 100,
        'submissionEndFrom': '2011-11-10',
        'submissionEndTo': '2015-11-11',
        'sortColumn': 'submissionEndDate',
        'sortOrder': 'desc'

    }

    resp = requests.get('http://api.topcoder.com/v2/challenges/past', payload)

    return resp.json()


def get_challenge_result(challenge_id):
    print("Making request to ", "http://api.topcoder.com/v2/develop/challenges/result/" + str(challenge_id))
    resp = requests.get("http://api.topcoder.com/v2/develop/challenges/result/" + str(challenge_id))
    return resp.json()


def get_members_result(challenge_type='Development'):
    today = datetime.date.today()
    yesterday = datetime.date.today() - datetime.timedelta(1)
    picture_location = models.RatingsPicture.objects.filter(date=today, challenge_type=challenge_type)

    if picture_location.count() > 0:
        return

    challenges = get_past_challenges(challenge_type=challenge_type)
    env = trueskill.TrueSkill()

    no_one = models.Member.objects.filter(handle="Toto", date=today, challenge_type=challenge_type)
    if no_one.count() <= 0:
        # no_one = models.Member.objects.filter(handle="Toto", date=yesterday, challenge_type=challenge_type)
        no_one = models.Member.objects.filter(handle="Toto", date=yesterday, challenge_type=challenge_type)
        if no_one.count() <= 0:
            r = env.create_rating()
            mu = r.mu
            sigma = r.sigma
        else:
            mu = no_one[0].mu
            sigma = no_one[0].sigma

        m = models.Member()
        m.handle = "Toto"
        m.sigma = sigma
        m.mu = mu
        m.rating = int(100*mu)
        m.volatibility = int(100*sigma)
        m.challenge_type = challenge_type
        m.date = today
        m.save()
        no_one = m
    else:
        no_one = no_one[0]


    for challenge in challenges["data"]:
        if challenge["status"] == "Completed":
            result = get_challenge_result(challenge_id=challenge['challengeId'])
            ratings = []
            handles = []
            ranks = []

            for member in result["results"]:
                model = models.Member.objects.filter(handle=member["handle"], date=today, challenge_type=challenge_type)
                if model.count() <= 0:
                    model = models.Member.objects.filter(handle=member["handle"], date=yesterday,
                                                         challenge_type=challenge_type)
                    if model.count() <= 0:

                        r = env.create_rating()
                        sigma = r.sigma
                        mu = r.mu
                    else:
                        mu = model[0].mu
                        sigma = model[0].sigma

                    m = models.Member()
                    m.handle = member["handle"]
                    m.sigma = sigma
                    m.mu = mu
                    m.rating = int(100*mu)
                    m.volatibility = int(100*sigma)
                    m.challenge_type = challenge_type
                    m.date = today
                    m.save()
                    res = m
                else:
                    res = model[0]


                try:
                    ranks.append(int(member["placement"])-1)
                    handles.append(res)
                    ratings.append((res.mu, res.sigma))
                except:
                    print(member, member["placement"], member["finalScore"])
                    continue

            if len(ranks) <= 0:
                continue
            #if len(ranks) == 1:
            ranks.append(len(ratings))
            ratings.append((no_one.mu, no_one.sigma))
            handles.append(no_one)

            new_ratings = update_skills(ratings, ranks)

            for i in xrange(len(new_ratings)):
                handles[i].mu = new_ratings[i][0]
                handles[i].sigma = new_ratings[i][1]
                handles[i].rating = int(100*new_ratings[i][0])
                handles[i].volatibility = int(100*new_ratings[i][1])
                handles[i].save()

    m = models.RatingsPicture()
    m.date = today
    m.challenge_type = challenge_type
    m.picture_done = False
    m.save()



def update_skills(ratings, ranks):

    env = trueskill.TrueSkill()

    new_ratings = [None]*len(ratings)

    r = [None]*len(ratings)
    for i in xrange(len(ratings)):
        r[i] = {i: env.create_rating(mu=float(ratings[i][0]), sigma=float(ratings[i][1]))}

    new_r = env.rate(r, ranks)

    for i in xrange(len(ratings)):
        new_ratings[i] = (new_r[i][i].mu, new_r[i][i].sigma)

    return new_ratings


def get_date(date_string):
    if isinstance(date_string, basestring):
        return datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
    else:
        return date_string


