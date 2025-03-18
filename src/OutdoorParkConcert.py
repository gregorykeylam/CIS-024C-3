"""
Filename: OutdoorParkConcert.py
Author: Gregory Lam
Created: March 16, 2025
Description: A program that help a company host outdoor concerts with social distancing
             for its audiences
"""

# Import statements
import json
import string
import os


def determine_pricing(rpos):
    """
    Determine seat type and price based on row position
    """
    # Set seat prices
    FRONT_SEAT_PRICE = 80
    MIDDLE_SEAT_PRICE = 50
    BACK_SEAT_PRICE = 25

    # Set pricing boundaries
    MIDDLE_SEAT_LOWER_BOUNDARY = 5
    BACK_SEAT_LOWER_BOUNDARY = 11

    # Given a row position, determine its section and price
    if rpos < MIDDLE_SEAT_LOWER_BOUNDARY:
        s_type = "Front"
        s_price = FRONT_SEAT_PRICE
    elif rpos < BACK_SEAT_LOWER_BOUNDARY:
        s_type = "Middle"
        s_price = MIDDLE_SEAT_PRICE
    else:
        s_type = "Back"
        s_price = BACK_SEAT_PRICE
    return (s_type, s_price)


def display_all_purchases():
    """
    Determine which seats are sold and calculate the total the venue has made
    """
    # Print header
    print(
        "\n====================================================================================="
    )
    print("                                   Purchase History")
    print(
        "====================================================================================="
    )
    print()

    amount = 0
    result = []
    transactions = []
    for rpos in ROW:
        for cpos in COL:
            if seating[str(rpos)][cpos].get("ReservedBy") is not None:
                spos = str(rpos) + cpos
                transactions.append(spos)
                stype, sprice = determine_pricing(rpos)
                result.append(stype)
                amount += sprice

    # Display all purchases and the total amount made
    ITEMS_PER_LINE = 15
    print("\nFollowing seats have been sold:\n")
    for i in range(0, len(transactions), ITEMS_PER_LINE):
        print(*transactions[i : i + ITEMS_PER_LINE], "\n")
    print()
    print(
        f"Transactions above ({result.count("Front")} Front, {result.count("Middle")} Middle "
        f"& {result.count("Back")} Back) have generated ${amount:.2f} of income"
    )
    print()
    print()


def generate_artifact(seat_count, seat_pos):
    """
    Determine which seats need to be reserved or blocked for the transaction

    """
    # Separate seat position inputted into row and column
    rpos = seat_pos[:-1]
    cpos = seat_pos[-1:]

    seat_wanted = []
    social_distancing = []

    ASCII_A = 65
    ASCII_Z = 90

    # Determine seating arrangement with the following requirement:
    #   * There must be 2 social distancing seats (available seats)
    #     between each occupied seat in a row.
    #   * 1 row distance between each row.
    #   * Bulk tickets that are purchased can sit next to each other.

    COL_SPACING = 2
    ROW_SPACING = 1
    RANGE_OFFSET = 1

    # Determine which seats to block to the left of the selected seats
    if ord(cpos) - COL_SPACING < ASCII_A:
        left = ASCII_A
    else:
        left = ord(cpos) - COL_SPACING
    for item in range(left, ord(cpos)):
        social_distancing.append([rpos, chr(item)])

    # Determine which seats to block to the right of the selected seats
    if ord(cpos) + int(seat_count) + COL_SPACING > ASCII_Z:
        right = ASCII_Z + RANGE_OFFSET
    else:
        right = ord(cpos) + int(seat_count) + COL_SPACING
    for item in range(ord(cpos) + int(seat_count), right):
        social_distancing.append([rpos, chr(item)])

    # Determine which seats to block behind the selected seats
    if int(rpos) + ROW_SPACING < ROW[-1]:
        for item in range(left, right):
            social_distancing.append([str(int(rpos) + ROW_SPACING), chr(item)])

    # Determine which seats to block in front of the selected seats
    if int(rpos) - ROW_SPACING > ROW[0]:
        for item in range(left, right):
            social_distancing.append([str(int(rpos) - ROW_SPACING), chr(item)])

    # Determine which seats are to be reserved
    for item in range(ord(cpos), ord(cpos) + int(seat_count)):
        seat_wanted.append([str(rpos), chr(item)])

    return (seat_wanted, social_distancing)


def initialize_env():
    """
    Load the existing seating chart or create a clean one
    """

    if os.path.exists(PATH_TO_FILE):
        file = open_file(PATH_TO_FILE, "r")
        current_seating = json.load(file)
    else:
        current_seating = {}
        print()
        for r in ROW:
            current_seating[str(r)] = {}
            for c in COL:
                current_seating[str(r)][c] = {}
                current_seating[str(r)][c]["Availability"] = AVAILABLE_SEAT
                current_seating[str(r)][c]["Position"] = str(r) + c
    return current_seating


def open_file(path, mode):
    """
    Try to open the json file and throw an error if it can't
    """
    try:
        file = open(path, mode, encoding="UTF-8")
    except OSError:
        print(f'ERROR: Unable to open the file "{path}"')
    return file


def print_receipt(rpos, seat_count, seat_wanted, name, email_addr):
    """
    Calculate and display receipt
    """
    # Calculate items needed for the receipt
    stype, sprice = determine_pricing(rpos)
    seat_purchased = [r + c for r, c in seat_wanted]
    ticket_cost = int(seat_count) * sprice
    total_mask_fee = int(seat_count) * MASK_FEE
    subtotal = ticket_cost + total_mask_fee
    tax = subtotal * TAX_RATE
    total = subtotal + tax

    # Display the receipt
    LEFT_JUST = 50
    print(
        "\n===================================================================================================="
    )
    print("                                       Receipt")
    print(
        "===================================================================================================="
    )
    print()
    print(f'{"Name:":<{LEFT_JUST}}', name)
    print(f'{"Email:":<{LEFT_JUST}}', email_addr)
    print(f'{"Number of seats:":<{LEFT_JUST}}', seat_count)
    print(
        f'{"Seat Type:":<{LEFT_JUST}}', stype, "($" + str(sprice) + ")"
    )
    print(f'{"Seats:  ":<{LEFT_JUST}}', *seat_purchased)
    print(f'{"Ticket Cost:":<{LEFT_JUST}}', "$" + f"{ticket_cost:.2f}")
    print(f'{"Mask Fee:":<{LEFT_JUST}}', "$" + f"{total_mask_fee:.2f}")
    print(f'{"Subtotal":<{LEFT_JUST}}', "$" + f"{subtotal:.2f}")
    print(f'{"Tax:":<{LEFT_JUST}}', "$" + f"{tax:.2f}")
    print(
        "----------------------------------------------------------------------------------------------------"
    )
    print(f'{"Total:":<{LEFT_JUST}}', "$" + f"{total:.2f}")
    print(
        "====================================================================================================\n\n"
    )


def purchase_seats(current_seating):
    """
    Initiate the purchasing process and print a receipt when it is done
    """
    # Ask user for seat count and then error check the input
    purchasing_seats = True
    while purchasing_seats:
        seat_count = input("\nNumber of seats desired:  ")
        if not seat_count.isnumeric() or int(seat_count) < 1:
            print("\nInvalid input.  Requires an integer greater than 1!")
        else:
            # Ask user for starting seat and then error check the input
            seat_pos = input("\nStarting seat (ex. 3D):  ")
            # Check if seat selection exist
            in_range = any(
                seat_pos in c.values() for r in seating.values() for c in r.values()
            )
            if in_range:
                # Separate seat position inputted into row and column
                rpos = int(seat_pos[:-1])
                cpos = seat_pos[-1:]

                # Find out all seats involved in this transaction
                seat_wanted, social_distancing = generate_artifact(seat_count, seat_pos)

                # Determine if number of seats wanted exceed capacity
                exceed_capacity = (
                    True if ord(cpos) + int(seat_count) - 1 > 90 else False
                )

            if not in_range or exceed_capacity:
                print("\nSeat selection not valid or seat count exceeds capacity!")
            elif violate_restrictions(seat_wanted, social_distancing):
                print(
                    "\nSelection not accepted due to social distancing or previous reservation!"
                )
            else:
                # If purchase is allowed to proceed, inform user and ask for name and email
                print(
                    f"\n{seat_count} seat(s) starting at {seat_pos} are available for purchase\n"
                )
                purchasing_seats = False

                name = input("Enter your name:  ")
                email_addr = input("Enter your email address:  ")

                # Update seating chart
                update_availability(seat_wanted, social_distancing, name, email_addr)
                print_receipt(rpos, seat_count, seat_wanted, name, email_addr)
                return current_seating


def search_by_customer(current_seating):
    """
    Search for all seats purchased by a particular user
    """
    # Ask user for name to be search
    search_name = input("Enter customer's name to be searched:  ")

    # Print header
    print(
        "\n====================================================================================="
    )
    print("                                   Search Result")
    print(
        "====================================================================================="
    )
    print()

    # Search seat purchased by inputted name
    seat_purchased = []
    for r in ROW:
        for c in COL:
            if current_seating[str(r)][c].get("ReservedBy") == search_name:
                spos = str(r) + c
                seat_purchased.append(spos)

    # Display result of the search
    if len(seat_purchased) > 0:
        print(f'\n"{search_name}" has purchased the following seat(s):\n')
        print(*seat_purchased)
    else:
        print(f'\nNo order found for "{search_name}"')
    print()
    print()


def update_availability(seat_wanted, social_distancing, name, email_addr):
    """
    Update the seat chart with different symbols to indicate whether it is
    open, blocked or reserved
    """
    # Update seating chart according to its designated symbol or letters
    for r, c in social_distancing:
        seating[r][c]["Availability"] = BLOCKED_SEAT
    for r, c in seat_wanted:
        seating[r][c]["Availability"] = RESERVED_SEAT
    for r, c in seat_wanted:
        seating[r][c]["ReservedBy"] = name
    for r, c in seat_wanted:
        seating[r][c]["Email"] = email_addr
    return seating


def view_seating(current_seating):
    """
    Display the current seating chart
    """
    # Print header
    print(
        "\n====================================================================================="
    )
    print("                                       Seating")
    print(
        "====================================================================================="
    )
    print()
    # Print sub header
    print("\t", end="")
    for c in COL:
        print(c, end=" ")
    print("\tType\t\tPrice")
    print(
        "\t"
        + "---------------------------------------------------"
        + "\t"
        + "------"
        + "\t\t"
        + "------"
    )
    # Print current seating chart
    for r in ROW:
        print(r, end="\t")
        for c in COL:
            print(current_seating[str(r)][c]["Availability"], end=" ")

        # print type & price for each row
        stype, sprice = determine_pricing(r)
        print(f"\t{stype}\t\t${sprice}", end="\t")
        print()


def violate_restrictions(seat_wanted, social_distancing):
    """
    Determine if seat selection and its social distance requiement
    is at odd with existing reservation
    """
    # Generate an array of reserved seats
    reserved = []
    for r in ROW:
        for c in COL:
            if seating[str(r)][c].get("Availability") == RESERVED_SEAT:
                reserved.append([str(r), c])
    # Determine if seats wanted has already been reserved or violate any COVID rules
    return any(item in reserved for item in social_distancing + seat_wanted)


if __name__ == "__main__":

    # Relative path to the data file
    PATH_TO_FILE = "../misc/OutdoorParkConcert.json"

    # Set matrix size
    ROW = range(20)
    COL = string.ascii_uppercase

    # Set symbol or letter for each representation
    RESERVED_SEAT = "R"
    BLOCKED_SEAT = "x"
    AVAILABLE_SEAT = "."

    # Set other pertinent information
    MASK_FEE = 5
    TAX_RATE = 0.0725

    # Load the existing seating chart or create a clean one
    seating = initialize_env()

    user_quit = False
    while not user_quit:

        # Print header
        print(
            "====================================================================================="
        )
        print("                              Outdoor Park Concert App")
        print(
            "====================================================================================="
        )
        print()

        # Print menu
        print("[P/p]     Purchase seat")
        print("[V/v]     View seating")
        print("[S/s]     Search seats purchased by customer's name")
        print("[D/d]     Display all purchase made amd total income")
        print("[Q/q]     Quit app")
        print("\n")

        # Ask the user for input on what task to perform.
        # Trigger different action based on input
        Command = input("Enter a command:  ")
        match Command.lower():
            case "p":
                purchase_seats(seating)
            case "v":
                view_seating(seating)
                print("\n")
            case "s":
                search_by_customer(seating)
            case "d":
                display_all_purchases()
            case "q":
                # Save current seat chart to preserve completed transaction
                json_file = open_file(PATH_TO_FILE, "w")
                json.dump(seating, json_file, indent=6)
                json_file.close()
                user_quit = True
            case _:
                print("\nInvalid input!  Please try again.")

