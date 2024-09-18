import streamlit as st
from streamlit_option_menu import option_menu
import os
import json
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import mysql.connector
import time
from sqlalchemy import create_engine


#MySQL Database connection
connection = mysql.connector.connect(
  host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
  port = 4000,
  user = "3eB7PgspgHbdnuZ.root",
  password = "kxMxkkdj8HXjSUmb",
  database = "Phonepe"
)
mycursor = connection.cursor(buffered=True)

#Streamlit page construction:

with st.sidebar:
    st.sidebar.image("D:\Data Science\phone pe pulse\img.png")


    menu = option_menu(
    menu_title='Dashboard',
    options=["Home","Count Information","Transaction Information","User Information","Top Charts","Insights"],
    menu_icon='cast',
    icons=['house','credit-card','person','bar-chart','bar-chart','person'],
    default_index=1)



if menu == "Home":
    st.image("D:\Data Science\phone pe pulse\img.png")
    st.markdown('<h1 style="color: #7413f0 ;">Phonepe Pulse Data Visualization</h1>', unsafe_allow_html=True)
    st.subheader(":green[PhonePe : The Best Unified Payments Interface in India]")
    st.write("PhonePe is one of India's leading digital payments platforms,founded in December 2015 by Sameer Nigam, Rahul Chari, and Burzin Engineer. It operates under the ownership of Flipkart, which is a subsidiary of Walmart. PhonePe is designed to facilitate seamless digital transactions and financial services using the Unified Payments Interface (UPI), an instant real-time payment system developed by the National Payments Corporation of India (NPCI). .")

    st.write(":green[**Major Benefits of Using PhonePe :**]")
    st.write("1. **Ease of Use :** PhonePe provides a user-friendly interface that makes it easy for users to navigate and perform transactions quickly.")
    st.write("2. **Multiple Payment Options :** Users can link multiple bank accounts to PhonePe and make payments using various methods such as UPI, bank transfers, debit/credit cards, and wallets.")
    st.write("3. **Instant Money Transfers :** Transactions through UPI are fast, secure, and available 24/7, including weekends and holidays.")
    st.write("4. **Merchant Payments :** Users can pay using QR codes, UPI, or the PhonePe wallet, enhancing convenience and reducing the need for cash transactions.")
    st.write("5. **Offers and Cashback :** PhonePe frequently offers discounts, cashback, and rewards to users for making transactions and using specific services within the app.")


st.image("D:\\Data Science\\phone pe pulse\\ICN.png", width=50)  # Decreases the width to 300px

if menu == "Count Information":

    def Agg_trans_count(state):
        query = "SELECT States, Years, SUM(Transaction_count) AS Transaction_Count FROM phonepe.Aggregated_trans \
                WHERE States=%s \
                GROUP BY Years"
        
        mycursor.execute(query, (state,))
        out = mycursor.fetchall()
        connection.commit()
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

        return df

    def Line_Plot(df):
        trace = go.Scatter(
            x=df['Years'],
            y=df['Transaction_Count'],
            mode='lines',
            name=df['States'].values[0],
            line=dict(color='orange'))

        layout = go.Layout(
            title=dict(text='Transaction Count Plot of ' + df['States'].values[0],font=dict(color='gold')),
            xaxis=dict(title='Years'),
            yaxis=dict(title='Transaction Count'))

        fig = go.Figure(data=[trace], layout=layout)

        return fig


    st.markdown('<h1 style="color: gold;">State-wise Transaction Count Information</h1>', unsafe_allow_html=True)
    states = ['Andaman & Nicobar','Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 
              'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 
              'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
                'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Andaman and Nicobar Islands', 'Chandigarh', 'Dadra and Nagar Haveli and Daman and Diu',
                  'Delhi', 'Lakshadweep', 'Puducherry']

    state_selected = st.selectbox(":blue[**Select State :**]", states)

    df = Agg_trans_count(state_selected)
    df2= df.sort_values(by="Years")
    df2 = df2.reset_index(drop=True)
    df2.index= df2.index + 1
    fig = Line_Plot(df)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<h1 style="color: gold; font-size: 16px;">Table View of Year wise Total Transaction Count</h1>', unsafe_allow_html=True)

    st.dataframe(df2)





if menu == "Transaction Information":
    st.image("D:/Data Science/phone pe pulse/banner.jpg", use_column_width=True) 
    



    # Select Year and Quarter inside the Transaction Information menu
    st.markdown("## Select Year and Quarter")
    Year = st.selectbox("Select Year", [2018, 2019, 2020, 2021, 2022, 2023], index=3, key="select_year_transaction")
    Quarter = st.selectbox("Select Quarter", [1, 2, 3, 4], index=0, key="select_quarter_transaction")

    col1, col2 = st.columns([1, 1], gap="medium")
    #GEO

    st.markdown("## :red[Overall State Data - Transactions Amount]")#sk
    mycursor.execute(f"""SELECT States, SUM(Transaction_count) as Total_Transactions, sum(Transaction_amount)
                        as Total_amount FROM map_trans
                        WHERE Years = {Year} and Quarter = {Quarter}
                        GROUP BY States order by States""")
    df1 = pd.DataFrame(mycursor.fetchall(),columns= ['States', 'Total_Transactions', 'Total_amount'])
        
    fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='States',
                    color='Total_amount',
                    color_continuous_scale='greens')

    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig,use_container_width=True)

        
    st.markdown("## :red[Overall State Data - Transactions Count]")
    mycursor.execute(f"""SELECT States, SUM(Transaction_count) as Total_Transactions, sum(Transaction_amount) 
                        as Total_amount FROM map_trans 
                        WHERE Years = {Year} and Quarter = {Quarter} 
                        GROUP BY States ORDER BY States""")
    df1 = pd.DataFrame(mycursor.fetchall(),columns= ['States', 'Total_Transactions', 'Total_amount'])
    df1.Total_Transactions = df1.Total_Transactions.astype(int)

    fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='States',
                    color='Total_Transactions',
                    color_continuous_scale='greens')
            
        

    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig,use_container_width=True)

    with col1:
        st.markdown("### :violet[State]")
        mycursor.execute(f"""SELECT States, SUM(Transaction_count) as Total_Transactions_Count, 
                        SUM(Transaction_amount) as Total FROM aggregated_trans WHERE 
                        Years = {Year} and
                        Quarter = {Quarter} 
                        GROUP BY States ORDER BY Total desc limit 10""")
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count', 'Total_Amount'])
        fig = px.pie(df, values='Total_Amount',
                            names='State',
                            title='Top 10 States',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Transactions_Count'],
                            labels={'Transactions_Count': 'Transactions_Count'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### :violet[District]")
        mycursor.execute(f"""SELECT Districts , SUM(Transaction_count) as Total_Count, SUM(Transaction_amount)
                        as Total FROM map_trans WHERE Years = {Year} and Quarter = {Quarter} 
                        GROUP BY Districts ORDER BY Total desc limit 10""")
        df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])

        fig = px.pie(df, values='Total_Amount',
                            names='District',
                            title='Top 10 District',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Transactions_Count'],
                            labels={'Transactions_Count': 'Transactions_Count'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    mycursor.execute(f"""SELECT States, Districts, Years, 
                    SUM(Transaction_count) as Total_Transactions
                    FROM map_trans
                    WHERE Years = {Year} 
                    GROUP BY States, Districts, Years ORDER BY States, Districts""")

    df2 = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Districts', 'Years', 'Total_Transactions'])

    fig = px.sunburst(df2, path=['Years', 'States', 'Districts'], values='Total_Transactions')
    st.plotly_chart(fig, use_container_width=True)


   #Map visualzation

    
        
        # BAR CHART - TOP PAYMENT TYPE
    st.markdown("## :red[Top Payment Type]")
    mycursor.execute(f"""SELECT Transaction_type, SUM(Transaction_count) as Total_Transactions, 
                        sum(Transaction_amount) as Total_amount FROM aggregated_trans 
                        WHERE Years= {Year} and Quarter = {Quarter} GROUP BY Transaction_type ORDER BY 
                        Transaction_type""")
    df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_Type', 'Total_Transactions','Total_amount'])

    fig = px.bar(df,
                    title='Transaction Types vs Total_Transactions',
                    x="Transaction_Type",
                    y="Total_Transactions",
                    orientation='v',
                    color='Total_amount',
                    color_continuous_scale=px.colors.sequential.Agsunset)
    st.plotly_chart(fig,use_container_width=False)
            

        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
    st.markdown("# ")
    st.markdown("# ")
    st.markdown("# ")
    st.markdown("## :red[Select any State to explore more]")
    selected_state = st.selectbox("",
                            ('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh',
                                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                'Uttarakhand', 'West Bengal'),index=30)
                                    
    mycursor.execute(f"""SELECT States, Districts,Years,Quarter, SUM(Transaction_count) 
                        as Total_Transactions, sum(Transaction_amount) as Total_amount FROM map_trans
                        WHERE Years = {Year} and Quarter = {Quarter} and States= '{selected_state}'
                        GROUP BY States, Districts,Years,Quarter order by States,Districts""")
        
    df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','Districts','Year','Quater',
                                                        'Total_Transactions','Total_amount'])
    fig = px.bar(df1,
                    title=selected_state,
                    x="Districts",
                    y="Total_Transactions",
                    orientation='v',
                    color='Total_amount',
                    color_continuous_scale=px.colors.sequential.Agsunset)
    st.plotly_chart(fig,use_container_width=True)




if menu == "User Information":

    st.image("D:\Data Science\phone pe pulse\Phonepe32.jpg", use_column_width=True) 


    # Select Year and Quarter inside the User Information menu
    st.markdown("## Select Year and Quarter")
    Year = st.selectbox("Select Year", [2018, 2019, 2020, 2021, 2022, 2023], index=3, key="select_year_transaction")
    Quarter = st.selectbox("Select Quarter", [1, 2, 3, 4], index=0, key="select_quarter_transaction")

    col1, col2 = st.columns([2, 3], gap="large")

    with col1:
        st.markdown("### :violet[Brands]")
        if Year == 2022 and Quarter in [2, 3, 4]:
            st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
        else:
            # Execute query to get brand data
            mycursor.execute(f"""
                SELECT brands, SUM(User_count) as Total_Count, AVG(percentage)*100 as Avg_Percentage
                FROM aggregated_user 
                WHERE Years = {Year} AND Quarter = {Quarter}
                GROUP BY brands 
                ORDER BY Total_Count DESC 
                LIMIT 10
            """)
            df_brands = pd.DataFrame(mycursor.fetchall(), columns=['Brands', 'Total_Users', 'Avg_Percentage'])

            # Plot brand data
            fig_brands = px.bar(
                df_brands,
                title='Top 10 Brands',
                x="Total_Users",
                y="Brands",
                orientation='h',
                color='Avg_Percentage',
                color_continuous_scale=px.colors.sequential.Agsunset
            )
            st.plotly_chart(fig_brands, use_container_width=True)

    with col2:
        st.markdown("### :violet[Districts]")
        # Execute query to get district data
        mycursor.execute(f"""
            SELECT Districts, SUM(Registered_Users) as Total_Users, SUM(App_Opens) as Total_Appopens
            FROM map_user 
            WHERE Years = {Year} AND Quarter = {Quarter}
            GROUP BY Districts 
            ORDER BY Total_Users DESC 
            LIMIT 10
        """)
        df_districts = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users', 'Total_Appopens'])

        # Plot district data
        fig_districts = px.bar(
            df_districts,
            title='Top 10 Districts',
            x="Total_Users",
            y="District",
            orientation='h',
            color='Total_Users',
            color_continuous_scale=px.colors.sequential.Agsunset
        )
        st.plotly_chart(fig_districts, use_container_width=True)
    col3,col4 = st.columns([2,3],gap="small")

    with col3:
         st.markdown("### :violet[Pincode]")
         mycursor.execute(f"""SELECT Pincodes, SUM(Registered_Users) as Total_Users 
                                FROM top_user 
                                WHERE Years = {Year} and Quarter = {Quarter} 
                                GROUP BY Pincodes ORDER BY Total_Users desc limit 10""")
         df = pd.DataFrame(mycursor.fetchall(), columns=['Pincodes', 'Total_Users'])
         fig = px.pie(df,
                            values='Total_Users',
                            names='Pincodes',
                            title='Top 10',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Total_Users'])
         fig.update_traces(textposition='inside', textinfo='percent+label')
         st.plotly_chart(fig,use_container_width=True)
                
    with col4:
         st.markdown("### :violet[State]")
         mycursor.execute(f"""SELECT States, SUM(Registered_Users) as Total_Users, sum(App_Opens) as 
                                Total_Appopens FROM map_user 
                                WHERE Years = {Year} and Quarter = {Quarter} 
                                GROUP BY States ORDER BY Total_Users desc limit 10""")
         df = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Total_Users','Total_Appopens'])
         fig = px.pie(df, values='Total_Users',
                                names='States',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Total_Appopens'],
                                labels={'Total_Appopens':'Total_Appopens'})

         fig.update_traces(textposition='inside', textinfo='percent+label')
         st.plotly_chart(fig,use_container_width=True)


          #india map....

         st.markdown("## :red[Overall State Data - User App opening frequency]")
         mycursor.execute(f"""SELECT States, sum(Registered_Users) as Total_Users, sum(App_Opens) as Total_Appopens 
                        FROM map_user 
                        WHERE Years = {Year} and Quarter = {Quarter} 
                        GROUP BY States ORDER BY States""")
         df1 = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Total_Users','Total_Appopens'])
        
         fig = px.choropleth(df1,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='States',
                    color='Total_Appopens',
                    color_continuous_scale='greens')
        

         fig.update_geos(fitbounds="locations", visible=False)
         st.plotly_chart(fig,use_container_width=True)



        
         # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
         st.markdown("## :red[Select any State to explore more]")
         selected_state = st.selectbox("",
                            ('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh',
                                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                'Uttarakhand', 'West Bengal'),index=30)
    
         mycursor.execute(f"""SELECT States,Years,Quarter,Districts,SUM(Registered_Users) as Total_Users, 
                        sum(App_Opens) as Total_Appopens 
                        FROM map_user 
                        WHERE Years = {Year} and Quarter = {Quarter} and States= '{selected_state}' 
                        GROUP BY States, Districts,Years,Quarter ORDER BY States,Districts""")
        
         df = pd.DataFrame(mycursor.fetchall(), columns=['States','Years', 'Quarter', 'Districts', 'Total_Users','Total_Appopens'])
         df.Total_Users = df.Total_Users.astype(int)
        
         fig = px.bar(df,
                    title=selected_state,
                    x="Districts",
                    y="Total_Users",
                    orientation='v',
                    color='Total_Users',
                    color_continuous_scale=px.colors.sequential.Agsunset)
         st.plotly_chart(fig,use_container_width=True)



if menu == "Top Charts":

    st.markdown('<h1 style="color: gold;">Top Charts</h1>', unsafe_allow_html=True)


    query_select = st.selectbox(":blue[**Select Query :**]",("Select",
                                "Top 10 States with Highest Net Transaction counts in 2023",
                                "Top 10 States of Net Registered users In 2023",
                                "State-wise Net Transaction Amount Data",
                                "State-wise Net Transaction Type Count Data"))
    


    if query_select=="Select the Query:":
        st.write("  ")

#Query 1:

    elif query_select=="Top 10 States with Highest Net Transaction counts in 2023":
        st.markdown('<h1 style="color: gold; font-size: 15px; ">Top 10 States with Highest Net Transaction counts in 2023</h1>', unsafe_allow_html=True)
    
        mycursor.execute("SELECT States,SUM(Transaction_count) AS Total_Count FROM phonepe.top_trans \
                        Where Years=2023\
                        GROUP BY States \
                        ORDER BY Total_Count DESC LIMIT 10")

        states = []
        total_counts = []
        for row in mycursor.fetchall():
            states.append(row[0])
            total_counts.append(row[1])


        fig, ax = plt.subplots(figsize=(15, 6))
        colors = ['blue', 'red', 'green', 'yellow', 'purple', 'orange', 'cyan', 'magenta', 'brown', 'pink']

        ax.bar(states, total_counts, color=colors)
        ax.set_xlabel('States')
        ax.set_ylabel('Total Count')
        ax.set_title('Top 10 States with Highest Net Transaction counts in 2023')

        st.pyplot(fig)

# Query 2:

    elif query_select=="Top 10 States of Net Registered users In 2023":
        st.markdown('<h1 style="color: gold; font-size: 15px; ">Top 10 States of Net Registered users In 2023</h1>', unsafe_allow_html=True)


        mycursor.execute("SELECT States,SUM(Registered_users) AS Register_User FROM phonepe.top_user \
                        Where Years=2023\
                        GROUP BY States \
                        ORDER BY Register_User DESC LIMIT 10")
        states = []
        register_users = []
        for row in mycursor.fetchall():
            states.append(row[0])
            register_users.append(row[1])

        fig, ax = plt.subplots(figsize=(15,6))
        colors = ['orange', 'cyan', 'magenta', 'brown', 'pink','blue', 'red', 'green', 'yellow', 'purple']

        ax.bar(states, register_users,color=colors)
        ax.set_xlabel('States')
        ax.set_ylabel('Register Users')
        ax.set_title('Top 10 States of Net Registered users In 2023')

        st.pyplot(fig)

# Query-3:

    elif query_select=="State-wise Net Transaction Amount Data":
        st.markdown('<h1 style="color: gold; font-size: 15px; ">State-wise Net Transaction Amount Data Chart</h1>', unsafe_allow_html=True)

        mycursor.execute("SELECT States, Years, Transaction_amount \
                      FROM phonepe.aggregated_trans \
                      WHERE years between 2018 and 2023 \
                      GROUP by States, Years, Transaction_amount")
    
        out = mycursor.fetchall()
        connection.commit()
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

        # Corrected: Use 'States' instead of 'State'
        fig = px.bar(df, x=df.States, 
                    y=df.Transaction_amount,
                    color=df.States,
                    title='State-wise Net Transaction Amount Data',
                    height=700, width=650)

        st.plotly_chart(fig)


# Query-4:

    elif query_select== "State-wise Net Transaction Type Count Data":
        st.markdown('<h1 style="color: gold; font-size: 15px; ">State-wise Net Transaction Type Count Data Chart</h1>', unsafe_allow_html=True)

        mycursor.execute("SELECT States,Years,Transaction_type,SUM(Transaction_count) Transaction_count \
                            FROM phonepe.aggregated_trans \
                            GROUP by States,Years,Transaction_type")
        out = mycursor.fetchall()
        connection.commit()
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

        fig = px.bar(df, x=df.States,
                        y=df.Transaction_count,
                        color=df.Transaction_type,
                        title='State-wise Net Transaction Type Count Data',
                        height=700,width=650)

        st.plotly_chart(fig)




elif menu == "Insights":

    st.title(":green[Five Major Insights :]")


    st.markdown('<h1 style="color:#7413f0 ; font-size: 25px; "> --> Top 3 States With Most Transaction Count</h1>', unsafe_allow_html=True)
    st.write("1. Karnataka")
    st.write("2. Telengana")
    st.write("3. Maharashtra") 

    st.markdown('<h1 style="color: #7413f0; font-size: 25px; "> --> Top 3 States With Most Transaction Amount</h1>', unsafe_allow_html=True)
    st.write("1. Maharashtra")
    st.write("2. Telengana")
    st.write("3. Karnataka") 

    st.markdown('<h1 style="color:#7413f0; font-size: 25px; "> --> Top 3 States With Most Registered Users</h1>', unsafe_allow_html=True)
    st.write("1. Maharashtra")
    st.write("2. Uttar Pradesh")
    st.write("3. Karnataka")

    st.markdown('<h1 style="color: #7413f0; font-size: 25px; "> --> Top 3 States With Most App Opens in 2023</h1>', unsafe_allow_html=True)
    st.write("1. Rajasthan")
    st.write("2. Maharashtra")
    st.write("3. Madhya Pradesh")

    st.markdown('<h1 style="color: #7413f0; font-size: 25px; "> --> Top 3 Brands With Most Users in India</h1>', unsafe_allow_html=True)
    st.write("1. Xiaomi")
    st.write("2. Samsung")
    st.write("3. Vivo")


    st.image("D:\Data Science\phone pe pulse\Phonepe2.png")


