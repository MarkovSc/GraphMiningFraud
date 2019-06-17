import json

with open("example.txt") as file:
    edges = [line for line in file]
    firstNodeMax = max([int(i.strip().split(' ')[0]) for i in edges])
    secondNodeMax = max([int(i.strip().split(' ')[1]) for i in edges])

print(firstNodeMax)
print(secondNodeMax)

nodes_list = [{"name":str(i)} for i in range(firstNodeMax + firstNodeMax + 2)]
links_list = [{"source":int(i.split(' ')[0]) , "target": int(i.strip().split(' ')[1]) + firstNodeMax +1 } for i in edges]

json_prep = {"nodes":nodes_list, "links":links_list}


json_dump = json.dumps(json_prep, indent=1, sort_keys=True)
print(json_dump)

filename_out = 'line.json'
json_out = open(filename_out,'w')
json_out.write(json_dump)
json_out.close()
