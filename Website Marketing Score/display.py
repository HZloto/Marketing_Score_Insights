
import pandas as pd
import numpy as np

def plot_scores(csv_path, queried_website, sep=",", social_weight=0.25, seo_weight=0.25, paid_weight=0.25, website_weight=0.25, rel=False):
    '''
    Given a website url, this function displays the scores of the website for its:
    - social media
    - seo performances
    - paid performance
    - website performance
    - a custom weighted average of the four

    Parameters
    ----------
        - csv_path: str
            The path to the csv that contains all the scores
        - queried_website: str
            The website whose score we're looking for
        - sep: str (default ',')
            The separator of the csv file (comma separated by default)
        - social_weight: float (default .25)
            The weight for the traffic score in the weighted average
        - seo_weight: float (default .25)
            The weight for the seo score in the weighted average
        - paid_weight: float (default .25)
            The weight for the traffic social media in the weighted average
        - website: float (default .25)
            The weight for the traffic social media in the weighted average           
        - rel: Bool (default False)
            Indicates if the function should use the relative or absolute score for SEO, paid and website weights
            
    Output
    ------
    Prints a string statement 
    -> It contains the site URL, and all its scores
    '''
    
    #Check if the weights add up to 1, return error message if not
    assert (social_weight+seo_weight+paid_weight+website_weight) == 1, ("The sum of all weights given should be 1")
    
    #Read csv and generate score array for the intended website
    dataframe = pd.read_csv(csv_path, sep=sep)
    totalscores = np.array(dataframe[dataframe["Site"] == queried_website])[0][1:]
    
    #Procedure if we want aboslute scores (we only keep the first 4 scores of the array)
    if rel == False: 
        scores = totalscores[0:4]
        average = np.mean(scores)
        weigthed_average = (scores[0] * social_weight) + (scores[1] * seo_weight) + (scores[2] * paid_weight) + (scores[3] * website_weight) 
        print(f"The site {queried_website} has:\n\n- a social score of {scores[0]}\n- a seo score of {scores[1]}\n- a paid score of {scores[2]}\n- a website score of {scores[3]}\n- an average score of {average: .4f}\n and a weighted average score of {weigthed_average: .4f}\n")
    
    #Procedure if we want relative scores
    elif rel == True:
        average = np.mean([totalscores[0],totalscores[4],totalscores[5],totalscores[6]])
        weigthed_average = (totalscores[0] * social_weight) + (totalscores[4] * seo_weight) + (totalscores[5] * paid_weight) + (totalscores[6] * website_weight) 
        print(f"The site {queried_website} has:\n\n- a social score of {totalscores[0]}\n- a relative seo score of {totalscores[4]}\n- a relative paid score of {totalscores[5]}\n- a relative website score of {totalscores[6]}\n- an average score of {average: .4f}\n and a weighted average score of {weigthed_average: .4f}\n")
        
        

queried_website = input("please enter website URL: ")

plot_scores('./final_scoretize_output.csv', queried_website, social_weight=0.2, seo_weight=0.3, paid_weight=0.2, website_weight=0.3, rel=False)