import os

import cov_core

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
