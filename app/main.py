import streamlit as st
from st_tailwind import tw_wrap

from utils import search_papers

# Streamlit app
st.set_page_config(page_title="Research Paper Semantic Search", layout="wide")

def main():
    tw_wrap(st.title)("Research Paper Semantic Search", classes="text-4xl font-bold mb-8 text-blue-600")

    search_query = tw_wrap(st.text_input)("Enter your search query:", key="search_input", classes="w-full p-2 border border-gray-300 rounded-md mb-4")
    search_button = tw_wrap(st.button)("Search", key="search_button", classes="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition duration-300")

    if search_button and search_query:
        try:
            results = search_papers(search_query)

            if results:
                tw_wrap(st.subheader)(f"Search Results for: {search_query}", classes="text-2xl font-semibold mb-4 text-blue-600")
                for paper in results:
                    with st.container():
                        tw_wrap(st.markdown)(f"### {paper['title']}", classes="text-xl font-semibold mb-2 text-blue-700")
                        tw_wrap(st.markdown)(f"**Authors:** {paper['author']}", classes="text-sm text-gray-600 mb-2")
                        tw_wrap(st.markdown)(f"**Published:** {paper['published_date']}", classes="text-sm text-gray-500 mb-4")
                        tw_wrap(st.markdown)("**Problem:**", classes="font-semibold text-gray-700")
                        tw_wrap(st.write)(paper['problem'], classes="text-gray-700 mb-2")
                        tw_wrap(st.markdown)("**Solution:**", classes="font-semibold text-gray-700")
                        tw_wrap(st.write)(paper['solution'], classes="text-gray-700 mb-2")
                        tw_wrap(st.markdown)("**Results:**", classes="font-semibold text-gray-700")
                        tw_wrap(st.write)(paper['result'], classes="text-gray-700 mb-2")
                        tw_wrap(st.markdown)(f"[View Paper]({paper['url']})", classes="text-blue-500 hover:underline")
            else:
                tw_wrap(st.warning)("No results found. Please try a different search query.", classes="text-red-500 font-semibold")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error("Make sure you have set up the 'match_documents' function in your Supabase project.")

if __name__ == "__main__":
    main()