import operator

from django.views.generic import ListView, TemplateView
from django.contrib.auth import get_user_model
from django.db.models import Sum

User = get_user_model()

from authtools.views import LoginRequiredMixin

from organizations.models import Organization

from shifts.models import Shift
from shifts.utils import group_shifts


class GridView(LoginRequiredMixin, ListView):
    template_name = "shifts/shifts.html"
    model = Shift

    def get_queryset(self):
        qs = super(GridView, self).get_queryset()
        return qs.select_related()

    def get_context_data(self, **kwargs):
        context = super(GridView, self).get_context_data(**kwargs)
        context['grouped_shifts'] = list(group_shifts(self.object_list))
        context['is_big_grid'] = True
        return context

    def extract_date(entity):
        'extracts the starting date from an entity'
        return entity.start_time.date()


class LeaderBoardView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = "shifts/leaderboard.html"
    context_object_name = "users"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs = super(LeaderBoardView, self).get_context_data(**kwargs)
        kwargs['user_leaders'] = User.objects.annotate(
            shift_length_sum=Sum('shifts__shift_length'),
        ).filter(
            shift_length_sum__isnull=False,
        ).order_by('-shift_length_sum')

        key = operator.attrgetter('total_member_shift_hours')
        kwargs['organization_leaders'] = sorted(
            filter(key, Organization.objects.all()),
            key=key,
        )
        return kwargs
