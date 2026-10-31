###############################################################################
# MIS 58600
# Group 29 - Ryan Brock and Thomas Adams
# Lab 1 - A Basic Engineering and Business Calculator
###############################################################################

###############################################################################
# Notes on collaboration
#
# Tasks done by Thomas:
# 1. Engineering Calculator - menus and subsequent calculators
# 2. Business Calculator - menus and subsequent calculators
# 3. Debugging and updates during pairing session
#
# Tasks done by Ryan:
# 1. Basic application framework such as the formatting, error handlers, and
#    comment structure
# 2. Basic calculator and the actions within
# 3. Reduced the complexity of some of the functions and removed duplicate code
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

# Used for the pi value
import math


##############################################################################
# Desc: This function will handle the float inputs and handle the exceptions
#       for the user. This will allow any float value, positive or negative
# Parameters: The message to display to the user to accept input
# Returns: The user's input
##############################################################################
def read_float_input_all_real_numbers(message_to_user):
    while True:
        try:
            user_value = float(input(message_to_user))
            return user_value
        except ValueError:
            print("\n  ERROR: Only numbers are valid. Please try again. \n")

##############################################################################
# Desc: This function will handle the float inputs and handle the exceptions
#       for the user. This function ensures the values are greater than
#       or equal to 0 (e.g. no negative numbers)
# Parameters: The message to display to the user to accept input
# Returns: The user's input
##############################################################################
def read_float_input_gte_zero(message_to_user):
    while True:
        user_value = read_float_input_all_real_numbers(message_to_user)
        if user_value < 0:
            print ("\n  ERROR: Values must be greater than or equal to 0. Please try again\n")
        else:
            return user_value

##############################################################################
# Desc: This function will read the user menu choice for the submenus and 
#       verify the range of the value input to ensure it is valid
# Parameters: The message to display to the user to accept input and the max
#             menu choice
# Returns: The user's input
##############################################################################
def read_menu_choice(message_to_user, max_menu_choice):
    while True:
        try:
            user_choice = int(input(message_to_user))
            if user_choice < 1 or user_choice > max_menu_choice:
                print(f"\n  ERROR: Your choice must be between 1 and {max_menu_choice}. Please try again.\n")
                continue
            return user_choice
        except ValueError:
            print("\n  ERROR: Please enter valid integers only. Try again. \n")


##############################################################################
# Desc: This function will calculate a break even point
# Parameters: None
# Returns: Void
##############################################################################
# Break Even Calculator
def break_even_point():
    print("  ##")
    print("  ## Calculate the Break Even Point \n")

    fixed_costs    = read_float_input_gte_zero("  ## Please enter the Fixed Costs = $ ")

    while True:
        sales_price    = read_float_input_gte_zero("  ## Please enter the per unit Sales Price = $ ")
        variable_costs = read_float_input_gte_zero("  ## Please enter the per unit Variable Costs. = $ ")

        # This ensures we do not have a scenario where we divide by zero. Variable costs can be 0, but
        # sales price cannot
        if variable_costs < sales_price:
            break
        else:
            print("\n  ERROR: Your Variable Costs cannot equal or exceed your Sales Price. Please try again.\n")

    # The above handlers allow 0 for the variable costs, which is valid. It does ensure that there are no
    # divide by zero scenarios, so sales_price - variable_costs cannot equal zero. 
    break_even_units = round(fixed_costs / (sales_price - variable_costs), 2)
    print(f"\n  The break even point = {break_even_units} units.\n")


##############################################################################
# Desc: This function will calculate compound interest
# Parameters: None
# Returns: Void
##############################################################################
# Compound Interest Calculator
def compound_interest():
    print("  ##")
    print("  ## Calculate Compound Interest \n")

    principal       = read_float_input_gte_zero("  ## Please enter the initial principal. p =$ ")
    annual_interest = read_float_input_gte_zero("  ## Please enter the interest rate (if 5% enter 5). i = ")
    number_periods  = read_float_input_gte_zero("  ## Please enter the number of periods. n = ")
    
    compounded = round((principal * (1 + (annual_interest/100))**number_periods) - principal, 2)
    balance = compounded + principal
    print(f"\n  The compounded interest of ${principal:.2f} at {annual_interest}% for {number_periods} periods. = ${compounded:.2f}, which brings your balance to ${balance:.2f}.\n")

##############################################################################
# Desc: This function will convert kilograms to pounds
# Parameters: None
# Returns: Void
##############################################################################
# Convert Kilograms to Pounds
def kilograms_to_pounds():
    print("  ##")
    print("  ## Convert Kilograms to Pounds \n")

    kilos = read_float_input_gte_zero("  ## Please enter the mass in kilograms. m = ")

    pounds = round(kilos * 2.20462, 2)
    
    print(f"\n  A mass of {kilos} kg weighs {pounds} lbs.\n\n")
    
##############################################################################
# Desc: This function will convert meters to feet
# Parameters: None
# Returns: Void
##############################################################################
# Convert Meters to Feet
def meters_to_feet():
    print("  ##")
    print("  ## Convert Meters to Feet \n")

    meters = read_float_input_gte_zero("  ## Please enter the length in meters. l = ")

    feet = round(meters * 3.28084, 2)
    
    print(f"\n  The length of {meters} m  = {feet} ft.\n\n")

##############################################################################
# Desc: This function will calculate the area of a circle
# Parameters: None
# Returns: Void
##############################################################################
# Area of a Circle
def circle_area():
    print("  ##")
    print("  ## Calculate the area of a Circle \n")

    radius = read_float_input_gte_zero("  ## Please enter the radius of the circle. r = ")
    area_circle = round(math.pi * radius ** 2, 2)
    
    print(f"\n  The area of your circle is pi * {radius}^2  = {area_circle}\n\n")



##############################################################################
# Desc: This function will calculate the area of a rectangle
# Parameters: None
# Returns: Void
##############################################################################
# Area of a Rectangle
def rectangle_area():
    print("  ##")
    print("  ## Calculate the area of a Rectangle \n")


    length = read_float_input_gte_zero("  ## Please enter the length of the rectangle. l = ")
    width  = read_float_input_gte_zero("  ## Please enter the width of the rectangle. w = ")

    area_rectangle = round(length * width, 2)
    
    print(f"\n  The area of your rectangle is {length} * {width}  = {area_rectangle}\n\n")

##############################################################################
# Desc: This function will calculate the area of a triangle
# Parameters: None
# Returns: Void
##############################################################################
# Area of a Triangle
def triangle_area():
    print("  ##")
    print("  ## Calculate the area of a Triangle \n")

    base   = read_float_input_gte_zero("  ## Please enter the base of the triangle. b = ")
    height = read_float_input_gte_zero("  ## Please enter the altitude height of the triangle. h = ")

    area_triangle = round((base * height)/2, 2)
    
    print(f"\n  The area of your triangle is ({base} * {height})/2  = {area_triangle}\n\n")

##############################################################################
# Desc: This function will calculate the volume of a cylinder
# Parameters: None
# Returns: Void
##############################################################################
# Volume of a Cylinder
def cylinder_volume():
    print("  ##")
    print("  ## Calculate the volume of a Cylinder \n")

    radius_cylinder = read_float_input_gte_zero("  ## Please enter the radius of the cylinder. r = ")
    height_cylinder = read_float_input_gte_zero("  ## Please enter the altitude height of the cylinder. h = ")

    volume_cylinder = round(math.pi * radius_cylinder ** 2 * height_cylinder, 2)
    
    print(f"\n  The volume of your cylinder is pi * {radius_cylinder}^2 * {height_cylinder}  = {volume_cylinder}\n\n")



##############################################################################
# Desc: This function will calculate the volume of a cone
# Parameters: None
# Returns: Void
##############################################################################
# Volume of a Cone
def cone_volume():
    print("  ##")
    print("  ## Calculate the volume of a Cone \n")

    radius_cone = read_float_input_gte_zero("  ## Please enter the radius of the cone. r = ")
    height_cone = read_float_input_gte_zero("  ## Please enter the altitude height of the cone. h = ")

    volume_cone = round((math.pi * radius_cone ** 2 * height_cone)/3, 2)
    
    print(f"\n  The volume of your cone is (pi * {radius_cone}^2 * {height_cone})/3  = {volume_cone}\n\n")

##############################################################################
# Desc: This function will calculate the volume of a cube
# Parameters: None
# Returns: Void
##############################################################################
# Volume of a Cube
def cube_volume():
    print("  ##")
    print("  ## Calculate the volume of a Cube \n")

    side_length = read_float_input_gte_zero("  ## Please enter the side length of the cube. s = ")

    volume_cube = round(side_length ** 3, 2)
    
    print(f"\n  The volume of your cube is {side_length}^3  = {volume_cube}\n\n")


##############################################################################
# Desc: This will execute Volume Menu
# Parameters: None
# Returns: Void
##############################################################################
# Volume Calculations
def volume_calculator():
    print("  ##")
    print("  ## Volume Calculator \n")
    print("  ## Please select one of the following Geometric Shapes: ")
    print("  ## 1. Cube")
    print("  ## 2. Cylinder")
    print("  ## 3. Cone")

    user_choice = read_menu_choice("  ## Select an option 1, 2, or 3: ", 3)

    if user_choice == 1:
        cube_volume()
    elif user_choice == 2:
        cylinder_volume()
    elif user_choice == 3:
        cone_volume()

##############################################################################
# Desc: This will execute Area Menu
# Parameters: None
# Returns: Void
##############################################################################
# Area Calculations
def area_calculator():
    print("  ##")
    print("  ## Area Calculator \n")
    print("  ## Please select one of the following Geometric Shapes: ")
    print("  ## 1. Triangle")
    print("  ## 2. Rectangle")
    print("  ## 3. Circle")

    user_choice = read_menu_choice("  ## Select an option 1, 2, or 3: ", 3)

    if user_choice == 1:
        triangle_area()
    elif user_choice == 2:
        rectangle_area()
    elif user_choice == 3:
        circle_area()

##############################################################################
# Desc: This is the menu for Geometric Calculators (Area or Volume)
# Parameters: None
# Returns: Void
##############################################################################
# Geometry Choices
def geometry_choices():
    print("  ##")
    print("  ## Geometry Calculator \n")
    print("  ## Please select one of the following Geometry Calculators: ")
    print("  ## 1. Area")
    print("  ## 2. Volume")

    user_choice = read_menu_choice("  ## Select an option 1 or 2: ", 2)

    if user_choice == 1:
        area_calculator()
    elif user_choice == 2:
        volume_calculator()


##############################################################################
# Desc: This is the menu for Unit Conversions
# Parameters: None
# Returns: Void
##############################################################################
def unit_choices():
    print("  ##")
    print("  ## Unit Conversions Calculator \n")
    print("  ## Please select one of the following Unit Conversions: ")
    print("  ## 1. Convert Meters to Feet")
    print("  ## 2. Convert Kilograms to Pounds")

    user_choice = read_menu_choice("  ## Select an option 1 or 2: ", 2)

    if user_choice == 1:
        meters_to_feet()
    elif user_choice == 2:
        kilograms_to_pounds()


##############################################################################
# Desc: This is the menu for Business Calculations
# Parameters: None
# Returns: Void
##############################################################################
def business_calculations():
    print("  ##")
    print("  ## Business Calculator \n")
    print("  ## Please select one of the following Business Calculations: ")
    print("  ## 1. Calculate Compound Interest")
    print("  ## 2. Calculate Break Even Point")

    user_choice = read_menu_choice("  ## Select an option 1 or 2: ", 2)

    if user_choice == 1:
        compound_interest()
    elif user_choice == 2:
        break_even_point()



    
##############################################################################
# Desc: This will execute the Engineering Calculations
# Parameters: None
# Returns: Void
##############################################################################
def engineering_calculations():

    print("  ##")
    print("  ## Engineering Calculator \n")
    print("  ## Please select one of the following operations: ")
    print("  ## 1. Geometry Calculator")
    print("  ## 2. Unit Conversions")

    user_choice = read_menu_choice("  ## Select an option 1 or 2: ", 2)

    if user_choice == 1:
        geometry_choices()
    elif user_choice == 2:
        unit_choices()
   
##############################################################################
# Desc: This will execute the basic calculator functions
# Parameters: None
# Returns: Void
##############################################################################
def basic_calculator_operations():
    print("  ##")
    print("  ## Basic Mathematical Operations \n")

    while True:
        user_operation = input("  ## Choose which operation you'd like to use +, -, *, /, mod, or ^:  ")

        # [Attention to the grader] This isn't in the material covered exactly, however this makes the code slightly cleaner and is
        # easier to read and understand
        if user_operation not in ["+", "-", "*", "/", "mod", "^"]:
            print("\n  ERROR: You must pick one of: +, -, *, /, mod, or ^. Try again.\n")
            continue

        left_value  = read_float_input_all_real_numbers("  ## What number is on the left side of the operation:  ")
        right_value = read_float_input_all_real_numbers("  ## What number is on the right side of the operation:  ")
        break

    try:
        if user_operation == "+":
            result = left_value + right_value
        elif user_operation == "-":
            result = left_value - right_value
        elif user_operation == "*":
            result = left_value * right_value
        elif user_operation == "/":
            result = left_value / right_value
        elif user_operation == "mod":
            result = left_value % right_value
        elif user_operation == "^":
            result = left_value ** right_value
    
        print(f"\n  Result of Calculation {left_value} {user_operation} {right_value} = {result}\n\n")
    except ZeroDivisionError:
        print("\n  ERROR: Your input values resulted in a divide by zero scenario, please try again\n")

##############################################################################
# Desc: This function renders the user menu
# Parameters: None
# Returns: Void
##############################################################################
def show_main_menu():
    print("  ############ A Basic Engineering and Business Calculator ############")
    print("  ##")
    print("  ## Welcome to the Basic Engineering and Business Calculator. ")
    print("  ## Please select one of the following operations: ")
    print("  ## 1. Basic Mathematical Operations")
    print("  ## 2. Engineering Calculations")
    print("  ## 3. Business Calculations")
    print("  ## 4. Exit")
    print("  ##")

##############################################################################
# Desc: This will execute the respective calculator function based on the 
#       user's selection from the menu
# Parameters: user_choice: int [1-3]
# Returns: Void
##############################################################################
def execute_user_option(user_choice):
    print("\n  You've chosen option " + str(user_choice) + "\n")

    if user_choice == 1:
        basic_calculator_operations()
    elif user_choice == 2:
        engineering_calculations()
    elif user_choice == 3:
        business_calculations()


##############################################################################
# Desc: Main entry into the Python application loop
# Parameters: None
# Returns: Void
##############################################################################
def main():

    while True:
        show_main_menu()
        user_choice = read_menu_choice("  ## Select an option 1, 2, or 3 (or 4 to exit): ", 4)

        if user_choice == 4:
            print("\n  Goodbye!")
            break

        execute_user_option(user_choice)


if __name__ == "__main__":
    main()


