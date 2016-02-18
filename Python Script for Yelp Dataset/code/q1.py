# -*- coding: utf-8 -*-
import pandas as pd, numpy as np
from scipy import stats
import matplotlib.pyplot as plt

plt.style.use('ggplot')

#read data
reviews = pd.read_table( "reviews\\review_all", sep="霽" )
cats =  pd.read_table( "business\\category.json", sep=":::" )
rev_cat = pd.merge( reviews, cats )

#find top 10 popular categories
rev_by_cat = rev_cat.groupby( "category" )
rev_cat_count = rev_by_cat["stars"].count()
rev_cat_count.sort(ascending=False)
top_10_cat = rev_cat_count.index.values[:10]

#find seasonal trend of the top 10 categories
top_10_cat_rev = rev_cat[ rev_cat["category"].isin( top_10_cat ) ]
top_10_cat_rev_by_season = top_10_cat_rev.groupby( ["category", "season"] )
top_10_cat_rev_by_season_count = top_10_cat_rev_by_season["stars"].count().unstack()
top_10_cat_rev_by_season_count[["summer","autumn","winter","spring"]].plot( kind="bar" )
plt.xlabel('category')
plt.ylabel('review count')
plt.title('Seasonal trend of top 10 popular categories')
#top_10_cat_rev_by_season_count.to_csv("result.csv", header=None)

#find the top 10 categoies with greatest seasonal variation using difference between z-scores
def zscore_diff( row ):
    zscores = stats.zscore(row)
    return np.max(zscores) - np.min(zscores)

rev_cat_count = rev_cat.groupby(["category","season"])["stars"].size()
rev_cat_count = rev_cat_count.unstack()
rev_cat_count["z_score_diff"] = rev_cat_count.apply(zscore_diff,axis=1) #rev_cat_count.std()
rev_cat_count["count"] = rev_cat_count[["summer","autumn","winter","spring"]].apply(sum,axis=1)
rev_cat_count = rev_cat_count[ rev_cat_count["count"] > 5000 ]
rev_cat_count.sort( "z_score_diff" )
top_10_var_cat = rev_cat_count.tail( 10 )
#top_10_var_cat[["summer","autumn","winter","spring"]].plot( kind="bar" )
plt.xlabel('category')
plt.ylabel('review count')
plt.title('top 10 categoies with greatest seasonal variation')

fig, axes = plt.subplots(nrows=2, ncols=5)
for i in range(0,10):
    axes[i/5,i%5].set_title( top_10_var_cat.index.values[i] )
    top_10_var_cat.ix[i][["summer","autumn","winter","spring"]].plot( kind="barh", ax=axes[i/5,i%5] )

plt.show()



