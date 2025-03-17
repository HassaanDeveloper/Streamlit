import streamlit as st
import json
import os
from datetime import datetime

# Page config
st.set_page_config(page_title="Personal Library Manager", page_icon="📚", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        .book-card {
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #ddd;
            margin: 10px 0;
        }
        .read-status-true { color: #00cc00; }
        .read-status-false { color: #ff0000; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'library' not in st.session_state:
    st.session_state.library = []
    # Load existing library if file exists
    if os.path.exists('library.txt'):
        try:
            with open('library.txt', 'r') as file:
                st.session_state.library = json.load(file)
        except:
            st.error("Error loading library file!")

# Title
st.title("📚 Personal Library Manager")

# Sidebar for adding books and statistics
with st.sidebar:
    st.header("📊 Library Statistics")
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book['read'])
    
    st.metric("Total Books", total_books)
    if total_books > 0:
        percentage_read = (read_books / total_books) * 100
        st.metric("Books Read", f"{read_books} ({percentage_read:.1f}%)")
        
        # Genre distribution
        st.subheader("Genre Distribution")
        genres = {}
        for book in st.session_state.library:
            genres[book['genre']] = genres.get(book['genre'], 0) + 1
        
        for genre, count in genres.items():
            percentage = (count / total_books) * 100
            st.text(f"{genre}: {count} ({percentage:.1f}%)")

# Main content
tab1, tab2, tab3 = st.tabs(["📖 Add Book", "🔍 View/Search Books", "❌ Remove Book"])

# Add Book Tab
with tab1:
    st.header("Add a New Book")
    with st.form("add_book_form"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Book Title")
            author = st.text_input("Author")
            year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, value=2024)
        with col2:
            genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science Fiction", "Mystery", "Romance", "Biography", "Other"])
            read = st.checkbox("Have you read this book?")
        
        if st.form_submit_button("Add Book"):
            if title and author:
                new_book = {
                    'title': title,
                    'author': author,
                    'year': year,
                    'genre': genre,
                    'read': read,
                    'date_added': datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.library.append(new_book)
                
                # Save to file
                with open('library.txt', 'w') as file:
                    json.dump(st.session_state.library, file, indent=4)
                
                st.success("✅ Book added successfully!")
            else:
                st.error("Please fill in both title and author!")

# View/Search Books Tab
with tab2:
    st.header("View/Search Books")
    search_col1, search_col2 = st.columns([3, 1])
    
    with search_col1:
        search_term = st.text_input("🔍 Search by title or author")
    with search_col2:
        search_type = st.selectbox("Filter by", ["All", "Read", "Unread"])
    
    # Filter books based on search and read status
    filtered_books = st.session_state.library
    if search_term:
        filtered_books = [book for book in filtered_books 
                        if search_term.lower() in book['title'].lower() 
                        or search_term.lower() in book['author'].lower()]
    
    if search_type == "Read":
        filtered_books = [book for book in filtered_books if book['read']]
    elif search_type == "Unread":
        filtered_books = [book for book in filtered_books if not book['read']]
    
    # Display books in a grid
    if filtered_books:
        for book in filtered_books:
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"""
                    ### {book['title']}
                    **Author:** {book['author']}  
                    **Year:** {book['year']} | **Genre:** {book['genre']}  
                    **Status:** {'✅ Read' if book['read'] else '⏳ Unread'}  
                    **Added on:** {book['date_added']}
                    """)
                with col2:
                    if st.button("Mark as Read", key=f"read_{book['title']}", disabled=book['read']):
                        book['read'] = True
                        with open('library.txt', 'w') as file:
                            json.dump(st.session_state.library, file, indent=4)
                        st.rerun()
                st.divider()
    else:
        st.info("No books found!")

# Remove Book Tab
with tab3:
    st.header("Remove Book")
    if st.session_state.library:
        book_to_remove = st.selectbox("Select book to remove", 
                                    [f"{book['title']} by {book['author']}" for book in st.session_state.library])
        
        if st.button("Remove Book"):
            title_to_remove = book_to_remove.split(" by ")[0]
            st.session_state.library = [book for book in st.session_state.library 
                                      if book['title'] != title_to_remove]
            
            # Save to file
            with open('library.txt', 'w') as file:
                json.dump(st.session_state.library, file, indent=4)
            
            st.success("✅ Book removed successfully!")
            st.rerun()
    else:
        st.info("No books in library to remove!") 