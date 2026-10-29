CANTEEN ORDER MANAGEMENT SYSTEM
================================

Technology:
- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- Data Structures: Dictionary, List, Queue (FIFO)

HOW TO RUN ON WINDOWS (VS CODE)
-------------------------------
1. Extract the ZIP file to a folder.
2. Open that folder in VS Code.
3. Open Terminal > New Terminal.
4. (Recommended) Create a virtual environment:
   python -m venv venv
5. Activate it in PowerShell:
   .\venv\Scripts\Activate.ps1
   If activation is blocked, you can skip activation and use:
   python -m pip install -r requirements.txt
6. Install Flask:
   python -m pip install -r requirements.txt
7. Start the app:
   python app.py
8. Open Chrome and visit:
   http://127.0.0.1:5000

FEATURES
--------
- Menu and prices: Sandwich ₹40, Burger ₹60, Tea ₹10,
  Coffee ₹20, Dosa ₹50, Poha ₹25
- Add items, change quantities, remove items by reducing quantity to zero
- Automatic total bill
- Place order and generate token number
- Pending order queue
- Process Next Order uses FIFO: first order placed is processed first
- Server-side validation for menu items and quantities

IMPORTANT
---------
This is a demonstration prototype. Orders are stored in memory, so they reset
when the Flask server restarts. It does not store orders in a database and does
not process real payments. Keep the terminal open while using the website.
