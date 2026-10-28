
# Cooler ascii to test later with
┌
└
┐
┘
│
┬
┴
├
┤
┼


# North, 1
─
 

# North, 1
 │


┌


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

cell = 9

if cell & NORTH:
    print("North wall exists")

if cell & EAST:
    print("East wall exists")

if cell & SOUTH:
    print("South wall exists")

if cell & WEST:
    print("West wall exists")

same idea as push swap, use bitwise operator to check the number and compare.
still harder than just - & +

# Connected directions / Character
Right + Down            ┌
Left + Down             ┐
Right + Up              └
Left + Up               ┘
Left + Right + Down     ┬
Left + Right + Up       ┴
Up + Down + Right       ├
Up + Down + Left        ┤
All four                ┼
