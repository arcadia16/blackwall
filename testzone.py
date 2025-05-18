my_dict = {"ipv4": "agent_id"}
for key in my_dict.keys():
    if my_dict.get(key) == "agent_id":
        print(key)
