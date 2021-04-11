#!/bin/bash
set -eo pipefail
# shellcheck source=/dev/null
. ~/.venv/bin/activate

# Now we install our package
pip install --progress-bar=off /tmp/workspace/dockerfixtures*.whl
cat > validate.py <<EOF
import logging
import os
import sys

import docker
from dockerfixtures import catalog, container, ci
from dockerfixtures.image import Image


def main():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()
    client = None
    if 'VIRTUAL_MACHINE' in os.environ:
        client = docker.from_env()
    cntr_gen = container.ci_fixture(client,
                                    Image('subfuzion/netcat'),
                                    command=['nc', '-vl', '9876'])
    try:
        cntr = next(cntr_gen)
        logger.info('Container address is: "%s"', cntr.address)
        cntr.wait((9876, 'tcp'), max_wait=10.0)
    except:
        logger.exception('Container did not start')
        raise
    finally:
        next(cntr_gen, None)
    logger.info('Container started.')


if __name__ == '__main__':
    main()
EOF

echo "***************************************************************************"
echo "Package validation script"
echo "==========================================================================="
cat validate.py
echo "==========================================================================="

python validate.py
rm validate.py
