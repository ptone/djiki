from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from taggit_autosuggest.managers import TaggableManager

class Versioned(object):
    def last_revision(self):
        try:
            return self.revisions.order_by('-created')[0]
        except IndexError:
            return None

    def last_change(self):
        last = self.last_revision()
        if last:
            return last.created

    def last_author(self):
        last = self.last_revision()
        if last:
            return last.author


class Revision(models.Model):
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    author = models.ForeignKey(User, verbose_name=_("Author"), null=True, blank=True)
    description = models.CharField(_("Description"), max_length=400, blank=True,
            help_text="A brief description of what changes you've made")

    class Meta:
        abstract = True
        ordering = ('-created',)


class Page(models.Model, Versioned):
    title = models.CharField(_("Title"), max_length=256, unique=True)
    tags = TaggableManager(help_text="Keywords or topics this relates to")

    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        return self.title


class PageRevision(Revision):
    page = models.ForeignKey(Page, related_name='revisions')
    content = models.TextField(_("Content"), blank=True)
    current_version = models.BooleanField(default=True)

    def __unicode__(self):
        return u"%s: %s" % (self.page, self.description)

    def save(self, *args, **kwargs):
        PageRevision.objects.filter(page=self.page).update(
                current_version=False)
        self.current_version = True
        super(PageRevision, self).save(*args, **kwargs)

def invalidate_content(sender, instance=None, **kwargs):
    # TODO: This doesn't look implemented
    instance.page.rendered_content = ''
    instance.page.save()
models.signals.post_save.connect(invalidate_content, sender=PageRevision)


class Image(models.Model, Versioned):
    name = models.CharField(_("Name"), max_length=128, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class ImageRevision(Revision):
    image = models.ForeignKey(Image, related_name='revisions')
    file = models.FileField(_("File"), upload_to=settings.DJIKI_IMAGES_PATH)
