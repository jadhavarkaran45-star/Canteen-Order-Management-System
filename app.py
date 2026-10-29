from flask import Flask, render_template, request, jsonify
from collections import deque
from datetime import datetime
import itertools

app = Flask(__name__)

# Dictionary: menu item -> price
MENU = {
    "Sandwich": 40,
    "Burger": 60,
    "Tea": 10,
    "Coffee": 20,
    "Dosa": 50,
    "Poha": 25
}

# Queue (FIFO): oldest pending order is processed first
pending_orders = deque()
token_counter = itertools.count(1001)


@app.route("/")
def home():
    return render_template("index.html", menu=MENU)


@app.route("/api/menu", methods=["GET"])
def get_menu():
    return jsonify(MENU)


@app.route("/api/orders", methods=["GET"])
def get_orders():
    return jsonify({
        "pending_orders": list(pending_orders),
        "next_token": next_token_value()
    })


def next_token_value():
    # itertools.count does not expose its next value; keep the displayed value
    return app.config.get("NEXT_TOKEN", 1001)


@app.route("/api/order", methods=["POST"])
def place_order():
    data = request.get_json(silent=True) or {}
    items = data.get("items", [])

    if not isinstance(items, list) or not items:
        return jsonify({"success": False, "message": "Your cart is empty."}), 400

    order_items = []
    total = 0

    for item in items:
        name = item.get("name")
        quantity = item.get("quantity")

        if name not in MENU:
            return jsonify({"success": False, "message": "Invalid menu item."}), 400

        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 1 or quantity > 99:
            return jsonify({"success": False, "message": "Quantity must be between 1 and 99."}), 400

        price = MENU[name]
        subtotal = price * quantity
        total += subtotal
        order_items.append({
            "name": name,
            "price": price,
            "quantity": quantity,
            "subtotal": subtotal
        })

    token = next(token_counter)
    order = {
        "token": token,
        "items": order_items,
        "total": total,
        "created_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "status": "Pending"
    }
    pending_orders.append(order)
    app.config["NEXT_TOKEN"] = token + 1

    return jsonify({
        "success": True,
        "message": "Order placed successfully!",
        "order": order,
        "pending_orders": list(pending_orders)
    }), 201


@app.route("/api/process-next", methods=["POST"])
def process_next_order():
    if not pending_orders:
        return jsonify({"success": False, "message": "There are no pending orders."}), 400

    # FIFO: popleft processes the oldest order first
    order = pending_orders.popleft()
    order["status"] = "Processed"

    return jsonify({
        "success": True,
        "message": f"Order #{order['token']} processed successfully.",
        "processed_order": order,
        "pending_orders": list(pending_orders)
    })


if __name__ == "__main__":
    app.run(debug=True)
