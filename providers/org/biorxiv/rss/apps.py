from django.utils.functional import cached_property

from share.provider import ProviderAppConfig
from .harvester import BiorxivHarvester


class AppConfig(ProviderAppConfig):
    name = 'providers.org.biorxiv.rss'
    version = '0.0.0'
    title = 'biorxiv'
    long_title = 'bioRxiv'
    home_page = 'http://biorxiv.org/'
    rate_limit = (1, 3)
    url = 'http://connect.biorxiv.org/biorxiv_xml.php?subject=all'
    time_granularity = False
    harvester = BiorxivHarvester
    disabled = True

    namespaces = {
        'http://purl.org/rss/1.0/': None,
        'http://purl.org/dc/elements/1.1/': 'dc',
    }

    @cached_property
    def user(self):
        from share.models import ShareUser
        return ShareUser.objects.get(robot='providers.org.biorxiv')
