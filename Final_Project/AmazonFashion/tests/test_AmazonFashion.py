from AmazonFashion import AmazonFashion a

def test_data():
   actual = a.df_all.shape
   expected = (10000, 24)
   assert actual == expected, "data was not correctly loaded"

def test_top_n_highest_review(n = 5, cat3 = 'Rail Vehicles'):
    df_cat3 = a.df_all[a.df_all['cat3']==cat3]
    df_cat3_top_n = df_cat3.sort_values(by = 'avg_rating', ascending = False).head(n)
    df_product = df_cat3_top_n[['product_name', 'product_information','product_description'
                         ,'price','average_review_rating', 'customers_who_bought_this_item_also_bought'
                        , 'items_customers_buy_after_viewing_this_item']]
    expected = (5,7)
    actual = df_product.shape
    assert expected == actual

