from django.conf import settings
from django.contrib import admin
from django.utils import timezone

from base.helpers import is_possible_connect_apps, is_same_database
from .models import QuestionOption
from .models import Question
from .models import CensusLocal, Voting, VotingLocal

from .filters import StartedFilter


try:
    from census.models import Census
except ImportError:
    CENSUS_LOCAL_AVAILABLE = False
else:
    CENSUS_LOCAL_AVAILABLE = (
        is_possible_connect_apps('voting', 'census')
        and is_same_database(Census, Voting)
        and is_possible_connect_apps('voting', 'authentication')
        and is_same_database(Census, settings.AUTH_USER_MODEL)
    )


def start(modeladmin, request, queryset):
    for v in queryset.all():
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()


def stop(ModelAdmin, request, queryset):
    for v in queryset.all():
        v.end_date = timezone.now()
        v.save()


def tally(ModelAdmin, request, queryset):
    for v in queryset.filter(end_date__lt=timezone.now()):
        token = request.session.get('auth-token', '')
        v.tally_votes(token)


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionInline]


class VotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [ start, stop, tally ]


class CensusInline(admin.TabularInline):
    model = CensusLocal
    fk_name = 'voting'
    extra = 1
    autocomplete_fields = ('voter',)


class VotingCensusAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def get_inlines(self, request, obj):
        return [CensusInline]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


if CENSUS_LOCAL_AVAILABLE:
    admin.site.register(VotingLocal, VotingCensusAdmin)

admin.site.register(Voting, VotingAdmin)
admin.site.register(Question, QuestionAdmin)
