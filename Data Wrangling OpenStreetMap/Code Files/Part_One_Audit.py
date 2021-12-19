import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint as pp
import re


#==============================================================================
# Data Wrangling Final Project
# 
#==============================================================================
filename = 'detroit_michigan.osm'
#==============================================================================
# 
#           PART ONE   
#1.	Measuring Validity: Does the Data Conform to a Schema:
#==============================================================================


tags = {}
 
elems = {
 "Parents": 0,
 "Stand_Alone": 0
 }
 
def count_tags(filename):
           
 for _, elem in ET.iterparse(filename):
     if elem.tag in tags:
         tags[elem.tag] += 1
     else:
         tags[elem.tag] = 1
    
 return tags
 
def count_elements_with_children(filename):
 for _, elem in ET.iterparse(filename):
     checkList = elem.getchildren()
     if len(checkList) > 0:
             elems["Parents"] += 1
     else:
         elems["Stand_Alone"] += 1
    
 return elems
 
#Uncomment the lines below to get the results of the tags count 
 
#count_tags(filename)
#count_elements_with_children(filename)
#pp.pprint(tags)
#pp.pprint(elems)


#==============================================================================
#2.	Measuring Data Accuracy: Perform an Audit of the Data
#==============================================================================
#Code taken from lesson 3 of DataWrangling with MongoDB
street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()

        street_types[street_type] += 1

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        pp.pprint( "%s: %d" % (k, v) )

def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

def audit():
    for event, elem in ET.iterparse(filename):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib['v'])   
    print_sorted_dict(street_types) 

#Uncomment the lines below to get the results of the audit of the street names 
#audit()
#==============================================================================
#3.	Measuring Data Accuracy: Perform an Audit of the Data – Non US Entries 
#==============================================================================
country_codes = {}

def audit_country():
    for event, elem in ET.iterparse(filename):
       if elem.tag == "tag":
           if elem.attrib['k'] == "addr:country":
               if elem.attrib['v'] in country_codes:
                   country_codes[elem.attrib['v']] += 1
               else:
                   country_codes[elem.attrib['v']] = 1
    return country_codes

#Uncomment the lines below to get the results of the audit of countries 
#audit_country()
#pp.pprint(countries)

#==============================================================================
# 4.	Measuring Data Accuracy: Perform an Audit of the Data – Erroneous Postal Codes
#==============================================================================
postcodes = {}
  
def audit_postcodes():
     for event, elem in ET.iterparse(filename):
         if elem.tag == "tag":
             if elem.attrib['k'] == "addr:postcode":
                 if elem.attrib['v'] in postcodes:
                     postcodes[elem.attrib['v']] += 1
                 else:
                     postcodes[elem.attrib['v']] = 1
     pp.pprint(postcodes)
     
#Uncomment the lines below to get the results of the audit of the postal codes   
#audit_postcodes()
#pp.pprint(postcodes)

#==============================================================================
#5. Measuring Data Accuracy: Perform an Audit of the Data – Erroneous  City Values
#============================================================================== 

city = {}
  
def audit_city():
     for event, elem in ET.iterparse(filename):
         if elem.tag == "tag":
             if elem.attrib['k'] == "addr:city":
                 if elem.attrib['v'] in city:
                     city[elem.attrib['v']] += 1
                 else:
                     city[elem.attrib['v']] = 1
     pp.pprint(city)
#Uncomment the lines below to get the results of the audit of the city data     
#audit_city()
#pp.pprint(city)