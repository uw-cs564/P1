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
                # looping through each item attributes
                #TODO need a function to format all string values, will make life a lot easier
                # add a quote in front of all instances of quotes in a string
                
                #TODO Check if None, turn into "NULL"
                
                #TODO if bids is empty, num of bids = NULL

                for key in item.keys():
                    bids_bool = False
                    bids_bool_id = False
                    if item[key] == 'null':
                        item[key] = "NULL"
                    if key == "ItemID":
                        insert = item[key]
                        bids_bool = True
                    elif key == "Name": 
                        insert = f"\"{item[key]}\""
                    elif key in money_keys:
                        insert = transformDollar(item[key])
                    elif key in date_keys:
                        insert = transformDttm(item[key])
                    elif key == 'Category':
                        for c in item[key]:
                            category.write(f"{ID}|\"{c}\"\n")
                    if key == 'Bids':
                        if item[key] == None:   
                            times1 = "" 
                            insert =  ""
                            bids_bool_id = True 
                        elif item[key] != None:
                            for b in item[key]:
                                    bids.write(f"{ID}|")
                                    bids.write(f"{b['Bid']['Bidder']['UserID']}|")
                                    bids.write(f"{b['Bid']['Time']}|")
                                    bids.write(f"{b['Bid']['Amount']}|""\n")
                      
                    else:
                        insert = f"\"{item[key]}\""
                        
                    item_file.write(f"{insert}|")
                    
                item_file.write("\n")
               

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
