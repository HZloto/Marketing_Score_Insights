#IMPORTS
import pandas as pd
from social_media_score import social_media_score
from seo_traffic_scores import seo_traffic_scores



def scoretize(csv_path):
    '''
    Given a csv path, this function computes the scores of the all rows (websites) for their:
    - social media
    - seo performances
    - paid performance
    - website performance

    Parameters
    ----------
        - csv_path: str
            The path to the csv that contains all the scores
            
    Output
    ------
    Returns a pandas dataframe called 'final_score' 
    -> It contains the site URLs, and all the scores computed

    '''

    #We use the path to define and import the csv
    df = pd.read_csv(csv_path)
    

    def scores_merger(results_media,results_seo_traffic):
        final_score = results_media.merge(results_seo_traffic, how='left', on='Site')
        return final_score.round(decimals=3)
        

    results_media = social_media_score(df)
    results_seo_traffic = seo_traffic_scores(df)
    
    return(scores_merger(results_media,results_seo_traffic))
    
    

scoretize(r"https://capstonetkf.s3.amazonaws.com/dataset_v4.csv").to_csv('final_scoretize_output.csv',header=True,index=False)