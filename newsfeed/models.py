from django.db import models
from django.shortcuts import reverse

from django.contrib.auth.models import User
# from qux.utils.slop import get_random_string
from qux.models import CoreModel
from qux.utils.urls import MetaURL
from shorturl.models import Link
import uuid


class Newsitem(CoreModel):
    SLUG_PREFIX = None

    slug = models.CharField(
        verbose_name="Slug", max_length=16, unique=True)
    title = models.CharField(
        verbose_name="Headline", max_length=256, unique=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    url = models.URLField(
        verbose_name="URL", max_length=2048)
    description = models.TextField(
        verbose_name="Description", default=None, null=True, blank=True)
    short_url = models.CharField(
        verbose_name="Short URL", max_length=8,
        unique=True, default=None, null=True, blank=True)
    votes = models.IntegerField(null=True)
    comments = models.IntegerField(null=True)

    class Meta:
        db_table = 'newsitem'
        verbose_name = 'News Item'
        verbose_name_plural = 'News Items'
        ordering = ['-id']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        metaurl_obj = MetaURL()
        metaurl_obj.url = self.url
        url_data = metaurl_obj.load() 
        self.title = url_data.get('title', None)
        self.description = url_data.get('description', None)
        self.short_url = uuid.uuid4().hex[:8]
        return super(Newsitem, self).save(*args, **kwargs)

    def get_absolute_url(self):
        url = reverse('newsfeed:view', kwargs={'pk': self.id})
        return url

    def count_votes(self):
        self.votes = len(self.vote_set.all())

    def count_comments(self):
        self.comments = len(self.comment_set.all())





class Vote(CoreModel):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Newsitem, on_delete=models.CASCADE)

    class Meta:
        db_table = 'newsitem_vote'
        unique_together = ('voter', 'item')

    def __unicode__(self):
        return f"{self.voter.username} upvoted {self.item.title}"


class Comment(models.Model):
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    item = models.ForeignKey(Newsitem, on_delete=models.CASCADE)
    content = models.TextField()
    identifier = models.IntegerField()
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, default=None, null=True, blank=True)

    class Meta:
        db_table = 'newsitem_comment'

    def __unicode__(self):
        return f"Comment by {self.creator.username}"