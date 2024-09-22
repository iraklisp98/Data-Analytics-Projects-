# import helpful libraries for data manipulation and plotting
import pandas as pd
import numpy as np
import plotly.graph_objects as go


url = 'https://storage.googleapis.com/courses_data/Assignment%20CSV/finance_liquor_sales.csv' # dataset
df = pd.read_csv(url) #convert dataset to pandas framework for easier manipulation

print(df.isnull().sum()) #find inconsistent data
df['store_location'].fillna('Unknown', inplace = True)
df['county_number'].fillna(method = 'ffill', inplace = True)
df['county'].fillna('Unknown', inplace = True)
df['category'].fillna('Unknown', inplace = True)
df['category_name'].fillna('Unknown', inplace = True)
df['date'] = pd.to_datetime(df['date']) #ensure date is set datetme in order to use 'Year' to filter my data
df['year'] = df['date'].dt.year #extract year
df = df[(df['year'] > 2015) & (df['year'] < 2020)].reset_index()  #filter year based on this condition
print(df.isnull().sum()) #recheck for inconsistent data

zipcodes_grouped = df.groupby(['zip_code','item_number'])['bottles_sold'].sum() #group by zipcode and item number and summ the bottles per item number per zip code
zipcodes_grouped = zipcodes_grouped.reset_index() #reset index in order to manipulate all the data accordingly
zipcodes_grouped = zipcodes_grouped.sort_values(['zip_code','item_number'], ascending = [True, False]) #sort values per zip code and item number
most_popular_item = zipcodes_grouped.sort_values('bottles_sold', ascending = False) #extract the most valuables items
most_popular_item = zipcodes_grouped.drop_duplicates(subset = 'zip_code', keep = 'first') #drop duplicates and keep only the first 

# This is another way using bar chart to display the top 10 most popoular items
# most_popular_item = zipcodes_grouped.drop_duplicates(subset = 'zip_code', keep = 'first').sort_values('bottles_sold',ascending = False).reset_index().head(10)
# print(most_popular_item)
# fig = go.Figure()
# fig.add_trace(
#     go.Bar(
#         x = most_popular_item['zip_code'].astype(str), 
#         y = most_popular_item['bottles_sold'], 
#         name = 'Most Popular Item',
#         marker = dict(
#             color=most_popular_item['bottles_sold'],
#             colorscale='Inferno',
#             showscale=True,
#             colorbar={"title": 'Bottles Sold'}
#             ),
#         text=most_popular_item['item_number'],
#         hovertemplate='Item Number: %{text}<br>Bottles Sold: %{y}<br>Zip Code: %{x}}'
#         )
#     )
# fig.update_layout(
#     title = 'Zip Code vs Most Popular Item between 2016-2019', 
#     xaxis = dict(title = 'Zip Code', title_font=dict(size=18)),
#     yaxis = dict(title = 'Bottles Sold', title_font=dict(size=18)), 
#     width = 700, 
#     height = 800
#     )
# fig.show()



fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x = most_popular_item['zip_code'], 
        y = most_popular_item['bottles_sold'], 
        name = 'Most Popular Item',
        mode = 'markers',
        marker = dict(
            size = most_popular_item['bottles_sold']/10,
            color=most_popular_item['bottles_sold'],
            colorscale='Inferno',
            showscale=True,
            colorbar={"title": 'Bottles Sold'}
            ),
        text=most_popular_item['item_number'],
        hovertemplate='Item Number: %{text}<br>Bottles Sold: %{y}<br>Zip Code: %{x}'
        )
    )
fig.update_layout(
    title = 'Zip Code vs Most Popular Item between 2016-2019', 
    xaxis = dict(title = 'Zip Code', title_font=dict(size=18)),
    yaxis = dict(title = 'Bottles Sold', title_font=dict(size=18)), 
    width = 700, 
    height = 800
    )
fig.show()



total_sales = df['sale_dollars'].sum() #Calculate total_sales
# print(total_sales)
stores_grouped = df.groupby('store_name')['sale_dollars'].sum() #group by store name and calclulate total sales per store
percentage_sales = (stores_grouped*100/total_sales).round(2) #round to 2 decimals because the percentage fills the whole screen
percentage_sales = percentage_sales.sort_values(ascending = False).head(15).sort_values(ascending = True) #sort values accordingly to make a horizontal bar chart
# print(percentage_sales)

fig = go.Figure()
fig.add_trace(
    go.Bar(
        x = percentage_sales.values,
        y = percentage_sales.index,
        text = percentage_sales.values,
        orientation= 'h',
        textposition = 'auto',
        hovertemplate='Store Name: %{y}<br>Percentage Sales: %{x}%<br>',
        marker = dict(
            color=percentage_sales.values,
            colorscale='Inferno',
            showscale=True,
            opacity = 0.8,
            colorbar={"title": 'Sale Dollars'}
            ),
    )
)
fig.update_layout(
    title = '%Sales by store', 
    xaxis = dict(title = '% percentage of Sales', title_font=dict(size=18)),
    yaxis = dict(title = 'Store name', title_font=dict(size=18)), 
    width = 1000, 
    height = 600
    )
fig.show()


# Ι tried to calculate the percentage of sales of every store in every zip code taking into account the every zip code has its own
# most famous item but the visualization was not significant due to the fact that a great number of stores sell only one product so the 
# percentage was either 0 or 100% in a lot of cases


# # i have to optimize this code
stores_grouped = df.groupby(['zip_code', 'store_number'])['bottles_sold'].sum().reset_index()
stores_grouped = stores_grouped.rename(columns = {'bottles_sold': 'bottles_sold_per_store'})
merged_df = pd.merge(df, most_popular_item, on=['zip_code', 'item_number'], how='inner')
# print(merged_df.head(10))
merged_df = pd.merge(merged_df, stores_grouped, on=['zip_code', 'store_number'])
merged_df['proportional_sales'] =100*merged_df['bottles_sold_x']/merged_df['bottles_sold_per_store']
merged_df = merged_df[['zip_code','store_name','bottles_sold_per_store','proportional_sales']].sort_values(['bottles_sold_per_store', 'proportional_sales'], ascending = [False, False])
print(merged_df.head(51))

fig = go.Figure()
fig.add_trace(
    go.Bar(
        x = merged_df['store_name'].head(15),
        y = merged_df['bottles_sold_per_store'].head(15),
        text = merged_df['proportional_sales'].head(15),
        textposition = 'auto',
        hovertemplate='Store Name: %{x}<br>Bottles Sold: %{y}<br>Proportional Sales: %{text}%<br>'
    )
)
fig.update_layout(
    title = 'Total Bottles Sold of the Most Popular Item by Store in Each Zip Code', 
    xaxis = dict(title = 'Store name', title_font=dict(size=18)),
    yaxis = dict(title = 'Bottles Sold', title_font=dict(size=18)), 
    width = 700, 
    height = 800
    )
fig.show()