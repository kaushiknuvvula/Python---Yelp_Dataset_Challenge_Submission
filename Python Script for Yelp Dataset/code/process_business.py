# -*- coding: utf-8 -*-
import pandas as pd
import json

#constants 
start_line = 0  #start from the line in the original file
break_line = 0 #stop process data in the line 
file_lines = 100000000 #how many lines in the generated file. if the generated file reach the number, create another new file.
file_dir = "business\\business"
file_no = 1 #the number constituing the file name of the generated file
line_count = 0 #for calculation of number of lines in the original file
sep = ":::"

category_file = open("business\\category.json", "w")
category_file.write( "business_id" + sep + "category" )

school_file = open("business\\school.json", "w")
school_file.write( "business_id" + sep + "school" )

#read the orignial file and transform it to table    
with open("yelp_academic_dataset_business.json", "r") as f:
            
    out_f = open( file_dir + str(file_no), "w" )
    out_f.write( "business_id"+sep+"name"+sep+"full_address"+sep+"city"+sep+"state"+sep+"latitude"+sep+"longitude"+sep+"stars"+sep+"review_count")
    for line in f:
        try:
            line_count += 1
            
            if line_count == break_line: break
            
            # create a new file            
            if line_count % file_lines == 0:
                out_f.close()
                file_no += 1
                filename = file_dir + str(file_no)                
                out_f = open( filename, "w" )  
                out_f.write( "business_id"+sep+"name"+sep+"full_address"+sep+"city"+sep+"state"+sep+"latitude"+sep+"longitude"+sep+"stars"+sep+"review_count")

            # change format          
              
            business_json = json.loads(line.strip().replace("\\n", " ") )                
            business = \
                ( str(business_json["business_id"]) + sep 
                + business_json["name"].encode("utf8") + sep  
                + business_json["full_address"].encode("utf8") + sep 
                + business_json["city"].encode("utf8") + sep 
                + str(business_json["state"]) + sep 
                + str(business_json["latitude"]) + sep 
                + str(business_json["longitude"]) + sep 
                + str(business_json["stars"]) + sep 
                + str(business_json["review_count"]) )
            
            out_f.write( "\n" )
            out_f.write( business )
            
            categories = business_json["categories"]
            for cat in categories:            
                category = business_json["business_id"] + sep + cat
                category_file.write( "\n" )
                category_file.write( category )
            
            if business_json.has_key("schools"):
                schools = business_json["schools"]
                for sch in schools:            
                    school = business_json["business_id"] + sep + sch
                    category_file.write( "\n" )
                    school_file.write( school )
            
        except BaseException as e:
            print e
            print "error occured in line: " + str(line_count)  
            continue  
    #for line in f:
            
    out_f.close() 
    category_file.close()
    school_file.close()
#with open("yelp_academic_dataset_review.json") as f:    

