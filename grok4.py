# Fishing and Camping Equipment Hire System
# This program implements a menu-driven system for recording equipment hires and generating earnings reports.
# No external modules are imported as per assignment constraints.
# Data is stored in a list of dictionaries for accessibility across functions.
# Input validation is included where applicable.
# Equipment uses 3-letter codes for input, mapped to full names and prices.
# Customer details (except ID) are entered in a single comma-separated line.
# Hire items are entered on separate lines (code,qty per line) until empty input.
# Number of nights asked separately.
# Returned after 2pm (late) asked separately as Y/N.
# Credit card input validated to be exactly 4 digits.
# Total cost calculation: base price for first night, 50% of base for each additional night, plus 50% of base if late return.

# Define equipment with 3-letter codes (read-only reference data)
# Format: code: (full_name, price)
equipment_data = {
    "DAY": ("Day chairs", 15.00),
    "BED": ("Bed chairs", 25.00),
    "BAS": ("Bite Alarm (set of 3)", 20.00),
    "BAI": ("Bite Alarm (single)", 5.00),
    "BAB": ("Bait Boat", 60.00),
    "CAT": ("Camping tent", 20.00),
    "SLB": ("Sleeping bag", 20.00),
    "R3T": ("Rods (3lb TC)", 10.00),
    "RBR": ("Rods (Bait runners)", 5.00),
    "REB": ("Reels (Bait runners)", 10.00),
    "CGS": ("Camping Gas stove (Double burner)", 10.00)
}

# Global list to store hire details (mutable data structure)
hires = []

def main_menu():
    """
    Displays the main menu and handles user choices.
    Loops until Exit is selected.
    For Option 1, loops to allow multiple hires until user chooses not to enter another.
    """
    while True:
        print("\nMain Menu:")
        print("1. Customer and hire details")
        print("2. Earnings report")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()
        
        # Input validation for menu choice
        if choice == '1':
            while True:
                hire_equipment()
                again = input("\nWould you like to enter another new hire? (Y/N): ").strip().upper()
                while again not in ['Y', 'N']:
                    print("Invalid input: must be Y or N.")
                    again = input("Would you like to enter another new hire? (Y/N): ").strip().upper()
                if again != 'Y':
                    break
        elif choice == '2':
            earnings_report()
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def hire_equipment():
    """
    Subroutine for Option 1: Records customer and hire details.
    Prompts for customer ID with validation (non-empty).
    Then prompts for a single comma-separated line for name, phone, house, postcode, last 4 digits of card.
    Validates that exactly 5 parts are provided, non-empty, and card is 4 digits.
    Then loops to enter item code,qty on separate lines until empty input.
    Then asks for number of nights separately.
    Then asks if returned after 2pm (late) as Y/N.
    Stores the hire in the global hires list.
    """
    print("\nEntering Customer and Hire Details:")
    
    # Prompt for customer ID with validation (loop until non-empty)
    customer_id = ""
    while not customer_id:
        customer_id = input("Customer ID: ").strip()
        if not customer_id:
            print("Customer ID cannot be empty.")
    
    # Prompt for customer details as single line
    while True:
        line = input("\nEnter customer details as: Name,Phone,House Number,Postcode,Last 4 Digits of Card: ").strip()
        parts = [p.strip() for p in line.split(',') if p.strip()]
        
        if len(parts) != 5:
            print("Invalid input: Exactly 5 comma-separated values required (Name,Phone,House Number,Postcode,Last 4 Digits of Card).")
            continue
        
        name, phone, house_number, postcode, card = parts
        if not all([name, phone, house_number, postcode, card]):
            print("All fields must be non-empty.")
            continue
        
        # Validate card is exactly 4 digits
        if not (len(card) == 4 and card.isdigit()):
            print("Last 4 digits of card must be exactly 4 numeric digits.")
            continue
        
        break
    
    # Now enter items on separate lines
    equipment = {}
    print("\nEnter equipment items one per line as: code,qty (e.g., DAY,2). Enter empty line to finish.")
    while True:
        line = input().strip()
        if not line:
            break
        parts = [p.strip() for p in line.split(',') if p.strip()]
        if len(parts) != 2:
            print("Invalid input: Must be code,qty.")
            continue
        code, qty_str = parts
        code = code.upper()  # Normalize to uppercase
        if code not in equipment_data:
            print(f"Invalid code: '{code}'. Must be one of: {', '.join(equipment_data.keys())}")
            continue
        try:
            qty = int(qty_str)
            if qty <= 0:
                print(f"Quantity for '{code}' must be a positive integer.")
                continue
            if code in equipment:
                equipment[code] += qty  # Add to existing if duplicate
            else:
                equipment[code] = qty
        except ValueError:
            print(f"Invalid quantity for '{code}': must be an integer.")
            continue
    
    if not equipment:
        print("No equipment entered. Hire not recorded.")
        return
    
    # Ask for number of nights
    while True:
        nights_str = input("\nEnter number of nights: ").strip()
        try:
            nights = int(nights_str)
            if nights < 1:
                print("Number of nights must be at least 1.")
                continue
            break
        except ValueError:
            print("Invalid number of nights: must be an integer.")
    
    # Ask if returned after 2pm (late)
    while True:
        on_time_input = input("\nWas the equipment returned after 2pm? (Y/N): ").strip().upper()
        if on_time_input in ['Y', 'N']:
            returned_on_time = (on_time_input == 'N')  # Y means after 2pm (not on time), N means before or on 2pm (on time)
            break
        else:
            print("Invalid input: must be Y or N.")
    
    # Ask if return is late - but since scenario ties late to after 2pm, we'll use the same for now.
    # If needed, add another question, but assuming it's the same.

    # Store the hire
    hires.append({
        'customer_id': customer_id,
        'name': name,
        'phone': phone,
        'house_number': house_number,
        'postcode': postcode,
        'card': card,
        'equipment': equipment,  # Stores codes and qtys
        'nights': nights,
        'returned_on_time': returned_on_time
    })
    print("Hire details recorded successfully.")

def earnings_report():
    """
    Subroutine for Option 2: Generates and displays the earnings report.
    Uses data from the global hires list.
    For equipment summary, converts codes back to full names.
    Calculates total cost and extra charge based on the scenario.
    Displays in a tabular format with specified columns.
    Reflects cumulative hires.
    """
    if not hires:
        print("\nNo hires recorded yet.")
        return
    
    print("\nEarnings Report:")
    # Print header with column widths for alignment
    print(f"{'Customer ID':<15}{'Equipment':<60}{'Nights':<10}{'Total cost':<15}{'Returned on time (y/n)':<25}{'Extra charge for delayed return':<30}")
    
    for hire in hires:
        # Equipment summary using full names
        equip_summary = "; ".join(f"{equipment_data[code][0]} - {qty}" for code, qty in hire['equipment'].items())
        
        # Calculate base cost using prices
        base = sum(qty * equipment_data[code][1] for code, qty in hire['equipment'].items())
        
        # Additional nights cost (50% of base per additional night)
        additional = 0.5 * base * max(0, hire['nights'] - 1)
        
        # Extra charge if not on time (late)
        extra = 0.5 * base if not hire['returned_on_time'] else 0.0
        
        # Total cost
        total = base + additional + extra
        
        # Returned on time string
        on_time_str = 'y' if hire['returned_on_time'] else 'n'
        
        # Print row
        print(f"{hire['customer_id']:<15}{equip_summary:<60}{hire['nights']:<10}{total:<15.2f}{on_time_str:<25}{extra:<30.2f}")

# Start the program
if __name__ == "__main__":
    main_menu()