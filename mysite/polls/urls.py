# from django.urls import path
# # from polls.views import hello
# from . import views
#
# # urlpatterns = [
# # #     path('hello', hello)
# # # ]
#
# urlpatterns = [
#     # path('hello/<int:year>', views.hello, name='hello')
#     path('hello', views.hello, name='hello')
#]
from django.urls import path
from polls.views import (
    animals,
    full_data,
    get_answer,
    get_choice,
    get_name,
    get_question,
    hello,
    index,
    questions,
    polls #choices, answers,
)
from polls.views import (
    AnswerDetailView,
    AnswerListView,
    AnswerFormView,
    ChoiceFormView,
    ChoiceTemplateView,
    QuestionCreateView,
    QuestionDeleteView,
    QuestionDetailView,
    QuestionFormView,
    QuestionListView,
    QuestionTemplateView,
    QuestionUpdateView,
    QuestionView,
    RegistrationCreateView
)

app_name = 'polls'
urlpatterns = [
    path('hello/<str:s0>/', hello),
    path('animals/', animals),
    path('questions/', questions, name='big-questions'),
    path('my-new-questions/', QuestionView.as_view()), #odpalamy kasę z metodą as view
    path('my-questions/', QuestionTemplateView.as_view(), name='my-questions' ), #jw.
    #path('answers/', answers, name='answers'),
    path('answers/', AnswerListView.as_view(), name='my-answers'),
    # path('choices/', choices, name='choices'),
    path('choices/', ChoiceTemplateView.as_view(), name='choices'),
    path('my-polls/', polls),
    path('', index, name="index"), #strona powitalna! url przyjmuje pustą wartość
    path('my_name_form/', get_name),
    path('my_question_form/', get_question, name="question_form"),
    path('my_choice_form/', get_choice, name="my-choice-form"),
    path('my_answer_form/', get_answer, name='my-answer-form'),
    path('full-data/', full_data, name="full-data"),
    path('questions-view/', QuestionView.as_view(), name="my-questions-view"),
    path('questions-form-view/', QuestionFormView.as_view(), name="my-questions-form-view"),
    path('answer-form-view/', AnswerFormView.as_view(), name="answers_from_view"),
    path('choices-form-view/', ChoiceFormView.as_view(), name="choices_from_view"),
    path('questions-create-view/', QuestionCreateView.as_view(), name="questions_create_view"),
    path('question-list-view', QuestionListView.as_view(), name="question_list_view"),
    path('question-detail-view/<pk>', QuestionDetailView.as_view(), name="my-question-detail-view"),
    path('answer-detail-view/<pk>', AnswerDetailView.as_view(), name="my-answer-detail-view"),
    path('questions-update-view/<pk>', QuestionUpdateView.as_view(), name="my-question-update-view"),
    path('questions-delete-view/<pk>', QuestionDeleteView.as_view(), name="my-question-delete-view"),
    path('answers-list-view', AnswerListView.as_view(), name="my-answers-list-view"),
    path('registration/', RegistrationCreateView.as_view(), name="my-registration")
]
