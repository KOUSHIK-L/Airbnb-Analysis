# Importing necessary Libraries
import pandas as pd 
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu

# Pie plt using Plotly express
def pie_plot(df, x, y, title,title_x=0.15):
    fig = px.pie(df, names=x, values=y, title=title,color_discrete_sequence=['#3C9D4E', '#7031AC', '#C94D6D', '#E4BF58', '#FD6787','#4174C9'])
    fig.update_layout(title_x=title_x, title=dict(font=dict(size=20, family='serif', color='black')))
    return st.plotly_chart(fig, theme="streamlit", use_container_width=True)

# Bar plot using Plotly express 
def bar_plot(df,x,y,title,xaxis,yaxis):
    fig = px.bar(df, x=x,y=y,title=title,text_auto='.2s',height=520,width=520)
    fig.update_traces(marker_color= '#FF5A5F', textfont_size = 14, textangle = 0, textposition = "outside")
    fig.update_layout(autosize=False, xaxis_title=xaxis,yaxis_title=yaxis, 
    title=dict(font=dict(size=22, family='serif', color='grey')),
    xaxis= dict(title_font=dict(size=18, family='serif', color='black'), tickfont=dict(size=14, family='serif')), 
    yaxis= dict(title_font=dict(size=16, family='serif', color='black'), tickfont=dict(size=14, family='serif'))) 
    return st.plotly_chart(fig, theme="streamlit", use_container_width=True)

def feature_count(column_name):
    count = df[f"{column_name}"].value_counts().rename_axis(f"{column_name}").reset_index(name='count').sort_values(by='count', ascending=False)
    return count

def unique(column_name):
    unique_values = df[f"{column_name}"].drop_duplicates().reset_index(drop=True).sort_values()
    unique_values =  list(unique_values)
    unique_values.insert(0,'')
    return unique_values

def country_wise_count(df, country, column_name):
    df1 = df[df['Country'] == country]
    df2 = df1.groupby(column_name, as_index=False)['Country'].count().rename(columns={'Country': f'{column_name}_count'})
    df2 = df2.sort_values(f'{column_name}_count', ascending=False).reset_index(drop=True)
    return df2

def type_wise_stay(df,country,column_name1,column_name2):
    df1 = df[df['Country'] == country]
    df2 = df1.groupby(column_name1, as_index=False)[column_name2].sum()
    df2 = df2.sort_values(column_name2, ascending=False).reset_index(drop=True)
    return df2

def country_property_wise_count(df, country,property, column_name):
    df1 = df[(df['Country'] == country) & (df['Property_type'] == f'{property}')]
    df2 = df1.groupby(column_name, as_index=False)['Country'].count().rename(columns={'Country': f'{column_name}_count'})
    df2 = df2.sort_values(f'{column_name}_count', ascending=False).reset_index(drop=True)
    return df2

def country_property_room_wise_count(df, country,property,room, column_name):
    df1 = df[(df['Country'] == country) & (df['Property_type'] == f'{property}') & (df['Room_type'] == f'{room}')]
    df2 = df1.groupby(column_name, as_index=False)['Country'].count().rename(columns={'Country': f'{column_name}_count'})
    df2 = df2.sort_values(f'{column_name}_count', ascending=False).reset_index(drop=True)
    return df2

def country_property_room_bed_type(df, country, property_type, room_type, column_name):
    df1 = df[(df['Country'] == country) & (df['Property_type'] == property_type) & (df['Room_type'] == room_type)]
    df2 = df1.groupby('Bed_type', as_index=False)[column_name].mean().round(2)
    df2 = df2.sort_values(by=column_name, ascending=False).reset_index(drop=True)
    return df2

def country_property_room_host(df, country, property_type, room_type, column_name):
    df1 = df[(df['Country'] == country) & (df['Property_type'] == property_type) & (df['Room_type'] == room_type)]
    df2 = df1.groupby('Host_name', as_index=False)[column_name].sum()
    df2 = df2.sort_values(by=column_name, ascending=False).reset_index(drop=True).iloc[0:10]
    return df2

def country_property_room_host_neighbourhood(df, country, property_type, room_type, column_name):
    df1 = df[(df['Country'] == country) & (df['Property_type'] == property_type) & (df['Room_type'] == room_type)]
    df2 = df1.groupby('Host_neighbourhood', as_index=False)[column_name].count()
    df2 = df2.sort_values(by=column_name, ascending=False).reset_index(drop=True).iloc[0:10]
    return df2


st.set_page_config(page_title='AirBnb Analysis', layout='wide')

st.markdown(f'''<h1 style="text-align:center; color: #d9138a">AirBnb Data Analysis<br>
            Travel Industry, Property Management and Tourism</h1>''', unsafe_allow_html=True)

select_menu = option_menu(None, ["About AirBnb", "AirBnb World","AirBnb Exploration"],
                       icons=["clipboard2-data", "cloud-download", "file-earmark-plus", "trash"],orientation="horizontal")

df = pd.read_csv("D:\\Airbnb Dataset\\airbnb_data.csv")

if select_menu == "About AirBnb":
    st.markdown(' - Airbnb, as in :red[**Air Bed and Breakfast**], is a service that lets property owners rent out their spaces to travelers looking for a place to stay')
    st.markdown(' - Airbnb is an American San Francisco-based company operating an online marketplace for short and long-term homestays and experiences.')
    st.markdown(' - The company acts as a broker and charges a commission from each booking.')


if select_menu == "AirBnb World":
    df = pd.read_csv("D:\\Airbnb Dataset\\airbnb_data.csv")
    st.subheader("Airbnb Analysis in Map view")
    df_ll = df.rename(columns={'Longitude':'lon', 'Latitude':'lat'})
    st.map(df_ll, color='#d9138a')

    st.subheader("Airbnb Analysis in All listed Countries - Average Price Wise")
    country_price_df = df.groupby('Country', as_index=False)['Price'].mean()
    fig = px.scatter_geo(country_price_df, locations = 'Country', color = 'Price', hover_data='Price', 
                        locationmode = 'country names', size = 'Price', color_continuous_scale = 'sunsetdark')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    st.subheader("Airbnb Analysis in All listed Countries - Average Review Score Rating Wise")
    country_rating_df = df.groupby('Country', as_index=False)['Review_scores_rating'].mean()
    fig = px.scatter_geo(country_rating_df, locations = 'Country', color = 'Review_scores_rating', hover_data='Review_scores_rating', 
                        locationmode = 'country names', size = 'Review_scores_rating', color_continuous_scale = 'sunsetdark')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)




if select_menu == "AirBnb Exploration":
    explore1 , eplore2, explore3  = st.tabs(['Overview','Overall Insights', 'Deeper Insights'])
    
    with explore1:
        country_count = feature_count('Country')
        bar_plot(country_count, 'Country', 'count', 'Countries listed with AirBnb and their Listing Counts', 'Count of AirBnb in Each Country', 'AirBnb Countries')
            
        property_count = feature_count('Property_type')
        bar_plot(property_count, 'Property_type', 'count', 'Different Types of Property with Airbnb','Count of Property Type','Highest Property Types')       
            
        room, bed = st.columns(2)
        with room:
            room_count = feature_count('Room_type')
            bar_plot(room_count, 'count', 'Room_type', 'Different Room Types Available in AirBnb','Count of Room Type','Room Types')
            
        with bed:
            bed_count = feature_count('Bed_type')
            bar_plot(bed_count, 'count', 'Bed_type', 'Different Bed Types Available in AirBnb','Count of Bed Type','Bed Types')

        with st.expander('**Tabular Count View of Features**'):
            a1,a2 = st.columns(2)
            with a1:
                st.table(country_count.style.background_gradient(cmap = "plasma"))
                st.table(room_count.style.background_gradient(cmap = "plasma"))
                st.table(bed_count.style.background_gradient(cmap = "plasma"))
            with a2:
                st.table(property_count.style.background_gradient(cmap = "plasma"))


    with eplore2:
        s1,s2,s3 = st.columns(3)
        with s1:
            select_country = st.selectbox('Select Country', unique('Country'))
            show_by_country = st.button('**Show by Country**')
        with s2:
            select_property_type = st.selectbox('Select Property Type', unique('Property_type'))
            show_by_property = st.button('**Show by Property type**')
        with s3:
            select_room_type = st.selectbox('Select Room Type', unique('Room_type'))
            show_by_room = st.button('**Show by Room type**')
        
        if select_country != '' and show_by_country:
            country_property = country_wise_count(df,f'{select_country}','Property_type')
            bar_plot(country_property, 'Property_type_count', 'Property_type', f'Property type counts in {select_country}','Property type count', 'Property type')
            sc1,sc2 = st.columns(2)
            with sc1:
                country_room = country_wise_count(df,f'{select_country}','Room_type')
                bar_plot(country_room, 'Room_type_count', 'Room_type', f'Room type counts in {select_country}','Room type count', 'Room type')
            with sc2:
                country_bed = country_wise_count(df,f'{select_country}','Bed_type')
                bar_plot(country_bed, 'Bed_type_count', 'Bed_type', f'Bed type counts in {select_country}','Bed type count', 'Bed type')

            with st.expander('**Tabular Count View of Features**'):
                c1,c2 = st.columns(2)
                with c1:
                    st.table(country_property.style.background_gradient(cmap='plasma', axis=0))
                with c2:
                    st.table(country_room.style.background_gradient(cmap='plasma', axis=0))
                    st.table(country_bed.style.background_gradient(cmap='plasma', axis=0))
            
        if select_country != '' and select_property_type  != '' and show_by_property:
            sp1,sp2 = st.columns(2)
            with sp1:
                property_room = country_property_wise_count(df,f'{select_country}',f'{select_property_type}','Room_type')
                bar_plot(property_room, 'Room_type_count', 'Room_type', f"Room type counts in {select_country}'s {select_property_type}",'Room type count', 'Room type')
            with sp2:
                property_bed = country_property_wise_count(df,f'{select_country}',f'{select_property_type}','Bed_type')
                bar_plot(property_bed, 'Bed_type_count', 'Bed_type', f"Bed type counts in {select_country}'s {select_property_type}",'Bed type count', 'Bed type')

            with st.expander('**Tabular Count View of Features**'):
                c1,c2 = st.columns(2)
                with c1:
                    st.table(property_room.style.background_gradient(cmap='plasma', axis=0))
                    
                with c2:
                    st.table(property_bed.style.background_gradient(cmap='plasma', axis=0))

        if select_country != '' and select_property_type != '' and select_room_type != '' and show_by_room:
            room_bed = country_property_room_wise_count(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Bed_type')
            bar_plot(room_bed, 'Bed_type_count', 'Bed_type', f"Bed type counts in {select_country}'s {select_property_type}-{select_room_type}",'Bed type count', 'Bed type')

            with st.expander('**Tabular Count View of Features**'):
                st.table(room_bed.style.background_gradient(cmap='plasma', axis=0))

    with explore3:
        s1,s2,s3 = st.columns(3)
        with s1:
            select_country = st.selectbox('Select Country', unique('Country'), key='sc')
        with s2:
            select_property_type = st.selectbox('Select Property Type', unique('Property_type'), key='sp')
        with s3:
            select_room_type = st.selectbox('Select Room Type', unique('Room_type'),key='sr')
        
        if select_country != '' and select_property_type != '' and select_room_type != '': 
            st.subheader(':red[Airbnb Homestay Facilities and its count - Bed type wise]')  
            cpr1,cpr2 = st.columns(2)
            with cpr1:
                st.subheader('Average Minimum Night Stay Counts')
                min_night = country_property_room_bed_type(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Minimum_nights')
                st.table(min_night.style.background_gradient(cmap='plasma', axis=0).format({'Minimum_nights': '{:.2f}'}))
            with cpr2:
                st.subheader('Average Maximum Night Stay Counts')
                max_night = country_property_room_bed_type(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Maximum_nights')
                st.table(max_night.style.background_gradient(cmap='plasma', axis=0).format({'Maximum_nights': '{:.2f}'}))
            
            cpr3,cpr4 = st.columns(2)
            with cpr3:            
                st.subheader('Average Number of Allowed Accomodates Count')
                accomodates = country_property_room_bed_type(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Accomodates')
                st.table(accomodates.style.background_gradient(cmap='plasma', axis=0).format({'Accomodates': '{:.2f}'}))
            with cpr4:
                st.subheader('Average Cleaning Fees')
                cleaning_fee = country_property_room_bed_type(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Cleaning_fee')
                st.table(cleaning_fee.style.background_gradient(cmap='plasma', axis=0).format({'Cleaning_fee': '{:.2f}'}))
            
            cpr5,cpr6 = st.columns(2)
            with cpr5:
                st.subheader('Average Number of Extra People Allowed')
                extravailability_people = country_property_room_bed_type(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Extra_people')
                st.table(extravailability_people.style.background_gradient(cmap='plasma', axis=0).format({'Extra_people': '{:.2f}'}))
            with cpr6:
                st.subheader('Average Number of Guests Included')
                guestes = country_property_room_bed_type(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Guests_included')
                st.table(guestes.style.background_gradient(cmap='plasma', axis=0).format({'Guests_included': '{:.2f}'}))
            
            cpr7,cpr8 = st.columns(2)
            with cpr7:
                st.subheader('Average Amount of Security Deposit')
                security_deposit = country_property_room_bed_type(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Security_deposit')
                st.table(security_deposit.style.background_gradient(cmap='plasma', axis=0).format({'Security_deposit': '{:.2f}'}))
            with cpr8:
                st.subheader('Average Review Score Ratings')
                reviews = country_property_room_bed_type(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','No_of_reviews')
                st.table(reviews.style.background_gradient(cmap='plasma', axis=0).format({'No_of_reviews': '{:.2f}'}))
            
            st.subheader(':red[Airbnb Host Analysis]')  
            pie1,pie2 = st.columns(2)
            with pie1:
                cancellation = country_property_room_wise_count(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Cancellation_policy')
                pie_plot(cancellation,'Cancellation_policy','Cancellation_policy_count','Overall Cancellation Policy Room Type wise')
            with pie2:
                host_identity = country_property_room_wise_count(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Host_identity_verified')
                pie_plot(host_identity,'Host_identity_verified','Host_identity_verified_count','Overall Host Identity Verificaiton Room Type wise')

            pie3,pie4 = st.columns(2)
            with pie3:
                location_exact = country_property_room_wise_count(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Is_location_exact')
                pie_plot(location_exact,'Is_location_exact','Is_location_exact_count','Probality of Exact Location Room Type wise')
            with pie4:
                host_identity = country_property_room_wise_count(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Host_response_time')
                pie_plot(host_identity,'Host_response_time','Host_response_time_count',' Overall Number of Host Identity Verification Room Type wise')

            bar1,bar2 = st.columns(2)
            with bar1:   
                host_rating = country_property_room_host(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Review_scores_rating')
                bar_plot(host_rating,  'Review_scores_rating','Host_name', 'Top Hosts with highest Reviews - Ratings','Review Scores Ratings', 'Top 10 Host Name')
            with bar2:
                host_communication = country_property_room_host(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Review_scores_communication')
                bar_plot(host_communication, 'Review_scores_communication', 'Host_name', 'Top Hosts with highest Reviews - Communication','Review Scores Communication', 'Top 10 Host Name')

            tab1,tab2 = st.columns(2)
            with tab1:
                st.subheader('Top Hosts with Highest Number of Reviews')
                host_review = country_property_room_host(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','No_of_reviews')
                st.table(host_review.style.background_gradient(cmap='plasma', axis=0))
            with tab2:
                st.subheader('Top Host Neighbourhood and its Host Counts')
                host_name = country_property_room_host_neighbourhood(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Host_name')
                st.table(host_name.style.background_gradient(cmap='plasma', axis=0))

            
            st.subheader(':red[Airbnb Homestays Availability Analysis]')  
            availability_30 = country_property_room_bed_type(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Availability_30')
            availability_60 = country_property_room_bed_type(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Availability_60')
            availability_90 = country_property_room_bed_type(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Availability_90')
            availability_365 = country_property_room_bed_type(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Availability_365')
            
            dfa = pd.merge(availability_30, availability_60, on='Bed_type')
            dfa = pd.merge(dfa, availability_90, on='Bed_type')
            dfa = pd.merge(dfa, availability_365, on='Bed_type')
            st.table(dfa.style.background_gradient(cmap='plasma', axis=0).format({'Availability_30': '{:.2f}', 'Availability_60': '{:.2f}', 'Availability_90': '{:.2f}', 'Availability_365': '{:.2f}'}))

            st.subheader(':red[Airbnb Homestays Review Score Analysis]')  
            cleanliness = country_property_room_bed_type(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Review_scores_cleanliness')
            location = country_property_room_bed_type(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Review_scores_location')
            communication = country_property_room_bed_type(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Review_scores_communication')
            rating = country_property_room_bed_type(df,f'{select_country}',f'{select_property_type}',f'{select_room_type}','Review_scores_rating')

            dfr = pd.merge(cleanliness, location, on='Bed_type')
            dfr = pd.merge(dfr, communication, on='Bed_type')
            dfr = pd.merge(dfr, rating, on='Bed_type')
            st.table(dfr.style.background_gradient(cmap='plasma', axis=0).format({'Review_scores_cleanliness': '{:.2f}', 'Review_scores_location': '{:.2f}', 'Review_scores_communication': '{:.2f}', 'Review_scores_rating': '{:.2f}'}))


            st.title(':violet[Thank You !!!]')
