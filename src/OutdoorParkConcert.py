"""
This example code creates a 2d list (2d matrix) that can store seating.
The matrix is populated with . since all seats are available
"""

import json
import string
import os



def Check_Overlap(SeatWanted, Distancing):
    
    Reserved = []
    for r in ROW:
        for c in COL:
            if Seating[str(r)][c].get("Availability") == reserved_seat:
                Reserved.append([str(r),c]) 
    return (any (item in Reserved for item in Distancing + SeatWanted))


def Determine_Pricing (rPos):

    FrontSeatPrice = 80
    MiddleSeatPrice = 50
    BackSeatPrice = 25

    MiddleSeatLowerBoundary = 5
    BackSeatLowerBoundary = 11

    if rPos < MiddleSeatLowerBoundary:
        SType = "Front"
        SPrice = FrontSeatPrice
    elif rPos < BackSeatLowerBoundary:
        SType = "Middle"
        SPrice = MiddleSeatPrice
    else:
        SType = "Back"
        SPrice = BackSeatPrice
    return (SType, SPrice)


def Display_All_Purchases (Seating):
    print ("\n=====================================================================================")
    print ("                                   Purchase History")
    print ("=====================================================================================")
    print ()

    Amount = 0
    sType = []
    Transactions = []
    for rPos in ROW:
        for c in COL:
            if Seating[str(r)][c].get("ReservedBy") != None:
                sPos = str(r) + c
                Transactions.append(sPos) 
                SType, SPrice = Determine_Pricing (rPos)
                sType.append(SType)       
                Amount += SPrice

    print ("\nFollowning seats have been sold:\n")
    print (*Transactions)
    print ()
    print ("Transactions above (" + str(sType.count("Front")) + " Front, " + str(sType.count("Middle")) + \
    " Middle & " + str(sType.count("Back")) + " Back) have generated $" + f'{Amount:.2f}' + " of income")
    print ()
    print ()


def Generate_Artifact (seatCount, seatPos):

    SeatWanted = []   
    Distancing = []
    
    rPos = seatPos[:-1]
    cPos = seatPos[-1:]
       
    if ord(cPos)-2 < 65:
        Left = 65
    else:
        Left = ord(cPos)-2
    for item in range(Left, ord(cPos)):
        Distancing.append([rPos, chr(item)])

    if ord(cPos)+int(seatCount)+2 > 90:
        Right = 90 + 1 
    else:
        Right = ord(cPos)+int(seatCount)+2
    for item in range(ord(cPos)+int(seatCount), Right):
        Distancing.append([rPos, chr(item)])

    if int(rPos)+1 < 19:
        for item in range(Left, Right):
            Distancing.append([str(int(rPos)+1), chr(item)])

    if int(rPos)-1 > 0:
        for item in range(Left, Right):
            Distancing.append([str(int(rPos)-1), chr(item)])

    for item in range(ord(cPos), ord(cPos)+int(seatCount)):
        SeatWanted.append([str(rPos), chr(item)]) 
    return (SeatWanted, Distancing)


def Initialize_Env (): 
    
    available_seat = '.'
    
    if os.path.exists(pathToFile):
        jsonFile = Open_File (pathToFile, "r")
        Seating = json.load(jsonFile)
    else:
        Seating = {}
        print ()

        for r in ROW:
            Seating[str(r)] = {}
            for c in COL:
                Seating[str(r)][c] = {}
                Seating[str(r)][c]["Availability"] = available_seat
                
    return Seating


def Open_File (pathToFile, mode):

    # try to open a file and throw a error if it is not found
    try:
        jsonFile = open(pathToFile, mode)
    except OSError:
        print("ERROR: Unable to open the file %s" % pathToFile)
    return jsonFile


def Purchase_Seat(Seating):           
    
    MaskFee = 5
    TaxRate = 0.0725

    state = True
    while state == True:
        seatCount = input ("Number of seats desired:  ")
        if not seatCount.isnumeric():
            print ("\nInput is NOT an integar!!!\n")
        else:
            state = False

    state = True
    while state == True:    
        
        seatPos = input  ("Starting seat (ex. 3D):  ")

        rPos = int(seatPos[:-1])
        cPos = seatPos[-1:]

        SeatWanted, Distancing = Generate_Artifact (seatCount, seatPos)

        if Check_Overlap (SeatWanted, Distancing):
            print ("\nSeat selection NOT valid due to social distancing!!\n")
        elif rPos not in ROW or cPos not in COL or ord(cPos)+int(seatCount) > 90:
            print ("\nInput exceeds capacity!!!\n")
        else:
            print (str(seatCount) + " seats starting at (" + seatPos + ") are available for purchase" )
            state = False

            name = input ("Enter your name:  ")
            emailAddr = input ("Enter your email address:  ")

            Update_Availability (SeatWanted, Distancing)
            SType, SPrice = Determine_Pricing(rPos)
            Seat = [x+y for x,y in SeatWanted]
            print (Seat)

            TicketCost = int(seatCount) * SPrice
            TotalMaskFee = int(seatCount) * MaskFee
            Subtotal = TicketCost + TotalMaskFee
            Tax = Subtotal * TaxRate
            Total = Subtotal + Tax

            print ("\n====================================================================================================")
            print ("                                       Receipt")
            print ("====================================================================================================")
            print ()
            print (f'{"Name:":<50}', name)
            print (f'{"Email:":<50}', emailAddr)
            print (f'{"Number of seats:":<50}', seatCount)
            print (f'{"Seat Type:":<50}', SType, "($" + str(SPrice) + ")")
            print (f'{"Seats:  ":<50}', *Seat)
            print (f'{"Ticket Cost:":<50}', "$" + f'{TicketCost:.2f}') 
            print (f'{"Mask Fee:":<50}', "$" + f'{TotalMaskFee:.2f}') 
            print (f'{"Subtotal":<50}', "$" + f'{Subtotal:.2f}') 
            print (f'{"Tax:":<50}', "$" + f'{Tax:.2f}') 
            print ("----------------------------------------------------------------------------------------------------")
            print (f'{"Total:":<50}', "$" + f'{Total:.2f}') 
            print ("====================================================================================================\n\n")
            return Seating


def Search_By_Customer (Seating):
    
    #print (Seating.get("2",{}))
    #print (Seating.get("2",{}).get("D",{}))
    #print (Seating.get("2",{}).get("D",{}).get("ReservedBy"))

    SearchName = input ("Enter customer's name to be searched:  ")

    print ("\n=====================================================================================")
    print ("                                   Search Result")
    print ("=====================================================================================")
    print ()

    Ticket = []
    for r in ROW:
        for c in COL:
            if Seating[str(r)][c].get("ReservedBy") == SearchName:
                sPos = str(r) + c
                Ticket.append(sPos) 
    if len(Ticket) > 0:
        print ("\n\"" + SearchName + "\" has purchased the following seat(s):\n")
        print (*Ticket)    
    else:
        print ("\nNo order found for \"" + SearchName + "\"")
    print ()
    print ()


def Update_Availability (SeatWanted, Distancing):

    for r, c in Distancing:   
        Seating[r][c]["Availability"]=blocked_seat
            
    for r, c in SeatWanted:
        Seating[r][c]["Availability"]=reserved_seat 
            
    return (Seating)


def View_Seating (Seating): 

    # print available seating
    print ("\n=====================================================================================")
    print ("                                       Seating")
    print ("=====================================================================================")
    print ()
    
    print ("\t", end="")
    for c in COL:
        print (c, end=" ")
    print ("\tType\t\tPrice")
    print ("\t" + "-" * 52 + "\t" + "-" * 6 + "\t\t" + "-" * 5)

    for r in ROW:
        print(r, end="\t")
        for c in COL:
            print(Seating[str(r)][c]["Availability"], end=" ") 

        SType, SPrice = Determine_Pricing(r)
        
        print("\t" + SType + "\t\t$" + str(SPrice), end="\t")
        print()  


if __name__ == '__main__':

    # relative path
    pathToFile = "../misc/OutdoorParkConcert.json"
    
    ROW = range(20)
    COL = string.ascii_uppercase

    reserved_seat = "R"
    blocked_seat = "x"

    Seating = Initialize_Env ()


    while True:

        print ("=====================================================================================")
        print ("                              Outdoor Park Concert App")
        print ("=====================================================================================")
        print ()

        print ("[P/p]     Purchase seat")
        print ("[V/v]     View seating")
        print ("[S/s]     Search seats purchased by customer's name")
        print ("[D/d]     Display all purchase made amd total income")
        print ("[Q/q]     Quit app")
        print ("\n")
        Command = input ("Enter a command:  ")
        match Command.lower():
            case "p":
                Purchase_Seat(Seating)
            case "v":
                View_Seating (Seating)
                print ("\n")
            case "s":
                Search_By_Customer (Seating)
            case "d":
                Display_All_Purchases (Seating)
            case "q":
                jsonFile = Open_File (pathToFile, "w")
                json.dump (Seating, jsonFile, indent=6)
                jsonFile.close()
                exit () 
            case _:
                print ("\nInvalid input!  Please try again.")