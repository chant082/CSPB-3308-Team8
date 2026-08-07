###############################################################################
## This Python script deletes the existing database (if it exists)
## It then calls create_db to create the tables again and insert initial test data
##
## CSPB 3308 Summer 2026
## Author: Team Infinity(Team 8)
##
###############################################################################

import os

from create_db import (DATABASE_NAME, create_table, insert_test_data)


# Delete the existing database
# Re-create the tables and inserts test data
def reset_database():

    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
        print("Existing database deleted.")

    create_table(DATABASE_NAME)
    insert_test_data(DATABASE_NAME)

    print("Database has been reset.")


def main():
    reset_database()


if __name__ == "__main__":
    main()