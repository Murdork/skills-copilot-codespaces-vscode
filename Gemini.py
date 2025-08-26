
# Student Number: 12345678
# No modules are imported, as per the assignment constraints.

# --- Data Structures ---

# Read-only reference data for equipment and their hire costs for the first night.
EQUIPMENT_PRICES = {
    1: {"name": "Day chairs", "cost": 15.00},
    2: {"name": "Bed chairs", "cost": 25.00},
    3: {"name": "Bite Alarm (set of 3)", "cost": 20.00},
    4: {"name": "Bite Alarm (single)", "cost": 5.00},
    5: {"name": "Bait Boat", "cost": 60.00},
    6: {"name": "Camping tent", "cost": 20.00},
    7: {"name": "Sleeping bag", "cost": 20.00},
    8: {"name": "Rods (3lb TC)", "cost": 10.00},
    9: {"name": "Rods (Bait runners)", "cost": 5.00},
    10: {"name": "Reels (Bait runners)", "cost": 10.00},
    11: {"name": "Camping Gas stove (Double burner)", "cost": 10.00},
}

# Mutable data structure to store all hire records.
# This list will be accessible by both the hiring and report functions.
hires = []
next_customer_id = 1

# --- Subroutines / Functions ---

def get_validated_input(prompt, validation_func, error_message):
    """
    Generic function to get and validate user input.
    It will repeatedly prompt the user until the input is valid.
    """
    while True:
        user_input = input(prompt)
        if validation_func(user_input):
            return user_input
        else:
            print(f"Invalid input: {error_message}")

def is_not_empty(value):
    """Validation function: checks if the input is not empty."""
    return len(value.strip()) > 0

def is_phone_number(value):
    """Validation function: checks if the input is a digit-based phone number."""
    return value.strip().isdigit() and len(value.strip()) > 0

def is_yes_or_no(value):
    """Validation function: checks if the input is 'y' or 'n'."""
    return value.strip().lower() in ['y', 'n']

def is_positive_integer(value):
    """Validation function: checks if the input is a positive integer."""
    return value.strip().isdigit() and int(value) > 0

def is_valid_equipment_choice(value):
    """Validation function: checks if the equipment choice is valid."""
    if not value.strip().isdigit():
        return False
    choice = int(value)
    return choice in EQUIPMENT_PRICES or choice == 0

def calculate_cost(hired_items, nights, is_late_return):
    """
    Calculates the total cost for a hire.
    - Standard rate for the first night.
    - 50% discount for each additional night.
    - 50% surcharge if returned late.
    """
    total_cost = 0.0
    
    for item_id, quantity in hired_items.items():
        item_cost = EQUIPMENT_PRICES[item_id]["cost"]
        
        # Cost for the first night
        first_night_cost = item_cost * quantity
        
        # Cost for additional nights (50% discount)
        additional_nights_cost = (item_cost * 0.5) * (nights - 1) * quantity
        
        total_cost += first_night_cost + additional_nights_cost

    # Extra charge for delayed return (50% of the first night's total cost)
    extra_charge = 0.0
    if is_late_return:
        base_total = sum(EQUIPMENT_PRICES[item_id]["cost"] * quantity for item_id, quantity in hired_items.items())
        extra_charge = base_total * 0.5
        total_cost += extra_charge
        
    return total_cost, extra_charge

def record_hire_details():
    """
    Task 2: Subroutine to capture customer and hire details.
    It gathers all necessary information and stores it in the global 'hires' list.
    """
    global next_customer_id
    print("\n--- New Hire Record ---")
    
    # 1. Capture Customer Details with validation
    customer_id = next_customer_id
    print(f"Assigning new Customer ID: {customer_id}")
    
    customer_name = get_validated_input("Enter customer name: ", is_not_empty, "Name cannot be blank.")
    phone_number = get_validated_input("Enter phone number: ", is_phone_number, "Please enter a valid phone number.")
    house_number = get_validated_input("Enter house number: ", is_not_empty, "House number cannot be blank.")
    postcode = get_validated_input("Enter postcode: ", is_not_empty, "Postcode cannot be blank.")
    card_ref = get_validated_input("Enter credit/debit card reference: ", is_not_empty, "Card reference cannot be blank.")

    # 2. Capture Equipment Hire Details
    hired_items = {}
    print("\n--- Available Equipment for Hire ---")
    for key, item in EQUIPMENT_PRICES.items():
        print(f"{key}. {item['name']} - £{item['cost']:.2f}")
    print("0. Finish selecting equipment")
    
    while True:
        choice_str = get_validated_input("\nEnter equipment number to add (or 0 to finish): ", is_valid_equipment_choice, "Please enter a valid number from the list.")
        choice = int(choice_str)
        
        if choice == 0:
            if not hired_items:
                print("No equipment selected. Cancelling hire.")
                return
            break
            
        quantity_str = get_validated_input(f"Enter quantity for '{EQUIPMENT_PRICES[choice]['name']}': ", is_positive_integer, "Quantity must be a positive number.")
        quantity = int(quantity_str)
        
        hired_items[choice] = hired_items.get(choice, 0) + quantity
        print(f"Added {quantity} x {EQUIPMENT_PRICES[choice]['name']}.")

    # 3. Capture Hire Duration and Return Status
    nights_str = get_validated_input("\nEnter number of nights for hire: ", is_positive_integer, "Number of nights must be a positive number.")
    nights = int(nights_str)
    
    returned_late_input = get_validated_input("Was the equipment returned late? (y/n): ", is_yes_or_no, "Please enter 'y' or 'n'.")
    returned_late = returned_late_input.lower() == 'y'

    # 4. Calculate Cost and Store Record
    total_cost, extra_charge = calculate_cost(hired_items, nights, returned_late)
    
    hire_record = {
        "customer_id": customer_id,
        "customer_name": customer_name,
        "phone_number": phone_number,
        "address": f"{house_number} {postcode}",
        "card_reference": card_ref,
        "hired_items": hired_items,
        "nights": nights,
        "returned_on_time": not returned_late,
        "total_cost": total_cost,
        "extra_charge": extra_charge
    }
    
    hires.append(hire_record)
    next_customer_id += 1
    
    print("\n--- Hire Recorded Successfully ---")
    print(f"Customer: {customer_name} (ID: {customer_id})")
    print(f"Total cost: £{total_cost:.2f}")
    print("---------------------------------")

def display_earnings_report():
    """
    Task 3: Subroutine to display the earnings report.
    It iterates through the 'hires' list and prints a formatted report.
    """
    print("\n--- Earnings Report ---")
    
    if not hires:
        print("No hires have been recorded yet.")
        print("-----------------------")
        return

    # Header
    print("{:<12} {:<40} {:<15} {:<12} {:<18} {:<15}".format(
        "Customer ID", "Equipment (Summary)", "Num. Nights", "Total Cost", "Returned on Time", "Extra Charge"
    ))
    print("-" * 115)

    grand_total_earnings = 0.0
    
    # Rows
    for record in hires:
        # Create a summary of hired equipment
        equipment_summary_list = []
        for item_id, quantity in record["hired_items"].items():
            item_name = EQUIPMENT_PRICES[item_id]["name"]
            equipment_summary_list.append(f"{item_name} (x{quantity})")
        equipment_summary = ", ".join(equipment_summary_list)
        
        # Truncate summary if too long for display
        if len(equipment_summary) > 38:
            equipment_summary = equipment_summary[:35] + "..."

        returned_on_time_str = 'y' if record["returned_on_time"] else 'n'
        
        print("{:<12} {:<40} {:<15} £{:<11.2f} {:<18} £{:<14.2f}".format(
            record["customer_id"],
            equipment_summary,
            record["nights"],
            record["total_cost"],
            returned_on_time_str,
            record["extra_charge"]
        ))
        
        grand_total_earnings += record["total_cost"]

    print("-" * 115)
    print(f"Total Cumulative Earnings: £{grand_total_earnings:.2f}")
    print("-----------------------")

def display_main_menu():
    """Displays the main menu options to the user."""
    print("\n===== Fishing and Camping Equipment Hire System =====")
    print("1. Record Customer and Hire Details")
    print("2. Display Earnings Report")
    print("3. Exit")
    print("===================================================")

def main():
    """
    Task 1: The main function to run the program.
    It displays the menu and handles user choices, calling the appropriate subroutines.
    """
    while True:
        display_main_menu()
        choice = input("Please select an option (1-3): ")
        
        if choice == '1':
            # This corresponds to Task 2
            record_hire_details()
        elif choice == '2':
            # This corresponds to Task 3
            display_earnings_report()
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            # Input validation for the menu
            print("Invalid option. Please enter 1, 2, or 3.")

# --- Program Start ---
if __name__ == "__main__":
    main()
