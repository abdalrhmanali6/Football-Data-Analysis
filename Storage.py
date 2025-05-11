#import needed libraries
from pymongo import MongoClient
from datetime import datetime
import sys
from pprint import pprint


################################################################################ Mongo db######################################################################

#connect to mongo db
try:
    # Connect to MongoDB with timeout and server selection timeout
    print("Attempting to connect to MongoDB...")
    client =client = MongoClient('mongodb+srv://abdalrahmanali632006:1.a2.s3.d@database.6zhfkgn.mongodb.net/?retryWrites=true&w=majority&appName=Database', 
                        serverSelectionTimeoutMS=5000,  # 5 second timeout
                        connectTimeoutMS=5000)
    
    # Verify the connection
    client.server_info()  # This will raise an exception if connection fails
    print("Successfully connected to MongoDB!")
    
    # Get database and collections
    db = client['football_db']
    head_to_head_collection = db['head_to_head_matches']
    league_table_collection = db['league_tables']
    
    # Verify database exists
    if 'football_db' not in client.list_database_names():
        print("Creating database 'football_db'...")
    
    # Verify collections exist
    if 'head_to_head_matches' not in db.list_collection_names():
        print("Creating collection 'head_to_head_matches'...")
    if 'league_tables' not in db.list_collection_names():
        print("Creating collection 'league_tables'...")
    
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    print("Please make sure MongoDB is installed and running on your system.")
    sys.exit(1)


# ### Store head to head Teams



def store_head_to_head_matches(team1, team2, matches):
    """
    Store head-to-head matches between two teams
    """
    try:
        # Create document with match data
        match_data = {
            "team1": team1,
            "team2": team2,
            "matches": matches,
            "stored_at": datetime.now()
        }
        exist=head_to_head_collection.find_one({"team1": match_data["team1"],"team2": match_data["team2"]})
        if not exist:
            print("Storing head-to-head matches...")
            result = head_to_head_collection.insert_one(match_data)
            print(f"Head-to-head matches successfully stored with ID: {result.inserted_id}")
            return result.inserted_id
        else:
            print("Data for this date already exists.")

    except Exception as e:
        print(f"Error storing head-to-head matches: {e}")
        return None


# ### Store league table data


def store_league_table(date, rank_list):
    """
    Store league table data for a specific date
    """
    try:
        # Create document with league table data
        table_data = {
            "date": date,
            "teams": rank_list,
            "stored_at": datetime.now()
        }
        exist=league_table_collection.find_one({"date": table_data["date"]})

        if not exist:
            print("Storing league table data...")
            result = league_table_collection.insert_one(table_data)
            print(f"League table data successfully stored with ID: {result.inserted_id}")
            return result.inserted_id
        else:
            print("Data for this date already exists.")
    except Exception as e:
        print(f"Error storing league table data: {e}")
        return None
        



