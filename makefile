clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

test_requirements:
	pip install -r requirements_test.txt

FLAKE8 := flake8 . --exclude=migrations,.venv,node_modules
PYTEST := pytest . -n auto -v -vv --dist=loadfile --ignore=node_modules --cov=. --cov-config=.coveragerc --capture=no $(pytest_args)
COLLECT_STATIC := python manage.py collectstatic --noinput
COMPILE_TRANSLATIONS := python manage.py compilemessages
CODECOV := \
	if [ "$$CODECOV_REPO_TOKEN" != "" ]; then \
	   codecov --token=$$CODECOV_REPO_TOKEN ;\
	fi

translations:
	$(DEBUG_SET_ENV_VARS) && python manage.py makemessages -a

compile_translations:
	$(DEBUG_SET_ENV_VARS) && python manage.py compilemessages

test:
	$(COLLECT_STATIC) && $(COMPILE_TRANSLATIONS) && $(FLAKE8) && $(PYTEST) && $(CODECOV)

DJANGO_WEBSERVER := \
	python manage.py collectstatic --noinput && \
	python manage.py runserver 0.0.0.0:$$PORT

django_webserver:
	$(DJANGO_WEBSERVER)


DEBUG_SET_ENV_VARS := \
	export PORT=8007; \
	export SECRET_KEY=debug; \
	export DEBUG=true ;\
	export API_SIGNATURE_SECRET=debug; \
	export API_CLIENT_BASE_URL=http://api.trade.great:8000; \
	export SSO_SIGNATURE_SECRET=api_signature_debug; \
	export SSO_API_CLIENT_BASE_URL=http://sso.trade.great:8003/; \
	export SSO_PROXY_LOGIN_URL=http://sso.trade.great:8004/accounts/login/; \
	export SSO_PROXY_LOGOUT_URL=http://sso.trade.great:8004/accounts/logout/?next=http://exred.trade.great:8007; \
	export SSO_PROXY_SIGNUP_URL=http://sso.trade.great:8004/accounts/signup/; \
	export SSO_PROFILE_URL=http://profile.trade.great:8006/about/; \
	export SSO_PROXY_REDIRECT_FIELD_NAME=next; \
	export SSO_SESSION_COOKIE=debug_sso_session_cookie; \
	export SESSION_COOKIE_SECURE=false; \
	export GOOGLE_TAG_MANAGER_ID=; \
	export UTM_COOKIE_DOMAIN=.trade.great; \
	export CORS_ORIGIN_ALLOW_ALL=true; \
	export COMPANIES_HOUSE_CLIENT_ID=debug-client-id; \
	export COMPANIES_HOUSE_CLIENT_SECRET=debug-client-secret; \
	export SECURE_HSTS_SECONDS=0; \
	export DIRECTORY_CONSTANTS_URL_GREAT_DOMESTIC=http://exred.trade.great:8007; \
	export DIRECTORY_CONSTANTS_URL_GREAT_INTERNATIONAL=http://international.trade.great:8012/international/; \
	export DIRECTORY_CONSTANTS_URL_FIND_A_BUYER=http://buyer.trade.great:8001; \
	export DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS=http://soo.trade.great:8008; \
	export DIRECTORY_CONSTANTS_URL_FIND_A_SUPPLIER=http://supplier.trade.great:8005/; \
	export DIRECTORY_CONSTANTS_URL_INVEST=http://invest.trade.great:8012; \
	export DIRECTORY_CONSTANTS_URL_SINGLE_SIGN_ON=http://sso.trade.great:8004/; \
	export SERVICES_EXOPPS_ACTUAL=http://opportunities.export.great.gov.uk; \
	export SECURE_SSL_REDIRECT=false; \
	export HEALTH_CHECK_TOKEN=debug; \
	export DIRECTORY_UI_EXPORT_READINESS_COMTRADE_API_TOKEN=DEBUG; \
	export RECAPTCHA_PUBLIC_KEY=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI; \
	export RECAPTCHA_PRIVATE_KEY=6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe; \
	export CMS_URL=http://cms.trade.great:8010; \
	export CMS_SIGNATURE_SECRET=debug; \
	export FEATURE_PERFORMANCE_DASHBOARD_ENABLED=true; \
	export FEATURE_SEARCH_ENGINE_INDEXING_DISABLED=true; \
	export REDIS_URL=redis://localhost:6379; \
	export PRIVACY_COOKIE_DOMAIN=.trade.great; \
	export UKEF_FORM_SUBMIT_TRACKER_URL=http://go.pardot.com/l/590031/2018-08-16/5kj25l; \
	export DIRECTORY_FORMS_API_BASE_URL=http://forms.trade.great:8011; \
	export FEATURE_PROTOTYPE_PAGES_ENABLED=false; \
	export FEATURE_MARKETS_PAGES_ENABLED=true; \
	export FEATURE_NEWS_SECTION_ENABLED=false; \
	export FEATURE_CAMPAIGN_PAGES_ENABLED=true; \
	export FIND_A_SUPPLIER_CONTACT_URL=http://supplier.trade.great:8005/industries/contact/; \
	export EUEXIT_AGENT_EMAIL=test@example.com; \
	export FIND_A_SUPPLIER_CONTACT_URL=http://supplier.trade.great:8005/industries/contact/; \
	export FEATURE_EXPORT_JOURNEY_ENABLED=false; \
	export FEATURE_MARKET_ACCESS_ENABLED=false; \
	export FEATURE_MARKET_ACCESS_GOV_LINK_ENABLED=true; \
	export FEATURE_LANDING_PAGE_EU_EXIT_BANNER_ENABLED=true; \
	export COMMUNITY_ENQUIRIES_AGENT_EMAIL_ADDRESS=community@example.com \
	export FEATURE_NEW_HEADER_FOOTER_ENABLED=true; \
	export FEATURE_SEARCH_ENABLED=false; \
	export FEATURE_EXPORTING_TO_UK_ON_ENABLED=True; \
	export FEATURE_NEW_INTERNATIONAL_HEADER_ENABLED=true

TEST_SET_ENV_VARS := \
	export DIRECTORY_FORMS_API_BASE_URL=http://forms.trade.great:8011; \
	export DIRECTORY_FORMS_API_API_KEY=debug; \
	export DIRECTORY_FORMS_API_SENDER_ID=debug; \
	export DEBUG=false; \
	export EU_EXIT_ZENDESK_SUBDOMAIN=debug; \
	export REDIS_URL=; \
	export CONTACT_EVENTS_USER_NOTIFY_TEMPLATE_ID=debug; \
	export CONTACT_EVENTS_AGENT_NOTIFY_TEMPLATE_ID=debug; \
	export CONTACT_EVENTS_AGENT_EMAIL_ADDRESS=events@example.com; \
	export CONTACT_DSO_AGENT_NOTIFY_TEMPLATE_ID=debug; \
	export CONTACT_DSO_AGENT_EMAIL_ADDRESS=dso@example.com; \
	export CONTACT_DSO_USER_NOTIFY_TEMPLATE_ID=debug; \
	export CONTACT_DIT_AGENT_NOTIFY_TEMPLATE_ID=debug; \
	export CONTACT_DIT_AGENT_EMAIL_ADDRESS=dit@example.com; \
	export CONTACT_DIT_USER_NOTIFY_TEMPLATE_ID=debug; \
	export CONTACT_INVEST_AGENT_NOTIFY_TEMPLATE_ID=debug; \
	export CONTACT_INVEST_AGENT_EMAIL_ADDRESS=invest-overseas@example.com; \
	export CONTACT_INVEST_USER_NOTIFY_TEMPLATE_ID=debug; \
	export CONTACT_EXPORTING_USER_NOTIFY_TEMPLATE_ID=debug; \
	export CONTACT_INTERNATIONAL_AGENT_NOTIFY_TEMPLATE_ID=debug; \
	export CONTACT_INTERNATIONAL_AGENT_EMAIL_ADDRESS=international@example.com; \
	export CONTACT_INTERNATIONAL_USER_NOTIFY_TEMPLATE_ID=debug; \
	export CONTACT_BUYING_AGENT_NOTIFY_TEMPLATE_ID=debug; \
	export CONTACT_BUYING_AGENT_EMAIL_ADDRESS=buying@example.com; \
	export CONTACT_BUYING_USER_NOTIFY_TEMPLATE_ID=debug; \
	export CONTACT_EXPORTING_USER_NOTIFY_TEMPLATE_ID=debug; \
	export CONTACT_EXPORTING_AGENT_SUBJECT=exporting-subject; \
	export COMPANIES_HOUSE_API_KEY=debug; \
	export CONTACT_ENQUIRIES_AGENT_EMAIL_ADDRESS=domesitc-enquiries@example.com; \
	export ACTIVITY_STREAM_API_URL=https://www.nonworkingdomaintoraiseconnectionerror.com; \
	export ACTIVITY_STREAM_API_SECRET_KEY=debug; \
	export ACTIVITY_STREAM_API_ACCESS_KEY=debug; \
	export ACTIVITY_STREAM_API_IP_WHITELIST=debug; \
	export CONTACT_DEFRA_AGENT_EMAIL_ADDRESS=debug; \
	export CONTACT_BEIS_AGENT_EMAIL_ADDRESS=debug

debug_webserver:
	$(DEBUG_SET_ENV_VARS) && $(DJANGO_WEBSERVER)

debug_pytest:
	$(DEBUG_SET_ENV_VARS) && $(TEST_SET_ENV_VARS) && $(COLLECT_STATIC) && $(PYTEST)

debug_test:
	$(DEBUG_SET_ENV_VARS) && $(TEST_SET_ENV_VARS) && $(COLLECT_STATIC) && $(PYTEST) --cov-report=html

debug_test_last_failed:
	make debug_test pytest_args='-v --last-failed'

debug_manage:
	$(DEBUG_SET_ENV_VARS) && ./manage.py $(cmd)

debug_shell:
	$(DEBUG_SET_ENV_VARS) && ./manage.py shell

debug: test_requirements debug_test

compile_requirements:
	pip-compile requirements.in
	pip-compile requirements_test.in

upgrade_requirements:
	pip-compile --upgrade requirements.in
	pip-compile --upgrade requirements_test.in

new_redirect:
	python scripts/add_new_redirect.py

compile_css:
	./node_modules/.bin/gulp sass

watch_css:
	./node_modules/.bin/gulp sass:watch

.PHONY: clean test_requirements debug_webserver debug_test debug heroku_deploy_dev heroku_deploy_demo
