from django.db import models
from django.utils.translation import ugettext_lazy as _


class Group(models.Model):
    name = models.CharField(_('Name'), max_length=128)
    slug = models.SlugField(max_length=128)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Group')

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=128)
    slug = models.SlugField(max_length=128)
    group = models.ForeignKey('Group', related_name='categories')

    class Meta:
        ordering = ('name',)
        verbose_name = _('Category')

    def first_letter(self):
        return self.name and self.name[0] or ''

    @models.permalink
    def get_absolute_url(self):
        return 'tools:project_list', (), {'category': self.slug}

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.group.name)


class Project(models.Model):
    name = models.CharField(_('Name'), max_length=128)
    website = models.URLField(_('Website'))
    category = models.ForeignKey('Category')

    class Meta:
        ordering = ('name',)
        verbose_name = _('Project')

    def get_absolute_url(self):
        return self.website

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.category.name)
