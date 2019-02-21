import records
import ast # convert string to dict

db = records.Database(open("connection.txt","r").read().split()[0])

def add_area(values_in) :
	if "name" not in values_in.keys() or values_in["name"] == "" :
		raise ValueError("ERROR: a name is needed to add an area!")
	values = {"id": int(db.query("SELECT MAX(id)+1 FROM area")[0]["?column?"]), "name": "", "light": False, "directions_complete": True
		, "descr": "", "items": False, "treasure": True, "information": False, "creatures": False}
	for key in values_in.keys() :
		if key in values.keys() :
			values[key] = values_in[key] 
	db.query("""INSERT INTO area (id,name,light,directions_complete,descr,items,treasure,information,creatures)
		VALUES (:id,:name,:light,:directions_complete,:descr,:items,:treasure,:information,:creatures)"""
		, id=values["id"], name=values["name"], light=values["light"], directions_complete=values["directions_complete"], descr=values["descr"]
		, items=values["items"], treasure=values["treasure"], information=values["information"], creatures=values["creatures"])

def update_area(values_in) :
	if "id" not in values_in.keys() or values_in["id"] == "" :
		raise ValueError("ERROR: an id is needed to update an area!")
	keys = list(values_in.keys())
	columns = ["%s, " %(keys[i]) for i in range(len(keys)-1) if keys[i] != "id"]
	values = ["%s, " %(str(values_in[keys[i]])) for i in range(len(keys)-1) if keys[i] != "id"]
	columns.append("%s" %(keys[len(keys)-1]))
	values.append("%s" %(str(values_in[keys[len(keys)-1]])))
	for i in range(len(columns)) :	
		db.query(f"""UPDATE area
			SET {columns[i]} = :value
			WHERE id = :id"""
			, value=values[i], id=int(values_in["id"]))

def delete_area(values_in) :
	if "id" not in values_in.keys() or values_in["id"] == "" :
		raise ValueError("ERROR: an id is needed to delete an area!")
	db.query("""DELETE FROM area
		WHERE id = :id"""
		, id=int(values_in["id"]))

def get_area(values_in) :
	if "id" not in values_in.keys() or values_in["id"] == "" :
		raise ValueError("ERROR: an id is needed to print an area!")
	print(db.query("""SELECT * FROM area WHERE id = :id""", id=values_in["id"])[0])

if __name__ == "__main__" :
	command = input("Enter command; a python dictionary:\n")
	print(command.split("; "))
	values_in = ast.literal_eval(str(command).split("; ")[1])
	command = str(command).split("; ")[0]

	if command.split("_")[1] == "area" :
		# data types
		if "id" in values_in.keys() :
			values_in["id"] = int(values_in["id"])
		if "light" in values_in.keys() :
			values_in["light"] = (True==values_in["light"])
		if "directions_complete" in values_in.keys() :
			values_in["directions_complete"] = (True==values_in["directions_complete"])
		if "items" in values_in.keys() :
			values_in["items"] = (True==values_in["items"])
		if "treasure" in values_in.keys() :
			values_in["treasure"] = (True==values_in["items"])
		if "information" in values_in.keys() :
			values_in["information"] = (True==values_in["information"])
		if "creatures" in values_in.keys() :
			values_in["creatures"] = (True==values_in["creatures"])
		# function call
		if command == "add_area" :
			add_area(values_in)
		if command == "update_area" :
			update_area(values_in)
		if command == "delete_area" :
			delete_area(values_in)
		if command == "get_area" :
			get_area(values_in)