// GREAT Specific Tagging Functionality.
// -------------------------------------
// REQUIRES
// jQuery
// dit.js


dit.tagging.domestic = (new function() {

  this.init = function(page) {
    $(document).ready(function() {
      switch(page) {
        case 'LandingPage':
          addTaggingForLandingPage();
        break;

        case 'ArticleListingPage':
          addTaggingForArticleList();
        break;

        case 'CountryGuidePage':
          addTaggingForCountryGuidePage();
        break;

        case 'MarketsLandingPage':
          addTaggingForMarketsLandingPage();
        break;

        case 'AdviceLandingPage':
          addTaggingForAdviceLandingPage();
        break;

        case 'SearchResultsPage':
          addTaggingForSearch();
        break;

        case 'ServicesLandingPage':
          addTaggingForServiceCtas();
        break;

        default: // nothing
      }
    });
  }

  function addTaggingForLandingPage() {
    $(".eu-exit-banner a").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'ContentLink',
        'type': 'EuExit',
        'element': 'EuExitBanner',
        'value': $(this).text().trim()
      });
    });

    $("#hero-campaign-section-watch-video-button").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'ContentLink',
        'type': 'Video',
        'element': 'HeroBannerVideoLink'
      });
    });

    $("#services a").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'type': 'Service',
        'element': 'Link',
        'value': $(this).find('h3').text().trim()
      });
    });

    $("#resource-advice a").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'type': 'Advice',
        'element': 'Link',
        'value': $(this).find('h3').text().trim()
      });
    });

    $("#carousel .casestudy-link").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'type': 'ExporterStory',
        'element': 'Link',
        'value': $(this).text().trim()
      });
    });
  }

  function addTaggingForArticleList() {
    $("#article-list-page .article a").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'ContentLink',
        'type': $(".article-list-page h1").text().trim(),
        'element': 'Article',
        'value': $(this).text().trim()
      });
    });
  }

  function addTaggingForCountryGuidePage() {
    $("#country-guide-accordions .ExpanderControl").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'ExpressInterest',
        'element': 'ExpanderControl',
        'value': $(this).text().trim()
      });
    });

    $("#country-guide-intro-ctas li .intro-cta-link").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'element': 'IntroRelatedCta',
        'value': $(this).text().trim()
      });
    });

    $("#country-guide-need-help-section .cta-link").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'element': 'NextStepCta',
        'value': $(this).text().trim()
      });
    });
  }

  function addTaggingForMarketsLandingPage() {
    $("#markets-list-section .card-link").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'element': 'MarketCta',
        'value': $(this).find("h3").text().trim()
      });
    });
  }

  function addTaggingForAdviceLandingPage() {
    $("#advice-list-section .card-link").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'element': 'AdviceCta',
        'value': $(this).find("h3").text().trim()
      });
    });
  }

  function addTaggingForSearch() {
    $("#search-form").on("submit", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Search',
        'type': 'General',
        'element': 'SearchForm',
        'value': $("#search-again-input").val().trim()
      });
    });
  }

  function addTaggingForServiceCtas() {
    $("#services-list-section .card-link").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'element': 'ServiceCta',
        'value': $(this).find("h3").text().trim()
      });
    });
  }
});
