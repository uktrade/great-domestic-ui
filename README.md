# directory-ui-export-readiness

[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![snyk-image]][snyk]

**Export Readiness (Exred) - the Department for International Trade (DIT)**  

---
### See also:
| [directory-api](https://github.com/uktrade/directory-api) | [directory-ui-buyer](https://github.com/uktrade/directory-ui-buyer) | [directory-ui-supplier](https://github.com/uktrade/directory-ui-supplier) | [directory-ui-export-readiness](https://github.com/uktrade/directory-ui-export-readiness) |
| --- | --- | --- | --- |
| **[directory-sso](https://github.com/uktrade/directory-sso)** | **[directory-sso-proxy](https://github.com/uktrade/directory-sso-proxy)** | **[directory-sso-profile](https://github.com/uktrade/directory-sso-profile)** |  |

For more information on installation please check the [Developers Onboarding Checklist](https://uktrade.atlassian.net/wiki/spaces/ED/pages/32243946/Developers+onboarding+checklist)


## Development


We aim to follow [GDS service standards](https://www.gov.uk/service-manual/service-standard) and [GDS design principles](https://www.gov.uk/design-principles).


## Requirements
[Python 3.6](https://www.python.org/downloads/release/python-36/)

### SASS
We use SASS CSS pre-compiler. If you're doing front-end work your local machine will also need the following dependencies:

[node](https://nodejs.org/en/download/)

[SASS](https://rubygems.org/gems/sass/versions/3.4.22)

### Run JS tests with gulp or npm

    $ gulp test
    $ npm test

### Host environment variables for docker-compose
``.env`` files will be automatically created (with ``env_writer.py`` based on ``env.json``) by ``make docker_test``, based on host environment variables with ``DIRECTORY_UI_EXPORT_READINESS_`` prefix.

#### Web server

## Running locally

### Installing
    $ git clone https://github.com/uktrade/directory-ui-export-readiness
    $ cd directory-ui-export-readiness
    $ virtualenv .venv -p python3.5
    $ source .venv/bin/activate
    $ pip install -r requirements_test.txt

### Running the webserver
    $ source .venv/bin/activate
    $ make debug_webserver

### Running the tests

    $ make debug_test

### CSS development

When doing front-end development work you will need to be able to compile SASS to CSS. First run:

    $ npm install

Then:

    $ gulp sass

...to compile sass. You can also watch for changes by running:

    $ gulp sass:watch

We add compiled CSS files to version control. This will sometimes result in conflicts if multiple developers are working on the same SASS files. However, by adding the compiled CSS to version control we avoid having to install node, npm, node-sass, etc to non-development machines.

You should not edit CSS files directly, instead edit their SCSS counterparts.

## Session

Signed cookies are used as the session backend to avoid using a database. We therefore must avoid storing non-trivial data in the session, because the browser will be exposed to the data.

## Translations

Follow the <a href="https://docs.djangoproject.com/en/1.11/topics/i18n/" target="_blank">Django documentation</a>

To create or update `.po` files:

    $ make debug_manage cmd="makemessages"

To compile `.mo` files (no need to add these to source code, as this is done automatically during build):

    $ make debug_manage cmd="compilemessages"


## Geolocation

This product includes GeoLite2 (data created by MaxMind), available from
<a href="http://www.maxmind.com">http://www.maxmind.com</a>.

To download the data run the following command:

    $ make debug_manage cmd="download_geolocation_data"


## SSO
To make sso work locally add the following to your machine's `/etc/hosts`:

| IP Adress | URL                      |
| --------  | ------------------------ |
| 127.0.0.1 | buyer.trade.great    |
| 127.0.0.1 | supplier.trade.great |
| 127.0.0.1 | sso.trade.great      |
| 127.0.0.1 | api.trade.great      |
| 127.0.0.1 | profile.trade.great  |
| 127.0.0.1 | exred.trade.great    |

Then log into `directory-sso` via `sso.trade.great:8001`, and use `directory-ui-export-readiness` on `exred.trade.great:8001`

Note in production, the `directory-sso` session cookie is shared with all subdomains that are on the same parent domain as `directory-sso`. However in development we cannot share cookies between subdomains using `localhost` - that would be like trying to set a cookie for `.com`, which is not supported by any RFC.

Therefore to make cookie sharing work in development we need the apps to be running on subdomains. Some stipulations:
 - `directory-ui-export-readiness` and `directory-sso` must both be running on sibling subdomains (with same parent domain)
 - `directory-sso` must be told to target cookies at the parent domain.


[circle-ci-image]: https://circleci.com/gh/uktrade/directory-ui-export-readiness/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-ui-export-readiness/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/directory-ui-export-readiness/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-ui-export-readiness

[snyk-image]: https://snyk.io/test/github/uktrade/directory-ui-export-readiness/badge.svg
[snyk]: https://snyk.io/test/github/uktrade/directory-ui-export-readiness
