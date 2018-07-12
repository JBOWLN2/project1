import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():

    # Open a file using Python's CSV reader.
    f = open("zips.csv")
    reader = csv.reader(f)
    next(reader, None) #Used to skip header line and resolve "zipcode" not an integer

    # Iterate over the rows of the opened CSV file.
    for row in reader:

        # Execute database queries, one per row; then print out confirmation.
        db.execute("INSERT INTO zips (zip, city, state, lat, long, pop) VALUES (:a, :b, :c, :d, :e, :f)",
        {"a": row[0], "b": row[1], "c": row[2], "d": row[3], "e": row[4], "f": row[5]})
        #print(f"Added flight from {row[0]} to {row[1]} lasting {row[2]} minutes.")

    # Technically this is when all of the queries we've made happen!
    db.commit()

if __name__ == "__main__":
    main()
