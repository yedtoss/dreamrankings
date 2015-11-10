from django.db import models

# Create your models here.


class Member(models.Model):
    handle = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=5)
    volatibility = models.IntegerField(default=5)
    mu = models.DecimalField(default=0, decimal_places=2, max_digits=19)
    sigma = models.DecimalField(default=0, decimal_places=2, max_digits=19)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    challenge_type = models.TextField(null=True, blank=True)


#class Ratings(models.Model):
#    member = models.ForeignKey(Member)
#    rating = models.IntegerField(default=5)
#    volatibility = models.IntegerField(default=5)
#    mu = models.DecimalField(default=0, decimal_places=2, max_digits=19)
#    sigma = models.DecimalField(default=0, decimal_places=2, max_digits=19)
#    date = models.DateField(auto_now_add=True)


class RatingsPicture(models.Model):
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    picture_location = models.TextField(null=True, blank=True)
    challenge_type = models.TextField(null=True, blank=True)
    picture_done = models.NullBooleanField()


