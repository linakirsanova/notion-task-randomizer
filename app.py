import streamlit as st
from notion_client import Client
import random
import os
from dotenv import load_dotenv

load_dotenv()

class NotionTaskRandomizer:
    def __init__(self, token, database_id):
        self.notion = Client(auth=token)
        self.database_id = database_id

    def get_tasks(self):
        filter_params = {
            "database_id": self.database_id,
        }
        try:
            response = self.notion.databases.query(**filter_params)
            return response["results"]
        except Exception as e:
            st.error(f"Error fetching tasks: {e}")
            return []

    def select_random_task(self):
        tasks = self.get_tasks()
        if not tasks:
            return None
        selected_task = random.choice(tasks)
        task_info = {
            "title": selected_task["properties"]["Content"]["rich_text"][0]["text"]["content"],
            "type": selected_task["properties"]["Type"]['title'][0]["text"]["content"],
            "url": selected_task["url"],
        }
        return task_info

# --- Streamlit UI ---
st.title("🎲 Notion Task Randomizer")

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
DATABASE_ID = os.environ.get("DATABASE_ID", "")

with st.expander("🔑 Set Notion Credentials"):
    NOTION_TOKEN = st.text_input("Notion Integration Token", value=NOTION_TOKEN, type="password")
    DATABASE_ID = st.text_input("Notion Database ID", value=DATABASE_ID)

if NOTION_TOKEN and DATABASE_ID:
    randomizer = NotionTaskRandomizer(NOTION_TOKEN, DATABASE_ID)
    if st.button("Pick a Random Task!"):
        task = randomizer.select_random_task()
        if task:
            st.success("🎉 Task Selected!")
            st.markdown(f"<h1 style='font-size: 2.5em; color: #4B8BBE;'>{task['title']}</h1>", unsafe_allow_html=True)
            st.write(f"**Type:** {task['type']}")
            st.markdown(f"[Open in Notion]({task['url']})")
        else:
            st.warning("No tasks available in this database.")
else:
    st.info("Please enter your Notion credentials above.")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit and Notion API")

