from flask import Flask, render_template,session,jsonify,send_from_directory
import plotly.subplots as sp
from plotly.subplots import make_subplots

from flask_basicauth import BasicAuth
from flask_login import LoginManager
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go

import matplotlib
matplotlib.use('Agg')
import seaborn as sns 
import plotly.express as px
from flask import render_template, redirect, url_for, request
app = Flask(__name__)
app.secret_key = b'1234'
# Configure basic authentication
basic_auth = BasicAuth(app)
app.config['BASIC_AUTH_USERNAME'] = 'abdelhamedelaila'
app.config['BASIC_AUTH_PASSWORD'] = 'cheefa'

# Load your dataset 
df = pd.read_csv(r'C:\Users\midoel3ila\Documents\Datasetcheefa.csv')

# route
@app.route('/')
def home():
    data ={
        'status_code':200,
        'page_name':'Home_page'
    }
    return jsonify(data)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
       if request.method == 'POST' and basic_auth.authenticate():

        return redirect(url_for('dashboard'))

       error_message = 'Invalid username or password. Please try again.'
       return render_template('login.html', error=error_message)


@app.route('/dashboard')
@basic_auth.required
def dashboard():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Bar chart: Distribution of product categories 
    Top_product_category = df['product_category_name'].value_counts().head(10)
    bar_chart = px.bar(df, x=Top_product_category.values, y=Top_product_category.index, title='Top 10 product category  sales by frequancy' )

    # Line chart: Order counts over time using Plotly
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    line_chart = px.line(df.resample('M', on='order_purchase_timestamp').size(),  title='Order Counts Over Time', labels={'value': 'Number of Orders'})

    payment_type=df['payment_type'].value_counts()
    bar_chart_payment = px.bar(df, x=df['payment_type'],y=df['payment_value'],title='Distribution of Payment Types',color=df['payment_type'],barmode='group')

    # Pie chart: Distribution of order status using Plotly Express
    pie_chart_order = px.pie(df, names='order_status', title='Distribution of Order Status',width=500)

    #map
    map_char= px.scatter_mapbox(
        df,
        lat='geolocation_lat',
        lon='geolocation_lng',
        color='geolocation_state',
        size='review_score',
        mapbox_style="open-street-map",
        zoom=3,
        height=800,
        title='Map of Review Scores'
    )



    # Render the dashboard template with the Plotly charts
    return render_template('dashboard_plotly.html', bar_chart_path=bar_chart.to_html(full_html=False), line_chart_path=line_chart.to_html(full_html=False),pie_chart_order_path=pie_chart_order.to_html(full_html=False),bar_chart_payment_path=bar_chart_payment.to_html(full_html=False),map_char_path=map_char.to_html(full_html=False))

@app.route('/data')
@basic_auth.required
def tabular_data():
    # Display the raw data in a tabular format
    table_html = df.to_html(classes='table table-striped', index=False)

    return render_template('data.html', table_html=table_html)

if __name__ == '__main__':
    app.run(port=8000,host="0.0.0.0",debug=True)
