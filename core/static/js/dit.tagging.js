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
          addTaggingForEuExitBanner();
          addTaggingForHeroBannerVideo();
          addTaggingForServiceTeasers();
          addTaggingForAdviceTeasers();
          addTaggingForExporterStories();
        break;

        case 'ArticleListingPage':
          addTaggingForArticleList();
        break;

        case 'MarketPage':
          addTaggingForOpportunities();
          addTaggingForNextSteps();
        break;

        case 'MarketsLandingPage':
          addTaggingForMarketCtas();
        break;

        case 'AdviceLandingPage':
          addTaggingForAdviceCtas();
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

  function addTaggingForEuExitBanner() {
    $(".eu-exit-banner a").on("click", function() {
      window.dataLayer.push({
        'eventAction': 'ContentLink',
        'eventCategory': 'EuExit',
        'eventLabel': 'EuExitBanner',
        'eventValue': $(this).text().trim()
      });
    });
  }

  function addTaggingForHeroBannerVideo() {
    $("#hero-campaign-section-watch-video-button").on("click", function() {
      window.dataLayer.push({
        'eventAction': 'ContentLink',
        'eventCategory': 'Video',
        'eventLabel': 'HeroBannerVideoLink'
      });
    });
  }

  function addTaggingForServiceTeasers() {
    $("#services a").on("click", function() {
      window.dataLayer.push({
        'eventAction': 'Cta',
        'eventCategory': 'Service',
        'eventLabel': 'Link',
        'eventValue': $(this).find('h3').text().trim()
      });
    });
  }

  function addTaggingForAdviceTeasers() {
    $("#resource-advice a").on("click", function() {
      window.dataLayer.push({
        'eventAction': 'Cta',
        'eventCategory': 'Advice',
        'eventLabel': 'Link',
        'eventValue': $(this).find('h3').text().trim()
      });
    });
  }

  function addTaggingForExporterStories() {
    $("#carousel h3 a").on("click", function() {
      window.dataLayer.push({
        'eventAction': 'Cta',
        'eventCategory': 'ExporterStory',
        'eventLabel': 'Link',
        'eventValue': $(this).text().trim()
      });
    });
  }

  function addTaggingForSearch() {
    $("#search-results-information .search").on("submit", function() {
      window.dataLayer.push({
        'eventAction': 'Search',
        'eventCategory': 'General',
        'eventLabel': 'SearchForm',
        'eventValue': $(this).find("input[type='text']").val().trim()
      });
    });
  }

  function addTaggingForArticleList() {
    $("#article-list-page .article a").on("click", function() {
      window.dataLayer.push({
        'eventAction': 'ContentLink',
        'eventCategory': $(".article-list-page h1").text().trim(),
        'eventLabel': 'Article',
        'eventValue': $(this).text().trim()
      });
    });
  }

  function addTaggingForOpportunities() {
    $("#country-guide-accordions .ExpanderControl").on("click", function() {
      window.dataLayer.push({
        'eventAction': 'ExpressInterest',
        'eventLabel': 'ExpanderControl',
        'eventValue': $(this).text().trim()
      });
    });

    $(".sector-ctas a").on("click", function() {
      // Selector is quite fragile and could be benefit from
      // use of functional class names in the target code.
      window.dataLayer.push({
        'eventAction': 'Cta',
        'eventCategory': $(this).parents("li").children().eq(0).text().trim().trim(),
        'eventLabel': 'SectorRelatedCta',
        'eventValue': $(this).text().trim()
      });
    });
  }

  function addTaggingForNextSteps() {
    $("#country-guide-need-help-section .cta-link").on("click", function() {
      window.dataLayer.push({
        'eventAction': 'Cta',
        'eventLabel': 'NextStepCta',
        'eventValue': $(this).text().trim()
      });
    });
  }

  function addTaggingForMarketCtas() {
    $(".topic-list-section .card-link").on("click", function() {
      window.dataLayer.push({
        'eventAction': 'Cta',
        'eventLabel': 'MarketCta',
        'eventValue': $(this).find("h3").text().trim()
      });
    });
  }

  function addTaggingForAdviceCtas() {
    $(".topic-list-section .card-link").on("click", function() {
      window.dataLayer.push({
        'eventAction': 'Cta',
        'eventLabel': 'AdviceCta',
        'eventValue': $(this).find("h3").text().trim()
      });
    });
  }

  function addTaggingForServiceCtas() {
    $(".card-link").on("click", function() {
      window.dataLayer.push({
        'eventAction': 'Cta',
        'eventLabel': 'ServiceCta',
        'eventValue': $(this).find("h3").text().trim()
      });
    });
  }
});
