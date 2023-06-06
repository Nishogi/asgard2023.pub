from django.shortcuts import render


def home(request):
    return render(request, "core/index.html")


def organigramm(request):
    return render(request, "core/organigramme.html")


def manifesto(request):
    return render(request, "core/programme.html")


def sponsors(request):
    return render(request, "core/partenariats.html")
