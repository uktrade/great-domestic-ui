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
        'event': 'gaEvent',
        'action': 'ContentLink',
        'type': 'EuExit',
        'element': 'EuExitBanner',
        'value': $(this).text().trim()
      });
    });
  }

  function addTaggingForHeroBannerVideo() {
    $("#hero-campaign-section-watch-video-button").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'ContentLink',
        'type': 'Video',
        'element': 'HeroBannerVideoLink'
      });
    });
  }

  function addTaggingForServiceTeasers() {
    $("#services a").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'type': 'Service',
        'element': 'Link',
        'value': $(this).find('h3').text().trim()
      });
    });
  }

  function addTaggingForAdviceTeasers() {
    $("#resource-advice a").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'type': 'Advice',
        'element': 'Link',
        'value': $(this).find('h3').text().trim()
      });
    });
  }

  function addTaggingForExporterStories() {
    $("#carousel h3 a").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'type': 'ExporterStory',
        'element': 'Link',
        'value': $(this).text().trim()
      });
    });
  }

  function addTaggingForSearch() {
    $("#search-results-information .search").on("submit", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Search',
        'type': 'General',
        'element': 'SearchForm',
        'value': $(this).find("input[name='q']").val().trim()
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

  function addTaggingForOpportunities() {
    $("#country-guide-accordions .ExpanderControl").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'ExpressInterest',
        'element': 'ExpanderControl',
        'value': $(this).text().trim()
      });
    });

    $(".sector-ctas a").on("click", function() {
      // Selector is quite fragile and could be benefit from
      // use of functional class names in the target code.
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'type': $(this).parents("li").children().eq(0).text().trim().trim(),
        'element': 'SectorRelatedCta',
        'value': $(this).text().trim()
      });
    });
  }

  function addTaggingForNextSteps() {
    $("#country-guide-need-help-section .cta-link").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'element': 'NextStepCta',
        'value': $(this).text().trim()
      });
    });
  }

  function addTaggingForMarketCtas() {
    $(".topic-list-section .card-link").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'element': 'MarketCta',
        'value': $(this).find("h3").text().trim()
      });
    });
  }

  function addTaggingForAdviceCtas() {
    $(".topic-list-section .card-link").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'element': 'AdviceCta',
        'value': $(this).find("h3").text().trim()
      });
    });
  }

  function addTaggingForServiceCtas() {
    $(".card-link").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'element': 'ServiceCta',
        'value': $(this).find("h3").text().trim()
      });
    });
  }
});
