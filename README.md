# yopass-cli

[![Build Status](https://travis-ci.org/zsolt-halo/yopass-cli.svg?branch=master)](https://travis-ci.org/zsolt-halo/yopass-cli)

[![PyPI version](https://badge.fury.io/py/yopass-cli.svg)](https://badge.fury.io/py/yopass-cli)

This is a command-line tool to interact with a (the) [yopass backend](https://github.com/jhaals/yopass) created by [Johan Haals](https://github.com/jhaals).
Even though it is possible to use the service via the [web-frontend](https://yopass.se) I felt the necessity of a cli tool to use this awesome software in our automation projects. 

This cli tool uses [sjcl](https://pypi.org/project/sjcl/) (just like the web-frontend) to perform encryption on the client side thus preventing your secret from ever leaving your os in a _cleartext_ form.

### Installation

yopass-cli requires [python3](https://www.python.org/downloads/)+ to run.

    $ pip install --user yopass-cli

Make sure to have the following 2 environment variables set before using:

- YOPASS_BACKEND_URL
- YOPASS_FRONTEND_URL
 
        $ export YOPASS_BACKEND_URL=https://api.yopass.se
        $ export YOPASS_FRONTEND_URL=https://yopass.se

If you use your own server, the front and backend URLs can be the same. For
example: `https://yopass.domain.net`

### Usage

    yopass-cli send [OPTIONS] SECRET
    cat <filename> | yopass-cli send [OPTIONS]
    echo "<my passphrase" | yopass-cli send [OPTIONS]
    yopass-cli get [OPTIONS] SID PASSPHRASE

Send Options:

    --expires [1h|1d|1w]
    --outmode [verbose|one-click-link|short-link|id]
    --outformat [plain|json]

Get Options:

    --outformat [plain|json]

### Todos

 - testing
 - proper README

License
----

MIT

**Free Software, Hell Yeah!**

Contribution is welcome :) 🍺Cheers 🍺
