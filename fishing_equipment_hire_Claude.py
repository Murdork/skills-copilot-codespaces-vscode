# COM4018 - Fishing and Camping Equipment Hire System
# Tasks 2 & 3 Combined Implementation

# Equipment pricing data (read-only reference data)
EQUIPMENT_PRICES = {
    "Day chairs": 15.00,
    "Bed chairs": 25.00,
    "Bite Alarm (set of 3)": 20.00,
    "Bite Alarm (single)": 5.00,
    "Bait Boat": 60.00,
    "Camping tent": 20.00,
    "Sleeping bag": 20.00,
    "Rods (3lb TC)": 10.00,
    "Rods (Bait runners)": 5.00,
    "Reels (Bait runners)": 10.00,
    "Camping Gas stove (Double burner)": 10.00
}

# Global data structure to store all hire records
hire_records = []

def display_menu():
    """Display the main menu options"""
    print("\n" + "="*50)
    print("FISHING & CAMPING EQUIPMENT HIRE SYSTEM")
    print("="*50)
    print("1. Customer and hire details")
    print("2. Earnings report")
    print("3. Exit")
    print("="*50)

def get_menu_choice():
    """Get and validate menu choice from user"""
    while True:
        try:
            choice = input("Please select an option (1-3): ").strip()
            if choice in ['1', '2', '3']:
                return int(choice)
            else:
                print("Invalid input. Please enter 1, 2, or 3.")
        except:
            print("Invalid input. Please enter 1, 2, or 3.")

def display_equipment_menu():
    """Display available equipment and prices"""
    print("\n" + "-"*60)
    print("AVAILABLE EQUIPMENT FOR HIRE")
    print("-"*60)
    for i, (equipment, price) in enumerate(EQUIPMENT_PRICES.items(), 1):
        print(f"{i:2d}. {equipment:<30} - £{price:.2f}")
    print("-"*60)

def get_customer_details():
    """Get customer details with basic validation"""
    print("\n--- CUSTOMER DETAILS ---")
    
    # Customer ID
    while True:
        customer_id = input("Enter Customer ID: ").strip()
        if customer_id:
            break
        print("Customer ID cannot be empty.")
    
    # Customer Name
    while True:
        customer_name = input("Enter Customer Name: ").strip()
        if customer_name:
            break
        print("Customer Name cannot be empty.")
    
    # Phone Number
    while True:
        phone = input("Enter Phone Number: ").strip()
        if phone:
            break
        print("Phone Number cannot be empty.")
    
    # House Number
    while True:
        house_number = input("Enter House Number: ").strip()
        if house_number:
            break
        print("House Number cannot be empty.")
    
    # Postcode
    while True:
        postcode = input("Enter Postcode: ").strip()
        if postcode:
            break
        print("Postcode cannot be empty.")
    
    # Credit/Debit Card Reference
    while True:
        card_ref = input("Enter Credit/Debit Card Reference: ").strip()
        if card_ref:
            break
        print("Card Reference cannot be empty.")
    
    return {
        'customer_id': customer_id,
        'customer_name': customer_name,
        'phone': phone,
        'house_number': house_number,
        'postcode': postcode,
        'card_reference': card_ref
    }

def get_equipment_selection():
    """Get equipment selection and quantities"""
    equipment_list = list(EQUIPMENT_PRICES.keys())
    selected_equipment = {}
    
    print("\n--- EQUIPMENT SELECTION ---")
    display_equipment_menu()
    
    while True:
        try:
            choice = input("\nEnter equipment number (1-11) or 'done' to finish: ").strip().lower()
            
            if choice == 'done':
                if selected_equipment:
                    break
                else:
                    print("Please select at least one piece of equipment.")
                    continue
            
            equipment_num = int(choice)
            if 1 <= equipment_num <= 11:
                equipment_name = equipment_list[equipment_num - 1]
                
                # Get quantity
                while True:
                    try:
                        quantity = int(input(f"Enter quantity for {equipment_name}: "))
                        if quantity > 0:
                            if equipment_name in selected_equipment:
                                selected_equipment[equipment_name] += quantity
                            else:
                                selected_equipment[equipment_name] = quantity
                            print(f"Added {quantity} x {equipment_name}")
                            break
                        else:
                            print("Quantity must be greater than 0.")
                    except ValueError:
                        print("Please enter a valid number for quantity.")
            else:
                print("Please enter a number between 1 and 11.")
        
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 11 or 'done'.")
    
    return selected_equipment

def get_hire_duration():
    """Get number of nights for hire"""
    while True:
        try:
            nights = int(input("Enter number of nights for hire (minimum 1): "))
            if nights >= 1:
                return nights
            else:
                print("Number of nights must be at least 1.")
        except ValueError:
            print("Please enter a valid number.")

def get_return_status():
    """Get whether equipment was returned on time"""
    while True:
        response = input("Was equipment returned on time (by 2pm next day)? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def calculate_costs(equipment_dict, nights, returned_on_time):
    """Calculate total costs including late return charges"""
    base_cost = 0
    
    # Calculate base cost for first night
    for equipment, quantity in equipment_dict.items():
        base_cost += EQUIPMENT_PRICES[equipment] * quantity
    
    # Calculate additional nights cost (50% discount)
    additional_nights_cost = 0
    if nights > 1:
        for equipment, quantity in equipment_dict.items():
            additional_nights_cost += (EQUIPMENT_PRICES[equipment] * quantity * 0.5) * (nights - 1)
    
    # Calculate late return charge (extra 50% per item)
    late_charge = 0
    if not returned_on_time:
        for equipment, quantity in equipment_dict.items():
            late_charge += (EQUIPMENT_PRICES[equipment] * quantity * 0.5)
    
    total_cost = base_cost + additional_nights_cost + late_charge
    
    return total_cost, late_charge

def format_equipment_summary(equipment_dict):
    """Format equipment summary for display"""
    summary_parts = []
    for equipment, quantity in equipment_dict.items():
        summary_parts.append(f"{equipment} — {quantity}")
    return "; ".join(summary_parts)

def customer_hire_details():
    """Handle customer hire details (Task 2)"""
    print("\n" + "="*50)
    print("CUSTOMER AND HIRE DETAILS")
    print("="*50)
    
    # Get customer details
    customer_details = get_customer_details()
    
    # Get equipment selection
    equipment_selection = get_equipment_selection()
    
    # Get hire duration
    nights = get_hire_duration()
    
    # Get return status
    returned_on_time = get_return_status()
    
    # Calculate costs
    total_cost, late_charge = calculate_costs(equipment_selection, nights, returned_on_time)
    
    # Create hire record
    hire_record = {
        'customer_id': customer_details['customer_id'],
        'customer_name': customer_details['customer_name'],
        'phone': customer_details['phone'],
        'house_number': customer_details['house_number'],
        'postcode': customer_details['postcode'],
        'card_reference': customer_details['card_reference'],
        'equipment': equipment_selection,
        'nights': nights,
        'returned_on_time': returned_on_time,
        'total_cost': total_cost,
        'late_charge': late_charge
    }
    
    # Add to global records
    hire_records.append(hire_record)
    
    # Display confirmation
    print("\n" + "-"*50)
    print("HIRE DETAILS RECORDED")
    print("-"*50)
    print(f"Customer ID: {customer_details['customer_id']}")
    print(f"Customer Name: {customer_details['customer_name']}")
    print(f"Equipment: {format_equipment_summary(equipment_selection)}")
    print(f"Number of nights: {nights}")
    print(f"Total cost: £{total_cost:.2f}")
    if late_charge > 0:
        print(f"Late return charge: £{late_charge:.2f}")
    print(f"Returned on time: {'Yes' if returned_on_time else 'No'}")
    print("-"*50)

def earnings_report():
    """Generate and display earnings report (Task 3)"""
    print("\n" + "="*80)
    print("EARNINGS REPORT")
    print("="*80)
    
    if not hire_records:
        print("No hire records found. Please add some customer hire details first.")
        return
    
    # Display header
    print(f"{'Customer ID':<12} {'Equipment Summary':<25} {'Nights':<7} {'Total Cost':<12} {'On Time':<8} {'Late Charge':<12}")
    print("-"*80)
    
    total_earnings = 0
    total_late_charges = 0
    
    # Display each record
    for record in hire_records:
        equipment_summary = format_equipment_summary(record['equipment'])
        # Truncate long equipment summaries for display
        if len(equipment_summary) > 22:
            equipment_summary = equipment_summary[:19] + "..."
        
        on_time_display = "Y" if record['returned_on_time'] else "N"
        
        print(f"{record['customer_id']:<12} {equipment_summary:<25} {record['nights']:<7} "
              f"£{record['total_cost']:<11.2f} {on_time_display:<8} £{record['late_charge']:<11.2f}")
        
        total_earnings += record['total_cost']
        total_late_charges += record['late_charge']
    
    # Display totals
    print("-"*80)
    print(f"{'TOTALS:':<45} £{total_earnings:<11.2f} {'':8} £{total_late_charges:<11.2f}")
    print(f"Total number of hires: {len(hire_records)}")
    print("="*80)

def main():
    """Main program loop"""
    print("Welcome to the Fishing & Camping Equipment Hire System")
    
    while True:
        display_menu()
        choice = get_menu_choice()
        
        if choice == 1:
            customer_hire_details()
        elif choice == 2:
            earnings_report()
        elif choice == 3:
            print("\nThank you for using the Fishing & Camping Equipment Hire System!")
            print("Goodbye!")
            break

# Run the program
if __name__ == "__main__":
    main()
