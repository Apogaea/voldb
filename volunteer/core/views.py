from django.views.generic import TemplateView


class SiteIndexView(TemplateView):
    template_name = 'home.html'


from volunteer.apps.departments.models import Department


class ShiftGridView(TemplateView):
    template_name = 'shift_grid.html'

    def get_context_data(self, **kwargs):
        context = super(ShiftGridView, self).get_context_data(**kwargs)

        department = Department.objects.get(pk=2)
        role = department.roles.get()
        shifts = role.shifts.all()

        context['shifts'] = shifts
        context['department'] = department
        context['role'] = role

        return context
