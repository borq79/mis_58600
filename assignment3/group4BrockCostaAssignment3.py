# -*- coding: utf-8 -*-
import numpy as np


###############################################################################
# MIS 58600
# Group 4 - Ryan Brock and Alvaro Simoes Francisco da Costa
# Assignment 3 - Data Analysis and Statistical Operations using Numpy
###############################################################################

###############################################################################
# Notes on collaboration
#
# Tasks done by Alvaro:
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
# upon request. 
#
###############################################################################



## TODO and NOTES
# Note: To get full credit on this assignment, you must use Numpy’s vectorized operations, ufuncs, and boolean/ indexing whenever applicable. 


daily_power_usage = np.array([
    [15, 18, 20, 22, 25, 30, 28],  # Household 1
    [35, 38, 40, 45, 50, 48, 42],  # Household 2
    [8, 10, 12, 15, 10, 8, 9],     # Household 3
    [50, 55, 60, 65, 70, 75, 80]   # Household 4 (High user)
])

sales_data = np.array([[200, 250, 300, 150],  # Jan
                       [180, 220, 280, 140],  # Feb
                       [220, 270, 310, 170],  # Mar
                       [210, 260, 330, 160],  # Apr
                       [230, 280, 320, 180],  # May
                       [190, 240, 300, 150],  # Jun
                       [210, 260, 310, 160],  # Jul
                       [250, 290, 340, 190],  # Aug
                       [220, 270, 310, 170],  # Sep
                       [230, 280, 320, 180],  # Oct
                       [240, 290, 330, 190],  # Nov
                       [260, 300, 340, 200]]) # Dec

months = np.array(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])


##############################################################################
# Desc: 
# Part 1: Data Manipulation and Analysis
# 1.    Creating Arrays:
#   -   Create a 1D array of 100 random integers between 1 and 500.
#   -   Reshape the 1D array into a 10x10 matrix.
# 2.    Array Slicing and Indexing:
#   -   Extract all elements from the third column of the matrix.
#   -   Extract the submatrix consisting of rows 2 through 5 and columns 4 through 8.
# 3.    Filtering Data:
#   -   Find all elements in the matrix that are greater than 200.
#   -   Replace all elements in the matrix that are less than 100 with a value of 0.
# 4.    Basic Statistical Analysis:
#   -   Calculate the mean, median, standard deviation, and variance of the entire matrix.
#   -   Calculate the mean of each row and each column.
# 5.    Sorting:
#   -   Sort each row of the matrix in ascending order.
#   -   Sort the entire matrix by the values in the second column
# Parameters: None
# Returns: None
##############################################################################
def partOneOperations(): 
    print("\n###################################################")
    print(" Part 1: Data Manipulation and Analysis ")
    print("###################################################")



##############################################################################
# Desc: 
# Part 2: Business Analytics Use Cases
# 6.    Power Consumption Analysis for Smart Grid Optimization: A smart grid 
#       system collects energy consumption data from multiple households in a 
#       city. The utility company wants to
#   -   Estimate total monthly power consumption based on daily usage.
#   -   Compute power wastage by comparing usage to an efficiency threshold.
#   -   Adjust energy bills dynamically using tiered pricing:
#       1.  Low usage (< 500 kWh) → Standard rate ($0.12 per kWh)
#       2.  Medium usage (500-1000 kWh) → Slightly higher rate ($0.15 per kWh)
#       3.  High usage (> 1000 kWh) → Premium rate ($0.20 per kWh)
#   -   Using NumPy's vectorized operations and ufuncs, help the company analyze 
#       and optimize power consumption by performing the above stated tasks
# 7.    Sales Data Analysis: A company has sales data for 4 products over 12 months
#   -   Find the total sales for each product over the year.
#   -   Find the month with the highest sales for each product.
#   -   Calculate the average sales per month across all products.
#   -   Find the product that has the highest average monthly sales
# Parameters: None
# Returns: None
##############################################################################
def partTwoOperations():
    print("\n\n###################################################")
    print(" Part 2: Business Analytics Use Cases ")
    print("###################################################")

    print("\n########################################")
    print(" Question 6 ")
    print("########################################")

    print("\n########################################")
    print(" Question 7 ")
    print("########################################")

    ########################################################################
    # Find the total sales for each product over the year
    ########################################################################
    total_sales_per_product = sales_data.sum(axis = 0)
    print("\nThe total sales for each product over the year (products are referenced as 0-based): ")
    for product in range(sales_data.shape[1]):
        print(f" Product {product}: {total_sales_per_product[product]}")

    ########################################################################
    # Find the month with the highest sales for each product.
    ########################################################################
    monthly_highest_sales = sales_data.max(axis = 0)

    # Build a 12x4 boolean mask with each value True if it is the highest sales
    # False if it is not. This is just so we can output an easier to read
    # format
    is_month_with_highest_sales = sales_data == monthly_highest_sales

    print("\nThe highest monthly sales for each product: ")

    # Iterate over each product. The number of products is defined by the 'shape' of the number of columns (index 1)
    for product in range(sales_data.shape[1]):
        # Print the month with the highest sales and the corresponding sales figure
        print(f"Product {product}: {months[is_month_with_highest_sales[:, product]]} {monthly_highest_sales[product]} units")
    
    ########################################################################
    # Calculate the average sales per month across all products.
    ########################################################################
    average_sales_per_month_across_all_products = sales_data.mean(axis = 1)
    print("\nThe average sales per month across all products: ")
    for i in range(len(months)):
        print(f" {months[i]}: {average_sales_per_month_across_all_products[i]:6.2f}")

    ########################################################################
    # Find the product that has the highest average monthly sales
    ########################################################################
    average_monthly_sales_per_product = sales_data.mean(axis = 0)
    highest_product_average = average_monthly_sales_per_product.max()

    # Create a way to find the highest product using the index
    product_numbers = np.arange(0, sales_data.shape[1])

    # build up a 4 element boolean mask to find the highest average
    is_highest_product = average_monthly_sales_per_product == highest_product_average

    print(f"\nThe product that has the highest average monthly sales is product {product_numbers[is_highest_product]} {highest_product_average:.2f} units")


##############################################################################
# Desc: 
# Part 3: Linear Regression Using Numpy
# 8.    Linear Regression: You are given a dataset representing the sales of a 
#       product (y) based on the advertising budget (x). Use Numpy to calculate 
#       the best-fit line using the formula for linear regression
#   -   Given n datapoints, calculate the slope (m) and intercept (c) of the 
#       best-fit line using the least squares method
#   -   Predict the sales for an advertising budget of 120 using the computed 
#       values of m and c.
#   -   Calculate the mean squared error (MSE) of the regression model
# Parameters: None
# Returns: None
##############################################################################
def partThreeOperations():
    print("\n\n###################################################")
    print(" Part 3: Linear Regression Using Numpy ")
    print("###################################################")

    print("\n########################################")
    print(" Question 8 ")
    print("########################################")

    # Advertising budget (x) and sales (y):
    x = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    y = np.array([25, 45, 65, 80, 100, 130, 150, 180, 210, 240])

    ########################################################################
    # Calculate the slope (m) and intercept (c) of the best-fit line using the least squares method
    ########################################################################

    # Get the number of data points first, to make it easier
    n = x.size

    m = ((n * np.sum(x * y)) - ((np.sum(x)) * (np.sum(y)))) / ((n * np.sum(x * x)) - (np.sum(x) ** 2))
    print(f"The slope (m) is: {m:.4f}")

    c = np.mean(y) - (m * np.mean(x))
    print(f"The y-intercept (c) is: {c:.4f}")

    ########################################################################
    # Predict the sales for an advertising budget of 120 using the computed values of m and c.
    ########################################################################
    print(f"The predicted sales for an advertising budget of $120 is: {((m * 120) + c):.2f}")


    ########################################################################
    # Calculate the mean squared error (MSE) of the regression model.
    ########################################################################
    y_predicted = m * x + c
    squared_errors = (y - y_predicted) ** 2
    mse = np.mean(squared_errors)
    print(f"The Mean Squared Error (MSE): {mse:.4f}")



partOneOperations()
partTwoOperations()
partThreeOperations()
