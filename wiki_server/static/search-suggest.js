(function () {
  var dropdown = document.createElement("div");
  dropdown.className = "search-suggest";

  function attach(input) {
    var form = input.closest("form");
    var wrapper = document.createElement("div");
    wrapper.className = "search-suggest-wrapper";
    input.parentNode.insertBefore(wrapper, input);
    wrapper.appendChild(input);
    wrapper.appendChild(dropdown);

    var timer, selected = -1, data = [];

    function hide() {
      dropdown.classList.remove("open");
      selected = -1;
    }

    function highlight(index) {
      Array.from(dropdown.children).forEach(function (el, i) {
        el.classList.toggle("selected", i === index);
      });
    }

    function fetch() {
      var val = input.value.trim();
      if (val.length < 2) { hide(); return; }

      var xhr = new XMLHttpRequest();
      xhr.open("GET", "/search/suggest?q=" + encodeURIComponent(val));
      xhr.onload = function () {
        if (xhr.status !== 200) return;
        data = JSON.parse(xhr.responseText);
        if (!data.length) { hide(); return; }
        dropdown.innerHTML = data.map(function (d, i) {
          return '<div class="suggest-item" data-index="' + i + '" data-url="' + d.url + '">' + escapeHtml(d.title) + '</div>';
        }).join("");
        dropdown.classList.add("open");
        selected = -1;
      };
      xhr.send();
    }

    function navigate(url) {
      hide();
      window.location.href = url;
    }

    input.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(fetch, 120);
    });

    input.addEventListener("keydown", function (e) {
      if (!dropdown.classList.contains("open")) return;
      var items = dropdown.children;
      if (e.key === "ArrowDown") {
        e.preventDefault();
        selected = Math.min(selected + 1, items.length - 1);
        highlight(selected);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        selected = Math.max(selected - 1, -1);
        highlight(selected);
      } else if (e.key === "Enter" && selected >= 0) {
        e.preventDefault();
        navigate(data[selected].url);
      } else if (e.key === "Escape") {
        hide();
      }
    });

    input.addEventListener("blur", function () {
      setTimeout(hide, 200);
    });

    dropdown.addEventListener("mousedown", function (e) {
      var item = e.target.closest(".suggest-item");
      if (item) navigate(item.dataset.url);
    });
  }

  function escapeHtml(str) {
    var div = document.createElement("div");
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  document.addEventListener("DOMContentLoaded", function () {
    var inputs = document.querySelectorAll('input[type="search"][name="q"]');
    Array.from(inputs).forEach(attach);
  });
})();
