import django_tables2 as tables


class BootstrapTable(tables.Table):
    class Meta:
        template = 'admin/partials/table.html'
        attrs = {
            'class': 'table table-striped table-bordered',
        }
