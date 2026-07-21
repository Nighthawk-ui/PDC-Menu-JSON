from bs4 import BeautifulSoup
import requests
import re
import json

def processList(menu):
    for i in range(len(menu)):
        if(any([char.isdigit() for char in menu[i]])):
            break
    del menu[:(i-1)]
def containsDigit(mystring):
    if any([char.isdigit() for char in mystring]):
        return True
    else:
        return False
def containsTime(mystring):
    if("PM" in mystring or "pm" in mystring or "AM" in mystring or "am" in mystring):
        return True
    else:
        return False
def isPrice(mystring):
    if(mystring.isdigit() or "F:" in mystring or "H:" in mystring or "Q:" in mystring):
        return True
    else: 
        return False

def parsePage(menu):#Extracts all the visible text on the page and then extracts and formats a list of menu items, the 2nd element may contain time
    for i in soup.stripped_strings:
        if containsDigit(i)and not(containsTime(i)) and (isPrice(i)):
            number_list = re.findall(r"\d+",i)
            menu.extend(number_list)
        else:
            menu.append(i)
    #if menu[0] == "The Off-Side Cafe":
    #print(menu)
    processList(menu)


def createDict(menu, menuDict, cuisine_img, food_images ):
    startIndex = 0
    if containsTime(menu[1]):
        startIndex = 2
        timelist = re.findall(r"\d+",menu[1])
        startTime = int(timelist[0]+timelist[1])
        endTime = int(timelist[2]+timelist[3])
        menuDict.update({"has_timings":True,"start_time":startTime, "end_time":endTime})
    else:
        menuDict.update({"has_timings":False})
    foodList = []
    itemPriceList = []
    allPriceList = []
    for i in range(startIndex,len(menu)):
        if menu[i].isdigit():
            itemPriceList.append(menu[i])
        else:
            if i == startIndex:
                foodList.append(menu[i])
            else:
                allPriceList.append(itemPriceList)
                itemPriceList = []
                foodList.append(menu[i])
    
    allPriceList.append(itemPriceList)
    
    menuDict.update({"cuisineImage": cuisine_img, "foodImages":food_images,"menu":foodList, "price":allPriceList})


main_url = 'https://pdc.lums.edu.pk/'

main_page = requests.get(main_url)
broth = BeautifulSoup(main_page.text, 'html.parser')
cuisine_list= broth.find_all(class_ = "d-flex flex-column justify-content-between")

cuisineDict = {}
#Lets try extracting all the visible text from the cuisines page and lets assume every food item will have a number in the next index.
for cuisine in cuisine_list:
    #print(cuisine)
    cuisine_img = cuisine.img["src"]

    cuisine = cuisine.find(class_ = "FoodName") 
    cuisine_url = cuisine.a["href"] 

    #print(cuisine.string)

    cuisine_page = requests.get(cuisine_url)
    soup = BeautifulSoup(cuisine_page.text, 'html.parser')

    food_images = []
    img_srcs = soup.find_all('img')
    for i in img_srcs:
        string = i["src"]
        if "get-picture.php?" in string:
            food_images.append(string)

    print(len(food_images))
    cuisine_name = cuisine.string
    menu = []
    print(cuisine_name)
    parsePage(menu)

    menuDict = {}
    
    createDict(menu, menuDict, cuisine_img, food_images)
    print(len(menuDict["menu"]))
    #if cuisine_name == "The Off-Side Cafe":
    #    print(menuDict["menu"])
    cuisineDict.update({cuisine_name:menuDict})
    #print(menu)
    print(" ")

fileName = "pdc.json"
with open(fileName,'w') as json_file:
    json.dump(cuisineDict, json_file, indent = 4)



    
    






# loops through each cuisine and outputs the menu for each. problem is the class tag is not consistent
# for cuisine in cuisine_list:

#     cuisine_url = cuisine.a["href"] 
#     cuisine_page = requests.get(cuisine_url)
#     soup = BeautifulSoup(cuisine_page.text, 'html.parser')
#     menu= soup.findAll(class_ = "col")
#     print(cuisine.string)
#     for food_item in menu:
#         menu = list(food_item.stripped_strings)
#         print(menu[0], )
#     print(" ")




