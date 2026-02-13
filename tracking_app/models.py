from django.db import models

class KeyPress(models.Model):
    key = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

class MouseClick(models.Model):
    button = models.CharField(max_length=20)
    x = models.IntegerField()
    y = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class MouseMovement(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class KeyCombination(models.Model):
    combination = models.CharField(max_length=100)
    count = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)