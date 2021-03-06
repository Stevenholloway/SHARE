import logging

from furl import furl

from share.harvest.oai import OAIHarvester

logger = logging.getLogger(__name__)


class ZenodoHarvester(OAIHarvester):

    def do_harvest(self, start_date, end_date):
        url = furl(self.url)
        url.args['verb'] = 'ListRecords'
        url.args['metadataPrefix'] = 'oai_datacite3'
        url.args['set'] = 'openaire_data'

        if self.time_granularity:
            url.args['from'] = start_date.format('YYYY-MM-DDT00:00:00', formatter='alternative') + 'Z'
            url.args['until'] = end_date.format('YYYY-MM-DDT00:00:00', formatter='alternative') + 'Z'
        else:
            url.args['from'] = start_date.date().isoformat()
            url.args['until'] = end_date.date().isoformat()

        return self.fetch_records(url)
