from django.shortcuts import render
from django.core.mail import send_mail

# Create your views here.


def index(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        sender = request.POST.get("email")
        body = request.POST.get('message')

        send_mail(
            subject=f"From {name}",
            message=f"Sender: {sender}\n\n{body}",
            recipient_list=["femimathias39@gmail.com",]
        )     

    return render(request, 'dickson/index.html')

