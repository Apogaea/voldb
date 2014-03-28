from django.views.generic import ListView
from django.contrib.auth import get_user_model
from django.db.models import Sum

User = get_user_model()

from authtools.views import LoginRequiredMixin

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
        return context

    def extract_date(entity):
        'extracts the starting date from an entity'
        return entity.start_time.date()


class LeaderBoardView(LoginRequiredMixin, ListView):
    model = User
    template_name = "shifts/leaderboard.html"
    context_object_name = "users"
    paginate_by = 10

    def get_queryset(self):
        qs = super(LeaderBoardView, self).get_queryset()
        return qs.annotate(
            shift_length_sum=Sum('shifts__shift_length'),
        ).filter(
            shift_length_sum__isnull=False,
        ).order_by('-shift_length_sum')
