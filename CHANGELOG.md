# Changelog

## Pre-release

**Implemented enhancements:**

- Added Google Analytics 360 tagging.
- Upgraded [CMS client][directory-cms-client] to allow `lookup_by_path`, to facilitate CMS tree based routing.
- Upgraded [CMS client][directory-cms-client] reduces noisy fallback cache logging.
- Upgraded [API client][directory-api-client], [Forms client][directory-forms-api-client], [SSO client][directory-sso-api-client], and [Companies House client][directory-companies-house-search-client].
- Added `DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS` env var.
- XOT-811 - Added UKEF Home Page Endpoint
- XOT-812 - Added UKEF Project Finance Page Endpoint
- XOT-816 - Added UKEF Contact Form and Success Pages
- XOT-813 - Added UKEF Getting Ready Page
- XOT-815 - Added UKEF What We Offer Page
- XOT-817 - Added UKEF Country Cover Page
- XOT-811 - Added UKEF Home Page Endpoint
- XOT-812 - Added UKEF Project Finance Page Endpoint
- XOT-839 - Re-ordered URL parameters on /search page
- MA-739 - Adjusted Market Access content
- CMS-1271 - Update teaser section on country guide pages
- MA-745 - Added Market Access tile to services pages
- CMS-1410 - Added redirect URLs for updated export advice articles
- XOT-830 - Parse Event URLS to user facing urls

**Fixed bugs:**
- Upgraded urllib3 to fix [vulnerability]
- CMS-1441 - Fix cookie notice banner from not being dismissible 
- CMS-1395 - Fix language cookie name and domain to be the same across all our services.


[directory-api-client]: https://github.com/uktrade/directory-api-client
[directory-client-core]: https://github.com/uktrade/directory-client-core
[directory-cms-client]: https://github.com/uktrade/directory-cms-client
[directory-forms-api-client]: https://github.com/uktrade/directory-forms-api-client
[directory-sso-api-client]: https://github.com/uktrade/directory-sso-api-client
[directory-companies-house-search-client]: https://github.com/uktrade/directory-companies-house-search-client
