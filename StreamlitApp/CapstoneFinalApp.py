import pandas as pd
import streamlit as st
import os

# for some reason renderer was empty

current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the file path
file_path = os.path.join(current_dir, 'DataFrameForAPI_newnames.csv')
df = pd.read_csv(file_path)

file_path2 = os.path.join(current_dir, 'World_Rank_Plot.csv')
df2 = pd.read_csv(file_path2)


# Set page configuration
st.set_page_config(
    page_title="Doctorate Discover",
    page_icon=":mortar_board:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Add custom CSS
css = """
body {
    background-image: url('https://example.com/background.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
.sidebar .sidebar-content {
    background-color: #f8f9fa;
    box-shadow: inset -1px 0px 0px rgba(0, 0, 0, 0.1);
}
}
"""

# Map function
import plotly.express as px

def generate_map(df):
    # Define a colormap based on the rank values
    ranks = df['rank']
    colorblind_friendly_colors = ['#4A90E2', '#50E3C2', '#F5A623', '#D0021B', '#9013FE']


    # Create a map object using Plotly Express
    fig = px.scatter_geo(
        df,
        lat="Latitude",
        lon="Longitude",
        hover_name="name",
        color="rank",
        color_continuous_scale=colorblind_friendly_colors,
        range_color=(ranks.min(), ranks.max()),
        projection="natural earth",
        #title="University Locations by World Rank",
    )
    
    fig.update_geos(
        center=dict(lat=20, lon=-20), # Center the map at the specified coordinates
        projection_scale=2 # Set the zoom level
    )
    fig.update_traces(marker=dict(sizemin=40))
    
    fig.update_layout(
    autosize=False,
    width=650,
    height=400,
    )
    
    # Return the map object
    return fig

school_map = generate_map(df2)


def generate_map2(df, criteria):
    # Define a colormap based on the criteria values
    values = df[criteria].sort_values()
    colorblind_friendly_colors = ['#4A90E2', '#50E3C2', '#F5A623', '#D0021B', '#9013FE']

    # Remove duplicates based on location and study_name
    df = df.drop_duplicates(subset=['LATITUDE', 'LONGITUDE', 'University'])

    # Format criteria text
    criteria_text = ' '.join(word.capitalize() for word in criteria.split('_'))

    # Create a map object using Plotly Express
    fig = px.scatter_geo(
        df,
        lat="LATITUDE",
        lon="LONGITUDE",
        hover_name="University",
        size=criteria,
        color=criteria,
        color_continuous_scale=colorblind_friendly_colors,
        range_color=(values.min(), values.max()),
        projection="natural earth",
        title=f"Schools by {criteria_text}",
        text="University",
        custom_data=[criteria],
    )

    # Customize hover information
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>{criteria_text}: %{customdata[0]}"
    )
    
    fig.update_geos(
        center=dict(lat=30, lon=-95), # Center the map at the specified coordinates
        projection_scale=3.5 # Set the zoom level
    )


    # Return the map object
    return fig

# Generate the map
#school_map = generate_map2(df2, "example_criteria")
#school_map.show()



# Apply custom CSS
st.write(f'<style>{css}</style>', unsafe_allow_html=True)


# Sidebar   


# Sidebar for selection criteria
with st.sidebar:
    st.write("## Select your Field!")
   
    selected_field = st.selectbox(" Field:", df['field'].unique())
    st.markdown('<span style="font-size: 10px;">Source: [https://www.phdportal.com](https://www.phdportal.com)</span>', unsafe_allow_html=True)
    
    st.markdown("---")

    field_info = df[df['field'] == selected_field][['PostPhdSalary', 'PostPhdEmploy']]
    st.write(f"Field salary post PhD: ${field_info['PostPhdSalary'].iloc[0]}")
    st.write(f"Field employment rate: {field_info['PostPhdEmploy'].iloc[0]}%")
    st.markdown('<span style="font-size: 10px;">Source: [https://ncses.nsf.gov/](https://ncses.nsf.gov/)</span>', unsafe_allow_html=True)
    
    st.markdown("---")

    st.write("## General Criteria")
    criteria = 'World Rank', 'USA Rank', 'Glassdoor Star', 'Tuition', 'Salary/Stipend', 'State Avg Salary/Stipend'
    criteria_field = st.selectbox("Pick Your Criteria:", (criteria))
    
    st.markdown("---")
    
    st.write("## Weighted Criteria")
    
    default_states = sorted(df['State'].fillna('Unknown').unique())
    selected_states = st.sidebar.multiselect('Select States:', default_states, default=[])
    if not selected_states:  
        selected_states = default_states  # consider all states selected
   
    weight_rank = st.slider("Weight for Rank:", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
    weight_tuition = st.slider("Weight for Tuition:", min_value=0.0, max_value=1.0, value=0.3, step=0.1)
    weight_salary = st.slider("Weight for Salary:", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
    
    if (weight_rank + weight_tuition + weight_salary) != 1.0:
        st.sidebar.error("Please adjust the weights so their total equals to 1.")


        
        
        

# Main Page    
st.title("Doctorate Discover")
st.markdown("TDI Capstone Project by Austyn Matheson")
st.markdown("---")

# Set up layout
col1, col2 = st.columns([1.5, 2.5])

# Left column (title and bullet points)
with col1:
    st.write("* **Streamlines** the US grad school search process.")
    st.write("* Search by ranking, stipend, cost of living, and inclusivity.")
    st.write("* Provides program information with a **user-friendly** interface.")
    st.write("* Save time and reduce stress with informed decision-making.")

# Right column (map)
with col2:
    st.write("### The location of the world's top universities")
    st.markdown('<span style="font-size: 10px;">Source: [https://www.timeshighereducation.com/world-university-rankings/2023/world-ranking](https://www.timeshighereducation.com/world-university-rankings/2023/world-ranking)</span>', unsafe_allow_html=True)
    st.components.v1.html(school_map._repr_html_(), height=400)
    
    
st.markdown("---")



df = df.rename(columns={'study_name': 'Project Title', 'summary': 'Description', 'WorldRank': 'World Rank', 
                        'USARank': 'USA Rank', 'Salary_avg': 'Salary/Stipend', 'State_Avg_Salary': 'State Avg Salary/Stipend','Star': 'Glassdoor Star'})       

# Show top 20 entries with highest stipend and stipend-field-state for selected field
if selected_field:
    st.write("### Filtered Programs:")
    st.markdown('<span style="font-size: 10px;">Source for USA University Rankings: [https://www.4icu.org/us/](https://www.4icu.org/us/)</span>', unsafe_allow_html=True)
    if (criteria_field == "World Rank") | (criteria_field == "USA Rank") | (criteria_field == "Tuition"):
        filtered_df = df[df['field'] == selected_field].sort_values(by=criteria_field, ascending=True).head(40)
        selected_cols = [criteria_field, 'Project Title', 'University', 'Description', 'Duration', 'City', 'State']
        st.write(filtered_df[selected_cols])
    else:
        filtered_df = df[df['field'] == selected_field].sort_values(by=criteria_field, ascending=False).head(40)
        selected_cols = [criteria_field, 'Project Title', 'University', 'Description', 'Duration', 'City', 'State']
        st.write(filtered_df[selected_cols])
    
    st.markdown("---")
   
    st.write("### Annual Cost of Living for One Adult:")
    st.markdown('<span style="font-size: 10px;">Source for USA living costs: [https://livingwage.mit.edu/](https://livingwage.mit.edu/)</span>', unsafe_allow_html=True)
    st.markdown('<span style="font-size: 10px;">Source for PhD Stipend/Salaries: [http://glassdoor.com](http://glassdoor.com)</span>', unsafe_allow_html=True)
    
    if (criteria_field == "World Rank") | (criteria_field == "USA Rank") | (criteria_field == "Tuition"):
        filtered_df = df[df['field'] == selected_field].sort_values(by=criteria_field, ascending=True).head(15)
    else:
        filtered_df = df[df['field'] == selected_field].sort_values(by=criteria_field, ascending=False).head(15)
    selected_cols = ['Project Title', 'University', 'Tuition', 'Salary/Stipend', 'State Avg Salary/Stipend', 'Required Income', 'Food', 'Housing', 'Transportation','Medical', 'Enough Income']
    st.write(filtered_df[selected_cols])
    st.components.v1.html(generate_map2(filtered_df, criteria_field)._repr_html_(), height=600)
    
    
st.markdown("---")  
    
if selected_states: 
    
    st.write("### Your Perfect Program:")
    #df["score"] = df["WorldRank"]*weight_rank + df["Tuition"]*weight_tuition + df["Salary_avg"]*weight_salary
    
    # Normalize usa rank, tuition, salary
    df["WorldRank_norm"] = (df["USA Rank"] - df["USA Rank"].min()) / (df["USA Rank"].max() - df["USA Rank"].min())
    df["Tuition_norm"] = (df["Tuition"] - df["Tuition"].min()) / (df["Tuition"].max() - df["Tuition"].min())
    df["Salary_avg_norm"] = (df["Salary/Stipend"] - df["Salary/Stipend"].min()) / (df["Salary/Stipend"].max() - df["Salary/Stipend"].min())

    # Now compute determine the score, make sure to inver the worl_rank because it is better to be lower
    df["score"] = (1 - df["WorldRank_norm"])*weight_rank + (1-df["Tuition_norm"])*weight_tuition + df["Salary_avg_norm"]*weight_salary
    
    
    filt_df = df[df['field'] == selected_field].sort_values(by="score", ascending=False).head(5)
    filt_df = filt_df[filt_df['State'].isin(selected_states)]
    
    sel_cols = ['USA Rank', 'Tuition', 'Salary/Stipend', 'Required Income', 'Enough Income', 'Project Title', 'University', 'Description', 'Duration', 'City', 'State']
    st.write(filt_df[sel_cols])


    filtered_df = filtered_df.dropna(subset=['LATITUDE', 'LONGITUDE'])
   

    



import requests
import configparser
import tweepy

# Read the bearer token from the config file
config = configparser.ConfigParser()
config.read('config.ini')
bearer_token = config.get('twitter', 'bearer_token')

# Set up Streamlit app layout

st.markdown("---")

# Set up the client, not using authorisation here
client = tweepy.Client(bearer_token=bearer_token)

st.write("### PhD Opportunities on Twitter in the Last 7 Days!")
selected_field = st.selectbox("Field of Interest:", df['field'].unique())


keyword_path = os.path.join(current_dir, 'Twitter_Field_KeyWords.csv')

key_df = pd.read_csv(keyword_path)
keywords = key_df[key_df['Category'] == selected_field]['Keyword'].tolist()

query_keywords = ' OR '.join(keywords)
query = f'"phd opportunities" ({query_keywords})'

tweets = client.search_recent_tweets(
    query=query,
    expansions="author_id",
    user_fields="username",
    tweet_fields=["context_annotations", "created_at"],
    max_results=10,
)

# Create a dictionary to map user IDs to usernames
usernames = {user.id: user.username for user in tweets.includes["users"]}

tweet_list = []

for tweet in tweets.data:
    tweet_dict = {}
    tweet_dict["Username"] = usernames[tweet.author_id]
    tweet_dict["Text"] = tweet.text
    tweet_dict["Tweet URL"] = f"https://twitter.com/{usernames[tweet.author_id]}/status/{tweet.id}"
    tweet_dict["Created At"] = tweet.created_at
    tweet_list.append(tweet_dict)

# Define tabs
tabs = st.tabs(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

# Iterate over the tabs and display the tweet information
for i, (tweet, tab) in enumerate(zip(tweet_list, tabs)):
    with tab:
        st.markdown(f"**User:** @ {tweet['Username']}")
        st.markdown(f"**Tweet:** {tweet['Text']}")
        st.markdown(f"**Posted:** {tweet['Created At']}")
        st.write(tweet['Tweet URL'])


st.markdown("---")
    
st.write("### Next Steps")
st.write("* Learn more about our user to define features of importance")
st.write("* Use NLP to process the Twitter API to screen for those hard to find and quick to go PhD/Research Opportunities.")
st.write("* Scrape Thesis DataBases to collect names of PhD Scholars in order to identify trends in employment and success metrics (LinkedIn/ResearchGate)")


st.markdown("---")
    
st.write("### Thank you")
st.write("* austynmatheson@thedataincubator.com")
st.write("* https://www.linkedin.com/in/austynmatheson/.")
st.write("* find the project soon on: github.com/mathesoa")

