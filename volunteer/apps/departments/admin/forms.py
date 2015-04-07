from betterforms.forms import BetterModelForm

from volunteer.apps.departments.models import Department


class AdminDepartmentForm(BetterModelForm):
    class Meta:
        model = Department
        fields = (
            'id',
            'name',
            'description',
        )
