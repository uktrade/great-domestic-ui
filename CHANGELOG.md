# Changelog

## Pre-release

**Implemented enhancements:**

- Added Google Analytics 360 tagging.
- Upgraded [CMS client][directory-cms-client] to allow `lookup_by_path`, to facilitate CMS tree based routing.
- Upgraded [CMS client][directory-cms-client] reduces noisy fallback cache logging.
- Upgraded [API client][directory-api-client], [Forms client][directory-forms-api-client], [SSO client][directory-sso-api-client], and [Companies House client][directory-companies-house-client] because [CMS client][directory-cms-client] upgrade results in [Client core][directory-client-core] being upgraded.
- Added `DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS` env var.


[directory-cms-client]: https://github.com/uktrade/directory-cms-client
[directory-api-client]: https://github.com/uktrade/directory-api-client
[directory-forms-api-client]: https://github.com/uktrade/directory-forms-api-client
[directory-cms-client]: https://github.com/uktrade/directory-cms-client
[directory-client-core]: https://github.com/uktrade/directory-client-core
