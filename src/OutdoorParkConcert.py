"""
Filename: OutdoorParkConcert.py
Author: Gregory Lam
Created: March 5, 2025
Description: A program that help a company host outdoor concerts with social distancing
             for its audiences
"""

# Import statements
import json
import string
import os


def Check_Restrictions (seatWanted, socialDistancing):
    
    # Generate an array of reserved seats
    reserved = []
    for r in ROW:
        for c in COL:
            if seating[str(r)][c].get("Availability") == reservedSeat:
                reserved.append([str(r),c]) 
    # Determine if seats wanted has already been reserved or violate any COVID rules
    return (any (item in reserved for item in socialDistancing + seatWanted))


def Determine_Pricing (rPos):
    
    # Set seat prices
    frontSeatPrice = 80
    middleSeatPrice = 50
    backSeatPrice = 25

    # Set pricing boundaries
    middleSeatLowerBoundary = 5
    breakackSeatLowerBoundary = 11

    # Given a row position, determine its section and price 
    if rPos < middleSeatLowerBoundary:
        sType = "Front"
        sPrice = frontSeatPrice
    elif rPos < breakackSeatLowerBoundary:
        sType = "Middle"
        sPrice = middleSeatPrice
    else:
        sType = "Back"
        sPrice = backSeatPrice
    return (sType, sPrice)


def Display_All_Purchases (seating):
    
    # Print header
    print ("\n=====================================================================================")
    print ("                                   Purchase History")
    print ("=====================================================================================")
    print ()

    # Determine which seats are sold and calculate the total the venue has made 
    amount = 0
    totalSeatType = []
    transactions = []
    for rPos in ROW:
        for cPos in COL:
            if seating[str(rPos)][cPos].get("ReservedBy") != None:
                sPos = str(rPos) + cPos
                transactions.append(sPos) 
                sType, sPrice = Determine_Pricing (rPos)
                totalSeatType.append(sType)       
                amount += sPrice

    # Display all purchases and the total amount made 
    print ("\nFollowning seats have been sold:\n")
    print (*transactions)
    print ()
    print (f"Transactions above ({totalSeatType.count("Front")} Front, {totalSeatType.count("Middle")} Middle & \
           {totalSeatType.count("Back")} Back) have generated ${amount:.2f} of income")
    print ()
    print ()


def Generate_Artifact (seatCount, seatPos):
    
    # Seperate seat postion inputted into row and column
    rPos = seatPos[:-1]
    cPos = seatPos[-1:]
 
    seatWanted = []   
    socailDistancing = []
    
    # Determine seating arrangement
    # Determine which seats to block to the left of the selected seats
    if ord(cPos)-2 < 65:
        left = 65
    else:
        left = ord(cPos)-2
    for item in range(left, ord(cPos)):
        socailDistancing.append([rPos, chr(item)])

    # Determine which seats to block to the right of the selected seats
    if ord(cPos)+int(seatCount)+2 > 90:
        right = 90 + 1 
    else:
        right = ord(cPos)+int(seatCount)+2
    for item in range(ord(cPos)+int(seatCount), right):
        socailDistancing.append([rPos, chr(item)])

    # Determine which seats to block behind the selected seats
    if int(rPos)+1 < 19:
        for item in range(left, right):
            socailDistancing.append([str(int(rPos)+1), chr(item)])

    # Determine which seats to block in front of the selected seats
    if int(rPos)-1 > 0:
        for item in range(left, right):
            socailDistancing.append([str(int(rPos)-1), chr(item)])
    
    # Determine which seats are to be reserved
    for item in range(ord(cPos), ord(cPos)+int(seatCount)):
        seatWanted.append([str(rPos), chr(item)]) 

    return (seatWanted, socailDistancing)


def Initialize_Env (): 
 
    # Load the existing seating chart or create a clean one 
    if os.path.exists(pathToFile):
        jsonFile = Open_File (pathToFile, "r")
        seating = json.load(jsonFile)
    else:
        seating = {}
        print ()
        for r in ROW:
            seating[str(r)] = {}
            for c in COL:
                seating[str(r)][c] = {}
                seating[str(r)][c]["Availability"] = availableSeat
    return seating


def Open_File (pathToFile, mode):

    # Try to open the json file and throw an error if it can't
    try:
        jsonFile = open(pathToFile, mode)
    except OSError:
        print(f'ERROR: Unable to open the file "{pathToFile}"')
    return jsonFile


def Purchase_Seat(seating):           
    
    # Ask user for seat count and then error check the input
    state = True
    while state == True:
        seatCount = input ("Number of seats desired:  ")
        if not seatCount.isnumeric():
            print ("\nInput is NOT an integar!!!\n")
        else:
            state = False

    # Ask user for starting seat and then error check the input
    state = True
    while state == True:    
        seatPos = input  ("Starting seat (ex. 3D):  ")
        
        # Seperate seat postion inputted into row and column
        rPos = int(seatPos[:-1])
        cPos = seatPos[-1:]
        
        # Find out what seats are involved in this transaction
        seatWanted, socialDistancing = Generate_Artifact (seatCount, seatPos)

        # Determine if selected seats can be purchased.  
        # Otherwise, print appropriate message
        if Check_Restrictions (seatWanted, socialDistancing):
            print ("\nSeat selection NOT valid due to social distancing!!\n")
        elif rPos not in ROW or cPos not in COL or ord(cPos)+int(seatCount) > 90:
            print ("\nInput exceeds capacity!!!\n")
        else:
            # If purchase is allowed, let user know and ask for name and email
            print (f'\n{seatCount} seat(s) starting at {seatPos} are available for purchase\n' )
            state = False

            name = input ("Enter your name:  ")
            emailAddr = input ("Enter your email address:  ")

            # Update seating chart
            Update_Availability (seatWanted, socialDistancing, name)

            # Calculate items needed for the receipt
            sType, sPrice = Determine_Pricing(rPos)
            seatPurchased = [r+c for r,c in seatWanted]
            ticketCost = int(seatCount) * sPrice
            totalMaskFee = int(seatCount) * maskFee
            subtotal = ticketCost + totalMaskFee
            tax = subtotal * taxRate
            total = subtotal + tax

            # Display the receipt
            print ("\n====================================================================================================")
            print ("                                       Receipt")
            print ("====================================================================================================")
            print ()
            print (f'{"Name:":<50}', name)
            print (f'{"Email:":<50}', emailAddr)
            print (f'{"Number of seats:":<50}', seatCount)
            print (f'{"Seat Type:":<50}', sType, "($" + str(sPrice) + ")")
            print (f'{"Seats:  ":<50}', *seatPurchased)
            print (f'{"Ticket Cost:":<50}', "$" + f'{ticketCost:.2f}') 
            print (f'{"Mask Fee:":<50}', "$" + f'{tryotalMaskFee:.2f}') 
            print (f'{"Subtotal":<50}', "$" + f'{subtotal:.2f}') 
            print (f'{"Tax:":<50}', "$" + f'{tryax:.2f}') 
            print ("----------------------------------------------------------------------------------------------------")
            print (f'{"Total:":<50}', "$" + f'{total:.2f}') 
            print ("====================================================================================================\n\n")
            
            return seating


def Search_By_Customer (seating):
    
    # Ask user for name to be search
    searchName = input ("Enter customer's name to be searched:  ")

    # Print header
    print ("\n=====================================================================================")
    print ("                                   Search Result")
    print ("=====================================================================================")
    print ()

    # Search seat purchased by inputted name
    seatPurchased = []
    for r in ROW:
        for c in COL:
            if seating[str(r)][c].get("ReservedBy") == searchName:
                sPos = str(r) + c
                seatPurchased.append(sPos) 

    # Display result of the search
    if len(seatPurchased) > 0:
        print (f'\n"{searchName}" has purchased the following seat(s):\n')
        print (*seatPurchased)    
    else:
        print (f'\nNo order found for "{searchName}"')
    print ()
    print ()


def Update_Availability (seatWanted, socailDistancing, name):
    # Update seating chart according to its designated symbol or letters
    for r, c in socailDistancing:   
        seating[r][c]["Availability"]=blockedSeat
            
    for r, c in seatWanted:
        seating[r][c]["Availability"]=reservedSeat 

    for r, c in seatWanted:
        seating[r][c]["ReservedBy"]=name 
            
    return (seating)


def View_Seating (seating): 

    # Print header
    print ("\n=====================================================================================")
    print ("                                       Seating")
    print ("=====================================================================================")
    print ()
    
    # Print sub header
    print ("\t", end="")
    for c in COL:
        print (c, end=" ")
    print ("\tType\tPrice")
    print ("\t" + "-" * 52 + "\t" + "-" * 6 + "\t" + "-" * 5)
    
    # Print current seating chart
    for r in ROW:
        print(r, end="\t")
        for c in COL:
            print(seating[str(r)][c]["Availability"], end=" ") 

        # print type & price for each row
        sType, sPrice = Determine_Pricing(r)
        print(f'\t{sType}\t${sPrice}', end="\t")
        print()  


if __name__ == '__main__':

    # Relative path to the data file
    pathToFile = "../misc/OutdoorParkConcert.json"
    
    # Set matrix size
    ROW = range(20)
    COL = string.ascii_uppercase

    # Set symbol or letter for each representation 
    reservedSeat = "R"
    blockedSeat = "x"
    availableSeat = '.'   

    # Set other pertinent information
    maskFee = 5
    taxRate = 0.0725

    # Load the existing seating chart or create a clean one 
    seating = Initialize_Env ()

    while True:

        # Print header
        print ("=====================================================================================")
        print ("                              Outdoor Park Concert App")
        print ("=====================================================================================")
        print ()

        # Print menu
        print ("[P/p]     Purchase seat")
        print ("[V/v]     View seating")
        print ("[S/s]     Search seats purchased by customer's name")
        print ("[D/d]     Display all purchase made amd total income")
        print ("[Q/q]     Quit app")
        print ("\n")

        # Ask user for input on what task to perform.  
        # Trigger different action based on input
        Command = input ("Enter a command:  ")
        match Command.lower():
            case "p":
                Purchase_Seat(seating)
            case "v":
                View_Seating (seating)
                print ("\n")
            case "s":
                Search_By_Customer (seating)
            case "d":
                Display_All_Purchases (seating)
            case "q":
                # Save current seat chart to preserve completed transaction  
                jsonFile = Open_File (pathToFile, "w")
                json.dump (seating, jsonFile, indent=6)
                jsonFile.close()
                exit () 
            case _:
                print ("\nInvalid input!  Please try again.")