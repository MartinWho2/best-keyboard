import math
import random
import matplotlib.pyplot as plt
import numpy as np


position = [1,5,8,11,14,2,6,9,12,15,3,4,7,10,13,16,17,20,23,26,29,32,18,21,24,27,30,33,19,22,25,28,31]
#keys = {"q":1,"w":5,"e":8, "r":11,"t":14,"z":17,"u":20,"i":23,"o":26,"p":29,"è":32,"a":2,"s":6,"d":9,
        #"f":12,"g":15,"h":18, "j":21,"k":24,"l":27,"é":30,"à":33,"<":3,"y":4,"x":7,"c":10,"v":13,"b":16,
        #"n":19,"m":22, ",":25,".":28,"-":31,
        #">":3,";":25,":":28}
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
def generate_keyboard():
    keyboard_keys = "qwertasdfg<yxcvbzuiopèhjkléànm,.-"
    length = len(keyboard_keys)
    keyboard_keys_list = []
    new_keyboard = ""
    for char in keyboard_keys:
        keyboard_keys_list.append(char)
    for iteration in range(length):
        choice = random.randint(0,length-1-iteration)
        new_keyboard += keyboard_keys_list[choice]
        del keyboard_keys_list[choice]
    #print(f"New keyboard generated : {new_keyboard}")
    return new_keyboard


#keys = keyboard_to_dict("bépoèauie,êàyx.kwvdljzctsrnm?qghf")
#keys = keyboard_to_dict("abcdefghijklmnopqrstuvwxyz,.-éèà?")
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

finger_pos = [2,6,9,12,21,24,27,30]
fingers = [(1,4),(5,7),(8,10),(11,16),(17,22),(23,25),(26,28),(29,33)]
index_to_finger = {}
n_generations = 50
population = 500
percentage_of_survivors = 0.25
survivors = round(population * percentage_of_survivors)

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
    text2 = file.read()
    file.close()
text = ""
ks = keyboard_to_dict(generate_keyboard())
for char in text2:
    if char.isupper():
        char = char.lower()
    if ks.get(char):
        text += char
print(text)
def calculate_fitness_score(keys,keys_missed = False):
    finger_position = [2,6,9,12,21,24,27,30]
    keys = keys
    dist_parcourue = 0
    not_found = []
    not_found_occurences = {}
    for char in text:
        #print(f"Scanning for char {char} --->",end="   ")
        #if char.isupper():
        #    char = char.lower()
        key = keys.get(char)
        if key:
            finger_used = index_to_finger[key]
            previous_pos = finger_position[finger_used]
            if previous_pos != key:
                present_dist = distances_between_points[frozenset([previous_pos,key])]
                #print(f"Going from {previous_pos} to {key} : distance is {present_dist}")
                dist_parcourue += present_dist
                finger_position[finger_used] = key
            else:
                #print(f"Same character : {previous_pos} --> skipped")
                pass
        elif keys_missed:
            if char not in not_found:
                not_found.append(char)
                not_found_occurences[char] = 1
            else:
                not_found_occurences[char] += 1
            #print("Character not found on the keyboard")
        else:
            raise Exception
    #print(f"Total distance = {dist_parcourue}")
    #print("I didn't find the characters : ")
    if keys_missed:
        for i in not_found:
            print(i+f" that appeared {not_found_occurences[i]} times,")
    return dist_parcourue
#keys = keyboard_to_dict("qwertasdfg<yxcvbzuiopèhjkléànm,.-")
#print(calculate_fitness_score(keys))
def new_keys_from_2_keys(keys_1:str,keys_2:str)->str:
    all_keys = "qwertasdfg<yxcvbzuiopèhjkléànm,.-"
    #print(f"Transforming 2 keyboards into 1 : \n {keys_1}\n{keys_2}")
    new_keys = keys_1[:16]

    for key in new_keys:
        all_keys = all_keys.replace(key, "")
    keys_2_used = keys_2[16:]
    empty_space = []
    for index,key in enumerate(keys_2_used):
        if key in new_keys:
            empty_space.append(16+index)
            new_keys += "0"
        else:
            new_keys += key
            all_keys = all_keys.replace(key,"")
    nb_missing_keys = len(all_keys)
    for index,missing_key in enumerate(all_keys):
        place = random.randint(0,nb_missing_keys-1-index)
        place_in_string = empty_space[place]
        del empty_space[place]
        new_keys = new_keys[:place_in_string]+ missing_key + new_keys[place_in_string+1:]
        all_keys = all_keys.replace(missing_key,"")
    return new_keys

def swap_2_keys(key:str):
    first_pos = random.randint(0,14)
    sec = random.randint(15,len(key)-1)
    new_str = key[:first_pos] + key[sec] + key[first_pos+1:sec]+key[first_pos]+key[sec+1:]
    return new_str
calculate_fitness_score(keyboard_to_dict(generate_keyboard()),keys_missed=True)
gens = []
swap_2_keys(generate_keyboard())
best_keys_1 = {}
best_fitness =[]


#print(f"fitness of bépo : {calculate_fitness_score(keyboard_to_dict('bépoèauie,êàyx.kwvdljzctsrnm?qghf'))}")
#print(f"fitness of qwertz : {calculate_fitness_score(keyboard_to_dict('qwertasdfg<yxcvbzuiopèhjkléànm,.-'))}")
#c = calculate_fitness_score(keyboard_to_dict("',.pyaoeui+;qjkxfgcrl?dhtns-bmwvs"))
#print(f"fitness of dvorak : {c}")
for i in range(population):
    keys = generate_keyboard()
    fitness = calculate_fitness_score(keyboard_to_dict(keys))
    best_keys_1[fitness] = keys
    best_fitness.append(fitness)
    print("|",end="")
for i in range(0):
    if i%5==1:
        k = ".jévqlsurmtdk-bwhpfày,cnaeoixzè<g"
    elif i%5 ==2:
        k = "réfzhcuavslw-yjà<qèpb,mteniodgkx."
    elif i%5 ==3:
        k = "é-èf,ueaiomjyà.<kghcqvlnsrtdpxzwb"
    elif i%5 == 4:
        k = "m.nhcueloipxyzgàjb-qfétdrsa,vwèk<"
    else:
        k = ",bskyirhclu.qwdgvém-àjnpteaox<èzf"
    fit = calculate_fitness_score(keyboard_to_dict(k))
    best_keys_1[fit] = k
    best_fitness[i*10] = fit
print()
best_fitness.sort()
print(f"gen 1 best keyboard : {best_fitness[0]}, The keyboard is "+best_keys_1[best_fitness[0]])
fig, ax = plt.subplots()
ax.plot(range(0,len(best_fitness)),best_fitness)

ax.set(xlabel='individual keyboards ', ylabel='Fitness score (m)',
               title=f'Keyboard fitness repartition at 1 generation')
ax.grid()
#fig.savefig(f"gen1-swap0.5.png")
plt.close(fig)
new_gen = []
for index in range(survivors):
    new_gen.append(best_keys_1[best_fitness[index]])
gens.append(best_keys_1)

best_fitness_per_gen = [best_fitness[0]]
for i in range(n_generations):
    gen_now = []
    best_keys = {}
    best_fitness = []
    for previous in new_gen:
        for j in range(round(1/percentage_of_survivors)):
            new_key = new_keys_from_2_keys(previous,new_gen[random.randint(0,survivors-1)])
            if random.randint(1,3) == 1:
                new_key = swap_2_keys(new_key)
            fitness = calculate_fitness_score(keyboard_to_dict(new_key))
            best_keys[fitness] = new_key
            best_fitness.append(fitness)
        print("|",end="")
    best_fitness.sort()
    best_fitness_per_gen.append(best_fitness[0])
    print(f"\nBest keyboard from generation {i+2} : {best_fitness[0]} , The keyboard is "+best_keys[best_fitness[0]])
    new_gen = []
    for index in range(survivors):
        new_gen.append(best_keys[best_fitness[index]])
    #fig, ax = plt.subplots()
    #ax.plot(range(0,len(best_fitness)),best_fitness)

#    ax.set(xlabel='individual keyboards ', ylabel='Fitness score (m)',
#               title=f'Keyboard fitness repartition at {i+2} generation')
#   ax.grid()
    #fig.savefig(f"gen{i+2}-swap0.2.png")
#    plt.close(fig)
    #print("New keyboard generated  -->  " + new_keyboard)
    #keys = keyboard_to_dict(new_keyboard)
    #fitness = calculate_fitness_score(keys)
fig, ax = plt.subplots()
ax.plot(range(0,len(best_fitness_per_gen)),best_fitness_per_gen)

ax.set(xlabel='Generation (n)', ylabel='Best fitness score (m)',
               title=f'Keyboard fitness repartition at every generation with 33% swap')
ax.grid()
fig.savefig("swap-0.3-mid-big.png")
