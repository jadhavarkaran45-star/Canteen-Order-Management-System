const cart = {}; // JavaScript object used as the cart dictionary in the browser.
const cartItemsEl = document.getElementById("cart-items");
const cartCountEl = document.getElementById("cart-count");
const subtotalEl = document.getElementById("subtotal");
const totalEl = document.getElementById("total");
const cartMessageEl = document.getElementById("cart-message");
const queueMessageEl = document.getElementById("queue-message");

function money(value) {
    return "₹" + Number(value).toLocaleString("en-IN");
}

function showMessage(element, message, isError = false) {
    element.textContent = message;
    element.classList.toggle("error", isError);
}

function getCartTotal() {
    return Object.values(cart).reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function renderCart() {
    const names = Object.keys(cart);
    const itemCount = names.reduce((sum, name) => sum + cart[name].quantity, 0);
    cartCountEl.textContent = itemCount;
    document.getElementById("pending-count").textContent =
        document.querySelectorAll(".queue-card").length;

    if (!names.length) {
        cartItemsEl.innerHTML = '<div class="empty-state"><span>🛒</span><p>Your cart is empty</p><small>Add something tasty from the menu.</small></div>';
    } else {
        cartItemsEl.innerHTML = names.map(name => {
            const item = cart[name];
            return `
                <div class="cart-row">
                    <div>
                        <div class="cart-row-name">${name}</div>
                        <div class="cart-row-price">${money(item.price)} each · ${money(item.price * item.quantity)}</div>
                    </div>
                    <div class="quantity-control">
                        <button data-action="minus" data-name="${name}" aria-label="Decrease ${name}">−</button>
                        <span>${item.quantity}</span>
                        <button data-action="plus" data-name="${name}" aria-label="Increase ${name}">+</button>
                    </div>
                </div>`;
        }).join("");
    }

    const total = getCartTotal();
    subtotalEl.textContent = money(total);
    totalEl.textContent = money(total);
    document.getElementById("place-order").disabled = !names.length;
}

document.querySelectorAll(".add-btn").forEach(button => {
    button.addEventListener("click", () => {
        const name = button.dataset.name;
        const price = Number(button.closest(".food-card").querySelector(".food-details strong").textContent.replace(/[₹,]/g, ""));
        if (!cart[name]) cart[name] = { price, quantity: 0 };
        if (cart[name].quantity >= 99) {
            showMessage(cartMessageEl, "Maximum quantity is 99 per item.", true);
            return;
        }
        cart[name].quantity += 1;
        showMessage(cartMessageEl, "");
        renderCart();
    });
});

cartItemsEl.addEventListener("click", event => {
    const button = event.target.closest("button[data-action]");
    if (!button) return;
    const { name, action } = button.dataset;
    if (!cart[name]) return;
    if (action === "plus" && cart[name].quantity < 99) cart[name].quantity += 1;
    if (action === "minus") {
        cart[name].quantity -= 1;
        if (cart[name].quantity <= 0) delete cart[name];
    }
    renderCart();
});

document.getElementById("clear-cart").addEventListener("click", () => {
    Object.keys(cart).forEach(name => delete cart[name]);
    showMessage(cartMessageEl, "");
    renderCart();
});

document.getElementById("place-order").addEventListener("click", async () => {
    const items = Object.entries(cart).map(([name, item]) => ({
        name,
        quantity: item.quantity
    }));
    if (!items.length) {
        showMessage(cartMessageEl, "Please add items before placing an order.", true);
        return;
    }

    const button = document.getElementById("place-order");
    button.disabled = true;
    try {
        const response = await fetch("/api/order", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ items })
        });
        const data = await response.json();
        if (!response.ok || !data.success) throw new Error(data.message || "Could not place order.");

        showMessage(cartMessageEl, `Order #${data.order.token} placed! Total: ${money(data.order.total)}`);
        Object.keys(cart).forEach(name => delete cart[name]);
        renderCart();
        renderQueue(data.pending_orders);
        showMessage(queueMessageEl, `Order #${data.order.token} added to the queue.`);
    } catch (error) {
        showMessage(cartMessageEl, error.message, true);
    } finally {
        button.disabled = Object.keys(cart).length === 0;
    }
});

function renderQueue(orders) {
    document.getElementById("pending-count").textContent = orders.length;
    const queueList = document.getElementById("queue-list");
    if (!orders.length) {
        queueList.innerHTML = '<div class="queue-empty">No pending orders yet. Place an order to see it here.</div>';
        return;
    }
    queueList.innerHTML = orders.map(order => {
        const itemsText = order.items.map(item => `${item.name} × ${item.quantity}`).join("<br>");
        return `
            <article class="queue-card">
                <div class="queue-card-top">
                    <span class="token">#${order.token}</span>
                    <span class="pending-badge">Pending</span>
                </div>
                <div class="queue-items">${itemsText}</div>
                <div class="queue-total">${money(order.total)}</div>
                <div class="queue-time">${order.created_at}</div>
            </article>`;
    }).join("");
}

async function loadQueue() {
    try {
        const response = await fetch("/api/orders");
        const data = await response.json();
        renderQueue(data.pending_orders);
    } catch (_) {
        showMessage(queueMessageEl, "Could not load pending orders.", true);
    }
}

document.getElementById("process-next").addEventListener("click", async () => {
    try {
        const response = await fetch("/api/process-next", { method: "POST" });
        const data = await response.json();
        if (!response.ok || !data.success) throw new Error(data.message || "Could not process order.");
        renderQueue(data.pending_orders);
        showMessage(queueMessageEl, data.message);
    } catch (error) {
        showMessage(queueMessageEl, error.message, true);
    }
});

renderCart();
loadQueue();
