# crane_grade_E.py : it is fully automatic so it reads from JSON action list




# IMPORT = bringing tools into the file

# Import modules : json + time + pymodbus.client
# ModbusTcpClient is class that we use to talk to Modbus
# json is standard python module for reading and writing JSON
# time is standard module and it uses here for sleep
from pymodbus.client import ModbusTcpClient
import json, time


# CREATING : Modbus client object and CONNECTING

# Creating_Object : client (it is object or instance of the class - ModbusTcpClient)
# Client & 127.0.0.1 and 502(lokal host) : creats the connection to Modbus sever (Simulation)

client = ModbusTcpClient("127.0.0.1", port=502)
client.connect()



# Reading JSON action plan
# open() is build-in function 
# with ...as f : is manager for automatically close the file
# json.load(f) : reads the file JSON & convert JSON text into python data structure
# Explanation: We open JSON - file & load into python so the result is dict with key actions and each element in this list is one step for the crane

with open("actions_grade_E.json") as f:
    actions = json.load(f)["actions"]




# Constants for registors
# we use here multiple assignment to define constants for Modbus register adress 
# 1 for X position , 2 for Y , 3 for vacuum

SETX, SETY, VAC = 1, 2, 3



# For - loop
# Enumerate () is built-in function & it gives (index,value)
# i : is the index (step number 1, 2, 3, ....)
# step : is the dict step (like - setX:55, SetY:250)
# we use for-loop & enumerate to go through all actions & print each step

for i, step in enumerate(actions, start=1):
    print("Step", i, step)



# if - statement: if + condition + block
# in : is value in sequence - True or False
# step: is dict - (vacuum in step : if this step includes a vacuum key we  write that value to registor VAC)
# Explanation : every step is small dict and contains keys for set X or set Y or vacuum
# so if the key exist we write that value to the right Modbus registor
# time.sleep : for pause the program between each action so the crane has time to move before we send next command

    if "vacuum" in step:
        client.write_register(VAC, step["vacuum"])
    if "setX" in step:
        client.write_register(SETX, step["setX"])
    if "setY" in step:
        client.write_register(SETY, step["setY"])

    time.sleep(2.5)




# Closing the connection
# client.close() : closes Modbus TCP connection so alla actions are finished

client.close()
print("Done.")
