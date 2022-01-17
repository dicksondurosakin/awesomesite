from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.


def index(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        sender = request.POST.get("email")
        body = request.POST.get('message')

        send_mail(
            subject=f"From {name}",
            message=f"Sender: {sender}\n\n{body}",
            from_email= settings.DEFAULT_FROM_EMAIL,
            recipient_list=["femimathias39@gmail.com",]
        )     

    return render(request, 'portfolio/index.html')

