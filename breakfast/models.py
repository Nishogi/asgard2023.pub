from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Order(models.Model):
    firstName = models.CharField(max_length=20, help_text="Prénom")
    lastName = models.CharField(max_length=40, help_text="Nom de famille")

    phone = PhoneNumberField(unique=True, help_text="Numéro de téléphone")

    email = models.EmailField(unique=True, help_text="Adresse électronique")

    address = models.CharField(
        max_length=100, help_text="Adresse / N° d'appartement maisel"
    )

    MENUS_AVAILABLE = [
        ("1", "Le festin de Baldr"),
        ("2", "Le buffet de Höd"),
        ("3", "Le délice de Vidar"),
    ]
    menu = models.CharField(
        max_length=1, choices=MENUS_AVAILABLE, default="1", help_text="Menu"
    )

    drinks = models.CharField(max_length=15, help_text="Boisson")

    deliveryTime = models.TimeField(help_text="Heure de livraison")

    comments = models.TextField(
        max_length=1000, blank=True, help_text="Exigences spécifiques"
    )

    token = models.CharField(
        max_length=64, unique=True, help_text="Jeton de confirmation"
    )
