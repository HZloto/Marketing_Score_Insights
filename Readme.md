# Marketing Score and Insights
<b>This repo groups two projets made in the context of a Capstone project by students of the ESADE Masters of Science in Business Analytics. Credit goes to Sudhanshu Dubey, Philip Story, Sandro Widmer and Hugo Zlotowski. The first project is a marketing score for websites, the second a data analysis tool for anonymised google analytics & google ads dataset with no common keys. </b>

<h2>Marketing Score - How to use</h2>

<li>Make sure you have the dataset in the right folder 
<li>Open your terminal to the location of the scripts and type “python display.py”
<li>A user prompt will appear. Write the full URL of the website you are interested in
<li></b>(NOTE: Make sure that your website is part of the dataset)

<h2>Design and architecture</h2>

This app is developed with using Python scripts seo_traffic_scores.py and social_media_score.py. Titles are self explanatory. The scoretize.py script joins the functionalities in one app and the display makes the app user friendly and outputs results in the terminal. The seo_traffic_score is based on rule based scoring through relative analysis of the dataset. The social media score uses Unsupervised Machine Learning, namely scikit learn's clustering, to categorize website into five groups and score them. 

<h2>Data Analysis - How to use</h2>

This projet is meant for pure visualisation and therefore is based on jupyter notebooks for simplicity and readabilitiy. We first group the two datasets of interest by date to merge them on this common key. The final visualisations and plotting of the newly merged dataset can be found in the visualisations.ipynb notebook. 

<h2>Warehouse.py</h2>

The Warehouse script contains the MainWarehouse class which includes all the functionalities of the app and its visual aspects. 

<b> This project is for educational purposes and not fit to be repurposed for any commercial use. Please contact the owner of the repository for more information.

