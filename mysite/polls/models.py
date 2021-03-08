from django.db import models
class Genre(models.Model):
    name = models.CharField(max_length=250) #CharField to pole znakowe
class Question(models.Model):
    question_text = models.CharField(max_length=250)
    pub_date = models.DateTimeField()

    def __str__(self):
        return f"{self.question_text}"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0) #jak nie podamy votes ustawi się na default czyli 0

    def __str__(self):
        return f"{self.choice_text}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.answer_text}"


    # Create your models here.
