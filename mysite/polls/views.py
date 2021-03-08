from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView, DetailView, UpdateView, DeleteView
from polls.models import Question, Answer, Choice
from polls.forms import AnswerForm, AnswerModelForm, ChoiceForm, ChoiceModelForm, NameForm, QuestionForm, QuestionModelForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm


@login_required(login_url='/login')
def get_name(request):
    print(request.user)
    print(request.user.is_authenticated)
    form = NameForm()
    if request.method == "POST":
        return HttpResponse("IT WORKED")
    return render(
        request,
        template_name="my_name.html",
        context={"form": form}
    )

#Sprawdzacz maila

class EmailCheckMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.username.startswith('u')

class QuestionView(View):
    def get(self, request):
        return render(
            request, template_name="my-new-questions.html",
            context={'questions': Question.objects.all()}
        )

class QuestionTemplateView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    template_name = "my_questions.html"
    extra_context = {'questions': Question.objects.all()}  # najprosze rozwiązanie, tylko wyświetla dane

def hello(request, s0):
    s1 = request.GET.get('s1', '')
    return render(
        request,
        template_name='hello.html',
        context={'adjectives': [s0, s1, 'beautiful', 'wonderful']}
    )

def animals(request):
    animals = request.GET.get('animals', '').split(",")  # ["bird", "cart", "dog"]
    return render(
        request,
        template_name='my_template.html',
        context={'animals': animals}
    )


def questions(request):
    return render(
        request,
        template_name='questions.html',
        context={'questions': Question.objects.all()}
    )


# def answers(request):
# #     return render(
# #         request,
# #         template_name='answers.html',
# #         context={'answers': Answer.objects.all()}
# )

class AnswerListView(ListView):
    template_name = "answers.html"
    model = Answer


# def choices(request):
#     return render(
#         request,
#         template_name='choices.html',
#         context={'choices': Choice.objects.all()}
#     )

class ChoiceTemplateView(TemplateView):
    template_name = "choices.html"
    extra_context = {'choices': Choice.objects.all()}


def polls(request):
    return render(
        request,
        template_name='my_poll.html',
        context={"questions": Question.objects.all()}
    )


def get_name(request):
    form = NameForm()
    if request.method == 'POST':
        return HttpResponse('IT WORKED')
    return render(request, 'my_name.html', {'form': form})


def index(request):
    return render(
        request,
        template_name='index-polls.html',  # context nie jest potrzebny
    )
#@login_required
@permission_required('add answer, choice, question')
def get_question(request):
    form = QuestionForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            question_text = form.cleaned_data["question_text"]
            pub_date = form.cleaned_data["pub_date"]
            Question.objects.create(question_text=question_text, pub_date=pub_date)
            return HttpResponseRedirect(reverse("polls:question_form"))
    return render(
        request,
        template_name="my_name.html",
        context={"form": form}
    )


class QuestionView(View):
    def get(self, request): #read - pokazuje o co prosimy
        form = QuestionForm()
        return render(
            request,
            template_name="my_name.html",
            context={"form": form}
        )

    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data["question_text"]
            pub_date = form.cleaned_data["pub_date"]
            Question.objects.create(question_text=question_text, pub_date=pub_date)
            return HttpResponseRedirect(reverse("polls:my-questions"))
        return render(
            request,
            template_name="my_name.html",
            context={"form": form}
        )


def get_choice(request):
    form = ChoiceForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            choice_text = form.cleaned_data["choice_text"]
            votes = form.cleaned_data["votes"]
            question = form.cleaned_data["question"]
            Choice.objects.create(choice_text=choice_text, votes=votes, question=question)
            return HttpResponse("IT WORKED")
    return render(
        request,
        template_name="my_name.html",
        context={"form": form}
    )


def get_answer(request):
    form = AnswerForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            answer_text = form.cleaned_data["answer_text"]
            date_added = form.cleaned_data["date_added"]
            question = form.cleaned_data["question"]
            Answer.objects.create(answer_text=answer_text, date_added=date_added, question=question)
            return HttpResponse("IT WORKED")
    return render(
        request,
        template_name="my_name.html",
        context={"form": form}
    )


# class GetAnswerTemplateView(TemplateView):
#     template_name = "answers.html"
#     extra_context = {'answers': Answrr.objects.all()}

def full_data(request):
    return render(
        request,
        template_name='full_data.html',
        context={
            "questions": Question.objects.all(),
            "answers": Answer.objects.all(),
            "choices": Choice.objects.all()
        }
    )


# def hello(request, ):
#     year = request.GET.get('year', "")
#     return HttpResponse(f'Hello, world! {year}')



class QuestionFormView(FormView):
    template_name = "my_name.html"
    # form_class = QuestionForm
    form_class = QuestionModelForm
    success_url = reverse_lazy("polls:my-questions-form-view")
    def form_valid(self, form):
        result = super().form_valid(form)
        question_text = form.cleaned_data["question_text"]
        pub_date = form.cleaned_data["pub_date"]
        Question.objects.create(question_text=question_text, pub_date=pub_date)
        return result

    def form_invalid(self, form):
        return super().form_invalid(form)


class AnswerFormView(FormView):
    template_name = "my_name.html"
    form_class = AnswerModelForm
    success_url = reverse_lazy("polls:answers_from_view")

    def form_valid(self, form):
        result = super().form_valid(form)
        answer_text = form.cleaned_data["answer_text"]
        question = form.cleaned_data["question"]
        Answer.objects.create(answer_text=answer_text, question=question)
        return result

    def form_invalid(self, form):
        return super().form_invalid(form)

class ChoiceFormView(FormView):
    template_name = "my_name.html"
    form_class = ChoiceModelForm
    success_url = reverse_lazy("polls:choices_from_view")

    def form_valid(self, form):
        result = super().form_valid(form)
        choice_text = form.cleaned_data["choice_text"]
        votes = form.cleaned_data["votes"]
        question = form.cleaned_data["question"]
        Choice.objects.create(choice_text=choice_text, votes=votes, question=question)
        return result

    def form_invalid(self, form):
        return super().form_invalid(form)

#Create View


class QuestionCreateView(PermissionRequiredMixin, EmailCheckMixin, CreateView):
    permission_required = ("polls.add_choice", )
    model = Question
    fields = "__all__"
    template_name = "my_name.html"
    success_url = reverse_lazy("polls:my-questions")
    # form_class = QuestionModelForm


class QuestionListView(ListView):
    model = Question
    template_name = "my_questions.html"

# class QuestionDetailView(DetailView):
#     model = Question
#     template_name = "my_questions.html"

class QuestionDetailView(DetailView):
    def get(self, request, pk):
        obj = get_object_or_404(Question, pk=pk)
        return render(
            request,
            template_name = 'my_question.html',
            context={"question": obj}
        )
#Update View

# class QuestionUpdateView(View):
#     def get(self, request, pk):
#         form = QuestionForm()
#         return render(
#             request,
#             template_name="my_name.html",
#             context={"form": form}
#         )
#     def post(self, request, pk):
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             q = Question.objects.get(pk=pk)
#             q.question_text = form.cleaned_data["question_text"]
#             q.pub_date = form.cleaned_data["pub_date"]
#             q.save()
#             return HttpResponseRedirect(reverse("polls:my-questions"))

class QuestionUpdateView(UpdateView):
    model = Question
    fields = ("question_text",)
    template_name = 'my_name.html'
    success_url = reverse_lazy("polls:my-questions")

#Delete

# class QuestionDeleteView(View):
#     def get(self, request, pk):
#         obj = get_object_or_404(Question, pk=pk)
#         obj.delete()
#         return HttpResponse("Deleted")

class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'delete_question.html'
    success_url = reverse_lazy("polls:my-questions")

# class QuestionDetailView(View):
#     def get(self, request, pk):
#         return render(
#             request,
#             template_name='my_questions.html',
#             context={'question': Question.objects.get(pk=pk)}
#         )
class AnswerCreateView(CreateView):
    model = Answer
    fields = "__all__"
    template_name = "my_name.html"
    success_url = reverse_lazy("polls:my-answers")

class ChoiceCreateView(CreateView):
    model = Choice
    fields = "__all__"
    template_name = "my_name.html"
    success_url = reverse_lazy("polls:my-choices")

class AnswersListView(ListView):
    model = Answer
    template_name = "answers.html"

class AnswerUpdateView(UpdateView):
    model = Answer
    fields = ("answer_text",)
    template_name = 'my_name.html'
    success_url = reverse_lazy("polls:my-answers")

class ChoiceUpdateView(UpdateView):
    model = Choice
    fields = ("choice_text",)
    template_name = 'my_name.html'
    success_url = reverse_lazy("polls:choices")

class AnswerDeleteView(DeleteView):
    model = Answer
    template_name = 'delete.html'
    success_url = reverse_lazy("polls:my-answers")

class AnswerDetailView(DetailView):
    def get(self, request, pk):
        obj = get_object_or_404(Answer, pk=pk)
        return render(
            request,
            template_name = 'my_answer.html',
            context={"question": obj}
        )

#Formularz rejestracyjny

class RegistrationCreateView(CreateView):
    template_name = "registration.html"
    success_url = reverse_lazy("polls:index")
    form_class = UserCreationForm

