# -*- coding: utf-8 -*-
import pandas as pd

reviews = pd.read_table( "reviews\\review_all", sep="霽" )
#"business_id"+sep+"user_id"+sep+"stars"+sep+"text"+sep+"year"+sep+"month"+sep+"day"+sep+"season"+sep+"useful"

#find stores with greatest variation of stars using std
rev_std = reviews.groupby("business_id")["stars"].std()
rev_count = reviews.groupby("business_id")["stars"].size()

rev_df = pd.DataFrame( [rev_std, rev_count] )
rev_df = rev_df.transpose()
rev_df.columns = ["std","count"]
rev_df_100 = rev_df[ rev_df["count"] > 100 ]
result = rev_df_100.sort( "std" ).tail(10)

#merge review and business
business = pd.read_table( "business\\business1", sep=":::" )
rev_busi = pd.merge(result, business, how='inner', right_on="business_id", left_index=True)
print rev_busi[["name","std","count","city","state","full_address"]]