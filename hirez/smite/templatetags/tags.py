from django import template

from smite import models

register = template.Library()


@register.simple_tag
def gods():
    return models.God.objects.all()