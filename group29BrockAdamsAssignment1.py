###############################################################################
# MIS 58600
# Group 29 - Ryan Brock and Thomas Adams
# Lab 1 - A Basic Engineering and Business Calculator
###############################################################################

## TODOS ##
# 1. Catch divide by zero errors
# 2. Improve error messages per the rubric
# 3. handle decimal input
# 4. Check the inputs right after and don't allow them to enter both and then check
# 
# The 7 bugs still open:
# Ryan
# - Dividing by zero crashes
# - Mod by zero crashes
# - The basic calculator doesn't take decimals

# Thomas
# - A negative radius is accepted
# - Break-even crashes when price = variable cost
# - Break-even can give negative units
# - The area menu's error message says "1 or 2"

import math


##############################################################################
# Desc: This function will handle the float inputs and handle the exceptions
#       for the user.
# Parameters: The message to display to the user to accept input
# Returns: The user's input
##############################################################################
def read_float_input(message_to_user):
    while True:
        try:
            user_value = float(input(message_to_user))
            if user_value < 0:
                print ("\n  ERROR: Values must be greater than or equal to 0. Please try again")
            else:
                return user_value
        except ValueError:
            print("\n  ERROR: Only numbers are valid. Please try again. \n")

##############################################################################
# Desc: This function will calculate a break even point
# Parameters: None
# Returns: Void
##############################################################################
# Break Even Calculator
def break_even_point():
    print("  ##")
    print("  ## Calculate the Break Even Point \n")

    fixed_costs    = read_float_input("  Please enter the Fixed Costs = $ ")
    sales_price    = read_float_input("  Please enter the per unit Sales Price = $ ")
    while True:
        variable_costs = read_float_input("  Please enter the Variable Costs. = $ ")
        if variable_costs < sales_price:
            break
        else:
            print("Your Variable Costs cannot equal nor exceed your Sales Price. Please try again.")
    # try:
        break_even_units = round(fixed_costs / (sales_price - variable_costs), 2)
        print(f"  The break even point = {break_even_units} units.")
    # except ZeroDivisionError:
    #     print("  ERROR: The variable costs and sales price are the same, which resulted in a divide by zero, please try again")


##############################################################################
# Desc: This function will calculate compound interest
# Parameters: None
# Returns: Void
##############################################################################
# Compound Interest Calculator
def compound_interest():
    print("  ##")
    print("  ## Calculate Compound Interest \n")

    principal       = read_float_input("  Please enter the intitial principal. p =$ ")
    annual_interest = read_float_input("  Please enter the interest rate (if 5% enter 5). i = ")
    number_periods  = read_float_input("  Please enter the number of periods. n = ")
    
    compounded = round((principal * (1 + (annual_interest/100))**number_periods) - principal, 2)
    balance = compounded + principal
    print(f"  The compounded interest of $ {principal} at {annual_interest} % for {number_periods} periods. = ${compounded}, which brings your balance to ${balance}.")

##############################################################################
# Desc: This function will convert kilograms to pounds
# Parameters: None
# Returns: Void
##############################################################################
# Convert Kilograms to Pounds
def kilograms_to_pounds():
    print("  ##")
    print("  ## Convert Kilograms to Pounds \n")

    kilos = read_float_input("  Please enter the mass in kilograms. m = ")

    pounds = round(kilos * 2.20462, 2)
    
    print(f"  A mass of {kilos} kg weighs {pounds} lbs.\n\n")
    
##############################################################################
# Desc: This function will convert meters to feet
# Parameters: None
# Returns: Void
##############################################################################
# Convert Meters to Feet
def meters_to_feet():
    print("  ##")
    print("  ## Convert Meter to Feet \n")

    meters = read_float_input("  Please enter the length in meters. l = ")

    feet = round(meters * 3.28084, 2)
    
    print(f"  The length of {meters} m  = {feet} ft.\n\n")

##############################################################################
# Desc: This function will calculate the area of a circle
# Parameters: None
# Returns: Void
##############################################################################
# Area of a Circle
def circle_area():
    print("  ##")
    print("  ## Calculate the area of a Circle \n")

    radius = read_float_input("  ## Please enter the radius of the circle. r = ")
    area_circle = round(math.pi * radius ** 2, 2)
    
    print(f"  The area of your circle is pi * {radius}^2  = {area_circle}\n\n")



##############################################################################
# Desc: This function will calculate the area of a rectangle
# Parameters: None
# Returns: Void
##############################################################################
# Area of a Rectangle
def rectangle_area():
    print("  ##")
    print("  ## Calculate the area of a Rectangle \n")


    length = read_float_input("  ## Please enter the length of the rectangle. l = ")
    width  = read_float_input("  ## Please enter the width of the rectangle. w = ")

    area_rectangle = round(length * width, 2)
    
    print(f"  The area of your rectangle is {length} * {width}  = {area_rectangle}\n\n")

##############################################################################
# Desc: This function will calculate the area of a triangle
# Parameters: None
# Returns: Void
##############################################################################
# Area of a Triangle
def triangle_area():
    print("  ##")
    print("  ## Calculate the area of a Triangle \n")

    base   = read_float_input("  ## Please enter the base of the triangle. b = ")
    height = read_float_input("  ## Please enter the altitude height of the triangle. h = ")

    area_triangle = round((base * height)/2, 2)
    
    print(f"  The area of your triangle is ({base} * {height})/2  = {area_triangle}\n\n")

##############################################################################
# Desc: This function will calculate the volume of a cylinder
# Parameters: None
# Returns: Void
##############################################################################
# Volume of a Cylinder
def cylinder_volume():
    print("  ##")
    print("  ## Calculate the volume of a Cylinder \n")

    radius_cylinder = read_float_input("  ## Please enter the radius of the cylinder. r = ")
    height_cylinder = read_float_input("  ## Please enter the altitude height of the cylinder. h = ")

    volume_cylinder = round(math.pi * radius_cylinder ** 2 * height_cylinder, 2)
    
    print(f"  The volume of your cylinder is pi * {radius_cylinder}^2 * {height_cylinder}  = {volume_cylinder}\n\n")



##############################################################################
# Desc: This function will calculate the volume of a cone
# Parameters: None
# Returns: Void
##############################################################################
# Volume of a Cone
def cone_volume():
    print("  ##")
    print("  ## Calculate the volume of a Cone \n")

    radius_cone = read_float_input("  ## Please enter the radius of the cone. r = ")
    height_cone = read_float_input("  ## Please enter the altitude height of the cone. h = ")

    volume_cone = round((math.pi * radius_cone ** 2 * height_cone)/3, 2)
    
    print(f"  The volume of your cone is (pi * {radius_cone}^2 * {height_cone})/3  = {volume_cone}\n\n")

##############################################################################
# Desc: This function will calculate the volume of a cube
# Parameters: None
# Returns: Void
##############################################################################
# Volume of a Cube
def cube_volume():
    print("  ##")
    print("  ## Calculate the volume of a Cube \n")

    side_length = read_float_input("  ## Please enter the side legnth of the cube. s = ")

    volume_cube = round(side_length ** 3, 2)
    
    print(f"  The volume of your cube is {side_length}^3  = {volume_cube}\n\n")


##############################################################################
# Desc: This will execute Volume Menu
# Parameters: user_choice: int [1-3]
# Returns: Void
##############################################################################
# Volume Calculations
def volume_calculator():
    print("Cubes, Cylinder, or Cones?")
    print("  ##")
    print("  ## Volume Calculator \n")
    print("  ## Please select one of the following Geometric Shapes: ")
    print("  ## 1. Cube")
    print("  ## 2. Cylinder")
    print("  ## 3. Cone")
    while True:
        try:
            user_choice = int(input("  ## Select an option 1, 2, or 3: "))
            break
        except ValueError:
            print("\n  ERROR: Please enter numbers only. Try again. \n")

    if user_choice == 1:
        cube_volume()
    elif user_choice == 2:
        cylinder_volume()
    elif user_choice == 3:
        cone_volume()
    else:
        raise ValueError("  ERROR: Your choice must be 1 or 2, please try again. ")

##############################################################################
# Desc: This will execute Area Menu
# Parameters: user_choice: int [1-3]
# Returns: Void
##############################################################################
# Area Calculations
def area_calculator():
    print("Triangles, retangles, or crcles?")
    print("  ##")
    print("  ## Area Calculator \n")
    print("  ## Please select one of the following Geometric Shapes: ")
    print("  ## 1. Triangle")
    print("  ## 2. Rectangle")
    print("  ## 3. Circle")
    while True:
        try:
            user_choice = int(input("  ## Select an option 1, 2, or 3: "))
            break
        except ValueError:
            print("\n  ERROR: Please enter numbers only. Try again. \n")

    if user_choice == 1:
        triangle_area()
    elif user_choice == 2:
        rectangle_area()
    elif user_choice == 3:
        circle_area()
    else:
        raise ValueError("  ERROR: Your choice must be 1 or 2, please try again. ")

##############################################################################
# Desc: This is the menu for Geometric Calculators (Area or Volume)
# Parameters: user_choice: int [1-2]
# Returns: Void
##############################################################################
# Geometry Choices
def geometry_choices():
    print("Area or Volume")
    print("  ##")
    print("  ## Geometry Calculator \n")
    print("  ## Please select one of the following Geometry Calculators: ")
    print("  ## 1. Area")
    print("  ## 2. Volume")
    while True:
        try:
            user_choice = int(input("  ## Select an option 1 or 2: "))
            break
        except ValueError:
            print("\n  ERROR: Please enter numbers only. Try again. \n")

    if user_choice == 1:
        area_calculator()
    elif user_choice == 2:
        volume_calculator()
    else:
        raise ValueError("  ERROR: Your choice must be 1 or 2, please try again. ")


##############################################################################
# Desc: This is the menu for Unit Conversions
# Parameters: user_choice: int [1-2]
# Returns: Void
##############################################################################
# Geometry Choices
def unit_choices():
    print("Unit Conversions")
    print("  ##")
    print("  ## Unit Conversions Calculator \n")
    print("  ## Please select one of the following Unit Conversions: ")
    print("  ## 1. Convert Meters to Feet")
    print("  ## 2. Convert Kilograms to Pounds")
    while True:
        try:
            user_choice = int(input("  ## Select an option 1 or 2: "))
            break
        except ValueError:
            print("\n  ERROR: Please enter numbers only. Try again. \n")

    if user_choice == 1:
        meters_to_feet()
    elif user_choice == 2:
        kilograms_to_pounds()
    else:
        raise ValueError("  ERROR: Your choice must be 1 or 2, please try again. ")

##############################################################################
##############################################################################
# Desc: This is the menu for Business Calculations
# Parameters: user_choice: int [1-2]
# Returns: Void
##############################################################################
# Business Choices
def business_calculations():
    print("  ##")
    print("  ## Business Calculator \n")
    print("  ## Please select one of the following Unit Conversions: ")
    print("  ## 1. Calculate Compound Interest")
    print("  ## 2. Calculate Break Even Point")
    while True:
        try:
            user_choice = int(input("  ## Select an option 1 or 2: "))
            break
        except ValueError:
            print("\n  ERROR: Please enter numbers only. Try again. \n")

    if user_choice == 1:
        compound_interest()
    elif user_choice == 2:
        break_even_point()
    else:
        raise ValueError("  ERROR: Your choice must be 1 or 2, please try again. ")



    
##############################################################################
# Desc: This will execute the Engineering Calculations
# Parameters: user_choice: int [1-2]
# Returns: Void
##############################################################################
# Engineering Calculator Function
def engineering_calculations():

    print("  ##")
    print("  ## Engineering Calculator \n")
    print("  ## Please select one of the following operations: ")
    print("  ## 1. Geometry Calculator")
    print("  ## 2. Unit Conversions")
    while True:
        try:
            user_choice = int(input("  ## Select an option 1 or 2: "))
            break
        except ValueError:
            print("\n  ERROR: Please enter numbers only. Try again. \n")


    if user_choice == 1:
        geometry_choices()
    elif user_choice == 2:
        unit_choices()
    else:
        raise ValueError("  ERROR: Your choice must be 1 or 2, please try again. ")
   
##############################################################################
# Desc: This will execute the basic calculator functions
# Parameters: None
# Returns: Void
##############################################################################
def basic_calculator_operations():
    print("  ##")
    print("  ## Basic Mathematical Operations \n")

    user_operation = input("  ## Choose which operation you'd like to use +, -, *, /, mod, or ^:  ")
    while True:
        try:
            left_value = int(input("  ## What number is on the left side of the operation:  "))
            right_value = int(input("  ## What number is on the right side of the operation:  "))
            break
        except ValueError:
            print("\n  ERROR: Please enter numbers only. Try again. \n")


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
        else:
            raise ValueError("  ERROR: You must pick one of the following operations: +, -, *, /, mod, or ^, please try again. ")
    
        print(f"  Result of Calculation {left_value} {user_operation} {right_value} = {result}\n\n")
    except ZeroDivisionError:
        print("  ERROR: Your input values resulted in a divide by zero scenario, please try again")

##############################################################################
# Desc: This function renders the user menu
# Parameters: None
# Returns: Void
##############################################################################
def show_menu():
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
# Desc: This will execute the respective calculator funciton based on the 
#       the user's selection from the menu
# Parameters: user_choice: int [1-3]
# Returns: Void
##############################################################################
def execute_user_option(user_choice):
    print("  You've chosen option " + str(user_choice))

    if user_choice == 1:
        basic_calculator_operations()
    elif user_choice == 2:
        engineering_calculations()
    elif user_choice == 3:
        business_calculations()
    else:
        raise ValueError("  ERROR: Your choice must be 1, 2, or 3, please try again. ")


##############################################################################
# Desc: This will read the user's input for the menu choice and return it
# Parameters: None
# Returns: user_choice: int [1-3]
##############################################################################
def read_user_menu_choice():
    while True:
        try:
            user_choice = int(input("  ## Select an option 1, 2, or 3 (or 4 to exit): "))
            break
        except ValueError:
            print("\n  ERROR: Please enter numbers only. Try again. \n")

    if user_choice == 4:
        quit()

    elif user_choice < 1 or user_choice > 3:
        raise ValueError("  ERROR: Your choice must be 1, 2, or 3, please try again. ")

    return user_choice


##############################################################################
# Desc: Main entry into the Python application loop
# Parameters: None
# Returns: Void
##############################################################################
def main():

    while True:
        try:
            show_menu()
            user_choice = read_user_menu_choice()
            execute_user_option(user_choice)
        except ValueError as e:
            print (f"{e}\n\n")

if __name__ == "__main__":
    main()


