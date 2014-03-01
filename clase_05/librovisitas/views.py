from django.shortcuts import render
from librovisitas.models import Comment

from datetime import datetime

def index(request):
    try:
        full_name = request.POST['full_name']
        email = request.POST['email']
        message = request.POST['message']
    except KeyError:
        pass
    else:
        c = Comment(full_name=full_name, email=email, message=message, pub_date=datetime.now())
        c.save()
    comments = Comment.objects.all()
    return render(request, 'index.html', {'comments': comments})
