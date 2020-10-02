from django.db import models

# Video title, description, publishing datetime, thumbnails URLs 
class ytmanager(models.Manager):
    def create_ytVid(self,title,description,pubDT,thumb,id):
        self.create(title=title,description=description,publishingDT=pubDT,thumbnails=thumb,iduid=id)
        

class ytVideo(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    publishingDT = models.DateTimeField()
    thumbnails = models.URLField(max_length=200)
    iduid = models.IntegerField(default=0)
    objects = ytmanager()