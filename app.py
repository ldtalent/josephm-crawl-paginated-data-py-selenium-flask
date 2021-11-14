from flask import Flask
from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from flask import json
import logging
import pandas as pd
from pandas import ExcelWriter


url ='https://www.edmunds.com/cars-for-sale-by-owner/'
webD = wb.Firefox()
webD.get(url)


# Insert data
# zipcode = webD.find_element_by_id("zip-input-3186404731091060")
# zipcode.send_keys('23831')
app = Flask(__name__)


card_data = webD.find_elements_by_class_name('usurp-inventory-card') # Get the data from the card holding car information
print(card_data)

carList = list() # create  an empty list
listOfLinks = list() # creates  an empty list

"""Loop through each card element from the website"""
for data in  card_data:
    car_name = data.find_element_by_class_name('card-title').text # gets and stores car name
    car_price = data.find_element_by_class_name('display-price').text  #gets and  stores the price

    # final_data = car_name+":"+car_price

    a = data.find_element_by_class_name('usurp-inventory-card-vdp-link') # finds and stores each item link available on the website by class name
    link = a.get_property('href') # used specifically to scrap the href link  

    carDict = {"car_name": car_name, "car_price": car_price,"link":link} # used to store the scrapped data in a key,Value pair
    linkDict ={"link":link}  # stores  only the link in a dictionary
    listOfLinks.append(link) # adds all the scrapped data into a list
    carList.append(carDict) # adds all the name and carprice into a dictionary called carList


#Returns all data scrapped from a certain  link
@app.route("/itemInfo")
def get_item_info():
    # itemLinks =listOfLinks
    iteDict=list() # creates an empty  item list
    sumList = list() # creates an empty list

    # Loops inside  the links
    for i in listOfLinks:
        webD.get(i) # opens an instance for every link found
        name = webD.find_element_by_class_name("not-opaque").text # gets and stores name of a  car

        price =webD.find_element_by_class_name("price-summary-section")
        price =price.find_element_by_tag_name("span").text # gets and stores price of a  car

        print(price)

        vehicle_summarry =webD.find_element_by_class_name('vehicle-summary') # gets the element that stores  vehiclle element
        miles =vehicle_summarry.find_element_by_xpath("/html/body/div[1]/div/main/div[1]/div[2]/div/div[1]/div[3]/div/div/section[1]/div/div[1]/div[1]/div[2]").text
        horsepower=vehicle_summarry.find_element_by_xpath('/html/body/div[1]/div/main/div[1]/div[2]/div/div[1]/div[3]/div/div/section[1]/div/div[2]/div[1]/div[2]').text
        ext = vehicle_summarry.find_element_by_xpath("/html/body/div[1]/div/main/div[1]/div[2]/div/div[1]/div[3]/div/div/section[1]/div/div[1]/div[2]/div[2]/span").text
        gas_engine =vehicle_summarry.find_element_by_xpath("/html/body/div[1]/div/main/div[1]/div[2]/div/div[1]/div[3]/div/div/section[1]/div/div[2]/div[2]/div[2]").text
        inc_Cashmere = vehicle_summarry.find_element_by_xpath("/html/body/div[1]/div/main/div[1]/div[2]/div/div[1]/div[3]/div/div/section[1]/div/div[2]/div[2]/div[2]").text
        address =vehicle_summarry.find_element_by_xpath("/html/body/div[1]/div/main/div[1]/div[2]/div/div[1]/div[3]/div/div/section[1]/div/div[2]/div[3]/div[2]").text # gets and stores address of a  car

        print (miles)
        print (inc_Cashmere)

        # Error handler to return scrap data in all the links that contain all the data
        try:
            vin1 = webD.find_element_by_class_name('mt-0_5')
            vin =vin1.find_element_by_tag_name("span").text
            print("Opaque",name)

            # store the resulting data in a dictionary
            itemDixt = {"name": name, "VIN": vin,'price':price, "Vehicle Summary":{"miles": miles, "horsepower":horsepower, "ext":ext, "gas_engine":gas_engine,"inc_Cashmere":inc_Cashmere,"adress":address}}
            iteDict.append(itemDixt)
                

        except Exception as e:
            print(i)
        dataframe = pd.DataFrame(iteDict) # converts the dictionary to a pandas dataframe
        print(dataframe)

        # Writes the data in an excel
        writer = ExcelWriter('CarData.xlsx') # 
        dataframe.to_excel(writer,'Sheet1')
        writer.save()
       
    return json.dumps(iteDict)
if __name__ == "__main__":
    app.run()    




