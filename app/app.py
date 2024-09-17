import streamlit as st
from utils import search_papers

st.set_page_config(page_title="Research Paper Semantic Search", layout="wide")

def main():
    st.title("Research Paper Semantic Search")

    # Search interface
    st.header("Search Papers")
    
    search_query = st.text_input("Enter your search query:")
    
    col1, col2 = st.columns(2)
    with col1:
        match_count = st.number_input("Number of results", min_value=1, max_value=20, value=6)
    with col2:
        similarity_threshold = st.slider("Similarity threshold", 0.0, 1.0, 0.75, 0.01)
    
    search_button = st.button("Search", type="primary")

    if search_button and search_query:
        results = search_papers(search_query, match_count, similarity_threshold)

        if results:
            st.subheader(f"Search Results for: {search_query}")
            
            # Display results count and average similarity
            avg_similarity = sum(paper['similarity'] for paper in results) / len(results)
            st.write(f"Found {len(results)} results with average similarity of {avg_similarity:.2f}")

            for paper in results:
                with st.expander(f"{paper['title']} (Similarity: {paper['similarity']:.2f})"):
                    st.write(f"**Authors:** {paper['author']}")
                    st.write(f"**Published:** {paper['published_date']}")
                    st.write("**Problem:**", paper['problem'])
                    st.write("**Solution:**", paper['solution'])
                    st.write("**Results:**", paper['result'])
                    st.markdown(f"[View Paper]({paper['url']})")

        else:
            st.warning("No results found. Please try a different search query.")

if __name__ == "__main__":
    main()