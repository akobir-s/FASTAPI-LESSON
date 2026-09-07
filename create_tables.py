import models

from database import Base, engine

Base.metadata.create_all(bind=engine)

print("Created tables")
for table in Base.metadata.tables:
    print("> ", table)

print()