"""
This example code creates a 2d list (2d matrix) that can store seating.
The matrix is populated with . since all seats are available
"""

import json
import string
import os


def  PurchaseSeat():

    MaskFee = 5
    TaxRate = 0.0725

    seatCount = int(input ("Number of seats desired:  "))
    seatPos = input  ("Starting seat (ex. 3D):  ")
    Validate_Availability (seatCount, seatPos)
    name = input ("Enter your name:  ")
    emailAddr = input ("Enter your email address:  ")

    rPos = int(seatPos[:-1])
    SType, SPrice = Determine_Pricing(rPos)

    TicketCost = seatCount * SPrice
    TotalMaskFee = seatCount * MaskFee
    Subtotal = TicketCost + TotalMaskFee
    Tax = Subtotal * TaxRate
    Total = Subtotal + Tax

    print ("\n=====================================================================================")
    print ("                                       Receipt")
    print ("=====================================================================================")
    print ()

    print (f'{"Name:":<65}' + name)
    print (f'{"Email:":<65}' + emailAddr)
    print (f'{"Number of seats:":<65}' + str(seatCount))
    print (f'{"Seat Type:":<65}' + SType + " ($" + str(SPrice) + ")")
    print (f'{"Seats:  ":<65}' + seatPos)
    print (f'{"Ticket Cost:":<65}' + "$" + f'{TicketCost:.2f}') 
    print (f'{"Mask Fee:":<65}' + "$" + f'{TotalMaskFee:.2f}') 
    print (f'{"Subtotal":<65}' + "$" + f'{Subtotal:.2f}') 
    print (f'{"Tax:":<65}' + "$" + f'{Tax:.2f}') 
    print ("_____________________________________________________________________________________")
    print (f'{"Total:":<65}' + "$" + f'{Total:.2f}') 
    print ("=====================================================================================\n\n")


def Validate_Availability (seatCount, seatPos):

    #rPos = seatPos[:-1]
    #cPos = seatPos[-1:]
    print (str(seatCount) + " seats starting at (" + seatPos + ") are available for purchase" )


def Determine_Pricing (r):

    FrontSeatPrice = 80
    MiddleSeatPrice = 50
    BackSeatPrice = 25

    MiddleSeatLowerBoundary = 5
    BackSeatLowerBoundary = 11

    if r < MiddleSeatLowerBoundary:
        SType = "Front"
        SPrice = FrontSeatPrice
    elif r < BackSeatLowerBoundary:
        SType = "Middle"
        SPrice = MiddleSeatPrice
    else:
        SType = "Back"
        SPrice = BackSeatPrice
    return (SType, SPrice)


def Open_File (pathToFile, mode):

    # try to open a file and throw a error if it is not found
    try:
        jsonFile = open(pathToFile, mode)
    except OSError:
        print("ERROR: Unable to open the file %s" % pathToFile)
    return jsonFile


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
                Seating[str(r)][c]["Name"] = str(r) + str(c)
                
                jsonFile = Open_File (pathToFile, "w")
                json.dump (Seating, jsonFile, indent=6)
                jsonFile.close()
    return Seating


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
                PurchaseSeat()
            case "v":
                View_Seating (Seating)
                print ("\n")
            case "s":
                print ("Search option has nothing yet")
            case "d":
                print ("Display option has nothing yet")
            case "q":
                exit () 
            case _:
                print ("\nInvalid input!  Please try again.")