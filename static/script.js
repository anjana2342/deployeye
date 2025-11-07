// let cart = getCart();


// document.querySelectorAll(".btn-dark").forEach((btn, index) => {
//   btn.addEventListener("click", function () {
//     const card = btn.closest(".card");
//     const title = card.querySelector(".card-title").textContent;
//     const priceText = card.querySelector(".card-text").textContent;
//     const image = card.querySelector("img").src;
//     const quantity = parseInt(card.querySelector("input[type='number']").value);
//     const price = parseInt(priceText.replace(/[^0-9]/g, ""));

//     const existingItem = cart.find(item => item.title === title);
//     if (existingItem) {
//          alert(`${title} is already in the cart.`)
//         existingItem.quantity += quantity;
//     } else {
//       cart.push({
//         title,
//         price,
//         image,
//         quantity
//       });
//     }

//     localStorage.setItem("cart", JSON.stringify(cart));
//     updateCartCount();
//     alert(`${quantity} ${title} added to cart`);
//   });
// });

// function getCart() {
//   return JSON.parse(localStorage.getItem("cart")) || [];
// }



// function updateCartCount() {
//   const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
//   const cartCountElement = document.getElementById("cart-count");
//   if (cartCountElement) {
//     if (totalItems > 0) {
//       cartCountElement.style.display = "inline-block";
//       cartCountElement.textContent = totalItems;
//     } else {
//       cartCountElement.style.display = "none";
//     }
//   }
// }
// updateCartCount();


// const cartItemsContainer = document.getElementById("cart-items");
// const totalItemsElement = document.getElementById("total-items");
// const totalPriceElement = document.getElementById("total-price");
// const emptyCartMessage = document.getElementById("empty-cart");
// const cartContent = document.getElementById("cart-content");

// function displayCart() {
//   const cartItems = getCart();

//   if (cartItems.length === 0) {
//     emptyCartMessage.style.display = "block";
//     cartContent.style.display = "none";
//     return;
//   } else {
//     emptyCartMessage.style.display = "none";
//     cartContent.style.display = "block";
//   }

//   cartItemsContainer.innerHTML = "";
//   let totalItems = 0;
//   let totalPrice = 0;

//   cartItems.forEach(item => {
//     const row = document.createElement("tr");
//     row.innerHTML = `
//       <td><img src="${item.image}" alt="${item.title}" style="width: 50px;"> ${item.title}</td>
//       <td>₹${item.price}</td>
//       <td>
//         <input type="number" value="${item.quantity}" min="1" class="quantity-input" data-title="${item.title}">
//       </td>
//       <td>₹${item.price * item.quantity}</td>
//       <td><button class="remove-item" data-title="${item.title}">Remove</button></td>
//     `;
//     cartItemsContainer.appendChild(row);

//     totalItems += item.quantity;
//     totalPrice += item.price * item.quantity;
//   });

//   totalItemsElement.textContent = totalItems;
//   // totalPriceElement.textContent = totalPrice.toFixed(2);/
//   totalPriceElement.innerHTML = "&#8377;" + totalPrice.toFixed(2);
// }
// displayCart();

// cartItemsContainer.addEventListener("input", function (e) {
//   if (e.target.classList.contains("quantity-input")) {
//     const title = e.target.dataset.title;
//     const newQuantity = parseInt(e.target.value);
//     const cartItems = getCart();
//     const item = cartItems.find(i => i.title === title);
//     if (item && newQuantity > 0) {
//       item.quantity = newQuantity;
//       localStorage.setItem("cart", JSON.stringify(cartItems));
//       displayCart();
//       updateCartCount();
//     }
//   }
// });

// cartItemsContainer.addEventListener("click",function(c){
//   if(c.target.classList.contains("remove-item")){
//     const title = c.target.dataset.title;
//     let cartItems = getCart();
//     cartItems = cartItems.filter(item => item.title !== title);
//     localStorage.setItem("cart", JSON.stringify(cartItems));
//     displayCart();
//     updateCartCount();
//     alert(`${title} removed from cart`);
//   }
// })