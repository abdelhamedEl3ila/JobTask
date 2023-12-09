import pandas as pd
import pyodbc

server = 'DESKTOP-8DHSNPI\SQLEXPRESS'
database = 'Amazon'
driver = 'SQL Server' 

conn_str = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
conn = pyodbc.connect(conn_str)

sql_query = 'select pd.product_id,cat.product_category_name_english as product_category_name  ,pd.product_name_lenght,pd.product_description_lenght,pd.product_photos_qty,pd.product_weight_g,pd.product_length_cm,pd.product_height_cm,pd.product_width_cm,ordit.order_id,ordit.freight_value,ordit.order_item_id,ordit.price,ordit.seller_id,ordit.shipping_limit_date ,seller.seller_city,seller.seller_state,seller.seller_zip_code_prefix,ord.customer_id,ord.order_approved_at,ord.order_delivered_carrier_date,ord.order_delivered_customer_date,ord.order_estimated_delivery_date,ord.order_purchase_timestamp,ord.order_status,cust.customer_city,cust.customer_state,cust.customer_zip_code_prefix,geo.geolocation_city,geo.geolocation_lat,geo.geolocation_lng,geo.geolocation_state,rev.review_answer_timestamp,rev.review_comment_message,rev.review_comment_title,rev.review_creation_date,rev.review_id,rev.review_score,ordp.payment_installments,ordp.payment_sequential,ordp.payment_type,ordp.payment_valuefrom dbo.Categories  cat join dbo.Products  pdON pd.product_category_name=cat.product_category_namejoin dbo.[Order Items]  orditON pd.product_id =ordit.product_idjoin dbo.Sellers sellerON ordit.seller_id=seller.seller_idjoin dbo.Orders ordON ord.order_id=ordit.order_idjoin dbo.Customers cust ON cust.customer_id = ord.customer_idjoin dbo.Geolocation geo ON geo.geolocation_zip_code_prefix=cust.customer_zip_code_prefixjoin dbo.Reviews rev ON rev.order_id=ord.order_idjoin dbo.[Order Payments] ordp ON ord.order_id=ordp.order_id'
df = pd.read_sql_query(sql_query, conn)

# Replace 'output_file.csv' with your desired CSV file name
csv_file_path = 'output_file.csv'

# Save the DataFrame to a CSV file
df.to_csv('C:\Users\midoel3ila\Documents\Datasetcheefa.csv', index=False)

# Close the SQL Server connection
conn.close()

print(f"Data has been successfully fetched from SQL Server and saved to 'C:\Users\midoel3ila\Documents\Datasetcheefa.csv'.")
