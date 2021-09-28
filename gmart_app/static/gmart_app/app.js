
var qty = 1;
var itmQty = document.querySelector('#item-quantity');
var qtyIncr = document.querySelector('#quantity-increase');
var qtyDecr = document.querySelector('#quantity-decrease');
var btnAddCart = document.querySelector('#add-to-cart');


qtyIncr.addEventListener('click', (e) => {
    qty += 1;
    itmQty.innerText = qty;
    btnAddCart.innerText = "Add " +qty+ " to Cart";
});

qtyDecr.addEventListener('click', (e) => {
    if(qty > 1) {
        qty -= 1;
        itmQty.innerText = qty;
        btnAddCart.innerText = "Add " +qty+ " to Cart";
    };
});

btnAddCart.addEventListener('click', (e) => {
    var addCartHref = btnAddCart.href.replace('555', qty);
    btnAddCart.href = addCartHref;
});

function eCommercePlaceholder() {
    alert("This is where the storefront app would connect with the ecommerce app.");
};



