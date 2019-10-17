# Changelog

## Pre-release

### Implemented enhancements
- XOT-1155 - amends to video modal transcript height issue, restyle close button
- XOT-1121 - market landing page changes and search pagination
- XOT-1155 - change related link field from rich text to string
- XOT-1151, XOT-1152, XOT-1137, XOT-1153, XOT-1155 - homepage redesigns v2
- XOT-1129 - add selector form to market landing page
- XOT-1122 - add sector selector and top sectors to homepage
- XOT-1123 - Add filtering by industry tag to markets landing page
- XOT-1118 - use CMS heading for page title
- XOT-1121 - add pagination to markets landing page, limit 12 per page
- XOT-1042 - restyle markets grid and some elements of landing page
- No ticket - Rename 'article' app folder to 'content'
- XOT-1107 - Add url for new article landing pages
- XOT-1078 - UKEF contact us button text issue on small resolutions
- XOT-1039 - Add campaign section with video
- no ticket - Upgrade to Django 2
- XOT-928 - Use user profile phone number on contact form

### Fixed bugs
- XOT-1042 - remove extra container markup
- no ticket - Fix international urls in develop and staging.
- no ticket - Silence captcha key checks

## [2019.09.23_1](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.09.23_1)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.09.23...2019.09.23_1)

### Hotfix
- Re-add case insensitive urls

## [2019.09.23](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.09.23)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.09.04_1...2019.09.23)

### Implemented enhancements
- XOT-1114 add video transcript to article page
- GTRANSFORM-368 update directory components version for list bullet colour
- GTRANSFORM-368 info_page now extends article/base for missing css
- GTRANSFORM-368 setup accessibility statement footer link and add href target template tag
- XOT-920 - add space before/after quote
- XOT-920 - fix spacing style issue in cms article template
- GTRANSFORM-213 - add labels to textareas identified in accessibility audit
- GTRANSFORM-238 - page heading fixes
- GTRANSFORM-238 - use page heading in the page title
- XOT-914 - Add search sort order healthcheck with feature flag
- XOT-1034 - Add new landing page, remove obsolete international page styling, update metadata for cms pages
- TT-1808: Update directory components to add "no-validate" no cache middleware
- No ticket - Add trade barriers to search
- CI-501 - Added redirect from `/contact/triage/international/` to new great-international-ui url `/international/contact`
- XOT-928 - Add user full name from new registration journey to SOO contact form

### Bug fixes
- No ticket - Fix report a trade barrier link in search-key-pages.json
- No ticket - Fix 500 error on UKEF contact form
- XOT-1115 - Fix IE hero bug, fix missing image on country guide hero, fix text colour on trade finance hero
- TT-1832 - Fix anon users unable to view feedback page
- TT-1816 - Upgrade directory components to fix js in non-chrome

## [2019.09.04_1](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.09.04_1)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.08.21...2019.09.04_1)

### Hotfix
- No ticket - Fix /community/join/ breadcrumbs

## [2019.09.04](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.09.04)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.08.21...2019.09.04)

### Implemented enhancements
- CMS-1754 - (Follow-up) Remove unused international form views (now in great international UI), move international Brexit contact form url into settings
- No ticket - route marketaccess requests to EU Exit zendesk
- No ticket - fix typo in email market access review form step
- XOT-920 - hide article type to prevent rendering of None and add missing subheading field
- GTRANSFORM-363 - Ensure market access summary page reflects the forms, add missing answers to questions
- No ticket - remove comma in report-trade-barriers 'Tell us what you’ve done to resolve your problem, even if this is your first step' error msg, that causes error message to render incorrectly
- No ticket - Fix /legal redirect
- XOT-920 - combined article/case study/blog template, full width quote section from cms content
- CMS-1754 - Rename EU Exit urls to Brexit
- CMS-1839 - Use correct header on international contact success page
- No ticket - Cleaned up old redirects to use new urls, removed old international pages
- GTRANSFORM-338 - adding add_href_tag to cms content pages
- XOT-1028 - Sightly update SSO contribution to SOO application form
- No ticket - Add export vouchers form


## [2019.08.21](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.08.21)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.08.20...2019.08.21)

### Implemented enhancements
- CMS-1824 - Fix redirect
- CMS-1824 - Red arrows redirect
- No ticket - Tidied up form choices with feature flags


## [2019.08.20](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.08.20)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.08.13...2019.08.20)

### Implemented enhancements
- XOT-1007 - remove hyperlink from title
- XOT-1007 - change content on search contact form
- GTRANSFORM-345 - missed external links attributes added to case studies
- GTRANSFORM-346 - Directory Component upgrade 27.6.0 - footer and card component changes
- GTRANSFORM-345 - add external link helper text
- CI-427 - Added Capital Invest contact form to International triage behind feature flag `CAPITAL_INVEST_CONTACT_IN_TRIAGE_ON`
- CMS-1764 - Added redirect for New Zealand events
- CMS-1756 - International trade and investment support directory redirect

### Fixed bugs
- No ticket - Fixed capital invest contact form in triage being behind a feature flag


## [2019.08.13](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.08.13)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.08.05...2019.08.13)

### Implemented enhancements
- GTRANSFORM-241 - Remove carousel and outdated case study from the homepage, make responsive column classes consistent across pages
- No ticket - Remove number of guides and publish date from cards, remove number of articles from article listing page hero.
- XOT-989 - remove Content from breadcrumbs for SOO market sign up
- XOT-968 - Fix security issues raised by latest pen test

### Fixed bugs
- GTRANSFORM-241 (Follow-up) - Fix services cards images not being displayed
- GTRANSFORM-241 - Content tweak
- No ticket - Fix card images being stretched, fix missing services page breadcrumbs
- XOT-991 - add container div to community export advocates form to fix alignment issue
- XOT-989 - add breadcrumb block to wizard-domestic to allow overrides
- No ticket - Upgrade django to 1.11.23

## [2019.08.05](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.08.05)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.08.01...2019.08.05)

### Implemented enhancements
- XOT-977 - breadcrumb change using cms page.title
- XOT-977 - change url to relative
- XOT-977 - additional text changes to marketing form success page
- CMS-1762 - Make advice article urls less restrictive to allow content editors to publish without dev work
- XOT-977 - text change
- XOT-977 - change postcode to use ukpostcodeutils, update breadcrumb text


## [2019.08.01](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.08.01)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.07.23...2019.08.01)

### Implemented enhancements
- CMS-1743 - Add redirect for Australia events
- XOT-977 - Add marketing campaigns form, original clone of community join-form
- No ticket - Consistent use of breadcrumbs component
- TT-1678 - Rename EU exit to Brexit

## [2019.07.23](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.07.23)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.07.16...2019.07.23)

### Implemented enhancements
- XOT-958 - bugfixes for XOT-922 (css changes, added cms_breadcrumbs, fixed template footer markup and hide block if fields not populated)
- XOT-914 - Add automated tests for search sort order
- XOT-906 - Update wording on search feedback form
- XOT-943 - Rename market and opportunity search classifiers in Search

### Fixed bugs
- TT-1602 - Fix radio buttons on /contact/domestic/
- No ticket - Fixed no GA bug on /community/success/

## [2019.07.16](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.07.16)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.06.26...2019.07.16)

### Implemented enhancements

XOT-922 - Marketing Article Page template [this relies on CMS change]
CMS-1666 - Upgraded directory-components to version 20.0.0 (Updated breadcrumbs tags and GA360 stuff to reflect the latest changes)
CMS-1666 - Upgraded directory-constants to 18.0.0

### Fixed bugs

TT-1602 - Fix radio buttons on /contact/domestic/
No ticket - Upgrade vulnerable django version to django 1.11.22


## [2019.06.26](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.06.26)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.06.19...2019.06.26)

### Implemented enhancements
- XOT-906 - Add feedback form to search

### Fixed bugs
- TT-1580 - Prevent duplicate "company type" showing on contact form
- TT-1579 invalid postcode fails on contact us
- XOT-913 Fixed various content issues on UKEF pages

## [2019.06.19](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.06.19)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.06.06...2019.06.19)

### Implemented enhancements
- [No ticket] - Fix missing breadcrumbs on services landing page
- XOT-763 - Add tagging for domestic header
- XOT-763 - Update GA360 tagging. **[Relies on this feature in directory-cms](https://github.com/uktrade/directory-cms/pull/487)**
- TT-1547 - Add redirects for events

### Fixed bugs
- TT-1449 - Added fieldset and legend html elements on related form fields
- TT-1450 - accessibility change h2 to h1
- TT-1452 - add label to contact us captcha's
- TT-1454/TT-1453 duplicate ids and empty links on finance contact-us
- XOT-934 Deleted unused CSS files from UKEF templates
- XOT-939 Fixed camel case URLs redirection for UKEF pages
- No ticket - upgrade django to fix vulnerability

## [2019.06.06](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.06.06)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.06.04...2019.06.06)

### Implemented enhancements
- CMS-1561 - Move CTAs on country guide page

## [2019.06.04](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.06.04)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.05.30...2019.06.04)

### Implemented enhancements
- no ticket - Upgrade django rest framework to fix security vulnerability
- XOT-912 - Fix search rankings


## [2019.05.30](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.05.30)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.05.29...2019.05.30)

### Implemented enhancements
- XOT-909 - UKEF content image and layout updates.
- XOT-911 - UKEF pages CSS updates.


## [2019.05.29](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.05.29)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.05.22...2019.05.29)

### Implemented enhancements
- Added 'Event' to whitelisted search types
- CMS-1587 Add beijingexpo2019 marketing redirect
- XOT-841 - UKEF various template and content updates

### Fixed bugs
- XOT-804 - Fix rounded corners on iOS search button
- XOT-763 - Fix tagging key names and selector
- XOT-831 - Fix search results found text


## [2019.05.22](https://github.com/uktrade/great-domestic-ui/releases/tag/2019.05.22)
[Full Changelog](https://github.com/uktrade/great-domestic-ui/compare/2019.04.11...2019.05.22)

### Implemented enhancements

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


### Fixed bugs
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
