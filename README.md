# Pizzeria
*Radiflow Python home assignment*

## Installation
1. clone repo
2. build: `docker-compose build`

## Execution
The program receives its input through a csv file 'orders.csv'.
Create such file in the directory the running command is run from.

**Input file format**   
Each line represents an order for a single pizza, and each pizza is represented by comma seperated toppings.
For example, the following file is interoperated as a list of 4 orders: First order with onion and mushroom toppings, second one with extra mozzarella, third one is plain, and the forth one with olives.
```
Onion,Mushrooms
Mozzarella

Olives
```

Once the input file is created and placed, simply use `docker-compose up` to run the program.

The pizzeria will process your orders, logging the different stages in the preparation, and will eventually print the prep time for each order and for the entire batch.  

Additionally, the said report is persisted to MongoDB and its id is also printed at the end of the run.  
For debugging/verification purposes, you can also run `RETRIEVAL_MODE=<report id> docker-compose up`, which will print out a report from the db, if found.

