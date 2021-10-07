#!/usr/bin/env python3
# Copyright 2021 Facundo Ciccioli
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

import hashlib

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus


class CharmProxyThrukAgent(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on['thruk-agent'].relation_changed,
                               self._update_thruk_agent_relation)
        self.framework.observe(self.on.config_changed, self._update_thruk_agent_relation)

        self.unit.status = ActiveStatus()

    def _update_thruk_agent_relation(self, event):
        thruk_data = {
            'url': self.config['url'],
            'nagios_context': self.config['nagios_context'],
            'thruk_key': self.config['thruk_key'],
            'thruk_id': hashlib.md5(self.config['nagios_context'].encode('utf-8')).hexdigest(),
        }

        for ta_relation in self.model.relations['thruk-agent']:
            ta_relation.data[self.model.unit].update(thruk_data)


if __name__ == "__main__":
    main(CharmProxyThrukAgent)
