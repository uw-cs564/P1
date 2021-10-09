"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""
import sys
from json import loads
from re import sub
import re
columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",
}

money_keys = ['Buy_Price', 'Currently', 'First_Bid']
date_keys = ['Started', 'Ends']
string_key = ['Name', 'Location', 'Country', 'Description']


def isJson(f):
    """
    Returns true if a file ends in .json
    """
    return len(f) > 5 and f[-5:] == ".json"


def transformMonth(mon):
    """
    Converts month to a number, e.g. 'Dec' to '12'
    """
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon


def transformDttm(dttm):
    """
    Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
    """
    dttm = dttm.strip().split(" ")
    dt = dttm[0].split("-")
    date = "20" + dt[2] + "-"
    date += transformMonth(dt[0]) + "-" + dt[1]
    return date + " " + dttm[1]


def transformDollar(money):
    """
    Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
    """
    if money == None or len(money) == 0:
        return money
    return sub(r"[^\d.]", "", money)


def check_strings(word):
    """
    Parses through the strings to check if there are any quotes, 
    and add anotehr quote after
    """ 
    check = ""
    if check in word:
        quote = re.findall(r'"(.*?)"', word)
        #add first extra quote
        word.index(quote)
        #add second extra quote 

def formatStr(s):
    """Function to add a quote before each single quote """
    temp = ''
    for i, c in enumerate(s):
        if c == '"':
            temp += '"'
        temp += c
    return temp
    

def parseJson(json_file):
    """
    Parses a single json file. Currently, there's a loop that iterates over each
    item in the data set. Your job is to extend this functionality to create all
    of the necessary SQL tables for your database.
    """
    with open(json_file, "r") as f:
        items = loads(f.read())[
            "Items"
        ]  # creates a Python dictionary of Items for the supplied json file
        
        # Open all data files
        with (
            open("data/items.dat", "w") as item_file,
            open("data/category.dat", "w") as category,
            open("data/bids.dat", "w") as bids,
            open("data/users.dat", "w") as users,
        ):

            times1 = ""
            for item in items:
                ID = item["ItemID"]
                seller = item["Seller"]
                sellerID = seller["UserID"]
                bids = item["Bids"]
                # looping through each item attributes
                #TODO need a function to format all string values, will make life a lot easier
                # add a quote in front of all instances of quotes in a string
                
                #TODO Check if None, turn into "NULL"
                
                #TODO if bids is empty, num of bids = NULL
                
                #TODO must cycle through a predetemined list of keys,
                # since some keys dont exist 
                item_file.write(f"\n")

                if item['ItemID'] is None:
                    item_file.write('NULL|')
                else:
                    item_file.write(f"{item['ItemID']}|")

                if item['Name'] is None:
                    item_file.write('NULL|')
                else:
                    item_file.write(f"\"{formatStr(item['Name'])}\"|")
                   
                if item['Currently'] is None:
                    item_file.write('NULL')
                else:
                    item_file.write(f"{transformDollar(item['Currently'])}|")
                    
                if item['First_Bid'] is None:
                    item_file.write('NULL')
                else:
                    item_file.write(f"{transformDollar(item['First_Bid'])}|")
                   
                if item['Number_of_Bids'] is None:
                    item_file.write('NULL')
                else:
                    item_file.write(f"{item['Number_of_Bids']}|")
                    
                if item['Started'] is None:
                    item_file.write('NULL')
                else:
                    item_file.write(f"{transformDttm(item['Started'])}|")
                    
                if item['Ends'] is None:
                    item_file.write('NULL')
                else:
                    item_file.write(f"{transformDttm(item['Ends'])}|")
                    
                item_file.write(f"\"{sellerID}\"|")
                    
                if item['Description'] is None:
                    item_file.write('NULL')
                else:
                    item_file.write(f"\"{formatStr(item['Description'])}\"|")
                
                item_file.write("\n")
'''
                for key in item.keys():
                    item_file.write(f"{key}|")
                    
                    
                item_file.write(f"\n")

                
                for key in item.keys():
                    # Handling empty 
                    insert = 'what'
                    if item[key] == 'null':
                        item[key] = "NULL"
                        
                    # Handling each key of the item data
                    if key == "ItemID":
                        insert = item[key]
                        
                    # Format values that might be strings to handle quotes
                    elif key in string_key: 
                        insert = f"\"{formatStr(item[key])}\""
                        
                    # Format values that are dollar amounts, turns into flaots
                    elif key in money_keys:
                        insert = transformDollar(item[key])
                        
                    # Formats data values into ISO format
                    elif key in date_keys:
                        insert = transformDttm(item[key])
                    
                    # Handles category table
                    elif key == 'Category':
                        for c in item[key]:
                            category.write(f"{ID}|\"{c}\"\n")
                        continue
                            
                    # Handles Bids table
                    elif key == "Number_of_Bids":
                        num_bids = int(item[key])
                        insert = num_bids
                        
                        if num_bids != 0:
                        # If the item has bids
                            for b in item['Bids']:
                                bids.write(f"{ID}|")
                                bids.write(f"{b['Bid']['Bidder']['UserID']}|")
                                bids.write(f"{b['Bid']['Time']}|")
                                bids.write(f"{b['Bid']['Amount']}|""\n")
                    
                    elif key == 'Bids':
                        # bids handled in num_bids
                        continue            
                        
                      
                    else:
                        print(key)
                        insert = f"\"{item[key]}\""
                       
                    item_file.write(f"{key}: {insert}| ")
                  '''  
               

def main(argv):
    """
    Loops through each json files provided on the command line and passes each file
    to the parser
    """
    if len(argv) < 2:
        "print(<Usage: python skeleton_json_parser.py <path to json files>>, sys.stderr)" 
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print(f"Success parsing {f}")


if __name__ == "__main__":
    main(sys.argv)
