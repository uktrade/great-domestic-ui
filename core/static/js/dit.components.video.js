// Video Component Functionality.
// Requires...
// dit.js
// dit.class.Modal.js

dit.components.video = (new function() {

  var VIDEO_COMPONENT = this;

  // Constants
  var CSS_CLASS_CONTAINER = "video-container";
  var VIDEO_CLOSE_BUTTON_ID = "hero-campaign-section-videoplayer-close"
  var SELECTOR_ACTIVATOR = "[data-node='videoactivator']";
  var TYPE_VIDEO = "video";
  var TYPE_IFRAME = "iframe";


  /* Contructor
   * Modal dialog enhancement specifically for video display.
   * @$dialog (jQuery node) Element containing video/iframe.
   * @options (Object) Configuration (see classes.Modal)
   **/
  function VideoDialog($dialog, options) {
    dit.classes.Modal.call(this, $dialog, options);
  }

  VideoDialog.loadWithVideo = function(src) {
    var $video = $("<video controls></video>");
    var format = src.replace(/^.*\.([a-z0-9/]+)$/, "$1");
    var $source = $("<source src=\"" + src + "\" type=\"video/" + format  + "\">");
    $video.append($source);
    this.setContent($video);
  }

  VideoDialog.loadWithIframe = function(src) {
    var $iframe = $("<iframe src=\"" + src + "\"></iframe>");
    this.setContent($iframe);
  }

  VideoDialog.activate = function() {
    var $activator = $(this.activator);
    var type = $activator.data("element");
    var url = $activator.attr("href") || $activator.data("src");
    switch(type) {
      case TYPE_VIDEO:
        VideoDialog.loadWithVideo.call(this, url);
        break;
      case TYPE_IFRAME:
        VideoDialog.loadWithIframe.call(this, url);
        break;
      default:
        type = null;
    }

    if(type) {
      this.resize();
    }
  }

  VideoDialog.prototype = new dit.classes.Modal;

  VideoDialog.prototype.open = function() {
    $('body').addClass('modal-open');
    VideoDialog.activate.call(this);
    dit.classes.Modal.prototype.open.call(this);
  }

  VideoDialog.prototype.resize = function() {
    var width = $(window).width();
    var height = $(window).height();
    var $iframe = $("iframe", this.$container);
    var sizes = [
      [320, 240],
      [640, 360],
      [853, 480],
      [1280, 720],
      [1920, 1080]
    ];

    var i = 0;
    var size;

    do {
      size = sizes[i],
      i++;
    } while (i < sizes.length && sizes[i][0] <= width && sizes[i][1] <= height);

    $iframe.attr("width", size[0]);
    $iframe.attr("height", size[1]);
    //t = Math.floor((o - s.height()) / 4),
    //t > 0 && i.$content.css('margin-top', String(t > 0 ? t : 0) + 'px')
  }

  function createContainer() {
    var $container = $(document.createElement("div"));
    $container.addClass(CSS_CLASS_CONTAINER);
    return $container;
  }

  function bindActivators($activators) {
    $activators.on("click keydown", function(e) {
     //dit.classes.Modal.activate.call(VIDEO_COMPONENT,  this, e);
      //VIDEO_COMPONENT.activate(this, e);
    });
  }

  function onClose() {
    $('body').removeClass('modal-open');
    this.$container.find('video').each(function(index, video) {
      video.pause();
    });
  }

  // Public
  this.init = function() {
    var $activators = $(SELECTOR_ACTIVATOR);
    var $container = createContainer();
    if($activators.length) {
      $(document.body).append($container);
      new VideoDialog($container, {
        $activators: $activators,
        closeButtonId: VIDEO_CLOSE_BUTTON_ID,
        onClose: onClose
      });
    }

    delete self.init; // Run once fuction.
  }
});
