from django.contrib import admin
from .models import Choice, Genre, Question, Answer

class QuestionAdmin(admin.ModelAdmin):
    ordering = ("id", )
    list_display = ('id', 'question_text', 'pub_year')
    list_display_links = ('id', 'question_text')
    list_per_page = 6
    list_filter = ('pub_date', )
    search_fields = ('question_text',)
    actions = ('cleanup_text',)
    fieldsets = [
        (None, {'fields': ['question_text']}),
        (
            'External Information',
            {
                'fields': ['pub_date'],
                'description': (
                    "To przykład opisu"
                )
            }
        )
    ]

    @staticmethod
    def pub_year(obj):
        return obj.pub_date.year

    @staticmethod
    def cleanup_text(modeladmin, request, queryset):
        queryset.update(question_text="")

class AnswerAdmin(admin.ModelAdmin):
    ordering = ("id", )
    list_display = ('id', 'question', 'answer_text')
    list_display_links = ('id',)
    list_per_page = 10
    list_filter = ('answer_text', )
    search_fields = ('answer_text',)
    actions = ('cleanup_text',)
    readonly_fields = ('date_added',)

class ChoiceAdmin(admin.ModelAdmin):
    ordering = ("id", )
    list_display = ('id', 'question', 'choice_text', 'votes')
    list_display_links = ('id',)
    list_per_page = 10
    list_filter = ('choice_text', )
    search_fields = ('choice_text',)
    actions = ('cleanup_text',)
    readonly_fields = ('votes',)

# Register your models here.
admin.site.register(Genre)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)