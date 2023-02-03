# Pizzeria
*Radiflow Python home assignment*

## Installation
1. clone repo `https://github.com/tamarabester/Radiflow-Pizza.git`
2. build: `docker-compose build`

## Execution
The program receives its input through a CSV file 'orders.csv'. Create this file in the directory the running command is run from.

**Input file format**
Each line represents an order for a single pizza, and each pizza is represented by comma-separated toppings.  
For example, the following file is interpreted as a list of 4 orders: The first order with onion and mushroom toppings, the second one with extra mozzarella, the third one plain, and the fourth one with olives.  
```
Onion,Mushrooms
Mozzarella

Olives
```

The pizzeria will process your orders, log the different preparation stages, and will eventually create a report with the prep time for each order and for the entire batch and persist said report to mongoDB.
At the end of the run, the log as well as its id in the database will be printed out.

For debugging/verification purposes, you can also run `RETRIEVAL_MODE=<report id> docker-compose up`, which will print out a report from the database, if found.
