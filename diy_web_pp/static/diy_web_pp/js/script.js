const container = document.getElementsByClassName('container')[0];
const nav = document.getElementById('navbar');
const close = document.getElementById('close');
const finalPrice = document.getElementById("fp");

// Navigation toggle
if (container) {
    container.addEventListener('click', () => {
        nav.classList.add('active');
    });
}

if (close) {
    close.addEventListener('click', () => {
        nav.classList.remove('active');
    });
}

// Price calculation and shipping logic
function Change() {
    const quantities = [document.getElementById("qty"), document.getElementById("qty1"), document.getElementById("qty2")];
    const prices = [document.getElementById("fp"), document.getElementById("fp1"), document.getElementById("fp2")];
    
    let sum = 0;
    quantities.forEach((qty, index) => {
        if (qty && prices[index]) {
            const price = parseInt(qty.value || 0) * 5600;
            prices[index].textContent = "Rs." + price;
            sum += price;
        }
    });

    const cart = document.getElementById('cart_sub');
    const ship = document.getElementById('shipping');
    const tot = document.getElementById('total');

    let ship_amt = 0;

    if (sum > 0 && sum < 2000) ship_amt = 50;
    else if (sum >= 2000 && sum < 5000) ship_amt = 40;
    else if (sum >= 5000 && sum < 8000) ship_amt = 30;
    else if (sum >= 8000 && sum < 11000) ship_amt = 20;
    else if (sum >= 11000 && sum < 14000) ship_amt = 10;

    const total = sum + ship_amt;

    if (cart && ship && tot) {
        cart.textContent = "Rs." + sum;
        ship.textContent = "Rs." + ship_amt;
        tot.textContent = "Rs." + total;
    }
}

// Fetch and display uploaded products
async function displayUploadedProducts() {
    console.log('displayUploadedProducts called');
    const productList = document.getElementById('product-list');

    if (productList) {
        productList.innerHTML = '';

        try {
            const response = await fetch('http://localhost:5000/api/products');
            const uploadedProducts = await response.json();

            if (uploadedProducts.length === 0) {
                productList.innerHTML = '<p>No products uploaded yet.</p>';
                return;
            }

            uploadedProducts.forEach((product, index) => {
                console.log('Processing product:', product);
                const li = document.createElement('li');
                li.className = 'product-item';

                li.innerHTML = `
                    <div class='product-card'>
                        <img src='http://localhost:5000${product.image_url}' alt='${product.name}' />
                        <h3>${product.name}</h3>
                        <p>${product.description}</p>
                        <span>Price: ₹${product.price}</span>
                        <button class="cart">Add to Cart</button>
                    </div>
                `;

                // Attach event listeners
                li.querySelector('.cart').addEventListener('click', (e) => {
                    e.stopPropagation(); // Prevent triggering viewProductDetails
                    addToCart(product);
                });

                li.querySelector('.product-card').addEventListener('click', () => {
                    viewProductDetails(product);
                });

                productList.appendChild(li);
            });
        } catch (error) {
            console.error('Error fetching products:', error);
            productList.innerHTML = '<p>Failed to load products.</p>';
        }
    }
}


// View product details
function viewProductDetails(product) {
    if (product) {
        console.log('Viewing product:', product);
        sessionStorage.setItem('currentProduct', JSON.stringify(product));
        window.location.href = 'sproduct.html';
    }
}

// Add to cart (stub function for now)
function addToCart(product) {
    console.log('Adding to cart:', product);
    alert(`${product.name} added to cart!`);
}

// Load products on page load
window.onload = function () {
    if (window.location.href.includes('uploaded-products.html')) {
        displayUploadedProducts();
    }
};

// Add product to cart
function addToCart(index) {
    const uploadedProducts = JSON.parse(localStorage.getItem('uploadedProducts')) || [];
    const product = uploadedProducts[index];

    if (product) {
        let cart = JSON.parse(sessionStorage.getItem('cart')) || [];
        const existingProductIndex = cart.findIndex(item => item.name === product.name);

        if (existingProductIndex !== -1) {
            cart[existingProductIndex].quantity += 1;
        } else {
            product.quantity = 1;
            cart.push(product);
        }

        sessionStorage.setItem('cart', JSON.stringify(cart));
        alert('Product added to cart!');
    }
}

// Load cart
function loadCart() {
    const cart = JSON.parse(sessionStorage.getItem('cart')) || [];
    console.log('Cart contents:', cart);
}

// Load uploaded products on page load
window.onload = function() {
    displayUploadedProducts();
    loadCart();
};
