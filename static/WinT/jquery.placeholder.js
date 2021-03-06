(function(q, f, d) {
  function r(b) {
    var a = {}, c = /^jQuery\d+$/;
    d.each(b.attributes, function(b, d) {
      d.specified && !c.test(d.name) && (a[d.name] = d.value);
    });
    return a;
  }
  function g(b, a) {
    var c = d(this);
    if (this.value == c.attr("placeholder") && c.hasClass("placeholder")) {
      if (c.data("placeholder-password")) {
        c = c.hide().next().show().attr("id", c.removeAttr("id").data("placeholder-id"));
        if (!0 === b) {
          return c[0].value = a;
        }
        c.focus();
      } else {
        this.value = "", c.removeClass("placeholder"), this == m() && this.select();
      }
    }
  }
  function k() {
    var b, a = d(this), c = this.id;
    if ("" == this.value) {
      if ("password" == this.type) {
        if (!a.data("placeholder-textinput")) {
          try {
            b = a.clone().attr({type:"text"});
          } catch (e) {
            b = d("<input>").attr(d.extend(r(this), {type:"text"}));
          }
          b.removeAttr("name").data({"placeholder-password":a, "placeholder-id":c}).bind("focus.placeholder", g);
          a.data({"placeholder-textinput":b, "placeholder-id":c}).before(b);
        }
        a = a.removeAttr("id").hide().prev().attr("id", c).show();
      }
      a.addClass("placeholder");
      a[0].value = a.attr("placeholder");
    } else {
      a.removeClass("placeholder");
    }
  }
  function m() {
    try {
      return f.activeElement;
    } catch (b) {
    }
  }
  var h = "placeholder" in f.createElement("input"), l = "placeholder" in f.createElement("textarea"), e = d.fn, n = d.valHooks, p = d.propHooks;
  h && l ? (e = e.placeholder = function() {
    return this;
  }, e.input = e.textarea = !0) : (e = e.placeholder = function() {
    this.filter((h ? "textarea" : ":input") + "[placeholder]").not(".placeholder").bind({"focus.placeholder":g, "blur.placeholder":k}).data("placeholder-enabled", !0).trigger("blur.placeholder");
    return this;
  }, e.input = h, e.textarea = l, e = {get:function(b) {
    var a = d(b), c = a.data("placeholder-password");
    return c ? c[0].value : a.data("placeholder-enabled") && a.hasClass("placeholder") ? "" : b.value;
  }, set:function(b, a) {
    var c = d(b), e = c.data("placeholder-password");
    if (e) {
      return e[0].value = a;
    }
    if (!c.data("placeholder-enabled")) {
      return b.value = a;
    }
    "" == a ? (b.value = a, b != m() && k.call(b)) : c.hasClass("placeholder") ? g.call(b, !0, a) || (b.value = a) : b.value = a;
    return c;
  }}, h || (n.input = e, p.value = e), l || (n.textarea = e, p.value = e), d(function() {
    d(f).delegate("form", "submit.placeholder", function() {
      var b = d(".placeholder", this).each(g);
      setTimeout(function() {
        b.each(k);
      }, 10);
    });
  }), d(q).bind("beforeunload.placeholder", function() {
    d(".placeholder").each(function() {
      this.value = "";
    });
  }));
})(this, document, jQuery);