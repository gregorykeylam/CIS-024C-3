"""
This example code creates a 2d list (2d matrix) that can store seating.
The matrix is populated with . since all seats are available
"""
FrontSeat = 0,1,2,3,4
MiddleSeat = 5,6,7,8,9,10
BackSeat = 11,12,13,14,15,16,17,18,19,20

def CalulateFees (SeatType, SeatCount):

    PriceOfFrontSeat = 80
    PriceOfMiddleSeat = 50
    PriceOfBackSeat = 25

    MaskFee = 5
    TaxRate = 0.0725

    print ()
    print(type(TaxRate))
    print ()

    match SeatType:
        case "Front":
            SeatPrice = PriceOfFrontSeat
        case "Middle":
            SeatPrice = PriceOfMiddleSeat
        case "Back":
            SeatPrice = PriceOfBackSeat

    TicketCost = SeatCount * SeatPrice
    TotalMaskFee = SeatCount * MaskFee
    Subtotal = TicketCost + TotalMaskFee
    Tax = Subtotal * TaxRate
    Total = Subtotal + Tax

    return (TicketCost, TotalMaskFee, Subtotal, Tax, Total)
    
# our test matrix has 4 rows and 10 columns
N_ROW = 4
N_COL = 10

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

SeatCount = int (input ("Number of seats desired:  "))
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