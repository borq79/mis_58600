# -*- coding: utf-8 -*-


###############################################################################
# MIS 58600
# Group 10 - Ryan Brock and Sachin Kumar
# Assignment 2 - Sales and Inventory Management System
###############################################################################

###############################################################################
# Notes on collaboration
#
# Tasks done by Sachin:
# 1. 
#
# Tasks done by Ryan:
# 1. 
#
# This was a 50/50 effort. We both wrote code on our own, merged the code, and
# then worked together to review bugs and clean up the code. To assist in
# ensuring we did not break anything during our sessions, we had Claude create
# a series of unit tests to validate the program. The unit tests allowed us to 
# refactor the code safely knowing we didn't break anything. They are available
# upon request. AI was not used in the creation of the code within this file,
# only the unit tests.
#
###############################################################################
# Initialize the product catalog
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
        print (f"Price       : ${product_details['Price']}")
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
        # get user input on which product to sell and how much quantity.
        id_of_sale = input("Enter the product id of the sale and the quanity: ")
        if not id_of_sale in product_catalog:
            print (f"Invalid id '{id_of_sale}'', please enter one of the product ids listed above.")
            continue
        break
            

    while True:
        try:
            quanity = int(input(f"Enter the quanity sold (in stock: {product_catalog[id_of_sale]['Stock']}): "))
            if quanity < 1 or quanity > product_catalog[id_of_sale]['Stock']:
                print (f"You've elected to sell more items ({quanity}) that are in stock ({product_catalog[id_of_sale]['Stock']}). Please try again.")
                continue  
            print (f"\nYou sold {quanity} of {id_of_sale} ({product_catalog[id_of_sale]['Name']})")
            break
        except ValueError:
            print (f"The quanity must be an integer between 1 and the number of units in stock")


    # Sachin: your code to make the sale 
    

##############################################################################
# Desc: This function will display the sales history
# Parameters: None
# Returns: None
##############################################################################
def view_sales_history():
    # Sachin: your code to view the sales history
    print("\nSales History:")


##############################################################################
# Desc: This function display the KPIs such as revenue, best-selling products
#       and the product with the highest revenue
# Parameters: None
# Returns: None
##############################################################################
def display_kpis():
    # Sachin: your code to view kpis
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

        try:
            if dictionary_key == 'Price':
                updated_value = float(updated_value)
            elif dictionary_key == 'Stock':
                updated_value = int(updated_value)
        except ValueError:
            print(f"Invalid Type for {dictionary_key}. Please try again.")
            continue

        if type(updated_value) != type(product_catalog[id_of_update][dictionary_key]):
            print (f"Invalid Type for field {dictionary_key}. Please try again.")
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
            id_of_update = input("Enter the product id of the sale: ")
            print (f"\nYou selected id: {id_of_update}, product: {product_catalog[id_of_update]['Name']}")
            break
        except KeyError:
            print (f"Invalid id '{id_of_update}'', please enter one of the product ids listed above.")

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
