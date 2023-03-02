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
    if pawel:
        pawel = pawel[0]
    if pati:
        pati = pati[0]
    if pawel and pati:
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
    print(context)
    return render(request, "home.html", context )


def scoreboard_view(request):
    today = datetime.date.today()
    pawel_month = Score.objects.filter(date__month=today.month, date__year=today.year, user = User.objects.get(pk=2))
    pawel_score_in_month = []
    pati_month = Score.objects.filter(date__month=today.month, date__year=today.year, user = User.objects.get(pk=3))
    pati_score_in_month = []
    scores = []
    total_monthly_score = [0,0]
    for i in range(today.day):
        print(i)
        #Wypisywanie wartości w danym dniu
        if pawel_month.filter(date__day=i+1):
            pawel_score_in_month.append(pawel_month.get(date__day=i+1).number_of_tries)
        else:
            pawel_score_in_month.append(-1)
        if pati_month.filter(date__day=i+1):
            pati_score_in_month.append(pati_month.get(date__day=i+1).number_of_tries)
        else:
            pati_score_in_month.append(-1)

        # Obliczanie wyników:
        if pati_score_in_month[i] == pawel_score_in_month[i]:
            scores.append([0.5, 0.5])
            total_monthly_score[0] = total_monthly_score[0] + 0.5
            total_monthly_score[1] = total_monthly_score[1] + 0.5
        elif pawel_score_in_month[i] < pati_score_in_month[i]:
            scores.append([1,0])
            total_monthly_score[0] = total_monthly_score[0] + 1
        elif pawel_score_in_month[i] > pati_score_in_month[i]:
            scores.append([0,1])
            total_monthly_score[1] = total_monthly_score[1] + 1


    
    context = {
        "pawel_wyniki" : pawel_score_in_month,
        "pati_wyniki" : pati_score_in_month,
        "score" : scores,
        "total_score" : total_monthly_score,
        "current_month" : today.strftime("%B")
    }
    print(context)
    return render(request, "monthly.html", context)

# import datetime
# from .models import Score
# from django.contrib.auth.models import User
# today = datetime.date.today()
# pawel = Score.objects.filter(date__gt=today, user = User.objects.get(pk=2)),

