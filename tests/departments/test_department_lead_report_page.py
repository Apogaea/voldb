from django.core.urlresolvers import reverse


def test_department_report_not_accessible_by_normal_user(user_client,
                                                         factories):
    department = factories.DepartmentFactory()
    url = reverse('department-shift-report', kwargs={'pk': department.pk})
    response = user_client.get(url)
    assert response.status_code == 404


def test_department_report_accessible_by_dept_lead(user_client,
                                                   factories):
    department = factories.DepartmentFactory()
    department.leads.add(user_client.user)
    url = reverse('department-shift-report', kwargs={'pk': department.pk})
    response = user_client.get(url)
    assert response.status_code == 200


def test_department_report_accessible_by_admin_user(admin_client,
                                                    factories):
    department = factories.DepartmentFactory()
    department.leads.add(admin_client.user)
    url = reverse('department-shift-report', kwargs={'pk': department.pk})
    response = admin_client.get(url)
    assert response.status_code == 200
