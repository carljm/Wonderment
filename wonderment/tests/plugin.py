import os

import cov_core
import pytest
from pytest_cov import CovPlugin


def pytest_addoption(parser):
    parser.addoption(
        '--no-cov', action='store_false', dest='coverage', default=True)


@pytest.mark.tryfirst
def pytest_configure(config):
    """Record coverage unless --no-cov flag given."""
    if config.getoption('coverage'):
        config.option.cov_source.append('wonderment')
        config.option.cov_report.append('html')
        if not config.pluginmanager.hasplugin('_cov'):
            plugin = CovPlugin(config.option, config.pluginmanager)
            config.pluginmanager.register(plugin, '_cov')

# Override pytest-cov's default implementation with our customized version
OldCentral = cov_core.Central


class Central(OldCentral):
    """Reports total coverage percentage on one line."""
    def summary(self, stream):
        OldCentral.summary(self, stream)

        with open(os.devnull, 'w') as null:
            pct = int(self.cov.report(ignore_errors=True, file=null))
        stream.write('Overall test coverage: {}%\n'.format(pct))

cov_core.Central = Central
