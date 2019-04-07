# tALLy

How to run:  
1. Go to db folder
2. Run startup.sh to start MongoDB
3. Go back to root directory
4. Run run.py to start server

How to run on Windows:
1. Go to your MongoDB bin folder: C:\Program Files\MongoDB\Server\4.0\bin
2. Run mongod --port 27017 --dbpath [tally data path]
where your tally data path should be something like: C:/code/tALLy/db/data
3. In a new terminal window, go to root tally directory
4. Run python run.py