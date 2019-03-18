
mcd_pack = "MD1"
mrd_pack = "MRD"
lob_pack = "LOB"
yes = "y"
no = "n"
pack_req = 0
y_n = 0
looper1 = False
looper2 = False
close = False

print("Welcome to the card shop! Which pack would you like to purchase?\n"
      "> [MD1] McDonald's Promotional Cards\n"
      "> [MRD] Metal Raiders\n"
      "> [LOB] Legend of Blue Eyes White Dragon\n"
      ">  [x]  Leave Shop")
while looper1 == False:
    pack_req = input()
    if pack_req == mcd_pack:
        looper1 = True
        print("Are you sure you would like to purchase MD1?\n> Yes [y]\n> No [n]")
        while looper2 == False:
            y_n = input()
            if y_n == yes:
                looper2 = True
                print("CARDS, BITCH!")
            elif y_n == no:
                looper2 = True
                looper1 = False
                pack_req = 0
                print("Which pack would you like to purchase?\n"
                      "> [MD1] McDonald's Promotional Cards\n"
                      "> [MRD] Metal Raiders\n"
                      "> [LOB] Legend of Blue Eyes White Dragon\n"
                      ">  [x]  Leave Shop")
            else: print("Invalid selection. Please pick yes [y] or no [n].")
    if pack_req == mrd_pack:
        looper1 = True
        print("Are you sure you would like to purchase MRD?\n> Yes [y]\n> No [n]")
        while looper2 == False:
            y_n = input()
            if y_n == yes:
                looper2 = True
                print("CARDS, BITCH!")
            elif y_n == no:
                looper2 = True
                looper1 = False
                pack_req = 0
                print("Which pack would you like to purchase?\n"
                      "> [MD1] McDonald's Promotional Cards\n"
                      "> [MRD] Metal Raiders\n"
                      "> [LOB] Legend of Blue Eyes White Dragon\n"
                      ">  [x]  Leave Shop")
            else: print("Invalid selection. Please pick yes [y] or no [n].")
    if pack_req == lob_pack:
        looper1 = True
        print("Are you sure you would like to purchase LOB?\n> Yes [y]\n> No [n]")
        while looper2 == False:
            y_n = input()
            if y_n == yes:
                looper2 = True
                print("CARDS, BITCH!")
            elif y_n == no:
                looper2 = True
                looper1 = False
                pack_req = 0
                print("Which pack would you like to purchase?\n"
                      "> [MD1] McDonald's Promotional Cards\n"
                      "> [MRD] Metal Raiders\n"
                      "> [LOB] Legend of Blue Eyes White Dragon\n"
                      ">  [x]  Leave Shop")
            else: print("Invalid selection. Please pick yes [y] or no [n].")
    if pack_req == "x":
        looper1 = True
        close = True
        print("Thanks for stopping by! Be sure to come again!")
    elif looper2 == False:
        print("Invalid selection. Please make another choice.")
    else: looper2 = False