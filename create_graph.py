from graphviz import Digraph
import matplotlib.pyplot as plt
import records

db = records.Database(open("connection.txt","r").read().split()[0])

area_symbols = {"light": "L","directions_complete": "X" ,"items": "I","treasure": "T", "information" : "Inf", "creature": "M"}
path_symbols = {}

def get_number_of_areas() :
    number_a = db.query("SELECT max(area.id) FROM area")[0]["max"]
    return number_a
    
def get_number_of_paths() :
    number_p = db.query("SELECT max(path.id) FROM path")[0]["max"]
    return number_p

#pl: place, num_i: number of items, it#?: item, cr: creatures
def get_areas() :
    number_a = get_number_of_areas()
    i = 1
    area_list = []
    #collect information for tikz-field
    while i <= number_a :
        act_area = {}
        place = db.query("""SELECT area.name, area.id, area.light, area.directions_complete, area.items, 
        				area.treasure, area.information, area.creatures FROM area WHERE area.id = :id""",
        				id=i)
       	# TODO: kann man bestimmt in Schleife packen!

        act_area["name"] = place[0]["name"]
        act_area["id"] = place[0]["id"]
        
        #light
        act_area["light"] = place[0]["light"]
        #directions_complete
        act_area["directions_complete"] = place[0]["directions_complete"]
        #items
        act_area["items"] = place[0]["items"]
        #treasure
        act_area["treasure"] = place[0]["treasure"]
        #information
        act_area["information"] = place[0]["information"]
        #creatures
        act_area["creatures"] = place[0]["creatures"]
       
        area_list.append(act_area)
        
        i += 1
    return area_list

#p_id: path id, st: start, des: destination, num_d: number of directions, d#: direction, col: color
#TODO keys anzeigen (ort)
def get_paths() :
	number_p = get_number_of_paths()
	path_list = []

	i = 1
	while i <= number_p :
		act_path = {}
		color = ""
		path = db.query("""SELECT path.id, path.start, path.destination, path.direction,
			path.usable, path.information, path.waterpath, path.notes
			FROM path
			WHERE path.id = :p_id
			AND path.destination IS NOT NULL"""
			, p_id = i)
		path.all()

		#check if destination is null or not
		if not path :
			path = db.query("""SELECT  path.id, path.start, path.destination, path.direction,
				path.usable, path.information, path.waterpath, path.notes FROM path WHERE path.id = :p_id"""
				, p_id = i)
			act_path["destination"] = "NON%d" %(i)
			graph.node("NON%d" %(i), "???")
		else :
			act_path["destination"] = path[0]["destination"]

		act_path["id"] = path[0]["id"]
		act_path["start"] = path[0]["start"]
		act_path["direction"] = path[0]["direction"]
		act_path["usable"] = path[0]["usable"]
		act_path["information"] = path[0]["information"]
		act_path["waterpath"] = path[0]["waterpath"]
		act_path["notes"] = path[0]["notes"]

		if not path[0]["waterpath"] :
			if not path[0]["usable"] :
				color = "#ff5959"
			else :
				color = "#000000"
		else :
			if not path[0]["usable"] :
				color = "#c246c4"
			else :
				color = "#3589ff"

		act_path["color"] = color
		path_list.append(act_path)
		i += 1
	return path_list

def write_areas_to_graph(area_list,graph) :
	total = len(area_list)
	for area in area_list :
		if not area["light"]:
			color = "#9ca0a8"
		else :
			color = "#f4f142"
		info = ""
		if area["information"] == True :
			info += "ℹ️"
		if area["treasure"] == True :
			info += "💎"
		if area["creatures"] == True :
			info += "🐉"
		# if area["items"] == True :
		# 	info += "🎁"
		if area["directions_complete"] == True :
			info += "✅"
		if area["items"] == True :
			icons = db.query("""SELECT icon
				FROM item
				WHERE in_room = :a_id
				""", a_id = int(area["id"]))
			try :
				info += "".join([icon["icon"] for icon in icons])
			except :
				pass

		graph.node(str(area["id"]), str(area["id"]) + " " + str(area["name"] + "\n" + info),color=color)

def write_paths_to_graph(path_list,graph) :
	total = len(path_list)
	for path in path_list :
		info = ""
		print(path["notes"])
		if path["notes"] is not None :
			info += "ℹ️"
		graph.edge(str(path["start"]),str(path["destination"]),label=str(path["direction"]) + info,color=path["color"])

if __name__ == "__main__" :
	fln = "graph.svg"
	graph = Digraph(format="svg")
	graph.graph_attr["rankdir"] = "LR"

	area_list = get_areas()
	path_list = get_paths()
	write_areas_to_graph(area_list,graph)
	write_paths_to_graph(path_list,graph)

	graph.render("graph.gv",view=True)