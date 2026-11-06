// The footer's theme switch (_includes/footer.html): system, light or dark.
// "System" stores nothing and leaves the page to prefers-color-scheme; light
// and dark are stored and set as data-theme on <html>, which _includes/head.html
// applies again before the first paint of the next page.
(function () {
  var box = document.querySelector('.theme-switch');
  if (!box) return;
  var root = document.documentElement;

  var current = root.getAttribute('data-theme') || 'system';
  var radio = box.querySelector('input[value="' + current + '"]');
  if (radio) radio.checked = true;

  box.addEventListener('change', function (e) {
    var theme = e.target.value;
    if (theme === 'light' || theme === 'dark') {
      root.setAttribute('data-theme', theme);
      try { localStorage.setItem('theme', theme); } catch (err) {}
    } else {
      root.removeAttribute('data-theme');
      try { localStorage.removeItem('theme'); } catch (err) {}
    }
  });

  box.hidden = false;
})();
