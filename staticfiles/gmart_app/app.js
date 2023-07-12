// This is the main JavaScript file for the website

// Initialize Variables
var qty = 1;
var itmQty = document.querySelector('#item-quantity');
var qtyIncr = document.querySelector('#quantity-increase');
var qtyDecr = document.querySelector('#quantity-decrease');
var btnAddCart = document.querySelector('#add-to-cart');

// Increment the quantity of items to be added to the cart
qtyIncr.addEventListener('click', (e) => {
    qty += 1;
    itmQty.innerText = qty;
    btnAddCart.innerText = "Add " +qty+ " to Cart";
});

// Decrement the quantity of items to be added to the cart
qtyDecr.addEventListener('click', (e) => {
    if(qty > 1) {
        qty -= 1;
        itmQty.innerText = qty;
        btnAddCart.innerText = "Add " +qty+ " to Cart";
    };
});

// Replace the actual quantity
btnAddCart.addEventListener('click', (e) => {
    var addCartHref = btnAddCart.href.replace('555', qty);
    btnAddCart.href = addCartHref;
});

// A placeholder function for ecommerce integration
function eCommercePlaceholder() {
    alert("This is where the storefront app would connect with the ecommerce app.");
};



