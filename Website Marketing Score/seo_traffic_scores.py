
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def seo_traffic_scores(df):
    ''' 
    This function scores the SEO and traffic performance of a website
    
    Parameters
    ----------
    df: A .csv file with TKF's website scrapping results
    
    Output
    ------
    Returns a pandas dataframe called 'score_df' 
    -> It countains the site URL, seo, paid and organic traffic absolute scores and relative scores
    '''
    
    def score(df):
        '''This function take the TKF df and scales all values between 0 and 1
        We call it for a df transformed with only numerical values
        '''
    
        df2 = df
        
        df2['BounceRate'] = -df2['BounceRate'] # change the orientation of Bounce rate
        for i in df2.columns:
            # Rescale outliers to cap them at the 90% quantile
            df2[df2[i]>df2[i].quantile(0.9)][i]=df2[i].quantile(0.9)

  
        #Scale data between 0 and 1
        scaler = MinMaxScaler()
        scaled = scaler.fit_transform(df2)

        return scaled


    def score_calculate(arr1):
        '''Create SEO, website and paid score'''
        seo_scores=[]
        website_scores =[]
        paid_scores=[]
        for i in (arr1):
            #Seo_score = np.mean([i[0],i[1],i[4]])
            Seo_score = i[1]
            website_score = np.mean([i[2],(1-i[3])]) #changed formula 1-bounce-rate
            paid_score = np.mean([i[5],i[6],i[7],i[8]])
            seo_scores.append(Seo_score)
            website_scores.append(website_score)
            paid_scores.append(paid_score)
        return seo_scores,website_scores,paid_scores


    def rel_score_calculate(df):
        
        df['rel_SEO_Score'] = df[['MonthlyTraffic', 'OrganicTraffic',  'DirectTraffic']].mean(axis=1)
        df['rel_SEO_Score'] = df['OrganicTraffic']
        df['rel_Website_Score'] = df[['Avg_PageViews', 'BounceRate']].mean(axis=1)
        df['rel_Paid_Score'] = df[['PaidTraffic', 'ReferredTraffic', 'MailTraffic', 'SocialTraffic']].mean(axis=1)
        
        return df
            

    #subcategories are excluded for now
    df[['Category','Sub_Category']] = df['Category'].str.split('/',expand=True)

    # keep only columns for traffic
    df_seo_traffic = df[['Site','Category',  'Sub_Category',
            'MonthlyTraffic', 'OrganicTraffic', 'Avg_TimeOnSite', 'Avg_PageViews', 'BounceRate', 'DirectTraffic', 'PaidTraffic', 'ReferredTraffic', 'MailTraffic', 'SocialTraffic']]


    category_list = df['Category'].unique()
    sites_dict = {}
    df_dict = {}
    arr_dict= {}
    rel_df_dict = {}
    seo_scores = {}
    paid_scores = {}
    website_scores = {}

    for i in category_list:
        #Subsets for category
        df_dict["df_{0}".format(i)] = df_seo_traffic[df_seo_traffic['Category'] == i]
        
        #Store websites in dictionnary
        sites_dict["df_{0}".format(i)] = df_dict["df_{0}".format(i)][['Site']]
        
        #Store a df with all numerical values in a dictionnary 
        df_dict["df_{0}".format(i)] = df_dict["df_{0}".format(i)][['MonthlyTraffic', 'OrganicTraffic', 'Avg_PageViews', 'BounceRate', 'DirectTraffic', 'PaidTraffic', 'ReferredTraffic', 'MailTraffic', 'SocialTraffic']]
        
        #Apply score function (scaling for 0 to 1) to df_dict (for every column)
        arr_dict["df_{0}".format(i)] = score(df_dict["df_{0}".format(i)])
        
        #Create the combined scores
        seo_scores["seo_{0}".format(i)], paid_scores["paid_{0}".format(i)], website_scores["website_{0}".format(i)] = score_calculate(arr_dict["df_{0}".format(i)])

        #Relative scoring of website base on quantiles
        rel_df_dict["df_{0}".format(i)] = df_dict["df_{0}".format(i)].rank(axis=0, pct=True)
        rel_df_dict["df_{0}".format(i)] = rel_score_calculate(rel_df_dict["df_{0}".format(i)])
        
        #Add site and SEO/Paid/Website score to categorised df
        df_dict["df_{0}".format(i)]["Site"] = sites_dict["df_{0}".format(i)]
        df_dict["df_{0}".format(i)]["SEO_Score"] = seo_scores["seo_{0}".format(i)]
        df_dict["df_{0}".format(i)]["Paid_Score"] = paid_scores["paid_{0}".format(i)]
        df_dict["df_{0}".format(i)]["Website_Score"] = website_scores["website_{0}".format(i)]
        
        rel_df_dict["df_{0}".format(i)]["Site"] = sites_dict["df_{0}".format(i)]
        
        


    '''Move all seperate category dictionnaries back into one final dataframe'''

    score_df = pd.DataFrame( )

    for i in df_dict:
        score_df = pd.concat([score_df,df_dict[i][['Site',"SEO_Score", "Paid_Score", "Website_Score"]]])    


    rel_score_df = pd.DataFrame( )

    for i in rel_df_dict:
        rel_score_df = pd.concat([rel_score_df,rel_df_dict[i][['Site',"rel_SEO_Score", "rel_Paid_Score", "rel_Website_Score"]]])
    
    score_df = score_df.merge(rel_score_df, on="Site")
    
    return(score_df)