# Changelog


## Pre-release

**Implemented enhancements:**
- CMS-1561 - Move CTAs on country guide page
- XOT-763 - Update GA360 tagging. **[Relies on this feature in directory-cms](https://github.com/uktrade/directory-cms/pull/487)**

**Fixed bugs:**


## [2019.06.04](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.06.04)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.05.30...2019.06.04)

**Implemented enhancements:**
- no ticket - Upgrade django rest framework to fix security vulnerability
- XOT-912 - Fix search rankings


## [2019.05.30](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.05.30)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.05.29...2019.05.30)

**Implemented enhancements:**
- XOT-909 - UKEF content image and layout updates.
- XOT-911 - UKEF pages CSS updates.


## [2019.05.29](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.05.29)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.05.22...2019.05.29)

**Implemented enhancements:**
- Added 'Event' to whitelisted search types
- CMS-1587 Add beijingexpo2019 marketing redirect
- XOT-841 - UKEF various template and content updates

**Fixed bugs:**
- XOT-804 - Fix rounded corners on iOS search button
- XOT-763 - Fix tagging key names and selector
- XOT-831 - Fix search results found text


## [2019.05.22](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.05.22)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.04.11...2019.05.22)

**Implemented enhancements:**

- [No ticket] Use events url from constants
- Added Google Analytics 360 tagging.
- Upgraded [CMS client][directory-cms-client] to allow `lookup_by_path`, to facilitate CMS tree based routing.
- Upgraded [CMS client][directory-cms-client] reduces noisy fallback cache logging.
- Upgraded [API client][directory-api-client], [Forms client][directory-forms-api-client], [SSO client][directory-sso-api-client], and [Companies House client][directory-companies-house-search-client].
- Added `DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS` env var.
- XOT-811 - Added UKEF Home Page Endpoint
- XOT-812 - Added UKEF Project Finance Page Endpoint
- XOT-896 - Updated UKEF Project Finance Page with new design.
- XOT-816 - Added UKEF Contact Form and Success Pages
- XOT-813 - Added UKEF Getting Ready Page
- XOT-815 - Added UKEF What We Offer Page
- XOT-817 - Added UKEF Country Cover Page
- XOT-900 - UKEF content updates
- XOT-839 - Re-ordered URL parameters on /search page
- MA-739 - Adjusted Market Access content
- CMS-1271 - Update teaser section on country guide pages
- MA-745 - Added Market Access tile to services pages
- CMS-1410 - Added redirect URLs for updated export advice articles
- MA-746 - Updated report a trade barrier form structure and content


**Fixed bugs:**
- Upgraded urllib3 to fix [vulnerability](https://nvd.nist.gov/vuln/detail/CVE-2019-11324)
- CMS-1441 - Fix cookie notice banner from not being dismissible
- CMS-1395 - Fix language cookie name and domain to be the same across all our services.
- XOT-830 - Parse Event URLS to user facing urls
- XOT-807 - Fix search result number format


[directory-api-client]: https://github.com/uktrade/directory-api-client
[directory-client-core]: https://github.com/uktrade/directory-client-core
[directory-cms-client]: https://github.com/uktrade/directory-cms-client
[directory-forms-api-client]: https://github.com/uktrade/directory-forms-api-client
[directory-sso-api-client]: https://github.com/uktrade/directory-sso-api-client
[directory-companies-house-search-client]: https://github.com/uktrade/directory-companies-house-search-client
