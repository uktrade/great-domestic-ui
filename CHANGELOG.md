# Changelog

## Pre-release

**Implemented enhancements:**

- Added Google Analytics 360 tagging.
- Upgraded [CMS client][directory-cms-client] to allow `lookup_by_path`, to facilitate CMS tree based routing.
- Upgraded [CMS client][directory-cms-client] reduces noisy fallback cache logging.
- Upgraded [API client][directory-api-client], [Forms client][directory-forms-api-client], [SSO client][directory-sso-api-client], and [Companies House client][directory-companies-house-search-client].
- Added `DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS` env var.
- Added UKEF Home Page Endpoint([XOT-811])
- Added UKEF Project Finance Page Endpoint([XOT-812])
- Added UKEF Contact Form and Success Pages([XOT-816])
- Added UKEF Getting Ready Page [[XOT-813]]
- Added UKEF What We Offer Page [[XOT-815]]
- Added UKEF Country Cover Page [[XOT-817]]
- Added UKEF Home Page Endpoint [[XOT-811]]
- Added UKEF Project Finance Page Endpoint [[XOT-812]]
- Re-ordered URL parameters on /search page [[XOT-839]]
- Adjusted Market Access content [[MA-739]]
- Update teaser section on country guide pages [[CMS-1271]]
- Added Market Access tile to services pages [[MA-745]]
- Added redirect URLs for updated export advice articles [[CMS-1410]]
- Parse Event URLS to user facing urls [[XOT-830]]

**Fixed bugs:**
- Upgraded urllib3 to fix [vulnerability]
- Fix cookie notice banner from not being dismissible [[CMS-1441]] 
- Fix language cookie name and domain to be the same across all our services. [[CMS-1395]]


[directory-api-client]: https://github.com/uktrade/directory-api-client
[directory-client-core]: https://github.com/uktrade/directory-client-core
[directory-cms-client]: https://github.com/uktrade/directory-cms-client
[directory-forms-api-client]: https://github.com/uktrade/directory-forms-api-client
[directory-sso-api-client]: https://github.com/uktrade/directory-sso-api-client
[directory-companies-house-search-client]: https://github.com/uktrade/directory-companies-house-search-client
