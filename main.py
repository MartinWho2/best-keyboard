import math
position = [1,5,8,11,14,2,6,9,12,15,3,4,7,10,13,16,17,20,23,26,29,32,18,21,24,27,30,33,19,22,25,28,31]
keys = {"q":1,"w":5,"e":8, "r":11,"t":14,"z":17,"u":20,"i":23,"o":26,"p":29,"è":32,"a":2,"s":6,"d":9,
        "f":12,"g":15,"h":18, "j":21,"k":24,"l":27,"é":30,"à":33,"<":3,"y":4,"x":7,"c":10,"v":13,"b":16,
        "n":19,"m":22, ",":25,".":28,"-":31,
        ">":3,";":25,":":28}
def keyboard_to_dict(keyboard:str):
    k = {}
    for index,char in enumerate(keyboard):
        k[char] = position[index]
        if char == "<":
            k[">"] = position[index]
        elif char == ",":
            k[";"] = position[index]
        elif char == ".":
            k[":"] = position[index]
    return k
#keys = keyboard_to_dict("qwertasdfg<yxcvbzuiopèhjkléànm,.-")
#keys = keyboard_to_dict("bépoèauie,êàyx.kwvdljzctsrnm?qghf")
#keys = keyboard_to_dict("abcdefghijklmnopqrstuvwxyz,.-éèà?")
finger_pos = [2,6,9,12,21,24,27,30]
"""
1-4
5-7
8-10
11-16
17-22
23-25
26-28
29-33
"""

fingers = [(1,4),(5,7),(8,10),(11,16),(17,22),(23,25),(26,28),(29,33)]
index_to_finger = {}
for index,tup in enumerate(fingers):
    for i in range(tup[0],tup[1]+1):
        index_to_finger[i] = index
up_mid = math.sqrt(1+0.25**2)
up_down = math.sqrt(2**2+0.75**2)
mid_down = math.sqrt(1+0.5**2)
side_to_side = 1
distances_between_points = {
    frozenset([1,2]):up_mid,frozenset([2,4]):mid_down,frozenset([1,4]):up_down,frozenset([1,3]):math.sqrt(1+0.25**2),
    frozenset([2,3]):mid_down,frozenset([3,4]):side_to_side
    }
up_keys = [5,8,11,14,17,20,23,26,29]
for key in up_keys:
    distances_between_points[frozenset([key,key+1])] = up_mid
    distances_between_points[frozenset([key,key+2])] = up_down
    distances_between_points[frozenset([key+1,key+2])] = mid_down
for a in {11,12,13,17,18,19,29,30}:
    distances_between_points[frozenset([a,a+3])] = side_to_side
for a in {11,17,29}:
    distances_between_points[frozenset([a,a+4])] = math.sqrt(1+1.25**2)
for a in {12,18}:
    distances_between_points[frozenset([a,a+4])] = math.sqrt(1+1.5**2)
for a in {12,18,30}:
    distances_between_points[frozenset([a,a+2])] = math.sqrt(1+0.75**2)
for a in {13,19,31}:
    distances_between_points[frozenset([a,a+2])] = mid_down
for a in {11,17}:
    distances_between_points[frozenset([a,a+5])] = math.sqrt(2**2+1.75**2)
for a in {13,19,31}:
    distances_between_points[frozenset([a,a+1])] = math.sqrt(2**2+0.25**2)
distances_between_points[frozenset([32,33])] = up_mid
with open("test.txt","r",encoding="utf-8") as file:
    text = file.read()
    file.close()
dist_parcourue = 0
print(f"text is {text}")
not_found = []
not_found_occurences = {}
for char in text:
    print(f"Scanning for char {char} --->",end="   ")
    if char.isupper():
        char = char.lower()
    key = keys.get(char)
    if key:
        finger_used = index_to_finger[key]
        previous_pos = finger_pos[finger_used]
        if previous_pos != key:
            present_dist = distances_between_points[frozenset([previous_pos,key])]
            print(f"Going from {previous_pos} to {key} : distance is {present_dist}")
            dist_parcourue += present_dist
            finger_pos[finger_used] = key
        else:
            print(f"Same character : {previous_pos} --> skipped")
    else:
        if char not in not_found:
            not_found.append(char)
            not_found_occurences[char] = 1
        else:
            not_found_occurences[char] += 1
        print("Character not found on the keyboard")
print(f"Total distance = {dist_parcourue}")
print("I didn't find the characters : ")
for i in not_found:
    print(i+f" that appeared {not_found_occurences[i]} times,")



