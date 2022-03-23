"""
Amazon Fashion, Code file
AmeliaHZW, Applied Data Science (GR5069)
"""

""" Import Packages """
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

""" Prepare Workspace """
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth',200)

cwd = os.getcwd()

""" Load in Data """
df = pd.read_csv('amazon_co-ecommerce_sample.csv')

""" Preprocessing and Wrangeling """
df_t = pd.DataFrame()
df_cat = df['amazon_category_and_sub_category'].str.split('>',expand = True)
for i in range(0,5):
    temp = df_cat[i].str.strip()
    df_t = pd.concat([df_t, temp], axis = 1)
    i = i+1
df_t.columns = ['cat1','cat2','cat3','cat4','cat5']

df['average_review_rating'] = df['average_review_rating'].apply(str)

df_star = df['average_review_rating'].str.split('out of',expand = True)[0].astype(float)
df_star = pd.DataFrame(df_star.rename('avg_rating', inplace = True))

df_price = df['price'].str.split('£',expand = True)[1].str.split('-',expand = True)[0].str.replace(',', '').astype(float)
df_price = pd.DataFrame(df_price.rename('p', inplace = True))

df_all = pd.concat([df, df_t, df_star, df_price], axis = 1)




""" Function 1: return list of column names """
def column_names():
    return [column for column in df_all]
    """
    This function is the start of the package, which returns a list of column names.

    Examples
    ----------
    >>> a.column_names()
    ['uniq_id', 'product_name', 'manufacturer', 'price', 'number_available_in_stock', 'number_of_reviews',
    'number_of_answered_questions', 'average_review_rating', 'amazon_category_and_sub_category',
    'customers_who_bought_this_item_also_bought', 'description', 'product_information', 'product_description',
    'items_customers_buy_after_viewing_this_item', 'customer_questions_and_answers', 'customer_reviews', 'sellers',
    'cat1', 'cat2', 'cat3', 'cat4', 'cat5', 'avg_rating', 'p']
    """



""" Function 2: List of unique values for selected column"""
def value_list(column = 'cat1'):
    """
    Using this function, you can get a list of unique values for a selected column.

    Parameters
    ----------
    column: string indicating column name, if you would like to know what columns are available, please us column_names().
            Default value for this parameter is 'cat1'.

    Returns
    ----------
    The result would be a list of unique values of the column that you specified.

    """
    assert column in [column for column in df_all], "Check the column name you entered."
    for m in df_all[column].unique():
        print(m)




""" Function 3: Average review rating or price by category"""
def category_avg_metric(metric, cat1 = 'cat1', cat2 = 'cat2'):
    """
    This function allows you to get the average review rating or price by category.

    Parameters
    ----------
    metric: possibie values are 'rating' or 'price'; only include one at a time.
    cat1: the first category index you want to check.
    cat2: the second category index you want to check.
    Note that cat1 and cat2 takes value from ['cat1','cat2', 'cat3', 'cat4','cat5'], we suggest that
        the first index is smaller than the second, so that you get a more structured return. Inputing
        the same index for both would yield a calculation only in one level of subcategory.

    Returns
    ----------
    A dataframe of average review rating or price by the level category that you input.

    """
    assert metric in ['rating', 'price'], "Please input 'rating' or 'price' "
    for category in [cat1, cat2]:
        assert category in ['cat1','cat2', 'cat3', 'cat4','cat5'], "The index of Category should be between 1 and 5"
    if metric == 'rating':
        df_cam = df_all['avg_rating'].groupby([df_all[cat1],df_all[cat2]]).mean()
    if metric == 'price':
        df_cam = df_all['p'].groupby([df_all[cat1],df_all[cat2]]).mean()
    return df_cam





def top_n_highest_review(n = 10, cat3 = 'Rail Vehicles'):
    """
    For a prespecified Category 3, what's the highest n review rating products?

    Parameters
    ----------
    n: an integer indicating the ranking for rating review in this function. Default value is 10.
    cat3: input the string for the Category 3 that you are interested in. Look up unique values
        of Category 3 using value_list(column = 'cat3').

    Returns
    ----------
    Informations of the top rated products in the category 3 prespecified.

    """
    assert n > 0, "n must be non-negative"
    df_cat3 = df_all[df_all['cat3']==cat3]
    df_cat3_top_n = df_cat3.sort_values(by = 'avg_rating', ascending = False).head(n)
    df_product = df_cat3_top_n[['product_name', 'product_information','product_description'
                         ,'price','average_review_rating', 'customers_who_bought_this_item_also_bought'
                        , 'items_customers_buy_after_viewing_this_item']]
    return df_product




def manufacturer_product(manufacturer = 'LEGO'):
    """
    A function to check products available on Amazon about a certain manufacturer.

    Parameters
    ----------
    manufacturer: a string of manufacturer name. Look up the manufacturer using
        value_list(column = 'manufacturer') if you don't know one. Default value is 'LEGO'.

    Returns
    ----------
    Informations of products by that manufacturer that are sold on Amazon UK at present.

    """
    df_m = df_all[df_all['manufacturer']==manufacturer]
    df_m_p = df_m[['manufacturer', 'product_name','price', 'number_available_in_stock'
                  ,'number_of_reviews','average_review_rating', 'amazon_category_and_sub_category'
                  ,'product_information', 'product_description'
                   ,'customers_who_bought_this_item_also_bought','items_customers_buy_after_viewing_this_item']]
    return df_m_p






def price_dist(cat2):
    """
    Using this function, you can get a price distribution for the Category 2 that you specified.

    Parameters
    ----------
    cat2: The name of the Category 2. Look it up if you do not have one using value_list(columns = 'cat2').

    Returns
    ----------
    Summary statistics of price for a certain Category 2, and a histogram of the price distribution.

    Examples
    ----------
    >>> a.price_dist('Accessories')
    Summary Statistics for Category 2: Accessories Price
    count    536.000000
    mean      14.715653
    std       32.182940
    min        0.890000
    25%        3.447500
    50%        7.990000
    75%       14.990000
    max      447.990000
    Name: p, dtype: float64

    """
    assert cat2 in df_all['cat2'].unique(), "The Category 2 you input does not exist. Please check!"
    df_category = df_all[df_all['cat2'] == cat2]
    print(f'Summary Statistics for Category 2: {cat2} Price')
    print(df_category.p.describe())

    p_mean = df_category.p.mean()

    fig,ax = plt.subplots(1,1,figsize=(12,6))
    df_category.p.hist( ax = ax, bins='auto', color = 'cornflowerblue')
    ax.set_xlabel('price in £')
    ax.set_ylabel('frequency')
    ax.set_title(f'Price Distribution for Category 2: {cat2}')
    ax.axvline(df_category.p.mean(),color='navy')
    ax.text(df_category.p.mean()+1,ax.get_ylim()[1]*.75,f'mean = {p_mean:0.2f}')
    plt.show()





def export(path = cwd):
    """
    What if I want to store the results after text-cleaning and do some further analysis from my end?

    Parameters
    ---------
    cwd: The working directory you want to save the csv file in. Default is current work directory.

    Returns
    ----------
    A saved csv file on local folder.

    """
    df_save = df_all.rename({'p':'price (£)'})
    df_save.to_csv('AmazonFashionProductsUK.csv')
