document.addEventListener('DOMContentLoaded', function () {

  const addToCartBtn = document.querySelector('form[action="/cart/add"] button[type="submit"]');

  if (!addToCartBtn) return;

  addToCartBtn.addEventListener('click', function (e) {
    e.preventDefault();

    let items = [];

    // MAIN PRODUCT
    const mainVariant = document.querySelector('input[name="id"]');
    if (mainVariant) {
      items.push({
        id: mainVariant.value,
        quantity: 1
      });
    }

    // CHECKBOX ADDONS
    document.querySelectorAll('.addon-checkbox:checked').forEach(el => {
      items.push({
        id: el.dataset.variantId,
        quantity: 1
      });
    });

    // DROPDOWN ADDON
    document.querySelectorAll('.addon-select').forEach(select => {
      const option = select.selectedOptions[0];
      if (option && option.dataset.variantId) {
        items.push({
          id: option.dataset.variantId,
          quantity: 1
        });
      }
    });

    // ADD TO CART
    fetch('/cart/add.js', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ items })
    })
    .then(res => res.json())
    .then(() => {
      window.location.href = '/cart';
    })
    .catch(err => console.error(err));
  });

});
