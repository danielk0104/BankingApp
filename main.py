# Programming Assessment 2
# Daniel Khoury
# w24011169

from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
import json


# PAGES


# Login page (web app will start from here)
def user_login():
    clear()

    put_html("<h1>Banking App</h1>")

    # Inputs for login page
    login_inputs = [
        input("Username", name="name"),
        input("Password", name="password", type=PASSWORD),
        actions("", ["Log in", "Forgotten Password"], name="action")
    ]

    # Login variables
    login = input_group("Log in", login_inputs)
    login_option = login["action"]

    # If the user clicks forgotten password, send that to that page...
    if login_option == "Forgotten Password":
        forgot_password()
    # ... otherwise send them to the accounts page
    else:
        accounts()

# Forgotten password page
def forgot_password():
    clear()

    put_html("<h1>Banking App</h1>")

    # Inputs for forgotten password page
    forgotten_password = [
        input("New Password", name="oldpassword", type=PASSWORD),
        input("Confirm Password", name="newpassword", type=PASSWORD),
        actions("", ["Change Password"], name="action")
    ]

    # Forgotten password variables
    forgotten_password = input_group("Forgotten Password", forgotten_password)

    # After the password is updated, send the user back to the login page
    user_login()

# Accounts page
def accounts():
    clear()

    put_html("<h1>Accounts</h1>")

    # Set up variable
    accounts_data = read_json("accounts")

    # Loop through JSON file for each account
    for account in accounts_data:
        # Put account information
        put_html(f"""
            <div style="padding: 15px;">
                <div style="border: 1px solid lightgrey; border-radius:20px; text-align: center;">
                    <h3>{account["name"]} | £{account["balance"]}</h3>
                    <img src="{account["image"]}" alt="Bank Card Image">
                    <h3>{account["number"]} | {account["code"]}</h3>
                </div>
            </div>
        """)
    
    # Image credit
    put_html("""
        <p>Bank card images from <a href="https://www.postermywall.com/index.php/art/template/eb1fa96e57f2bf2a0ff20cfd07432803/atm-card-design-template">www.postermywall.com</a>.</p>
    """)

    # Footer menu
    footer_menu()

# Payments page
def payments():
    clear()

    put_html("<h1>Make a Payment</h1>")

    # List of payees
    payees = []

    # Set up variable
    payee_data = read_json("payees")

    # Loop through JSON file for each payee
    for payee in payee_data:
        # Add payee to list
        payees.append(payee["name"])

    # Inputs for payment menu
    payee_inputs = [
        radio("Payees", options=payees, name='payees'),
        actions("", ["Add a New Payee"], name="addnew"),
        input("Enter Amount", name="amount", type=NUMBER),
        actions("", ["Submit", "Cancel"], name="action")
    ]

    # Payment menu variables
    payment_menu = input_group("Select Payee", payee_inputs)
    payee_option = payment_menu["payees"]
    amount_option = payment_menu["amount"]
    payment_option = payment_menu["action"]
    new_payee_option = payment_menu["addnew"]

    # If the user clicks submit payment... (and none of the required fields are empty)
    if payment_option == "Submit" and payee_option != None and amount_option != None:
        popup("PAYMENT SUCCESS", f"Payment of £{amount_option} successfully made to {payee_option}.", size=PopupSize.LARGE)
        account_summary()
    # ... otherwise, if the user clicks cancel...
    elif payment_option == "Cancel":
        account_summary()
    # ... otherwise, if the user clicks add a new payee...
    elif new_payee_option == "Add a New Payee":
        new_payee()
    # ... or if the required information is NOT filled, just reload the page
    else:
        popup("ERROR", "You must choose a payee and an amount!", size=PopupSize.LARGE)
        payments()

# Account summary page
def account_summary():
    clear()

    put_html("<h1>Account Summary</h1>")

    # Current balance
    put_html("<h3>Current Balance: £XX.XX</h3>")

    # Move money button
    put_button("Move Money", onclick=lambda: payments())

    # Transactions heading
    put_html("<h2>Transactions</h2>")

    # Set up variable
    transaction_data = read_json("transactions")

    # Loop through JSON file for each transaction
    for transaction in transaction_data:
        # Put information about transaction
        put_html(f"""
            <div style="padding: 15px;">
                <div style="padding: 10px; border: 1px solid lightgrey; border-radius:20px;">
                    <h3>Payment to {transaction["name"]}</h3>
                    <h4>Amount Sent: £{transaction["amount"]}</h4>
                    <p>Transaction made on {transaction["date"]}</p>
                </div>
            </div>
        """)
    
    # Footer menu
    footer_menu()

# Add a new payee page
def new_payee():
    clear()

    put_html("<h1>Add New Payee</h1>")

    # Inputs for login page
    payee_inputs = [
        input("Payee Name", name="name", required=True),
        input("Bank", name="bank", required=True),
        input("Account Number", name="accountno", required=True),
        input("Sort Code", name="code", required=True),
        actions("", ["Add Payee"], name="action")
    ]

    # Payee variables
    payee = input_group("Enter Payee Details", payee_inputs)
    payee_name = payee["name"]

    # When finished, show a popup and return to account summary page
    popup("NEW PAYEE ADDED", f"New payee {payee_name} has been added.", size=PopupSize.LARGE)
    account_summary()

# Products page
def products():
    clear()

    put_html("<h1>Products</h1>")

    # Set up variable
    product_data = read_json("products")
    
    # Loop through JSON file for each product
    for product in product_data:
        # Put information about product
        put_html(f"""
            <div style="padding: 15px;">
                <div style="padding: 10px; border: 1px solid lightgrey; border-radius:20px; text-align: center;">
                    <h3>{product["name"]}</h3>
                <img src="{product["image"]}" style="width: 100px;" alt="Bank Card Image">
                </div>
            </div>
        """)
        # If the product is loans...
        if product["name"] == "Loans":
            put_button("More Info", onclick=lambda: loans())
        # ... otherwise if the product is mortgages...
        elif product["name"] == "Mortgages":
            put_button("More Info", onclick=lambda: products())
        # ... otherwise if the product is credits cards
        elif product["name"] == "Credit Cards":
            put_button("More Info", onclick=lambda: products())

    # Image credit for loans
    put_html("""
        <p>Loan image from <a href="https://uxwing.com/loan-icon/">uxwing.com</a>.</p>
    """)

    # Image credit for mortgages
    put_html("""
        <p>Mortgage image from <a href="https://uxwing.com/house-hand-mortgage-icon/">uxwing.com</a>.</p>
    """)

    # Image credit for credit cards
    put_html("""
        <p>Credit card image from <a href="hhttps://www.svgrepo.com/svg/146677/credit-card">www.svgrepo.com</a>.</p>
    """)

    # Footer menu
    footer_menu()

# Loans page
def loans():
    clear()

    put_html("<h1>Loans</h1>")

    # Set up variable
    product_data = read_json("products")

    # Loop through JSON file for each product
    for product in product_data:
        # If the product is loans...
        if product["name"] == "Loans":
            # Put the loan image
            put_html(f"""
                <div style="padding: 15px;">
                    <div style="padding: 10px; text-align: center;">
                    <img src="{product["image"]}" style="width: 100px;" alt="Bank Card Image">
                    </div>
                </div>
            """)
        
    put_html("<h3>Loans Options</h3>")

    # Loop through JSON file for each product
    for product in product_data:
        # If the product is loans...
        if product["name"] == "Loans":
            # Put the loan information
            put_html(f"""
                <div style="padding: 15px;">
                    <div style="padding: 10px;">
                    <p>{product["info"]}</p>
                    </div>
                </div>
            """)


# OTHER FUNCTIONS


# Read data.json file
def read_json(data_point):
    # Open JSON file
    with open("data.json", "r") as file:
        data = json.load(file)
    
    # Return variable
    return data[data_point]

# Footer menu
def footer_menu():
    # Inputs for footer menu
    footer_inputs = [
        actions("", ["Home", "Payments", "Products"], name="action")
    ]

    # Footer menu variables
    footer = input_group("", footer_inputs)
    footer_option = footer["action"]

    # If the user clicks the home button...
    if footer_option == "Home":
        accounts()
    # ... or the payments button...
    elif footer_option == "Payments":
        payments()
    # ... or the products button
    elif footer_option == "Products":
        products()


# SERVER


# Start server
if __name__ == "__main__":
    start_server(user_login, port=5000, debug=True)