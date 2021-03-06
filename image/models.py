from django.db import models
from datetime import datetime, timezone, timedelta


class Image(models.Model):
    user = models.ForeignKey('auth.User')
    title = models.CharField(max_length=40)
    description = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    picture = models.FileField()
    graphic = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        if self.picture:
            return self.picture.url
        return "http://images.clipartpanda.com/animated-question-mark-for-powerpoint-1256186461796715642question-mark-icon.svg.hi.png"

    def score(self):
        return sum([vote.score for vote in self.vote_set.all()])

class Comment(models.Model):
    user = models.ForeignKey('auth.User')
    body = models.CharField(max_length=140)
    image = models.ForeignKey(Image)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    def score(self):
        return sum([vote.score for vote in self.commentvote_set.all()])

    @property
    # def time_ago(self):
    #     now = datetime.now()
    #     print(now - self.time)
    #     return datetime.now() - self.time

    def day(self):
        return self.time


class Vote(models.Model):
    user = models.ForeignKey('auth.User')
    image = models.ForeignKey(Image)
    value = models.BooleanField()

    class Meta:
        unique_together = ('user', 'image')

    @property
    def score(self):
        if self.value:
            return 1
        return -1

class CommentVote(models.Model):
    user = models.ForeignKey('auth.User')
    comment = models.ForeignKey(Comment)
    value = models.BooleanField()

    class Meta:
        unique_together = ('user', 'comment')

    @property
    def score(self):
        if self.value:
            return 1
        return -1
