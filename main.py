import streamlit as st
import matplotlib.pyplot as plt
from scrap import head_to_head_data,League_Standing
from Storage import store_head_to_head_matches,store_league_table
from datetime import datetime


st.set_page_config(
    page_title="Football Data Analysis",
    page_icon="⚽",
    layout="wide"
)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Head-to-Head Analysis", "League Table Analysis"])

teams1_display_to_value = {
    "Arsenal": "arsenal",
    "Chelsea": "chelsea",
    "Aston Villa": "aston-villa",
    "AFC Bournemouth": "afc-bournemouth",
    "Brentford": "brentford",
    "Brighton and Hove Albion": "brighton-and-hove-albion",
    "Crystal Palace": "crystal-palace",
    "Everton": "everton",
    "Fulham": "fulham",
    "Ipswich Town": "ipswich-town",
    "Leicester City": "leicester-city",
    "Liverpool": "liverpool",
    "Manchester City": "manchester-city",
    "Manchester United": "manchester-united",
    "Newcastle United": "newcastle-united",
    "Nottingham Forest": "nottingham-forest",
    "Southampton": "southampton",
    "Tottenham Hotspur": "tottenham-hotspur",
    "West Ham United": "west-ham-united",
    "Wolverhampton Wanderers": "wolverhampton-wanderers"
}


teams2_display_to_value = {
    "Arsenal": "Arsenal",
    "Aston Villa": "Aston%20Villa",
    "Brentford": "Brentford",
    "Brighton and Hove Albion": "Brighton%20and%20Hove%20Albion",
    "Chelsea": "Chelsea",
    "Chester City": "Chester%20City",
    "Crystal Palace": "Crystal%20Palace",
    "Everton": "Everton",
    "Fulham": "Fulham",
    "Ipswich Town": "Ipswich%20Town",
    "Leicester City": "Leicester%20City",
    "Liverpool": "Liverpool",
    "Manchester City": "Manchester%20City",
    "Manchester United": "Manchester%20United",
    "Tottenham Hotspur": "Tottenham%20Hotspur",
    "Wolverhampton Wanderers": "Wolverhampton%20Wanderers",
    "AFC Bournemouth": "AFC%20Bournemouth",
    "Newcastle United": "Newcastle%20United",
    "Nottingham Forest": "Nottingham%20Forest",
    "Southampton": "Southampton",
    "West Ham United": "West%20Ham%20United"
}



if page == "Head-to-Head Analysis":
    st.header("Head-to-Head Match Analysis")
    
    # Input fields
    col1, col2 = st.columns(2)
    with col1:
        team1_select = st.selectbox("Enter Team 1",list(teams1_display_to_value.keys()))
        team1 = teams1_display_to_value[team1_select]

    with col2:
        team2_select = st.selectbox("Enter Team 2",list(teams2_display_to_value.keys()))
        team2 = teams2_display_to_value[team2_select]


    @st.cache_data
    def fetch_head_to_head(team1, team2):
        matches, matches_list = head_to_head_data(team1, team2)
        return matches, matches_list
    if st.button("Analyze Head-to-Head"):
        
            if team1_select==team2_select:
                 st.warning("Please enter two different teams.")
            else:
                try:
                    with st.spinner("Fetching match data..."):
                        # Get matches using the scraper
                        matches, matches_list = fetch_head_to_head(team1, team2)
                        
                        # Store the matches in MongoDB
                        store_head_to_head_matches(team1, team2, matches_list)
                    
                        # Display the matches
                        st.subheader(f"Head-to-Head: {team1_select} vs {team2_select}")
                        if not matches.empty:
                           
                            st.dataframe(matches)
                        
                            # Add some statistics
                            total_matches = len(matches)
                            team1_wins = (matches['Winner'] == team1_select).sum()
                            team2_wins = (matches['Winner'] == team2_select).sum()
                            draws = (matches['Winner'] == "Draw").sum()

                        
                            st.subheader("Statistics")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Matches", total_matches)
                            with col2:
                                st.metric(f"{team1_select} Wins", team1_wins)
                            with col3:
                                st.metric(f"{team2_select} Wins", team2_wins)

                            with st.expander("Win/Loss/Draw Pie Chart"):
                                result = matches["Winner"].value_counts()

                                fig, ax = plt.subplots(figsize=(6, 6))
                                ax.pie(result, labels=result.index, autopct="%1.1f%%", startangle=140)
                                ax.set_title(f"Head-to-Head Results: {team1_select} vs {team2_select}")
                                st.pyplot(fig)
                                st.divider()

                            with st.expander("Home vs Away Advantage"):
                                home_wins = (matches['Winner'] == matches['HomeTeam']).sum()
                                away_wins = (matches['Winner'] == matches['AwayTeam']).sum()
                                draws = (matches['Winner'] == 'Draw').sum()
                                labels = ['Home Win', 'Away Win', 'Draw']
                                values = [home_wins, away_wins, draws]

                                fig2, ax2 = plt.subplots()
                                ax2.bar(labels, values, color=['navy', 'darkred', 'gray'])
                                ax2.set_title('Home vs Away Wins')
                                ax2.set_xlabel('Result Type')
                                ax2.set_ylabel('Count')
                                st.pyplot(fig2)
                                st.divider()



                            
                        else:
                            st.warning("No matches found between these teams.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                  
elif page == "League Table Analysis":
    st.header("League Table Analysis")
    
    # Date input
    date = st.date_input("Select Date", datetime.now())
    
    @st.cache_data
    def fetch_League_Table(date):
        rank_list,ranks_dic = League_Standing(date)
        return  rank_list,ranks_dic
    
    if st.button("Get League Table"):
        try:
            with st.spinner("Fetching league table data..."):
                # Format date for the scraper
                formatted_date = date.strftime("%d-%B-%Y")
                
                # Get league table using the scraper
                rank_list,ranks_dic = fetch_League_Table(formatted_date)
                
                # Store the league table in MongoDB
                store_league_table(formatted_date,ranks_dic)
                
                # Display the league table
                st.subheader(f"League Table for {date.strftime('%d %B %Y')}")
                if not rank_list.empty:
                    # Convert to DataFrame for better display
                    
                    st.dataframe(rank_list)
                    
                    # Add some statistics
                    st.subheader("League Statistics")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Top Team", rank_list.iloc[0]['Team name'])
                    with col2:
                        st.metric("Most Goals For", rank_list.loc[rank_list['Goals for'].idxmax()]['Team name'])
                    with col3:
                        st.metric("Most Points", rank_list.loc[rank_list['Points'].idxmax()]['Team name'])

                    with st.expander("Bar Chart of Team Points"):
                        fig, ax = plt.subplots(figsize=(23, 6))
                        ax.bar(rank_list["Team name"],rank_list["Points"])
                        ax.set_xlabel("Teams")
                        ax.set_ylabel("Points")
                        ax.set_title("Teams point")
                        st.pyplot(fig)
                        st.divider()

                    with st.expander("Home vs Away Advantage"):
                          

                        fig2, ax2 = plt.subplots()
                        rank_list.plot(x='Team name', y=['Goals for', 'Goals in'], kind='bar', figsize=(12,6),ax=ax2)
                        ax2.set_title("Goals Scored vs Conceded")
                        plt.ylabel("Goals")
                        plt.ylim(bottom=0)
                        st.pyplot(fig2)
                        st.divider()

                else:
                    st.warning("No league table data found for this date.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


# Add some styling
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
    }
    .stTextInput>div>div>input {
        background-color: #f0f2f6;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True) 
