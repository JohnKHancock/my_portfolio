import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint as pp
import re
import codecs
import json

#==============================================================================
# 
#           Part Two – Clean, Shape, and Load the Data 
##==============================================================================


filename = 'detroit_michigan.osm'

#==============================================================================
# 6.	Cleaning and Shaping the Data
#==============================================================================


CREATED = [ "version", "changeset", "timestamp", "user", "uid"]               
element_Id_err_set = set()   

def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

       
def is_parent_elem(elem):
    checkList = elem.getchildren()
    if len(checkList) >= 1:
        return True
    else:        
        return False

def is_valid_postcode(postcode):
    strPostCode = str(postcode)
    if strPostCode is None:
        return False
    elif strPostCode.startswith("MI"):
        return True
    elif not strPostCode.startswith("4"):
        return False
    else:
        cleaned_postcode = clean_postcodes(strPostCode)
        if cleaned_postcode not in range(48201,48288):
            return False
        else:
            return True
        
        
def check_element_id(elem):
    for child in elem:
        for tag in child.iter("tag"):
            if "city" in tag.attrib['k']:
                updated_city = clean_city(tag.attrib['v'])
                if updated_city != "Detroit" or updated_city is None:
                    element_Id_err_set.add(elem.get("id"))
            elif "postcode" in tag.attrib['k']:
                  if not is_valid_postcode(tag.attrib['v']):                   
                      element_Id_err_set.add(elem.get("id"))
            elif "country" in tag.attrib['k']:
                     if tag.attrib['v'] != "US":
                        element_Id_err_set.add(elem.get("id"))
            else:
                break
            
            
        
def clean_city(city):
    if city is not None and city.startswith("Detroit") :
         return "Detroit"
    elif city is None:
         return None

def clean_postcodes(postal_code):
 
     strPostCode = str(postal_code)
     
     if strPostCode.startswith("MI"):
         cleaned_postcode = strPostCode.split(' ')
         return int(cleaned_postcode[1])
                     
     elif len(strPostCode) > 5:
         return int(strPostCode[:5])
     
     else:
         return int(strPostCode)




def audit_street_name(street_name):
       temp = street_name.split(' ')
       temp[-1] = clean_abbreviations(temp[-1])
       clean_name = ' '.join(temp)
       return clean_name        
        
def audit():
       for event, elem in ET.iterparse(filename):
           if is_street_name(elem):
               audit_street_name(elem.attrib['v'])   
     
def clean_abbreviations(abbr):
       
       full_names = {
               "ave":"Avenue",
               "Ave":"Avenue",
               "Ave.":"Avenue",
               "Blvd":"Boulevard",
               "Blvd.":"Boulevard",
               "Ct":"Court",
               "Dr": "Drive",
               "DR":"Drive",
               "Dr.": "Drive",
               "Hwy": "Highway",
               "Pkwy":"Parkway",
               "Pl":"Place",
               "Pl.":"Place",
               "Rd":"Road",
               "Rd.":"Road",
               "road":"Road",
               "St":"Street",
               "St.":"Street",
               "way":"Way"              
       
       }
       
       if abbr in full_names:    
           return full_names[abbr]
       else:
           return abbr
      
   

   

def shape_stand_alone(elem):
    load_node = {}
    created = {}
    pos = []
    
    
    
    if elem.tag == "node" or elem.tag == "way" or elem.tag == "relation":
               load_node["type"] = elem.tag
               for tag in elem.iter(elem.tag):
                  keys = tag.keys()
                  for k in keys:
                      
                      if k in CREATED:
                          created[k] = tag.attrib[k]                           
                      elif k == "lat":
                          pos.append(float(tag.attrib[k]))
                      elif k == "lon":
                          pos.append(float(tag.attrib[k]))
                      else:
                           load_node[k] = tag.attrib[k]
               
               load_node["created"] = created
                           
               if len(pos) > 0:
                   load_node["pos"] = sorted(pos, reverse=True)
    return load_node

def shape_parent_element(elem):
        
    address = {}
    node_refs = []
    other_info = {}
    load_node = {}
    
    check_element_id(elem)
    if elem.get("id") not in element_Id_err_set:
    
        load_node = shape_stand_alone(elem)
              
        for child in elem:            
                     for child_elem in child.iter(child.tag):
                         
                         if child_elem.tag == 'nd':
                             node_refs.append(child_elem.attrib["ref"])
                             
                         elif child_elem.tag == 'tag':
                             
                             if child_elem.attrib["k"].startswith("addr"):
                                 addr = child_elem.attrib["k"].split(':')
                                 address[addr[1]] = child_elem.attrib["v"]                        
                             
                             elif ":" in child_elem.attrib["k"]:
                                 tag_name = child_elem.attrib["k"].split(':')
                                 other_info[tag_name[1]] = child_elem.attrib["v"]
                             
                             else:
                                 load_node[child_elem.attrib["k"]] = child_elem.attrib["v"]
        try:       
           
            if "city" in address:
                address["city"] = clean_city(address["city"])
            if "street" in address:
                address["street"] = audit_street_name(address["street"])
            if "postcode" in address:
                address["postcode"] = clean_postcodes(address["postcode"])                
            if len(node_refs) > 0:
               load_node["node_refs"] = node_refs
            if len(address) > 0:
               load_node["address"] = address
            if len(other_info) > 0:
               load_node["other_info"] = other_info
        except:
            pp.pprint(elem.get("id"))    
            
    return load_node
    
   

#==============================================================================
# 7. load the element               
#==============================================================================

#Code based on the code from the Data Wrangling course
def process_map(file_in, pretty = False):
       file_out = "{0}.json".format(file_in)
       data = []
       with codecs.open(file_out, "w") as fo:
           for _, element in ET.iterparse(file_in):
               if not is_parent_elem(element):
                   el = shape_stand_alone(element)
                   
                   if el:
                       data.append(el)
                       if pretty:
                           fo.write(json.dumps(el, indent=2)+"\n")
                       else:
                           fo.write(json.dumps(el) + "\n")
               else:
                   el = shape_parent_element(element)
                   if el:
                     data.append(el)
                     if pretty:
                           fo.write(json.dumps(el, indent=2)+"\n")
                     else:
                           fo.write(json.dumps(el) + "\n")
                
       return data
   
data = process_map(filename, False)
pp.pprint(element_Id_err_set)
  

