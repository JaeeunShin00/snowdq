import streamlit as st
import pandas as pd
# from streamlit_option_menu import option_menu
from snowflake_client import load_data
from utils import *
from streamlit_extras.switch_page_button import switch_page
import json
st.set_page_config(layout="wide",initial_sidebar_state="collapsed")
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)
# st.set_page_config(page_title="SnowDQ | Suites", page_icon="static/favicon.ico", layout="wide", initial_sidebar_state="collapsed")
navWithLogo()
suitsDf = load_data(st.secrets.DQ_TABLE.SUITE)

suitsDf['MODIFIED_DATE'] = pd.to_datetime(suitsDf['MODIFIED_DATE'])

suitsDf = suitsDf.sort_values(by='MODIFIED_DATE', ascending=False)

#TODO : create sort function for universal use.

 

 

 

suiteRulesDf = load_data(st.secrets.DQ_TABLE.SUITE_RULE)

col1,col2, = st.columns((9,1))

 

with col1:

    search = st.text_input("Search Suites",label_visibility="visible", placeholder="Search Suites...")

 

 

with col2:

    buttons()

    create_suite_button = st.button("Create Suites")

    if create_suite_button:

        switch_page("Create_suite")

# ############################################
if 'page' not in st.session_state:

    st.session_state.page = 1

 

 

 

# items_per_page = st.selectbox("Rows Per Page",[10,25,50],label_visibility="visible")

items_per_page = 10

if search:

    df = suitsDf[suitsDf['NAME'].str.contains(search, case=False)]

    page_data, total_pages = paginate_dataframe(df, st.session_state.page, items_per_page)

else:

    page_data, total_pages = paginate_dataframe(suitsDf, st.session_state.page, items_per_page)

 
for index, row in page_data.iterrows():

    col1, col2, col3, col4, col5, col6 = st.columns((2.0, 0.5, 1.1, 3, 2, 0.5))

    with col1:

        rule = page_data['NAME'][index]

        st.write(f"**{rule}**")

        st.write(page_data['DESCRIPTION'][index])

 

    with col2:

        st.write("**Owner**")

        owner = page_data["OWNER"][index]

        suite_owner_circle(owner[0].upper())

 

    with col3:

        st.write("**Used In Projects**")

        # category = page_data["CATEGORY"][index]

        suite_owner_circle("10")

        # st.write(f"**--**")

 

    with col4:

        st.write("**Applied Rules**")

        appliedRulesDf = suiteRulesDf[suiteRulesDf["GROUP_ID"]== page_data['ID'][index]]

        appliedRules = appliedRulesDf["RULE"].tolist()

        if appliedRules:

            suite_rule_background(appliedRules[0])

            if len(appliedRules) > 1:

                suite_rule_background(f"+{len(appliedRules) - 1}")

        else:

            suite_rule_background("None")

 

    with col5:

        st.write("**Tags**")

        tags = json.loads(page_data["TAGS"][index])

        if tags:

            suite_rule_background(tags[0])

            suite_rule_background(f"+{len(tags) - 1}")

        else:

            pass

            # suite_rule_background("None")

    with col6:
        def optionContainer(click, index):
            with stylable_container(key="container_with_border",
                css_styles="""{z-index: 9999999;
                background-color:    #1D4077;
                position: fixed;
                top: 20%;
                right: 02%;
                width: 20%;
                height: 35%;
                border: 3px solid blue;
                border: 1px solid rgba(39, 41, 53, 0.1);
                border-radius: 0.5rem;
                padding: calc(1em - 1px);}"""):
                with st.container():
                    View = st.button("View suite", key=f"View_button_{page_data['NAME'][index]}_{index}")
                    Update = st.button("Update suite", key=f"Update_button_{index}")
                    Delete = st.button("Delete suite", key=f"Delete_button_{index}")
                    if "View_button" not in st.session_state:
                        st.session_state["View_button"] = False
                    if "Update_button" not in st.session_state:
                        st.session_state["Update_button"] = False
                    if "del_button" not in st.session_state:
                        st.session_state["del_button"] = False
                    if View:
                        st.session_state["View_button"] = not st.session_state["View_button"]
                    if Update:
                        st.session_state["Update_button"] = not st.session_state["Update_button"]
                    if Delete:
                        st.write(index)
                        st.session_state["del_button"] = not st.session_state["del_button"]
                if st.session_state["del_button"] == True:
                    delete_callback_group(page_data['ID'][index])
                if st.session_state["Update_button"] == True:
                    switch_page("Create_suite")
                if st.session_state["View_button"] == True:
                    st.session_state.selected_rules = []
        click = st.button("⋮", key=f"button_{index}",)
        st.markdown("<style>body {background-color: #3498DB;}</style>", unsafe_allow_html=True)
        st.markdown("<style>.stButton>button {width: 100%; height: 40px; margin-top:10px; margin-left:0px;background: linear-gradient(to right, #a02a41 0%,    #1D4077 100%); color: white; border-radius: 15px;}</style>", unsafe_allow_html=True)  # Unique key for each button
        if "click" not in st.session_state:
            st.session_state["click"] = False
        if click:
            st.session_state["click"] = not st.session_state["click"]
        if st.session_state["click"] == True:
            optionContainer(click, index)
    st.markdown("""---""")
col1, col2, col3= st.columns([40,150,40])
if col1.button('Previous Page', key='prev_page'):
    
    if st.session_state.page > 1:

        st.session_state.page -= 1

        st.experimental_rerun()

 

 

 

if col3.button('Next Page', key='next_page'):

    if st.session_state.page < total_pages:

        st.session_state.page += 1

        st.experimental_rerun()

 

 

col2.write(f'Page {st.session_state.page}/{total_pages}')

 
