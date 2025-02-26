"""
This example code creates a 2d list (2d matrix) that can store seating.
The matrix is populated with . since all seats are available
"""
FrontSeat = 0,1,2,3,4
MiddleSeat = 5,6,7,8,9,10
BackSeat = 11,12,13,14,15,16,17,18,19,20

def  PurchaseSeat ():
    SeatCount = int(input ("Number of seats desired:  "))
    SeatType = input  ("Type of seat desired:  ")
    Name = input ("Enter your name:  ")
    EmailAddr = input ("Enter your email address:  ")

    TicketCost, MaskFee, SubTotal, Tax, Total = CalulateFees(SeatType, SeatCount)

    print ("Name:  " + Name)
    print ("Email:  " + EmailAddr)
    print ("Number of seats:  " + str(SeatCount))
    print ("Seat Type:  " + SeatType)
    print ("Seats:  #####")
    print ("Ticket Cost:  " + str(TicketCost))
    print ("Mask Fee:  " + str(MaskFee))
    print ("Subtotal:  " + str(SubTotal))
    print ("Tax:  " + str(Tax))
    print ("Total:  " + str(Total)) 

def CalulateFees (SeatType, SeatCount):

    FrontSeatPrice = 80
    MiddleSeatPrice = 50
    BackSeatPrice = 25

    MaskFee = 5
    TaxRate = 0.0725

    match SeatType:
        case "Front":
            SeatPrice = FrontSeatPrice
        case "Middle":
            SeatPrice = MiddleSeatPrice
        case "Back":
            SeatPrice = BackSeatPrice

    TicketCost = SeatCount * SeatPrice
    TotalMaskFee = SeatCount * MaskFee
    Subtotal = TicketCost + TotalMaskFee
    Tax = Subtotal * TaxRate
    Total = Subtotal + Tax

    return (TicketCost, TotalMaskFee, Subtotal, Tax, Total)

def ViewSeating ():

    # our test matrix has 4 rows and 10 columns
    N_ROW = 10
    N_COL = 26

    # available seat
    available_seat = '.'

    # create some available seating
    seating = []
    for r in range(N_ROW):
        row = []
        for c in range(N_COL):
            row.append(available_seat)
        seating.append(row)

    # print available seating
    for r in range(N_ROW):
        print(r+1, end="\t")
        for c in range(N_COL):
            print(seating[r][c], end=" ")
        print() 




while True:
    print ("[p]     Purchase seat")
    print ("[v]     View seating")
    print ("[s]     Search seats purchased by customer's name")
    print ("[d]     Display all purchase made amd total income")
    print ("[q]     Quit app")
    Command = input ("Enter a command:  ")
    match Command:
        case "p":
            PurchaseSeat()
        case "v":
            ViewSeating()
        case "s":
            print ("S has nothing yet")
        case "d":
            print ("D has nothing yet")
        case "q":
            exit () 
        case _:
            print ("Invalid input.  Please try again...")