from django import forms

from betterforms.forms import BetterModelForm

from volunteer.apps.departments.models import (
    Department,
    Role,
)


class AdminDepartmentForm(BetterModelForm):
    class Meta:
        model = Department
        fields = (
            'name',
            'description',
        )


class AdminDepartmentMergeForm(BetterModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.none(),
        help_text=(
            "Select the department that this department should be merged into."
        ),
    )
    verify = forms.CharField(
        help_text=(
            "Please type the name of the department you are merging to confirm "
            "you want to perform this action"
        ),
    )

    def __init__(self, *args, **kwargs):
        super(AdminDepartmentMergeForm, self).__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.exclude(pk=self.instance.pk)

    class Meta:
        model = Department
        fields = tuple()

    def clean_verify(self):
        if self.cleaned_data['verify'] != self.instance.name:
            raise forms.ValidationError(
                "The typed name did not match the department being merged"
            )
        return self.cleaned_data['verify']

    def save(self, *args, **kwargs):
        other_department = self.cleaned_data['department']
        self.instance.roles.update(department=other_department)
        self.instance.delete()
        return other_department


class AdminRoleForm(BetterModelForm):
    class Meta:
        model = Role
        fields = (
            'name',
            'description',
        )


class AdminRoleMergeForm(BetterModelForm):
    role = forms.ModelChoiceField(
        queryset=Role.objects.none(),
        help_text=(
            "Select the role that this role should be merged into."
        ),
    )
    verify = forms.CharField(
        help_text=(
            "Please type the name of the role you are merging to confirm "
            "you want to perform this action"
        ),
    )

    def __init__(self, *args, **kwargs):
        super(AdminRoleMergeForm, self).__init__(*args, **kwargs)
        self.fields['role'].queryset = self.instance.department.roles.exclude(
            pk=self.instance.pk,
        )

    class Meta:
        model = Role
        fields = tuple()

    def clean_verify(self):
        if self.cleaned_data['verify'] != self.instance.name:
            raise forms.ValidationError(
                "The typed name did not match the role being merged"
            )
        return self.cleaned_data['verify']

    def save(self, *args, **kwargs):
        other_role = self.cleaned_data['role']
        self.instance.shifts.update(role=other_role)
        self.instance.delete()
        return other_role
