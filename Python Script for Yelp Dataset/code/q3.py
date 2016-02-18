# -*- coding: utf-8 -*-
import pandas as pd, numpy as np
from scipy import stats
import matplotlib.pyplot as plt

plt.style.use('ggplot')

# constants
start_month = "2011-11"
end_month = "2014-12"
month_limit = 38 #should have at least ... months worth of reviews
moving_avg_period = 3
city_focused = "Las Vegas" # e.g "Las Vegas". empty string => all cities
city_excluded = "" # e.g "Las Vegas". empty string => do not exclude any cities

def review_trend( df ):
    """
    df: DataFrame( index=business_id, names=["time_index", "stars"] )
    return: DataFrame( names=["mean", "sufficient_reviews", "rolling_mean", "diff"] )
    """
    result_df = pd.DataFrame( df["stars"].resample( "M", kind="period", how="mean" ) )
    result_df.columns = ["mean"]

    # check whether a business has reviews in every month
    month_count = sum( result_df["mean"].isnull() == False )    
    result_df["sufficient_reviews"] = (month_count >= month_limit)
    
    # calculate mean, moving average and difference between the two
    result_df["rolling_mean"] = pd.rolling_mean( result_df["mean"], moving_avg_period )
    result_df["diff"] = result_df["mean"] - result_df["rolling_mean"]
    return result_df.ix[2:] # exclude the first two months ( NaN after rolling mean )

        
def plot_trend( trend_df, business_id, busi_name, axis, category_mean, ylim ):
    result_df = pd.DataFrame( trend_df.ix[business_id][["mean","rolling_mean"]] )
    result_df["category_mean"] = category_mean
    result_df.columns = ["rating mean", "moving mean", "category mean"] #legends in plot
    
    result_df.plot( ax=axis, ylim=ylim )    
    axis.set_xlabel('Time')
    axis.set_ylabel('Rating')
    axis.set_title( busi_name )
    
def trend_slope( row ):
    trend = np.polyfit( row.index.values, row.values, 1 )
    return trend[0]

# read files        
# csv file column names: "index", "business_id", "user_id", "stars", "year", "month", "day", "season", "useful"
reviews = pd.read_csv( "reviews\\rev_no_com.csv", header=None, \
                        names = ["index", "business_id", "user_id", "stars", "year", "month", "day", "season", "useful"], \
                        parse_dates={"time_index":["year", "month", "day"]})

if len(city_focused) != 0:
    businesses = pd.read_csv( "business\\business1", sep=":::" )
    businesses = businesses[ businesses["city"] == city_focused ]
    reviews = reviews[ reviews["business_id"].isin( businesses["business_id"] ) ]

if len(city_excluded) != 0:
    businesses = pd.read_csv( "business\\business1", sep=":::" )
    businesses = businesses[ businesses["city"] != city_excluded ]
    reviews = reviews[ reviews["business_id"].isin( businesses["business_id"] ) ]

# get reivews in given period
reviews = reviews[ (reviews["time_index"] >= start_month) & (reviews["time_index"] <= end_month) ]

# add category information to reviews
cats =  pd.read_table( "business\\category.json", sep=":::" )
reviews = pd.merge( reviews, cats, how="left" )

# get reviews in Restaurants category
res_reviews = reviews[ reviews["category"] == "Restaurants" ]

# create review time series
res_reviews.index = res_reviews["time_index"]

# get businesses which have reviews in every month
res_reviews_trend = res_reviews.groupby( ["business_id"] ).apply( review_trend )
res_reviews_trend = pd.DataFrame.copy( res_reviews_trend[ res_reviews_trend["sufficient_reviews"] ] )

# compare trends with other stores in the same category
res_reviews_trend["diff_z"] = res_reviews_trend["diff"].unstack().apply( stats.zscore, axis=0 ).stack()

# trendline
trend2 = res_reviews_trend["mean"].unstack().apply( trend_slope, axis=1 )
trend2.sort()
better_bus_ids = trend2.tail(4).index.values
worse_bus_ids = trend2.head(4).index.values


"""
res_reviews_trend (dataframe):
------------------------------------------------------------------------------------
                         |  mean | sufficient_reviews | rolling_mean | diff | diff_z
------------------------------------------------------------------------------------                         
business_id | time_index |

------------------------------------------------------------------------------------
mean: mean of ratings of a business in a given period
sufficient_reviews: whether the business has reviews in every month
rolling_mean: rolling mean of ratings of a business in a given period (start from two months before, which are not included in this result)
diff: mean - rolling_mean
diff_z: the z-score of diff. The population is all diffs in the same period (time_index)
"""

"""
questions:
1. The 4 business with the most steady ratings compare to other stores in the same category
2. The 4 business with the most dramatic ratings compare to other stores in the same category    
"""

# find out the restaurants generaly close to or away from category trend.
abs_z_sum = res_reviews_trend["diff_z"].unstack().apply( lambda row: np.abs(row).sum() ,axis=1 )
abs_z_sum.sort()
steady_busi_ids = abs_z_sum.tail(4).index.values
dramatic_busi_ids = abs_z_sum.head(4).index.values


# look up business name
business = pd.read_table( "business\\business1", sep=":::" )
business.index = business["business_id"]

# calculate category mean, a benchmark shown on plot
category_mean = res_reviews["stars"].resample("M", how="mean", kind="period")

# plot
result_list = [ better_bus_ids, worse_bus_ids, steady_busi_ids, dramatic_busi_ids ]

for result in result_list:
    fig, axes = plt.subplots(nrows=2, ncols=2)
    i = 0
    for busi_id in result:
        bus = business.ix[busi_id]
        title = bus["name"] + " (" + bus["city"] + ", " + bus["state"] + ")"
        plot_trend( res_reviews_trend, busi_id, title, axes[i/2,i%2], category_mean, (1,5) )
        i += 1

plt.show()

#def period_business_size (ooo):
#    return ooo.unique().size
