// Cart functionality script

const cartItems = document.querySelectorAll('.cart-item');
const subtotalElement = document.getElementById('subtotal');
const shippingElement = document.getElementById('shipping');
const totalElement = document.getElementById('total');
const couponInput = document.getElementById('coupon-code');
const applyCouponBtn = document.getElementById('apply-coupon');

const shippingCost = 5.00; // Example flat shipping cost
let discount = 0;

function updateCartTotals() {
    let subtotal = 0;
    
    cartItems.forEach(item => {
        const priceElement = item.querySelector('.price');
        const quantityElement = item.querySelector('.quantity-input');
        const totalElement = item.querySelector('.total');

        const price = parseFloat(priceElement.innerText.replace('$', ''));
        const quantity = parseInt(quantityElement.value);
        const itemTotal = price * quantity;

        totalElement.innerText = `$${itemTotal.toFixed(2)}`;
        subtotal += itemTotal;
    });

    subtotalElement.innerText = `$${subtotal.toFixed(2)}`;
    shippingElement.innerText = `$${shippingCost.toFixed(2)}`;

    let grandTotal = subtotal + shippingCost - discount;
    totalElement.innerText = `$${grandTotal.toFixed(2)}`;
}

// Handle quantity change
cartItems.forEach(item => {
    const quantityInput = item.querySelector('.quantity-input');
    quantityInput.addEventListener('change', updateCartTotals);
});

// Handle coupon code
applyCouponBtn.addEventListener('click', () => {
    const couponCode = couponInput.value.trim();

    if (couponCode === 'DIY10') {
        discount = 10;
        alert('Coupon applied! $10 discount added.');
    } else {
        discount = 0;
        alert('Invalid coupon code.');
    }
    updateCartTotals();
});

// Initial calculation
updateCartTotals();

// Next step: Save the order to the database on checkout!
