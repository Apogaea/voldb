from django.views.generic import ListView
from django.contrib.auth import get_user_model
from django.db.models import Sum

from authtools.views import LoginRequiredMixin

from volunteer.apps.shifts.models import Shift
from volunteer.apps.shifts.utils import group_shifts

User = get_user_model()


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
