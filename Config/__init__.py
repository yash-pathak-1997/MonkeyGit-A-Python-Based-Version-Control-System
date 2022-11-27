import json

jsonFile = open("./Config/config.json", "r")
conf_obj = json.load(jsonFile)
selfFile = open("./Config/self_conf.json", "r")
self_obj = json.load(selfFile)
UnTrackedNew = "U0"
UnTrackedMod = "U1"
UnTrackedDel = "U2"
TrackedNew = "T0"
TrackedMod = "T1"
TrackedDel = "T2"
