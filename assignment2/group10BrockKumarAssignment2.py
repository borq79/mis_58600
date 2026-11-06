# -*- coding: utf-8 -*-


###############################################################################
# MIS 58600
# Group 10 - Ryan Brock and Sachin Kumar
# Assignment 2 - Sales and Inventory Management System
###############################################################################

###############################################################################
# Notes on collaboration
#
# Tasks done by Sachin: ()
# 1. Implemented view_sales_history function
# 2. Implemented display_kpis function
# 3. Implemented make_sale logic and sale recording
#
# Tasks done by Ryan:
# 1. Implemented view_catalog function
# 2. Implemented update_product_attribute function
# 3. Implemented update_product_details function
#
# This was a 50/50 effort. We both wrote code on our own, merged the code, and
# then worked together to review bugs and clean up the code. To assist in
# ensuring we did not break anything during our sessions, we had Claude create
# a series of unit tests to validate the program. The unit tests allowed us to
# refactor the code safely knowing we didn't break anything. They are available
# upon request. 
# Ryan: AI was not used in the creation of the code within this file,only the unit tests.
# Sachin Kumar:  AI tool used : Auto suggestion/code complete built-in within VSS Code IDE.
#
###############################################################################
# Initialize the product catalog

import math
from datetime import datetime

product_catalog = {
    'P1':  {'Name': 'Product 1',  'Price': 10.99,  'Stock': 100},
    'P2':  {'Name': 'Product 2',  'Price': 5.99,   'Stock': 50},
    'P3':  {'Name': 'Product 3',  'Price': 1.99,   'Stock': 200},
    'P4':  {'Name': 'Product 4',  'Price': 15.99,  'Stock': 150},
    'P5':  {'Name': 'Product 5',  'Price': 3.99,   'Stock': 10},
    'P6':  {'Name': 'Product 6',  'Price': 6.99,   'Stock': 5},
    'P7':  {'Name': 'Product 7',  'Price': 100.99, 'Stock': 1},
    'P8':  {'Name': 'Product 8',  'Price': 5.99,   'Stock': 3},
    'P9':  {'Name': 'Product 9',  'Price': 12.99,  'Stock': 16},
    'P10': {'Name': 'Product 10', 'Price': 45.99,  'Stock': 50}
}

# Initialize the sales history
sales_history = []

##############################################################################
# Desc: This function displays the catalog with details about each product
# Parameters: None
# Returns: None
##############################################################################
def view_catalog():
    print("\nProduct Catalog:")
    print ("=============================================\n")

    for product_id, product_details in product_catalog.items():
        print (f"Product Name: {product_details['Name']}")
        print (f"ID          : {product_id}")
        print (f"Price       : ${product_details['Price']:.2f}")
        print (f"Quantity    : {product_details['Stock']}\n")
        print ("---------------------------------------------\n")

##############################################################################
# Desc: This function will execute the sale
# Parameters: None
# Returns: None
##############################################################################
def make_sale():
    #show product catalog to the user
    view_catalog()

    while True:
        # get user input on which product to sell
        id_of_sale = input("Enter the product id of the sale: ")
        if not id_of_sale in product_catalog:
            print (f"Invalid id '{id_of_sale}', please enter one of the product ids listed above.")
            continue
        break

    if product_catalog[id_of_sale]['Stock'] == 0:
        print(f"Sorry, {product_catalog[id_of_sale]['Name']} is out of stock.")
        return

    while True:
        try:
            quantity = int(input(f"Enter the quantity sold (in stock: {product_catalog[id_of_sale]['Stock']}): "))
            if quantity < 1:
                print (f"The quantity must be at least 1.")
                continue
            if quantity > product_catalog[id_of_sale]['Stock']:
                print (f"You've elected to sell more items ({quantity}) than are in stock ({product_catalog[id_of_sale]['Stock']}). Please try again.")
                continue
            print (f"\nYou sold {quantity} of {id_of_sale} ({product_catalog[id_of_sale]['Name']})")
            break
        except ValueError:
            print (f"The quantity must be an integer between 1 and the number of units in stock")

    sale = {
        'Sale ID': f'S{len(sales_history) + 1}',
        'Date and Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Product ID': id_of_sale,
        'Product Name': product_catalog[id_of_sale]['Name'],
        'Quantity': quantity,
        'Total Sale Amount': round(product_catalog[id_of_sale]['Price'] * quantity, 2)
    }
    product_catalog[id_of_sale]['Stock'] -= quantity
    sales_history.append(sale)
    print(f"Sale {sale['Sale ID']} completed. Total: ${sale['Total Sale Amount']:.2f}")
    print(f"Remaining stock: {product_catalog[id_of_sale]['Stock']}")
    print ("---------------------------------------------\n")


##############################################################################
# Desc: This function will display the sales history
# Parameters: None
# Returns: None
##############################################################################
def view_sales_history():
    print("\nSales History:")
    if not sales_history:
        print("No sales history available.")
    else:
        for sale in sales_history:
            print(f"Sale: {sale['Sale ID']}, Product: {sale['Product Name']}, Quantity: {sale['Quantity']}, Total: ${sale['Total Sale Amount']:.2f}, Date: {sale['Date and Time']}")

##############################################################################
# Desc: This function display the KPIs such as revenue, best-selling products
#       and the product with the highest revenue
# Parameters: None
# Returns: None
##############################################################################
def display_kpis():
    total_revenue = sum(sale['Total Sale Amount'] for sale in sales_history)
    print(f"\nTotal Sales Revenue: ${total_revenue:.2f}")

    if not sales_history:
        print("No sales history available to determine best-selling products.")
        return

    # Calculate best-selling products
    product_sales = {}
    for sale in sales_history:
        product_name = sale['Product Name']
        quantity = sale['Quantity']
        if product_name in product_sales:
            product_sales[product_name] += quantity
        else:
            product_sales[product_name] = quantity

    best_selling_product = sorted(product_sales, key=product_sales.get, reverse=True)[0]
    print(f"Best-Selling Product: {best_selling_product} with {product_sales[best_selling_product]} units sold.")

    # Find product with highest revenue
    product_revenue = {}
    for sale in sales_history:
        product_name = sale['Product Name']
        total_sale_amount = sale['Total Sale Amount']
        if product_name in product_revenue:
            product_revenue[product_name] += total_sale_amount
        else:
            product_revenue[product_name] = total_sale_amount

    highest_revenue_product = sorted(product_revenue, key=product_revenue.get, reverse=True)[0]

    print(f"Product with Highest Revenue: {highest_revenue_product} with ${product_revenue[highest_revenue_product]:.2f} in revenue.")

    return


##############################################################################
# Desc: This function will update a product catalog entry
# Parameters: The id of the product catalog item and the specific key
# Returns: None
##############################################################################
def update_product_attribute(id_of_update, dictionary_key):
    if not id_of_update in product_catalog:
        print (f"Invalid Product id {id_of_update}")
        return

    if not dictionary_key in product_catalog[id_of_update]:
        print (f"Invalid Product Catalog Attribute Name {dictionary_key}")
        return

    while True:
        updated_value = input(f"Enter the updated {dictionary_key}: ")

        if dictionary_key == 'Price':
            try:
                updated_value = float(updated_value)
            except ValueError:
                print(f"Invalid Type for {dictionary_key}. Please try again.")
                continue
            if math.isnan(updated_value) or math.isinf(updated_value):
                print(f"Invalid Type for {dictionary_key}. Please try again.")
                continue
            if updated_value < 0:
                print(f"Price cannot be negative. Please try again.")
                continue
        elif dictionary_key == 'Stock':
            try:
                updated_value = int(updated_value)
            except ValueError:
                print(f"Invalid Type for {dictionary_key}. Please try again.")
                continue
            if updated_value < 0:
                print(f"Stock cannot be negative. Please try again.")
                continue
        elif dictionary_key == 'Name':
            if updated_value.strip() == '':
                print(f"Name cannot be blank. Please try again.")
                continue

        break

    try:
        product_catalog[id_of_update][dictionary_key] = updated_value
    except KeyError:
        print (f"Invalid Product id or dictionary key provided {id_of_update}, {dictionary_key}")

##############################################################################
# Desc: This function will allow a user to update the product details
# Parameters: None
# Returns: None
##############################################################################
def update_product_details():
    while True:
        try:
            # get user input on which product to update
            id_of_update = input("Enter the product id to update: ")
            print (f"\nYou selected id: {id_of_update}, product: {product_catalog[id_of_update]['Name']}")
            break
        except KeyError:
            print (f"Invalid id '{id_of_update}', please enter one of the product ids listed above.")

    while True:
        print ("What would you like to update, Name, Price, or Stock?")
        print ("1. Name")
        print ("2. Price")
        print ("3. Stock")
        print ("4. Done Editing")
        choice = input("Enter your choice: ")

        if choice == '1':
            update_product_attribute(id_of_update, 'Name')
        elif choice == '2':
            update_product_attribute(id_of_update, 'Price')
        elif choice == '3':
            update_product_attribute(id_of_update, 'Stock')
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")


# Main program loop
while True:
    print("\nMain Menu:")
    print("1. View Catalog")
    print("2. Make a Sale")
    print("3. View Sales History")
    print("4. Display Sales KPIs")
    print("5. Update Product Details")
    print("6. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        view_catalog()
    elif choice == '2':
        make_sale()
    elif choice == '3':
        view_sales_history()
    elif choice == '4':
        display_kpis()
    elif choice == '5':
        update_product_details()
    elif choice == '6':
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
