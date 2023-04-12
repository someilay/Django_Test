from django.core.exceptions import ValidationError
from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=50, default='Untitled')


class Entry(models.Model):
    name = models.CharField(max_length=50, default='Untitled')
    parent = models.ForeignKey(to='self', null=True, blank=True, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'[{self.id}: {self.name}, {self.parent.id if self.parent else None}, {self.menu.id}]'

    def clean(self):
        if self.parent and self.parent.menu.id != self.menu.id:
            raise ValidationError('Parent should lie in the same menu as child!')
