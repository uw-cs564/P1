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
            open("data/items.dat", "a") as item_file,
            open("data/category.dat", "a") as category_file,
            open("data/bids.dat", "a") as bid_file,
            open("data/users.dat", "a") as user_file,
        ):

            times1 = ""
            for item in items:
                ID = item["ItemID"]
                seller = item["Seller"]
                sellerID = seller["UserID"]
                bids = item["Bids"]
                category = item['Category'] # array of categories
                

                if ID is None:
                    item_file.write('NULL|')
                else:
                    item_file.write(f"{ID}|")

                if 'Name' not in item or item['Name'] is None:
                    item_file.write('NULL|')
                else:
                    item_file.write(f"\"{formatStr(item['Name'])}\"|")
                   
                if 'Currently' not in item or item['Currently'] is None:
                    item_file.write('NULL')
                else:
                    item_file.write(f"{transformDollar(item['Currently'])}|")
                    
                if 'First_Bid' not in item or item['First_Bid'] is None:
                    item_file.write('NULL')
                else:
                    item_file.write(f"{transformDollar(item['First_Bid'])}|")
                   
                if 'Number_of_Bids' not in item or item['Number_of_Bids'] is None:
                    item_file.write('NULL')
                else:
                    item_file.write(f"{item['Number_of_Bids']}|")
                    
                if 'Started' not in item or item['Started'] is None:
                    item_file.write('NULL|')
                else:
                    item_file.write(f"{transformDttm(item['Started'])}|")
                    
                if 'Ends' not in item or item['Ends'] is None:
                    item_file.write('NULL|')
                else:
                    item_file.write(f"{transformDttm(item['Ends'])}|")
                    
                item_file.write(f"\"{formatStr(sellerID)}\"|")
                    
                if 'Description' not in item or item['Description'] is None:
                    item_file.write('NULL')
                else:
                    item_file.write(f"\"{formatStr(item['Description'])}\"")
                
                item_file.write("\n")


                ## For BIDS table
                if item['Bids'] is not None:
                    bids = item['Bids']
                    
                    # For ecah palced Bid/Row in bid table
                    for b in bids:
                        bid = b['Bid']
                        bidder = bid['Bidder']
                        
                        bid_file.write(f"{ID}|")
                        
                        if 'UserID' not in bidder or bidder['UserID'] is None:
                            bid_file.write("NULL|")
                        else:
                            bid_file.write(f"\"{formatStr(bidder['UserID'])}\"|")
                            user_file.write(f"\"{formatStr(bidder['UserID'])}\"|")
                            
                        if 'Time' not in bid or bid['Time'] is None:
                            bid_file.write("NULL|")
                        else:
                            bid_file.write(f"{transformDttm(bid['Time'])}|")
                            
                        if 'Amount' not in bid or bid['Amount'] is None:
                            bid_file.write("NULL")
                        else:
                            bid_file.write(f"{transformDollar(bid['Amount'])}")
                            
                            
                        ## User table, Bidder
                        if 'Rating' not in bidder or bidder['Rating'] is None:
                            user_file.write("NULL|")
                        else:
                            user_file.write(f"{bidder['Rating']}|")
                            
                        if 'Location' not in bidder or bidder['Location'] is None:
                            user_file.write("NULL|")
                        else:
                            user_file.write(f"\"{formatStr(bidder['Location'])}\"|")
                            
                        if 'Country' not in bidder or bidder['Country'] is None:
                            user_file.write("NULL")
                        else:
                            user_file.write(f"\"{formatStr(bidder['Country'])}\"")
                            
                        bid_file.write('\n')
                        user_file.write('\n')
                        
                ## For User table, sellers
                user_file.write(f"\"{formatStr(sellerID)}\"|")
                
                if 'Rating' not in seller or seller['Rating'] is None:
                    user_file.write("NULL|")
                else:
                    user_file.write(f"{seller['Rating']}|")
                
                if 'Location' not in item or item['Location'] is None:
                    user_file.write("NULL|")
                else:
                    user_file.write(f"\"{formatStr(item['Location'])}\"|")
                    
                if 'Country' not in item or item['Country'] is None:
                    user_file.write("NULL")
                else:
                    user_file.write(f"\"{formatStr(item['Country'])}\"")
                
                user_file.write('\n')
                
                ## for Category table
                # Remove duplicate categories for a given item
                for c in list(set(category)):
                    category_file.write(f"{ID}|")
                    category_file.write(f"\"{formatStr(c)}\"")
                    category_file.write("\n")
                    
                    
                    
                

                
                
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
