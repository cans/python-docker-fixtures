#!/bin/bash
set -eo pipefail
# shellcheck source=/dev/null
. ~/.venv/bin/activate

# Now we install our package
pip install --progress-bar=off /tmp/workspace/dockerfixtures*.whl
cat > validate.py <<EOF
import logging
import sys

import docker
from dockerfixtures import catalog, container


def main():
    logging.basicConfig()
    client = docker.from_env()
    try:
        with container.Container(catalog.PG_11, dockerclient=client) as cntr:
            cntr.wait((5432, 'tcp'), max_wait=10.0)
    except:
        logger.exception('Container did not start')
        raise
    print('Container started.', file=sys.stderr)


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
