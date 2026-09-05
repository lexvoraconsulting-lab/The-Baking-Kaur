/* The Baking Kaur — product buy-box behaviour (vanilla, no deps) */
(function () {
  var root = document.querySelector('[data-bk-product]');
  if (!root) return;

  var dataEl = document.querySelector('[data-bk-variants]');
  var variants = [];
  try { variants = JSON.parse(dataEl.textContent); } catch (e) { variants = []; }

  var idInput = root.querySelector('[data-bk-variant-id]');
  var priceEl = root.querySelector('[data-bk-price]');
  var addText = root.querySelector('[data-bk-add-text]');
  var addBtn = root.querySelector('[data-bk-add]');
  var selects = root.querySelectorAll('[data-bk-option-selector]');
  var stickyPrice = document.querySelector('[data-bk-sticky-price]');

  function moneyFmt(cents) {
    var amount = (cents / 100).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    var fmt = (window.Shopify && Shopify.money_format) || '₹{{amount}}';
    return fmt.replace(/\{\{\s*amount\s*\}\}/, amount);
  }

  function currentOptions() {
    return Array.prototype.map.call(selects, function (s) { return s.value; });
  }

  function findVariant(opts) {
    return variants.find(function (v) {
      return (v.options || []).every(function (o, i) { return o === opts[i]; });
    });
  }

  function update() {
    if (!selects.length) return;
    var v = findVariant(currentOptions());
    if (!v) {
      if (addText) addText.textContent = 'Unavailable';
      if (addBtn) addBtn.setAttribute('disabled', 'disabled');
      return;
    }
    if (idInput) idInput.value = v.id;
    var priceStr = moneyFmt(v.price);
    if (priceEl) priceEl.textContent = priceStr;
    if (stickyPrice) stickyPrice.textContent = priceStr;
    if (v.available) {
      if (addBtn) addBtn.removeAttribute('disabled');
      if (addText) addText.innerHTML = 'ADD TO CART&nbsp;·&nbsp;' + priceStr;
    } else {
      if (addBtn) addBtn.setAttribute('disabled', 'disabled');
      if (addText) addText.textContent = 'Sold Out';
    }
    // reflect in URL for shareable variant links
    if (window.history && v.id) {
      var url = new URL(window.location.href);
      url.searchParams.set('variant', v.id);
      window.history.replaceState({}, '', url);
    }
  }

  Array.prototype.forEach.call(selects, function (s) {
    s.addEventListener('change', update);
  });

  // Gallery thumbnails
  var mainImg = document.getElementById('bk-main-image');
  root.querySelectorAll('[data-bk-thumb]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      if (mainImg) mainImg.src = btn.getAttribute('data-full');
      root.querySelectorAll('[data-bk-thumb]').forEach(function (b) { b.classList.remove('is-active'); });
      btn.classList.add('is-active');
    });
  });

  // Wishlist toggle (visual only — wire to your app if needed)
  var wish = root.querySelector('[data-bk-wish]');
  if (wish) wish.addEventListener('click', function () { wish.classList.toggle('is-active'); });

  // Sticky bar reveal after hero scrolls out
  var sticky = document.querySelector('[data-bk-sticky]');
  var hero = root.querySelector('.bk-hero');
  if (sticky && hero && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      sticky.hidden = entries[0].isIntersecting;
    }, { rootMargin: '-200px 0px 0px 0px' }).observe(hero);
  }

  update();
})();

/* FAQ accordion (used by bk-faq section) */
document.addEventListener('click', function (e) {
  var btn = e.target.closest('[data-bk-faq-toggle]');
  if (!btn) return;
  var item = btn.closest('[data-bk-faq-item]');
  if (item) item.classList.toggle('is-open');
});
