#IMPORTS
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer

def social_media_score(df):
    ''' 
    This function scores the social media performance of a website
    
    Parameters
    ----------
    df: A .csv file with TKF's website scrapping results
    
    Output
    ------
    Returns a pandas dataframe called 'results_media' 
    -> It countains the site URL, yt_score, has_social, cluster_score, and the final social_score
    '''
    
    #1. YOUTUBE
    # Create the Youtube score based on quantile of views, websites with 'None' are not scored
    df['yt_score'] = np.where(df['yt_view']<= df['yt_view'].quantile(q=0.25),0.25,
                                            np.where(df['yt_view']<= df['yt_view'].quantile(q=0.5),0.5,
                                                    np.where(df['yt_view']<= df['yt_view'].quantile(q=0.75),0.75,
                                                            np.where(df['yt_view']<= df['yt_view'].quantile(q=1),1,0))))
    df['has_social'] = np.where(df['SocialTraffic']<= 0,0,1)

    #2. INITIALIZE OUTPUT DF 
    results_media = df[['Site','yt_score','has_social']]

    #Create the df with all relevant media KPIs
    mediadf = df[['MonthlyTraffic', 'SocialTraffic', 'Social_1_traffic', 'Social_2_traffic', 'Social_3_traffic', 'fb_likes',
                  'fb_follows', 'fb_checkins', 'fb_shares', 'fb_comments', 'fb_reactions', 'insta_posts', 'insta_folllowers',
                  'insta_following', 'pins']]
    # Delete all the strings (No URL), change them into NaNs 
    mediadf = mediadf._convert(numeric=True)

    # Scaling the features to the website size (MonthlyTraffic)
    scaler = mediadf['MonthlyTraffic']
    for i in mediadf.columns:
        mediadf[i] = mediadf[i]/ scaler
    mediadf.drop(['MonthlyTraffic'],axis=1, inplace =True) # We can now drop monthlytraffic as it is not a social media variable
    
    # Dropping the highly correlated columns
    mediadf = mediadf.drop(['fb_likes','fb_comments','SocialTraffic','fb_reactions'], axis=1)   

    #Impute missing values as 0 and scale the KPIs
    #Imputing means instead of NaNs (Kmeans doesn't work with NaN)
    imp_mean = SimpleImputer(missing_values=np.nan, strategy='constant', fill_value=0)
    mediadf_imputed = imp_mean.fit_transform(mediadf)

    #Scaling the data
    scaler = MinMaxScaler()
    scaled = scaler.fit(mediadf_imputed)
    X = scaler.transform(mediadf_imputed)

    #Run the kmeans
    km = KMeans(
        n_clusters=5, init='k-means++',
        n_init=10, max_iter=300, 
        tol=1e-04, random_state=0
    )
    y_km = km.fit_predict(X)

    #Create centroids dataframe to rank them
    centroids = pd.DataFrame(km.cluster_centers_)

    # Create weighted sum to give more importance to social 1,2,3
    centroids.columns = mediadf.columns.to_list()
    centroids['weighted_sum'] = 0.5*centroids['Social_1_traffic']+0.2*centroids['Social_2_traffic']+0.1*centroids['Social_3_traffic']+ 0.2/7*(centroids['fb_follows']+centroids['fb_checkins']+centroids['fb_shares']+centroids['insta_posts']+centroids['insta_folllowers']+centroids['insta_following']+centroids['pins'])
    centroids['cluster'] = centroids.index

    # Create the score from 0-10 based on the rank of weighted sum (5 clusters, x2 to get a /10 score)
    centroids['score'] = centroids['weighted_sum'].rank()/5

    #PROVISION FOR CHANGING CLUSTER RANK - CREATE A DICT WITH EACH CLUSTER/RANK PAIR EVERY TIME THE FUNCTION RUNS
    #Add the Cluster score to the result df
    score_dict = {}

    for i in range (0,len(centroids)):
        score_dict[centroids.loc[i,'cluster']] = centroids.loc[i,'score']
    cluster_score = []

    for i in y_km:
        cluster_score.append(score_dict[i])

    #Add cluster score as a column for our result df
    results_media['cluster_score']= cluster_score

    # Update the Cluster score based on 'has_social': if no social media, set score to 0
    results_media['cluster_score'] = np.where( results_media['has_social']==0,0,results_media['cluster_score'])

    # Combine the scores (YT is a max bonus of 10%, not penalised if no Youtube channel)
    results_media['social_score'] =  results_media['cluster_score']+ results_media['yt_score']/10

    # Cap the score at 10
    results_media['social_score'] = np.where( results_media['social_score']>1,1,  results_media['social_score'])
    
    results_media_output = results_media[['Site','social_score']]
    
    return results_media_output

