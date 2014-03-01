from django.db import models


class Comment(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    message = models.TextField()
    pub_date = models.DateTimeField('date_published')

    def __str__(self):
        return '%s: %s' % (self.full_name, self.message)
