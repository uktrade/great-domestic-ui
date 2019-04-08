# great-domestic-ui

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gitflow-image]][gitflow]
[![calver-image]][calver]

**GREAT.gov.uk, Domestic facing FE service - the Department for International Trade (DIT)**  

---

## Development

### Installing
    $ git clone https://github.com/uktrade/great-domestic-ui
    $ cd great-domestic-ui
    $ virtualenv .venv -p python3.6
    $ source .venv/bin/activate
    $ pip install -r requirements_test.txt


### Requirements
[Python 3.6](https://www.python.org/downloads/release/python-366/)

[Redis](https://redis.io/)


### Configuration

Secrets such as API keys and environment specific configurations are placed in `conf/.env` - a file that is not added to version control. You will need to create that file locally in order for the project to run.

Here is an example `conf/.env` with placeholder values to get you going:

```
COMPANIES_HOUSE_API_KEY=debug
DIRECTORY_FORMS_API_API_KEY=debug
DIRECTORY_FORMS_API_SENDER_ID=debug
EU_EXIT_ZENDESK_SUBDOMAIN=debug
CONTACT_EVENTS_AGENT_EMAIL_ADDRESS=debug
CONTACT_DSO_AGENT_EMAIL_ADDRESS=debug
CONTACT_DIT_AGENT_EMAIL_ADDRESS=debug
CONTACT_INTERNATIONAL_AGENT_EMAIL_ADDRESS=debug
CONTACT_ENQUIRIES_AGENT_EMAIL_ADDRESS=debug
EXPORTING_OPPORTUNITIES_API_BASE_URL=debug
EXPORTING_OPPORTUNITIES_API_SECRET=debug
EXPORTING_OPPORTUNITIES_SEARCH_URL=debug
GET_ADDRESS_API_KEY=debug
ACTIVITY_STREAM_API_ACCESS_KEY=123
ACTIVITY_STREAM_API_IP_WHITELIST=1.2.3.4
ACTIVITY_STREAM_API_SECRET_KEY=123
ACTIVITY_STREAM_API_URL=http://localhost:8080/v1/objects
CONTACT_DEFRA_AGENT_EMAIL_ADDRESS=debug
CONTACT_BEIS_AGENT_EMAIL_ADDRESS=debug
```

### Running the webserver
    $ source .venv/bin/activate
    $ make debug_webserver

You must have the directory-cms project running locally to run this project.

### Running the tests

    $ make debug_test

## CSS development

We use SASS CSS pre-compiler. If you're doing front-end work your local machine will also need the following dependencies:

[node](https://nodejs.org/en/download/)
[SASS](https://rubygems.org/gems/sass/versions/3.4.22)

Then run:

    $ npm install yarn
    $ yarn install --production=false

We add compiled CSS files to version control. This will sometimes result in conflicts if multiple developers are working on the same SASS files. However, by adding the compiled CSS to version control we avoid having to install node, npm, node-sass, etc to non-development machines.

You should not edit CSS files directly, instead edit their SCSS counterparts.

### Update CSS under version control

    $ make compile_css


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
| 127.0.0.1 | cms.trade.great      |


Then log into `directory-sso` via `sso.trade.great:8001`, and use `great-domestic-ui` on `exred.trade.great:8001`

Note in production, the `directory-sso` session cookie is shared with all subdomains that are on the same parent domain as `directory-sso`. However in development we cannot share cookies between subdomains using `localhost` - that would be like trying to set a cookie for `.com`, which is not supported by any RFC.

Therefore to make cookie sharing work in development we need the apps to be running on subdomains. Some stipulations:
 - `great-domestic-ui` and `directory-sso` must both be running on sibling subdomains (with same parent domain)
 - `directory-sso` must be told to target cookies at the parent domain.


## Helpful links
* [Developers Onboarding Checklist](https://uktrade.atlassian.net/wiki/spaces/ED/pages/32243946/Developers+onboarding+checklist)
* [Gitflow branching](https://uktrade.atlassian.net/wiki/spaces/ED/pages/737182153/Gitflow+and+releases)
* [GDS service standards](https://www.gov.uk/service-manual/service-standard)
* [GDS design principles](https://www.gov.uk/design-principles)

## Related projects:
https://github.com/uktrade?q=directory
https://github.com/uktrade?q=great

[code-climate-image]: https://codeclimate.com/github/uktrade/great-domestic-ui/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/great-domestic-ui

[circle-ci-image]: https://circleci.com/gh/uktrade/great-domestic-ui/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/great-domestic-ui/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/great-domestic-ui/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/great-domestic-ui

[gitflow-image]: https://img.shields.io/badge/Branching%20strategy-gitflow-5FBB1C.svg
[gitflow]: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow

[calver-image]: https://img.shields.io/badge/Versioning%20strategy-CalVer-5FBB1C.svg
[calver]: https://calver.org
    
