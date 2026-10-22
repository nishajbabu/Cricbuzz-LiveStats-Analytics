"""
Administrative CRUD Page for Managing Player Records
"""
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.crud_service import get_all_players, get_teams, add_player, update_player, delete_player

st.set_page_config(page_title="CRUD Operations - Cricbuzz LiveStats", layout="wide")

st.title("⚙️ Administrative Data Management (CRUD Portal)")
st.write("Create, Read, Update, and Delete cricket records directly in the SQL database.")

teams_dict = get_teams()
roles_list = ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"]
bat_styles = ["Right Handed", "Left Handed"]
bowl_styles = ["Right-arm fast", "Right-arm fast-medium", "Right-arm medium", "Right-arm offbreak", "Right-arm legbreak", "Left-arm fast", "Slow left-arm orthodox", "None"]

tab_read, tab_create, tab_update, tab_delete = st.tabs(["📋 View Players (Read)", "➕ Add Player (Create)", "✏️ Update Player (Update)", "🗑️ Delete Player (Delete)"])

# 1. READ
with tab_read:
    st.subheader("Current Player Roster")
    df_players = get_all_players()
    st.dataframe(df_players, use_container_width=True)

# 2. CREATE
with tab_create:
    st.subheader("Add a New Player to Database")
    with st.form("add_player_form"):
        name_input = st.text_input("Full Name *")
        team_select = st.selectbox("Select Team *", list(teams_dict.keys()))
        role_select = st.selectbox("Playing Role *", roles_list)
        bat_select = st.selectbox("Batting Style *", bat_styles)
        bowl_select = st.selectbox("Bowling Style *", bowl_styles)
        submit_add = st.form_submit_button("➕ Register Player")

        if submit_add:
            if not name_input.strip():
                st.error("Player name cannot be empty!")
            else:
                team_id = teams_dict[team_select]
                add_player(name_input.strip(), team_id, role_select, bat_select, bowl_select)
                st.success(f"Player '{name_input}' successfully added to database!")
                st.rerun()

# 3. UPDATE
with tab_update:
    st.subheader("Edit Existing Player Details")
    df_players = get_all_players()
    player_options = dict(zip(df_players['player_id'], df_players['full_name'] + " (" + df_players['team_name'] + ")"))
    
    selected_p_id = st.selectbox("Select Player to Edit:", list(player_options.keys()), format_func=lambda x: player_options[x])

    if selected_p_id:
        p_row = df_players[df_players['player_id'] == selected_p_id].iloc[0]
        with st.form("edit_player_form"):
            edit_name = st.text_input("Full Name", value=p_row['full_name'])
            edit_team = st.selectbox("Team", list(teams_dict.keys()), index=list(teams_dict.keys()).index(p_row['team_name']) if p_row['team_name'] in teams_dict else 0)
            edit_role = st.selectbox("Role", roles_list, index=roles_list.index(p_row['playing_role']) if p_row['playing_role'] in roles_list else 0)
            edit_bat = st.selectbox("Batting Style", bat_styles, index=bat_styles.index(p_row['batting_style']) if p_row['batting_style'] in bat_styles else 0)
            edit_bowl = st.selectbox("Bowling Style", bowl_styles, index=bowl_styles.index(p_row['bowling_style']) if p_row['bowling_style'] in bowl_styles else 0)
            submit_update = st.form_submit_button("💾 Save Changes")

            if submit_update:
                update_player(selected_p_id, edit_name.strip(), teams_dict[edit_team], edit_role, edit_bat, edit_bowl)
                st.success(f"Player ID {selected_p_id} updated successfully!")
                st.rerun()

# 4. DELETE
with tab_delete:
    st.subheader("Remove Player from Database")
    df_players = get_all_players()
    player_del_options = dict(zip(df_players['player_id'], df_players['full_name'] + " (" + df_players['team_name'] + ")"))

    del_p_id = st.selectbox("Select Player to Delete:", list(player_del_options.keys()), format_func=lambda x: player_del_options[x], key="del_select")
    
    st.warning("⚠️ Deleting a player record will permanently remove them from the database.")
    if st.button("🗑️ Permanently Delete Player", type="primary"):
        delete_player(del_p_id)
        st.success(f"Player ID {del_p_id} successfully deleted!")
        st.rerun()