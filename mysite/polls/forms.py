from django import forms
from polls.models import Answer, Choice, Question
from django.core.exceptions import ValidationError
from datetime import datetime
import pytz
utc = pytz.UTC

class PastMonthField(forms.DateTimeField):

    def validate(self, value):
        super().validate(value)
        if value >= datetime.today().replace(tzinfo=utc):
            raise ValidationError("Only past dates allowed here.")

class PastDateField(forms.DateTimeField):
    def validate(self, value):
        utc = pytz.utc
        super().validate(value)
        if value >= datetime.today().replace(tzinfo=utc):
            raise ValidationError("Date needs to be before today")

def capitalized_validator(value):
    if value[0].islower():
        raise ValidationError("Value must be capitalized")

def upper_validator(value):
    if value.isupper():
        raise ValidationError("Value must not contain capital letters")

class NameForm(forms.Form):
    name = forms.CharField(max_length=128)

class QuestionForm(forms.Form):
    question_text = forms.CharField(max_length=250) #, validators=[capitalized_validator]
    pub_date = PastMonthField(label="Data publikacji", widget=forms.TextInput(attrs={'placeholder': 'eg.2006-10-25 14:30:59'}))

    def clean_question_text(self):
        import re
        # Force each sentence of the description to be capitalized.
        initial = self.cleaned_data['question_text']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)

    def clean(self):
        result = super().clean()
        if result['question_text'][0] == 'A' and result['pub_date'].year < 2000:
            self.add_error('question_text', "Can't start with an A")
            self.add_error('pub_date', "Can't be before 2000")
            raise ValidationError(
                "Can't match A with year before 2000"
            )
        return result

    def clean_choice_text(self):
        return self.cleaned_data['choice_text'].upper()

class ChoiceForm(forms.Form):
    choice_text = forms.CharField(max_length=128)
    votes = forms.IntegerField(max_value=10)
    question = forms.ModelChoiceField(queryset=Question.objects.all())

    def clean(self):
        result = super().clean()
        if result['choice_text'][0] == 'W' and result['votes'] == 0:
            self.add_error('choice_text', "Can't start with a W")
            self.add_error('votes', "Can't be 0")
            raise ValidationError(
                "Can't match W with votes equal 0"
            )
        return result

class AnswerForm(forms.Form):

    question = forms.ModelChoiceField(queryset=Question.objects.all())
    answer_text = forms.CharField(max_length=128, validators=[upper_validator])
    date_added = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': 'eg.2006-10-25 14:30:59'}))


class QuestionModelForm(forms.ModelForm):
    pub_date = PastDateField(
        widget=forms.TextInput(attrs={'placeholder': 'eg.2006-10-25 14:30:59'}))
    class Meta:
        model = Question
        fields = "__all__"



class AnswerModelForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = "__all__"

class ChoiceModelForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = "__all__"

