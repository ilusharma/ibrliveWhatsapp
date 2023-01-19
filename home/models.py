from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100,blank=True)
    number = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.number


class ContactGroup(models.Model):
    name = models.CharField(max_length=100)
    contacts = models.ManyToManyField(Contact)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class TemplateList(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=100,blank=True)
    template = models.CharField(max_length=100)
    type = models.CharField(max_length=100,choices=(('single','single'),('multi','multi')),default='single')
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class TemplateReport(models.Model):
    template = models.ForeignKey(TemplateList,on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact,on_delete=models.CASCADE)
    msg_id = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    seenTime = models.DateTimeField(blank=True,null=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.template.name


class Message(models.Model):
    name = models.CharField(max_length=100)
    msg = models.CharField(max_length=100)
    date = models.DateTimeField()
    contact = models.CharField(max_length=100)
    msg_id = models.CharField(max_length=100)
    def __str__(self):
        return self.msg

