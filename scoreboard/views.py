import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .models import Score
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import ScoreForm
# Create your views here.


def add_score(request):
    submitted = False
    if request.method == "POST":
        form = ScoreForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = User.objects.get(username = request.user)
            obj.save()
            return HttpResponseRedirect("/")
    context = {"form" : ScoreForm}
    return render(request, "add_score.html", context )


def homepage(request):
    today = datetime.date.today()
    
    pawel = Score.objects.filter(date__gt=today, user = User.objects.get(pk=2))
    pati = Score.objects.filter(date__gt=today, user = User.objects.get(pk=3))
    print(pawel)
    winner = None
    if pawel and pati:
        pawel = pawel[0]
        pati = pati[0]
        if pawel.number_of_tries > pati.number_of_tries:
            winner = pati
        elif pawel.number_of_tries < pati.number_of_tries:
            winner = pawel
        else:
            winner = "REMIS"
    if not pawel:
        pawel = "empty"
    if not pati:
        pati = "empty"

    context = {
        "pawel" : pawel if (str(request.user) == "pawel" or pati is not  "empty" or pati is pawel) else "brak_dostepu",
        "pati" :  pati if (str(request.user) == "pati" or pawel is not "empty" or pati is pawel) else "brak_dostepu",
        "if_form_enabled" : True if ((str(request.user) == "pati" and pati is "empty") or (str(request.user) == "pawel" and pawel is "empty")) else False,
        "winner" : winner,
    }
    print(pawel)
    print(pati)
    print(context)
    return render(request, "home.html", context )

# import datetime
# from .models import Score
# from django.contrib.auth.models import User
# today = datetime.date.today()
# pawel = Score.objects.filter(date__gt=today, user = User.objects.get(pk=2)),

