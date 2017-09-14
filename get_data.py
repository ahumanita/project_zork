#!/usr/bin/python3
# coding=UTF-8

###
# this file is used, to get access to the database 'zork' and
# export the data.
###

import records
import os #compile tex doc

db = records.Database(open("connection.txt","r").read().split()[0])

def get_number_of_areas() :
    number_a = db.query("SELECT max(area.id) FROM area")[0]["max"]
    return number_a

def write_tex_header(fln) :
    file = open(fln, "w")
    number_a = get_number_of_areas()
        
    header = r"""% !TEX program = pdflatex
% !TEX encoding = UTF-8 Unicode
% !TEX spellcheck = en

\documentclass{standalone}""" + r"""\usepackage{tikz}
\usetikzlibrary{trees,arrows,positioning,shapes.multipart}

"""
    header += r"""\begin{document}
    \begin{tikzpicture}[node distance = 2cm, all/.style = {shape = rectangle, draw, align=center, rectangle split, rectangle split parts = 3}]""" + "\n"
    
    file.write(header)
    print("header written to tex-file")
    file.close()
    
def close_document(fln) :
    file = open(fln, "a")
    closing = r"""    \end{tikzpicture}
\end{document}"""
    file.write(closing)
    print("closing written to tex-file")
    file.close()
    
def compile_tex_doc(fln) :
    compile = os.popen("pdflatex %s" %(fln))
    print("compiled tex-file")

def direction_to_tikz(word) :
    res = ""
    if word == "N" :
        res = "above = of"
    if word == "S" :
        res = "below = of"
    if word == "W" :
        res = "left = of"
    if word == "E" :
        res = "right = of"
    if word == "NE" :
        res = "above right = of"
    if word == "NW" :
        res = "above left = of"
    if word == "SW" :
        res = "below left = of"
    if word == "SE" :
        res = "below right = of"
    if word == "U" :
        res = "above = of"
    if word == "D" :
        res = "below = of"
    if word == "OUT" :
        res = "below = of"
    return res

#pl: place, num_i: number of items, it#?: item, cr: creatures
def get_areas_with_items_and_people() :
    number_a = get_number_of_areas()
    i = 1
    area_list = []
    #collect information for tikz-field
    while i <= number_a :
        act_area = {}
        place = db.query("SELECT area.name, area.id FROM area WHERE area.id = :id", id=i)
        act_area["pl"] = place[0]["name"]
        act_area["pl_id"] = place[0]["id"]
        
        #find items to actual area
        number_i = db.query("SELECT count(*) FROM item WHERE item.in_room = :room_id", room_id = place[0]["id"])[0]["count"]
        act_area["num_i"] = number_i
        
        item = db.query("SELECT item.name FROM item WHERE item.in_room = :room_id", room_id = place[0]["id"])
        j = 0
        if number_i != 0 :
            while j < number_i :
                it_name = item[j]["name"]
                act_area["it%i" %(j)] = it_name
                j += 1
        
        #find creatures to actual area
        #TODO!!! auch datenbank ändern!
        
        area_list.append(act_area)
        
        i += 1
    return area_list
    
def write_areas_to_tikz(area_list, fln) :
    file = open(fln, "a")
    number = len(area_list)
    
    #first node
    node1 = r"\node[all] (1) {" + "%s " %(area_list[0]["pl"]) + r"\nodepart{second} "
    for j in range(0,area_list[0]["num_i"]-1) :
        node1 += "%s, " %(area_list[0]["it%i" %(j)])
    node1 += "%s};" %(area_list[0]["it%i" %(area_list[0]["num_i"]-1)])
    print(node1)
    file.write(node1)
    
    #other nodes
    i = 1
    while i < len(area_list) :
        directions_to = db.query("""SELECT path.start, path.direction, path.destination
            FROM path, area
            WHERE path.destination = :area_id
            AND path.start = area.id
            AND area.id < :area_id""", area_id = area_list[i]["pl_id"])
        directions_from = db.query("""SELECT path.start, path.direction, path.destination
            FROM path, area
            WHERE path.start = :area_id
            AND path.destination = area.id
            AND area.id < :area_id""", area_id = area_list[i]["pl_id"])
        
        directions_to.all()
        directions_from.all()
        
        k = 0
        neighboors = []
        node = r"\node[all"
        while k < len(directions_to) :
            if directions_to[k]["start"] not in neighboors :
                direc = directions_to[k]["direction"]
                tikz_direc = direction_to_tikz(direc)
                node += ", %s " %(tikz_direc) + "%i" %(directions_to[k]["start"])
                neighboors.append(directions_to[k]["start"])
            else :
                pass
            k += 1
        
        m = 0
        while m < len(directions_from) :
            if directions_from[m]["destination"] not in neighboors :
                direc = directions_from[m]["direction"]
                tikz_direc = direction_to_tikz(direc)
                node += ", %s " %(tikz_direc) + "%i" %(directions_from[m]["destination"])
                neighboors.append(directions_from[m]["destination"])
            else :
                pass
            m += 1
        node += "]"
        node += " (%i)" %(area_list[i]["pl_id"])
        node += r" {" + "%s" %(area_list[i]["pl"]) + r"\nodepart{second} "
        
        l = 0
        while l < area_list[i]["num_i"]-1 :
            node += "%s, " %(area_list[i]["it%i" %(l)])
            l += 1
        if area_list[i]["num_i"] > 0 :
            node += "%s" %(area_list[i]["it%i" %(area_list[i]["num_i"]-1)])
                
        node += "}; \n"
        file.write(node)
        print(node)
        i += 1
    file.close()
    print("nodes written to file")
    
# def get_places() :
# for item in directions_to :
            
# def get_items() :
# 
# def get_people() :
# 
# def get_paths() :
    
if __name__ == '__main__':
    fln = "graph.tex"
    area_list = []
    area_list = get_areas_with_items_and_people()
    write_tex_header(fln)
    write_areas_to_tikz(area_list, fln)
    close_document(fln)
    compile_tex_doc(fln)