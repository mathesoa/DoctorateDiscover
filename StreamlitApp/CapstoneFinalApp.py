import pandas as pd
import streamlit as st
import os
import matplotlib.pyplot as plt
import seaborn as sns


# The function to make the map based on PhD Opportunities and criteria
from map_plot_functions import world_rank_map, phd_select_map, generate_box_plots, generate_affordability_box_plot

current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the file path
file_path = os.path.join(current_dir, 'DataFrameForAPI_newnames.csv')
df = pd.read_csv(file_path)
df = df.rename(columns={'study_name': 'Project Title', 'summary': 'Description', 'WorldRank': 'World Rank', 
                        'USARank': 'USA Rank', 'Salary_avg': 'Salary/Stipend', 'State_Avg_Salary': 'State Avg Salary/Stipend','Star': 'Glassdoor Star'})    

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





# Apply custom CSS
st.write(f'<style>{css}</style>', unsafe_allow_html=True)


# Setting up the sidebar selection criteria
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
    
    st.write("## Find your perfect PhD program, set the weight of importance")
    
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

    # here the map is generated
    school_map = world_rank_map(df2) 
    st.components.v1.html(school_map._repr_html_(), height=400)
    
    
st.markdown("---")



   

# Show field entries
if selected_field:
    st.write("### See the newest PhD Programs:")
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
        filtered_df = df[df['field'] == selected_field].sort_values(by=criteria_field, ascending=True).head(40)
    else:
        filtered_df = df[df['field'] == selected_field].sort_values(by=criteria_field, ascending=False).head(40)
    selected_cols = ['Project Title', 'University', 'Tuition', 'Salary/Stipend', 'State Avg Salary/Stipend', 'Required Income', 'Food', 'Housing', 'Transportation','Medical', 'Enough Income']
    st.write(filtered_df[selected_cols])
    
    st.components.v1.html(phd_select_map(filtered_df, criteria_field)._repr_html_(), height=600)

    
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
   

    




st.markdown("---")
    
st.write("### Next Steps")
st.write("* Learn more about our user to define features of importance")
st.write("* Use NLP to process the Twitter API to screen for those hard to find and quick to go PhD/Research Opportunities.")
st.write("* Scrape Thesis DataBases to collect names of PhD Scholars in order to identify trends in employment and success metrics (LinkedIn/ResearchGate)")


st.markdown("---")
    
st.write("### Thank you")
st.write("* austyn.matheson@gmail.com")
st.write("* https://www.linkedin.com/in/austynmatheson/.")
st.write("* find the project on: github.com/mathesoa/DoctorateDiscover")

st.markdown("---")
st.write("## Want to know more about your field or state? Check out the interactive graphics below!")

selected = st.selectbox("Check out the stats on your State or 'Field'", ("field", "State"))

if selected: 
    # Generate violin plots
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # Plot Salary/Stipend
    generate_box_plots(df, xcolumn=selected, ycolumn="Salary/Stipend", ax=axs[0, 0])
    axs[0, 0].set_title(f'Salary/Stipend by {selected}')

    # Plot Tuition
    generate_box_plots(df, xcolumn=selected, ycolumn="Tuition", ax=axs[0, 1])
    axs[0, 1].set_title(f'Tuition by {selected}')

    # Plot Glassdoor Star
    generate_box_plots(df, xcolumn=selected, ycolumn="Glassdoor Star", ax=axs[1, 0])
    axs[1, 0].set_title(f'Ranking by {selected}')

    # Plot Affordability
    generate_affordability_box_plot(df, xcolumn=selected, ax=axs[1, 1])
    axs[1, 1].set_title(f'Affordability (Salary - Tuition) by {selected}')

    plt.tight_layout()
    st.pyplot(fig)
