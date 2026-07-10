(function () {
  "use strict";

  /* Mobile nav */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("click", function (e) {
      if (!nav.contains(e.target) && !toggle.contains(e.target)) {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* Auto TOC from h2 in .prose */
  var prose = document.querySelector(".post-body.prose");
  var lists = [
    document.getElementById("post-toc-list"),
    document.getElementById("post-toc-list-desktop")
  ].filter(Boolean);
  if (prose && lists.length) {
    var headings = prose.querySelectorAll("h2");
    if (headings.length >= 3) {
      headings.forEach(function (h, i) {
        if (!h.id) {
          h.id = "section-" + (i + 1);
        }
        lists.forEach(function (tocRoot) {
          var li = document.createElement("li");
          var a = document.createElement("a");
          a.href = "#" + h.id;
          a.textContent = h.textContent;
          li.appendChild(a);
          tocRoot.appendChild(li);
        });
      });
      var tocMobile = document.getElementById("post-toc");
      var tocDesktop = document.getElementById("post-toc-desktop");
      if (tocMobile) tocMobile.hidden = false;
      if (tocDesktop) tocDesktop.hidden = false;
    } else {
      var td = document.getElementById("post-toc-desktop");
      if (td) td.style.display = "none";
    }
  }
})();
