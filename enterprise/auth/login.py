import streamlit as st

USERS = {

    "admin":{

        "password":"admin123",

        "role":"Admin"

    },

    "manager":{

        "password":"manager123",

        "role":"Manager"

    },

    "analyst":{

        "password":"analyst123",

        "role":"Analyst"

    }

}


def login():

    st.title("🔐 Login")

    username = st.text_input(

        "Username"

    )

    password = st.text_input(

        "Password",

        type="password"

    )

    if st.button("Login"):

        if username in USERS and USERS[username]["password"] == password:

            st.session_state.logged_in = True

            st.session_state.user = username
            st.session_state.role = USERS[username]["role"]

            st.success("Login Successful")

            st.rerun()

        else:

            st.error(

                "Invalid Username or Password"

            )