=============================
Integration tests with docker
=============================

To run these tests, you need a running docker daemon on your system.

TODO (or not)
"""""""""""""

Provide means to configure the use of a remote docker daemon ?
Doesn't that require a different client
(:class:`docker.client.APIClient`), which changes the API ? (e.g. no
access to the `client.container.run()` function)


Notes
"""""

If you use docker's `exec` or `run` commands, make sure you do not use
the `-t` flag, which requires a tty to be allocated. Pytest's terminal
capture will mess with that and you test will fail.
