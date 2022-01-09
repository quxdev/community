import django.http.response
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse

from qux.models import CoreModel
from qux.models import default_null_blank
from qux.utils.urls import MetaURL


class Newsitem(CoreModel):
    SLUG_PREFIX = None

    slug = models.CharField(verbose_name="Slug", max_length=16, unique=True)
    title = models.CharField(
        verbose_name="Headline", max_length=256, **default_null_blank
    )
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, **default_null_blank)
    url = models.URLField(verbose_name="URL", max_length=2048)
    domain = models.CharField(
        verbose_name="Domain", max_length=512, **default_null_blank
    )
    description = models.TextField(verbose_name="Description", **default_null_blank)
    image = models.URLField(max_length=2048)
    short_url = models.CharField(
        verbose_name="Short URL", max_length=32, unique=True, **default_null_blank
    )
    votes = models.IntegerField(null=True)
    comments = models.IntegerField(null=True)

    class Meta:
        db_table = "newsitem"
        verbose_name = "News Item"
        verbose_name_plural = "News Items"
        ordering = ["-id"]
        unique_together = ["url", "creator"]

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        metaurl = MetaURL()
        metaurl.url = self.url
        metadata = metaurl.load()
        if type(metadata) is django.http.response.JsonResponse:
            self.title = self.url
        else:
            self.url = metadata.get("url", self.url)
            self.domain = metaurl.domain
            self.title = metadata.get("title", None)
            self.description = metadata.get("description", None)
            self.image = metadata.get("image", None)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        url = reverse("newsfeed:view", kwargs={"pk": self.id})
        return url

    def count_votes(self):
        self.votes = self.vote_set.all().count()

    def count_comments(self):
        self.comments = self.comment_set.all().count()


class Vote(CoreModel):
    item = models.ForeignKey(Newsitem, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "newsitem_vote"
        unique_together = ["item", "voter"]

    def __unicode__(self):
        return f"{self.voter.username} upvoted {self.item.title}"


class Comment(models.Model):
    item = models.ForeignKey(Newsitem, on_delete=models.CASCADE)
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, default=None, null=True, blank=True
    )
    content = models.TextField()
    identifier = models.IntegerField()
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, default=None, null=True, blank=True
    )

    class Meta:
        db_table = "newsitem_comment"

    def __unicode__(self):
        return f"Comment by {self.creator.username}"
