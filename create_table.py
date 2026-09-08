import models
from database import Base, engine


Base.metadata.create_all(bind=engine)

print("Created tables")
for t in Base.metadata.tables:
    print('> ', t)





