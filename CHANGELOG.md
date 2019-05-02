# Changelog

## Pre-release

**Implemented enhancements:**

- Added Google Analytics 360 tagging.
- Upgraded [CMS client][directory-cms-client] to allow `lookup_by_path`, to facilitate CMS tree based routing.
- Upgraded [CMS client][directory-cms-client] reduces noisy fallback cache logging.
- Upgraded [API client][directory-api-client], [Forms client][directory-forms-api-client], [SSO client][directory-sso-api-client], and [Companies House client][directory-companies-house-search-client].
- Added `DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS` env var.
- Added UKEF Home Page Endpoint([XOT-811](https://uktrade.atlassian.net/browse/XOT-811))
- Added UKEF Project Finance Page Endpoint([XOT-812](https://uktrade.atlassian.net/browse/XOT-812))
- Added UKEF Contact Form and Success Pages([XOT-816](https://uktrade.atlassian.net/browse/XOT-816))
- Added UKEF getting ready page([XOT-813](https://uktrade.atlassian.net/browse/XOT-813))
- [[XOT-811]](https://uktrade.atlassian.net/browse/XOT-811) Added UKEF Home Page Endpoint
- [[XOT-812]](https://uktrade.atlassian.net/browse/XOT-812) Added UKEF Project Finance Page Endpoint

**Fixed bugs:**
- Upgraded urllib3 to fix [vulnerability](https://nvd.nist.gov/vuln/detail/CVE-2019-11324)
- [[CMS-1441]](https://uktrade.atlassian.net/browse/CMS-1441) Fix cookie notice banner from not being dismissible



[directory-api-client]: https://github.com/uktrade/directory-api-client
[directory-client-core]: https://github.com/uktrade/directory-client-core
[directory-cms-client]: https://github.com/uktrade/directory-cms-client
[directory-forms-api-client]: https://github.com/uktrade/directory-forms-api-client
[directory-sso-api-client]: https://github.com/uktrade/directory-sso-api-client
[directory-companies-house-search-client]: https://github.com/uktrade/directory-companies-house-search-client
