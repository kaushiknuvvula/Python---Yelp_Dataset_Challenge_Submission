# -*- coding: utf-8 -*-
import pandas as pd
import json

#constants 
start_line = 0  #start from the line in the original file
break_line = 0 #stop process data in the line 
file_lines = 1000000000 #how many lines in the generated file. if the generated file reach the number, create another new file.
file_dir = "reviews\\review"
file_no = 1 #the number constituing the file name of the generated file
line_count = 0 #for calculation of number of lines in the original file
sep = "霽"

#read the orignial file and transform it to table    
with open("yelp_academic_dataset_review.json") as f:
            
    #out_f = open( file_dir + str(file_no), "w" )
    out_f = open( file_dir + "_all", "w" )
    out_f.write( "business_id"+sep+"user_id"+sep+"stars"+sep+"text"+sep+"year"+sep+"month"+sep+"day"+sep+"season"+sep+"useful" )
    for line in f:
        try:
            line_count += 1
            
            if line_count == break_line: break
            
            # create a new file                        
            if line_count % file_lines == 0:
                print file_no
                out_f.close()
                file_no += 1
                filename = file_dir + str(file_no)                
                out_f = open( filename, "w" )  
                out_f.write( "business_id"+sep+"user_id"+sep+"stars"+sep+"text"+sep+"year"+sep+"month"+sep+"day"+sep+"season"+sep+"useful" )

            # change format            
            review_json = json.loads(line.strip())   
            
            date = review_json["date"].split("-")
            season = 0
            month = int(date[1])
            if month >= 3 and month <= 5:
                season = "spring"
            elif month >= 6 and month <= 8:
                season = "summer"
            elif month >= 9 and month <= 11:
                season = "autumn"
            elif month == 12 or month == 1 or month == 2:
                season = "winter"
                
            if not( review_json.has_key("business_id") and review_json.has_key("user_id") \
                    and review_json.has_key("stars") and review_json.has_key("text") \
                    and review_json.has_key("votes") and review_json.has_key("date") ):
                    continue
                
            review = \
                ( str(review_json["business_id"]) + sep 
                + str(review_json["user_id"]) + sep  
                + str(review_json["stars"]) + sep 
                + (review_json["text"]).replace("\n","\\n").encode('utf8') + sep 
                + str(date[0]) + sep 
                + str(date[1]) + sep 
                + str(date[2]) + sep
                + str(season) + sep
                + str(review_json["votes"]["useful"]) )
            
            out_f.write( "\n" )
            out_f.write( review )
        except BaseException as e:
            print e
            print "error occured in line: " + str(line_count)  
            continue  
    #for line in f:
            
    out_f.close() 
#with open("yelp_academic_dataset_review.json") as f:    

