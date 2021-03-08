from django.db import models

class Actor(models.Model):
    GENDER_CHOICES = [
        ("W", "WOMAN"),
        ("M", "MAN")
    ]
    name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.name} {self.last_name}"


class Country(models.Model):
    name = models.CharField(max_length=250)
    iso_code = models.CharField(max_length=3)

    class Meta: #klasa Meta, czyli dane o danych, nie zmienia danych w bd, jest informacją dla Django
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.name} {self.iso_code}"

class Movie(models.Model):
    title = models.CharField(max_length=250)
    genre = models.CharField(max_length=250)
    year = models.IntegerField()
    actor = models.ForeignKey(Actor, on_delete=models.PROTECT, related_name="movies")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name="movies")

    def __str__(self):
        return f"{self.title} {self.year}"

class Oscar(models.Model):
    category = models.CharField(max_length=250)
    year = models.IntegerField()
    actor = models.ForeignKey(Actor, on_delete=models.SET_NULL, related_name="oscars", null=True,  blank=True) #null=True pozwalamy by w bazie było puste
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, related_name="oscars", null=True,  blank=True)

    def __str__(self):
        return f"{self.category} {self.year}"

# Create your models here.
