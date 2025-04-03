import streamlit as st
import requests

# Replace with your API endpoint URLs
API_ENDPOINT_POSTS = "http://localhost:8000/posts"
API_ENDPOINT_LOGIN = "http://localhost:8000/login"  # Your login endpoint

st.title("Retrieve Posts with JWT Authentication")

# Hardcoded credentials (NOT RECOMMENDED FOR PRODUCTION)
email = "tom@gmail.com"  # Replace with your test email
password = "irfan123" # Replace with your test password

if "access_token" not in st.session_state:
    st.session_state.access_token = None

# Perform login automatically
try:
    # 1. Login to get JWT token
    login_data = {"username": email, "password": password}
    login_response = requests.post(API_ENDPOINT_LOGIN, data=login_data)
    login_response.raise_for_status()
    token_data = login_response.json()
    st.session_state.access_token = token_data["access_token"]
    st.success("Login successful!")

except requests.exceptions.RequestException as e:
    st.error(f"Error: {e}")
except KeyError:
    st.error("Invalid credentials or token format.")

if st.session_state.access_token:
    limit = st.slider("Limit", min_value=1, max_value=50, value=10, step=1)
    if st.button("Fetch Posts"):
        try:
            headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
            params = {"limit": limit}
            posts_response = requests.get(API_ENDPOINT_POSTS, headers=headers, params=params)
            posts_response.raise_for_status()
            posts = posts_response.json()

            if posts:
                st.write("Retrieved Posts:")
                for post in posts:
                    st.write(f"**Title:** {post.get('title', 'N/A')}")
                    st.write(f"**Content:** {post.get('content', 'N/A')}")
                    st.write(f"**Published:** {post.get('published', 'N/A')}")
                    st.write(f"**Created At:** {post.get('created_at', 'N/A')}")
                    st.write("---")
            else:
                st.write("No posts found.")

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching posts: {e}")

