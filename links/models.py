import hashlib

import django.http.response
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse

from qux.models import CoreModel
from qux.models import default_null_blank
from qux.utils.urls import MetaURL

OPENGRAPH_TYPES = (
    ("article", "Article"),
    ("book", "Book"),
    ("profile", "Profile"),
    ("website", "Website"),
    (
        "Music", (
            ("song", "Song"),
            ("album", "Album"),
        ),
    ),
    (
        "Video", (
            ("movie", "Movie"),
            ("episode", "Episode"),
            ("tvshow", "TV Show"),
            ("other", "Other"),
        ),
    ),
    (
        "File", (
            ("file:pdf", "PDF"),
            ("file:xls", "XLS"),
            ("file:doc", "DOC"),
            ("file:ppt", "PPT"),
        )
    )
)


class Link(CoreModel):
    SLUG_PREFIX = None

    slug = models.CharField(verbose_name="Slug", max_length=16, unique=True)
    tags = models.CharField(verbose_name="Tags", max_length=256, **default_null_blank)
    title = models.CharField(
        verbose_name="Headline", max_length=256, **default_null_blank
    )
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, **default_null_blank)
    url = models.URLField(verbose_name="URL", max_length=2048)
    url_hash = models.CharField(verbose_name="URL MD5 Hash", max_length=32)
    orig_url = models.URLField(verbose_name="Original URL", **default_null_blank)
    domain = models.CharField(
        verbose_name="Domain", max_length=512, **default_null_blank
    )
    type = models.CharField(max_length=32, choices=OPENGRAPH_TYPES, default="website")
    description = models.TextField(verbose_name="Description", **default_null_blank)
    image = models.URLField(max_length=2048, **default_null_blank)
    short_url = models.CharField(
        verbose_name="Short URL", max_length=128, unique=True, **default_null_blank
    )
    is_favorite = models.BooleanField(default=False, verbose_name="Favorite")
    is_shared = models.BooleanField(default=True, verbose_name="Shared")
    votes = models.IntegerField(null=True)
    comments = models.IntegerField(null=True)

    class Meta:
        db_table = "qux_link"
        verbose_name = "Link"
        verbose_name_plural = "Links"
        ordering = ["-id"]
        unique_together = ["url_hash", "creator"]

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        metaurl = kwargs.get("metaurl", None)
        if metaurl is None:
            metaurl = MetaURL()
            metaurl.url = self.url
            metadata = metaurl.load()

            if type(metadata) is django.http.response.JsonResponse:
                self.title = self.url

        self.writeattr(metaurl)

        if "metaurl" in kwargs:
            kwargs.pop("metaurl")

        print(self.__dict__)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        url = reverse("links:view", kwargs={"slug": self.slug})
        return url

    def count_votes(self):
        self.votes = self.vote_set.all().count()

    def count_comments(self):
        self.comments = self.comment_set.all().count()

    def writeattr(self, metaurl: MetaURL = None):
        if not isinstance(metaurl, MetaURL):
            return

        self.url = metaurl.url
        if not self.orig_url:
            self.orig_url = metaurl.orig_url
        self.domain = metaurl.domain
        self.type = metaurl.type
        self.image = metaurl.image
        self.title = metaurl.title
        self.description = metaurl.description
        if not self.description and self.orig_url:
            self.description = self.orig_url
        self.url_hash = hashlib.md5(self.url.encode("utf-8")).hexdigest()


class Vote(CoreModel):
    item = models.ForeignKey(Link, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "qux_link_vote"
        unique_together = ["item", "voter"]

    def __unicode__(self):
        return f"{self.voter.username} upvoted {self.item.title}"


class Comment(models.Model):
    item = models.ForeignKey(Link, on_delete=models.CASCADE)
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, default=None, null=True, blank=True
    )
    content = models.TextField()
    identifier = models.IntegerField()
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, default=None, null=True, blank=True
    )

    class Meta:
        db_table = "qux_link_comment"

    def __unicode__(self):
        return f"Comment by {self.creator.username}"
