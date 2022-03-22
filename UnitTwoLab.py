'''
Date: 1/26/22
Author: Chance Homme

This code is responsible for parsing, modifying and displaying keys and values contained in a dictionary.

'''
#==================================================
#Defining the dictionary and printing its contents.
#==================================================

router1 = { "brand": "cisco", "model": "1941", "mgmtIP": "10.0.0.1", "G0/0": "10.0.1.1/24", "G0/1": "10.0.2.1", "G0/2": "10.0.3.1/24", "hostname": "r1"}
'''
print("Pre Modified Contents")

print(router1.values())

print(router1.keys())

print(router1.items())

print("======================================================================")
'''
#===================================================
#Modifing values in the dictionary.
#===================================================

router1["G0/2"] = "10.1.3.1/24"

router1["model"] = "2901"
'''
print("Post Modified Contents")

print(router1["G0/2"])

print(router1["model"])

print(router1.values())

print(router1.keys())

print(router1.items())
'''

#======================================================================================================
#Iterating through the dictionary keys and values and printing with basic formatting using a for loop.
#======================================================================================================
'''
for key in router1:
        print("Key = " + key + "    " + "Value = " + router1[key])
'''
        
#==========================================================================================================================
#Iterating through the dictionary keys and values and printing with advanced formatting and parsing using for loops.
#==========================================================================================================================

for key in router1:
    if len(router1[key]) >=8 :
        print(key + '\t\t', end ='\t' )
    else:
        print(key + '\t', end= '\t')

print('\n' + "-" * 140)

for key in router1:
    formatedValue = router1[key].replace("/24", '')

    print(formatedValue + '\t', end ='\t' )
print("\n")





#===========================================================================================================================
#Printing the newly formatted dictionary keys and values and providing option to modify mgmtIP using multipule logic gates.
#===========================================================================================================================

count = 0

modifyIP = input("Would you like to change the Management IP Address? (y or n): " )

if modifyIP == "y":
    newIP = input("Enter a valid IP address in the x.x.x.x format: " )
    ipCheck = list(newIP.split('.'))
    for item in ipCheck:
        item.isalpha()
        if item.isalpha() == True:
            print("Please enter a valid IP address in the x.x.x.x format.")
            break
            
        else:    
            if int(item) >= 0 and int(item) <= 255:
                item.isnumeric()
                if item.isnumeric() == True:
                    count +=1
    if count == 4 and len(ipCheck) == 4:
        router1["mgmtIP"] = str(ipCheck[0]+"."+ ipCheck[1]+"."+ ipCheck[2]+"."+ ipCheck[3])
        for key in router1:
            if len(router1[key]) >=8 :
                print(key + '\t\t', end ='\t' )
            else:
                print(key + '\t', end= '\t')

        print('\n' + "-" * 140)

        for key in router1:
            formatedValue = router1[key].replace("/24", '')
            print(formatedValue + '\t', end ='\t' )

if modifyIP == 'n':
    print("No values were changed.")


                  



    


