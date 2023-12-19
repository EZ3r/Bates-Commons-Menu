'''
A python program to autoprint Bates menu information
Authors: Elvis Zhou and Henry Liu
Publish date: 2023 Dec 18
Version: 1.0
Last updated date: 2023 Dec 18
'''
########################################################################
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager as chrome
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as Soup
from prettytable import PrettyTable as Table
########################################################################
# Define the URL
url = "https://menu.bates.edu/NetNutrition/1"
########################################################################
def get_info (url:str,date:str)->list:
    '''
    Using selenium to get menu information from a particular URL (now only support Bates) for a particular date
    Parameters:
    URL: The URL link of Bates Commons menu
    date: the date you want to get information from
    return: a list that contains information:
    whether have breakfast for the particular date
    if have, the content of breakfast menu
    whether have brunch for the particular date
    if have, the content of brunch menu
    whether have lunch for the particular date
    if have, the content of lunch menu
    whether have dinner for the particular date
    if have, the content of dinner menu
    '''
    web = webdriver.Chrome(service=Service(chrome().install()))
    web.get(url)
    time.sleep(2)
    web.execute_script("NetNutrition.UI.unitsSelectUnit(1);")
    time.sleep(2)
    breakfast_c=""
    brunch_c=""
    lunch_c=""
    dinner_c=""
    
    try:
        breakfast = web.find_elements(By.XPATH, f"//div[header[contains(text(),'{date}')]]//a[contains(text(), 'Breakfast')]")
        breakfast[0].click()
        time.sleep(2)
        breakfast_c=web.page_source
        breakfast_i=1
        time.sleep(1)
        back = web.find_element(By.LINK_TEXT, 'Back')
        back.click()
    except:
        pass
        breakfast_i=0
    
    try:
        brunch = web.find_elements(By.XPATH, f"//div[header[contains(text(),'{date}')]]//a[contains(text(), 'Brunch')]")
        brunch[0].click()
        time.sleep(2)
        brunch_c=web.page_source
        brunch_i=1
        time.sleep(1)
        back = web.find_element(By.LINK_TEXT, 'Back')
        back.click()
    except:
        pass
        brunch_i=0
        
    try:
        lunch = web.find_elements(By.XPATH, f"//div[header[contains(text(),'{date}')]]//a[contains(text(), 'Lunch')]")
        lunch[0].click()
        time.sleep(2)
        lunch_c=web.page_source
        lunch_i=1
        time.sleep(1)
        back = web.find_element(By.LINK_TEXT, 'Back')
        back.click()
    except:
        pass
        lunch_i=0
    
    try:
        dinner = web.find_elements(By.XPATH, f"//div[header[contains(text(),'{date}')]]//a[contains(text(), 'Dinner')]")
        dinner[0].click()
        time.sleep(2)
        dinner_c=web.page_source
        dinner_i=1
    except:
        pass
        dinner_i=0
        
    web.quit()
    return([breakfast_i,breakfast_c,brunch_i,brunch_c,lunch_i,lunch_c,dinner_i,dinner_c])

########################################################################

def converting_dates(date)->str:
    '''
    A function to convert defult date to the date format required
    Parameter: date: the deful date to convert
    returns: a formatted date (string)
    '''
    time=date.strftime("%A, %B %d, %Y")
    return time

########################################################################

def getDish(html_str:str)->tuple:
    '''
    This function takes the html in string type, convert it into beautifulsoup object, and returns the dish of the meal that html string represents.

    parameter:
    html_str: the html, but in string type

    return: a tuple of type_list and all_dish
    type_list: a list of strings that types of dish that meal provides
    all_dish: all dishes of one type of dish, corresponding to the type in type_list
    '''
    soup = Soup(html_str, 'html.parser')
    body=soup.find('tbody')
    all_types=["Bobcat Bar","Grill","Vegan Bar","Brick Oven","Pasta Bar","Deli","Bakery","Grab 'n Go","Waffle Station","Sunday Sundae Bar"]
    type_list=[]
    dish=[]
    all_dish=[]
    for item in body:
        if item.text in all_types:
            type_list.append(item.text)
            if dish==[]:
                pass
            else:
                all_dish.append(dish)
                dish=[]
        else:
            dish.append(item.find_all('td')[1].text)
    all_dish.append(dish)
    return(type_list, all_dish)

########################################################################

def printMeal(title:str, the_list:tuple)->None:
    '''
    This function takes the information of a meal and prints a table using prettytable function that contains those information

    parameters:
    title: string object that indicates which meal it is (breakfast, lunch, etc.) and the date
    the_list: a list that contains two lists of all information of that meal. the first list is the list of types of dish; the second list is the list of dishes in this meal, corresponds to the type in first list

    return: None    
    '''
    table1=Table()
    type_list=the_list[0]
    dish_list=the_list[1]
    table1.field_names = type_list
    table1.title = title
    for type in type_list:
        table1.align[type] = 'l'
    length_list=[]
    for i in range (0,len(dish_list)):
        length_list.append(len(dish_list[i]))
    max_length=max(length_list)
    for i in range (0,len(dish_list)):
        for j in range (0,max_length-len(dish_list[i])):
            dish_list[i].append("")
    for i in range (0,max_length):
        new_row=[]
        for j in range (0,len(dish_list)):
            new_row.append(dish_list[j][i])
        table1.add_row(new_row)
    print(table1)

########################################################################
    
def main():
    user_input=input("You want today's menu or tomorrow's menu?(td for today, tmr for tomorrow) ")
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    today = converting_dates(today)
    tomorrow = converting_dates(tomorrow)
    if user_input=='td':
        menu_c=get_info(url, today)
        if menu_c[0]==1:
            breakfast=f"Breakfast of {today}"
            breakfast_c=getDish(menu_c[1])
            printMeal(breakfast,breakfast_c,)
        if menu_c[2]==1:
            brunch=f"Bunch of {today}"
            brunch_c=getDish(menu_c[3])
            printMeal(brunch,brunch_c)
        if menu_c[4]==1:
            lunch=f"Lunch of {today}"
            lunch_c=getDish(menu_c[5])
            printMeal(lunch,lunch_c)
        if menu_c[6]==1:
            dinner=f"Dinner of {today}"
            dinner_c=getDish(menu_c[7])
            printMeal(dinner,dinner_c)

    elif user_input=="tmr":
        menu_c2=get_info(url, tomorrow)
        if menu_c2[0]==1:
            breakfast=f"Breakfast of {tomorrow}"
            breakfast_c=getDish(menu_c2[1])
            printMeal(breakfast,breakfast_c)
        if menu_c2[2]==1:
            brunch=f"Bunch of {tomorrow}"
            brunch_c=getDish(menu_c2[3])
            printMeal(brunch,brunch_c)
        if menu_c2[4]==1:
            lunch=f"Lunch of {tomorrow}"
            lunch_c=getDish(menu_c2[5])
            printMeal(lunch,lunch_c)
        if menu_c2[6]==1:
            dinner=f"Dinner of {tomorrow}"
            dinner_c=getDish(menu_c2[7])
            printMeal(dinner,dinner_c)
    else:
        print("please enter 'td' or 'tmr'")
        
########################################################################

if __name__ == "__main__":
    main()