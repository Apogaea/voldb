from django.views.generic import ListView, TemplateView
from django.contrib.auth import get_user_model
from django.db.models import Sum

from authtools.views import LoginRequiredMixin

User = get_user_model()


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


class ShiftAppView(TemplateView):
    template_name = "shifts/app.html"
