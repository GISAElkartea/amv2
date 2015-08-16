from django.utils.translation import ugettext_lazy as _

from grappelli.dashboard import modules, Dashboard


class AntxetamediaDashboard(Dashboard):
    def init_with_context(self, context):
        self.children.append(modules.Group(
            title=_('Main content'),
            column=1,
            collapsible=True,
            children=[
                modules.ModelList(
                    _('News'),
                    collapsible=True,
                    column=1,
                    css_classes=('grp-collapse grp-closed',),
                    models=('antxetamedia.news.*',),
                ),
                modules.ModelList(
                    _('Radio'),
                    collapsible=True,
                    column=1,
                    css_classes=('grp-collapse grp-closed',),
                    models=('antxetamedia.radio.*',),
                ),
                modules.ModelList(
                    _('Events'),
                    collapsible=True,
                    column=1,
                    css_classes=('grp-collapse grp-closed',),
                    models=('antxetamedia.events.*',),
                ),
            ]
        ))

        self.children.append(modules.Group(
            title=_('Others'),
            column=1,
            collapsible=True,
            css_classes=('grp-collapse',),
            children=[
                modules.ModelList(
                    _('Projects'),
                    collapsible=True,
                    column=1,
                    css_classes=('grp-collapse grp-closed',),
                    models=('antxetamedia.projects.*',),
                ),
                modules.ModelList(
                    _('Flatpages'),
                    collapsible=True,
                    column=1,
                    css_classes=('grp-collapse grp-closed',),
                    models=('antxetamedia.flatpages.*',),
                ),
                modules.ModelList(
                    _('Schedule'),
                    collapsible=True,
                    column=1,
                    css_classes=('grp-collapse grp-closed',),
                    models=('antxetamedia.schedule.*',),
                ),
                modules.ModelList(
                    _('Widgets'),
                    collapsible=True,
                    column=1,
                    css_classes=('grp-collapse grp-closed',),
                    models=('antxetamedia.widgets.*',),
                ),
            ]
        ))

        self.children.append(modules.ModelList(
            _('Blobs'),
            collapsible=True,
            column=1,
            css_classes=('grp-collapse',),
            models=('antxetamedia.blobs.*',),
        ))

        self.children.append(modules.ModelList(
            _('Admin'),
            collapsible=True,
            column=1,
            css_classes=('grp-collapse grp-closed',),
            models=('django.contrib.auth.*', 'django.contrib.sites.*'),
        ))

        self.children.append(modules.LinkList(
            _('Support'),
            column=2,
            children=[
                {
                    'title': _('User documentation'),
                    'url': 'https://gisaelkartea.github.io/amv2/users/',
                    'external': True,
                },
                {
                    'title': _('Contact'),
                    'url': 'mailto:unai@gisa-elkartea.org',
                    'external': True,
                },
            ]
        ))

        self.children.append(modules.Feed(
            title=_('Latest development changes'),
            column=2,
            feed_url='https://github.com/GISAElkartea/amv2/commits/master.atom',
            limit=5,
        ))

        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))
