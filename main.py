'''
Title: Random Quote Generator
Author: Dominic Khorrami-Arani
Date-created: 2021-12-26
'''

import sqlite3
import pathlib
from types import NoneType

# --- VARIABLES --- #
DATABASE = 'quotes.db'
FIRST_RUN = True

# Test if database already exists
if (pathlib.Path.cwd() / DATABASE).exists():
    FIRST_RUN = False

CONNECTION = sqlite3.connect(DATABASE)
CURSOR = CONNECTION.cursor()

# --- FUNCTIONS --- #
## INPUTS

def checkInt(NUMBER):
    if NUMBER.isnumeric():
        return int(NUMBER)
    else:
        print("Enter a valid number!")
        NEW_NUMBER = input("> ")
        return checkInt(NEW_NUMBER)


def menu():
    """User inputs option

    Returns:
        (int):
    """
    print("""
Please select an option:
    1. Get Random Quote
    2. Add Quote
    3. Remove Quote
    4. Update Quote
    5. Exit
    """)
    CHOICE = input("> ")
    CHOICE = checkInt(CHOICE)
    if CHOICE > 0 and CHOICE < 6:
        return CHOICE
    else:
        print("Please enter a number in the menu!")
        return menu()

def addQuote():
    """User inputs quote into quotes table
    """
    global CURSOR, CONNECTION
    # INPUTS
    QUOTE = input("Quote: ")
    AUTHOR = input("Author: ")
    BOOK = input("Where is the quote from?: ")
    # PROCESSING
    if QUOTE == "":
        print("Quote is required!")
    else:
        CURSOR.execute('''
            INSERT INTO
                quotes (
                    quote,
                    author,
                    book
                )
            VALUES (
                ?, ?, ?
            )
        ;''', (QUOTE, AUTHOR, BOOK))
        # OUTPUT
        CONNECTION.commit()
        print(f"{QUOTE} was successfully saved to table.")

def getQuoteID():
    """User selects individual quote information

    Returns:
        (int): primary key
    """
    global CURSOR

    INFO = CURSOR.execute('''
        SELECT
            *
        FROM
            quotes
    ;''').fetchall()

    print("Please select a quote.")
    for i in range(len(INFO)):
        print(f"{i + 1}. {INFO[i][1]} {INFO[i][2]}")

    ROW_INDEX = input("> ")
    ROW_INDEX = int(ROW_INDEX) - 1

    QUOTE_ID = INFO[ROW_INDEX][0]
    return QUOTE_ID

def updateQuote(ID):
    """User updates contact information

    Args:
        ID (int): primary key
    """
    global CURSOR, CONNECTION

    QUOTE_INFO = CURSOR.execute('''
        SELECT
            quote,
            author,
            book
        FROM
            quotes
        WHERE
            id = ?
    ;''', [ID]).fetchone()

    # INPUTS
    print("Leave field blank for no changes")
    QUOTE = input(f"Quote: ({QUOTE_INFO[0]}) ")
    AUTHOR = input(f"Author: ({QUOTE_INFO[1]}) ")
    BOOK = input(f"Where is the book from?: ({QUOTE_INFO[2]}) ")

    # PROCESSING
    INFO = [QUOTE, AUTHOR, BOOK]
    for i in range(len(INFO)):
        if INFO[i] == "":
            INFO[i] = QUOTE_INFO[i]

    INFO.append(ID)

    # OUTPUT
    CURSOR.execute('''
        UPDATE
            quotes
        SET
            quote = ?,
            author = ?,
            book = ?
        WHERE
            id = ?
    ;''', INFO)

    CONNECTION.commit()
    print(f"{INFO[0]} is successfully updated!")

## PROCESSING
def setup():
    """Creates table in the database
    """
    global CONNECTION, CURSOR

    CURSOR.execute('''
        CREATE TABLE
            quotes (
                id INTEGER PRIMARY KEY,
                quote TEXT NOT NULL,
                author TEXT,
                book TEXT
            )
    ;''')
    CONNECTION.commit()


def deleteQuote(ID):
    """Deletes quote information in the directory

    Args:
        ID (int): primary key
    """
    global CURSOR, CONNECTION
    INFO = CURSOR.execute('''
        SELECT
            *
        FROM
            quotes
        WHERE
            id = ?
    ;''', [ID]).fetchone()

    # DELETE
    CURSOR.execute('''
        DELETE FROM
            quotes
        WHERE
            id = ?
    ;''', [ID])

    CONNECTION.commit()

    print(f"{INFO[1]} was successfully deleted.")

def randomQuote():
    """User selects random quote
    """
    global CURSOR
    QUOTES = CURSOR.execute('''
        SELECT
            quote,
            author,
            book
        FROM
            quotes
        ORDER BY
            random()
        LIMIT
            1
    ;''').fetchone()

    if QUOTES == None:
        print("There are no quotes in the database!")
        return MENU
    
    QUOTES = list(QUOTES)

    if QUOTES[1] == "" and QUOTES[2] == "":
        print(f"{QUOTES[0]}")
    elif QUOTES[2] == "":
        print(f"""
{QUOTES[0]}

    - {QUOTES[1]}
        """)
    else:
        print(f"""
{QUOTES[0]}

    - {QUOTES[1]} ({QUOTES[2]})
        """)

## OUTPUTS
def startText():
    """Starting text for program
    """
    print("Welcome to the Random Quote Generator!")

# --- MAIN PROGRAM CODE --- #

if __name__ == "__main__":
    if FIRST_RUN:
        setup()
    
    startText()

    while True:
        MENU = menu()
        if MENU == 1:
            randomQuote()
        elif MENU == 2:
            addQuote()
        elif MENU == 3:
            QUOTE_ID = getQuoteID()
            deleteQuote(QUOTE_ID)
        elif MENU == 4:
            QUOTE_ID = getQuoteID()
            updateQuote(QUOTE_ID)
        elif MENU == 5:
            print("Goodbye!")
            exit()