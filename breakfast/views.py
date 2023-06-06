from django.shortcuts import render
from django.views import View
from django.core.exceptions import PermissionDenied

from random import randbytes
from django.utils import timezone
from datetime import datetime
import pytz


from .models import Order
from .forms import OrderModelForm

from .cotisation import isCotisant


def delivery_time_validation(time):
    time_list = [
        "8:00",
        "9:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
    ]
    if time not in time_list:
        return False
    if Order.objects.filter(deliveryTime=time).count() >= 69:
        return False
    return True


def delivery_time_available():
    slot_list = [
        "entre 8h00 et 9h00",
        "entre 9h00 et 10h00",
        "entre 10h00 et 11h00",
        "entre 11h00 et 12h00",
        "entre 12h00 et 13h00",
        "entre 13h00 et 14h00",
        "entre 14h00 et 15h00",
        "entre 15h00 et 16h00",
        "entre 16h00 et 17h00",
        "entre 17h00 et 18h00",
    ]
    available_time = []
    orders = Order.objects.all()
    for slot in slot_list:
        time = slot.split(" ")[1].replace("h", ":")
        if orders.filter(deliveryTime=time).count() < 69:
            available_time.append(slot)
    return available_time


def drinks_avaible():
    drink_list = [
        "Orangina",
        "Coca-cola",
        "Oasis",
    ]
    available_drink = ["Pas de boisson"]
    orders = Order.objects.all()
    for drink in drink_list:
        if orders.filter(drinks="['" + drink + "']").count() < 96:
            available_drink.append(str(drink))
    return available_drink


class BreakfastView(View):
    def get(self, request):
        OrderForm = OrderModelForm()
        context = {
            "orderform": OrderForm,
            "available_time": delivery_time_available(),
            "possible_drinks": drinks_avaible(),
        }
        return render(request, "breakfast/breakfast.html", context=context)

    def post(self, request):
        utc = pytz.UTC

        today = timezone.now()
        enddate = utc.localize(datetime(2023, 2, 9))
        end = utc.localize(datetime(2023, 2, 13))

        if today > end:
            context = {
                "title": "Les ptits dejs, c'est déjà fini !",
                "subtitle": "Et la campagne aussi, merci à tous ceux qui ont cru en nous. Bises asgardiennes !",
            }
            return render(request, "breakfast/pasok.html", context)

        if today > enddate:
            context = {
                "title": "Les ptits dejs, c'est déjà fini !",
                "subtitle": "On se retrouve aux stands et à la soirée de vendredi !",
            }
            return render(request, "breakfast/pasok.html", context)

        if request.META.get("HTTP_REFERER") is None:
            raise PermissionDenied

        posted_data = request.POST.copy()
        slot = posted_data.pop("deliveryTime")[0]
        time = slot.split(" ")[1].replace("h", ":")
        OrderForm = OrderModelForm(posted_data)

        drink = posted_data.pop("drink_wanted")

        if not OrderForm.is_valid():
            context = {
                "title": "Le formulaire comporte des champs incorrects ou tu as déjà fait une commande !",
                "subtitle": "Si tu penses qu'il y a quand même une erreur, contacte Nicolas Asgard Rocq sur Messenger.",
            }
            return render(request, "breakfast/pasok.html", context)

        if not delivery_time_validation(time):
            context = {
                "title": "L'heure de livraison est incorrecte !",
                "subtitle": "Si tu penses qu'il y a quand même une erreur, contacte Nicolas Asgard Rocq sur Messenger.",
            }
            return render(request, "breakfast/pasok.html", context)

        data = OrderForm.cleaned_data

        if not isCotisant(data["firstName"], data["lastName"]):
            context = {
                "title": "Es-tu sûr de l'orthographe de ton nom et de ton prénom ? Si oui, il semblerait que tu ne sois pas cotisant BDE.",
                "subtitle": "Si tu penses qu'il y a quand même une erreur, contacte Nicolas Asgard Rocq sur Messenger.",
            }
            return render(request, "breakfast/pasok.html", context)

        # Save order
        new_order = Order(
            firstName=data["firstName"],
            lastName=data["lastName"],
            phone=data["phone"],
            email=data["email"],
            address=data["address"],
            menu=data["menu"],
            drinks=drink,
            deliveryTime=time,
            comments=data["comments"],
            token=randbytes(7).hex(),
        )
        new_order.save()
        return render(request, "breakfast/ok.html")
