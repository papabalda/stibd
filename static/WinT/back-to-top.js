var stt = {set:{scrollto:0}, controlHTML:'<i class="fa fa-angle-up"></i>', state:{iv:!1, sv:!1}, up:function() {
  this.cssfs || this.$control.css({opacity:0});
  var a = isNaN(this.set.scrollto) ? this.set.scrollto : parseInt(this.set.scrollto), a = "string" == typeof a && 1 == jQuery("#" + a).length ? jQuery("#" + a).offset().top : 0;
  this.$body.animate({scrollTop:a}, 1E3);
}, kf:function() {
  var a = jQuery(window), b = a.scrollLeft() + a.width() - this.$control.width() - 5, a = a.scrollTop() + a.height() - this.$control.height() - 5;
  this.$control.css({left:b + "px", top:a + "px"});
}, tc:function() {
  var a = jQuery(window).scrollTop();
  this.cssfs || this.kf();
  this.state.sv = a >= 100 ? !0 : !1;
  this.state.sv && !this.state.iv ? (this.$control.stop().animate({opacity:1}, 500), this.state.iv = !0) : 0 == this.state.sv && this.state.iv && (this.$control.stop().animate({opacity:0}, 100), this.state.iv = !1);
}, init:function() {
  jQuery(document).ready(function(a) {
    var b = stt, c = document.all;
    b.cssfs = !c || c && "CSS1Compat" == document.compatMode && window.XMLHttpRequest;
    b.$body = window.opera ? "CSS1Compat" == document.compatMode ? a("html") : a("body") : a("html,body");
    b.$control = a('<div id="topcontrol">' + b.controlHTML + "</div>").css({position:b.cssfs ? "fixed" : "absolute", bottom:5, right:5, opacity:0, cursor:"pointer"}).attr({title:"Scroll Back to Top"}).click(function() {
      b.up();
      return !1;
    }).appendTo("body");
    document.all && !window.XMLHttpRequest && "" != b.$control.text() && b.$control.css({width:b.$control.width()});
    b.tc();
    a('a[href="#top"]').click(function() {
      b.up();
      return !1;
    });
    a(window).bind("scroll resize", function(a) {
      b.tc();
    });
  });
}};
stt.init();