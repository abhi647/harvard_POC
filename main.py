import streamlit as st
import os
import openai
import fitz  # PyMuPDF
from pathlib import Path

# Set your OpenAI API key
openai.api_key = 'sk-proj-3yHoOiS5Z6H6CS1i7uSFT3BlbkFJATTWo9JHC8Ew8neadFgA'

# Function to read PDF
def read_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to perform semantic search
def semantic_search(query, documents):
    query_embedding = openai.Embedding.create(
        input=query, 
        model="text-embedding-ada-002"
    )['data'][0]['embedding']

    results = []
    for doc in documents:
        doc_embedding = openai.Embedding.create(
            input=doc['text'], 
            model="text-embedding-ada-002"
        )['data'][0]['embedding']
        
        similarity = cosine_similarity(query_embedding, doc_embedding)
        results.append((doc['title'], similarity, doc['text']))

    results.sort(key=lambda x: x[1], reverse=True)
    return results

# Function to calculate cosine similarity
def cosine_similarity(vec1, vec2):
    return sum(a*b for a, b in zip(vec1, vec2)) / (sum(a*a for a in vec1) * sum(b*b for b in vec2))**0.5

# Function to handle chatbot interaction
def chat_with_gpt(messages):
    client = openai.OpenAI(api_key=openai.api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.9,
    )
    return response.choices[0].message.content.strip()

# Set the page configuration
st.set_page_config(page_title="Harvard University Content Store", layout="wide")

# Load documents from "uploaded_files"
uploaded_files_path = Path("uploaded_files")
documents = []
for file in uploaded_files_path.glob("*.pdf"):
    documents.append({
        'title': file.stem,
        'text': read_pdf(file)
    })

# Sidebar - Advanced Filters
st.sidebar.title("Harvard University")

# Collapsible Advanced Filters
with st.sidebar.expander("Advanced Filters"):
    st.sidebar.selectbox("Page", ["Home"], key="page1")

st.sidebar.header("Ask Me!")
st.sidebar.image("images/sidebar.png", use_column_width=True)  # Dummy path for the image
st.sidebar.write("Hey there! Just let me know what you're researching on today? Just ask me, I am happy to help you with your research.")

# Chatbot interface in sidebar
st.sidebar.subheader("Chat with GPT")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.sidebar.write(f"{msg['role'].title()}: {msg['content']}")

user_input = st.sidebar.text_input("You:", key="user_input")
if st.sidebar.button("Send", key="send_button"):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = chat_with_gpt(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.experimental_rerun()

# Main content
if 'search_results' not in st.session_state:
    st.session_state.search_results = []

def search():
    query = st.session_state.search_query
    st.session_state.search_results = semantic_search(query, documents)
    st.experimental_rerun()

# Dummy image paths for each article
image_paths = [
    "images/1.jpeg",
    "images/2.jpeg",
    "images/3.jpeg",
    "images/4.jpeg",
    "images/5.jpeg",
    "images/6.jpeg",
    "images/7.png",
    "images/8.jpeg",
    "images/9.jpeg",
    "images/10.png",
    "images/11.jpeg",
    "images/12.jpeg",
    "images/13.jpg",
    "images/14.jpeg",
    "images/15.png",
    "images/16.png",
    "images/17.jpeg",
    "images/18.png",
    "images/19.jpeg",
    "images/20.jpg",
]

# Home Page
if not st.session_state.search_results:
    st.title("Harvard University Content Store")
    
    # Search bar
    st.text_input("Search for research content here:", key="search_query", on_change=search)
    
    # Article headings and placeholders for the main articles
    article_headings = [
        "Advances in Quantum Computing: Breaking New Ground in Computational Capabilities",
        "Exploring the Human Genome: Unraveling the Complexities of Genetic Variation",
        "Climate Change and Its Impact on Global Biodiversity: A Comprehensive Analysis",
        "Artificial Intelligence in Healthcare: Transforming Patient Diagnosis and Treatment",
        "Renewable Energy Technologies: Innovations and Future Prospects",
        "Economic Implications of Global Trade Policies: A Cross-Country Comparison",
        "Neuroscience and Cognitive Development: Insights from Brain Imaging Studies",
        "Sustainable Urban Planning: Integrating Green Spaces into City Landscapes",
        "Advancements in Nanotechnology: Applications in Medicine and Industry",
        "Cybersecurity Challenges in the Digital Age: Strategies for Data Protection",
        "The Role of Big Data in Shaping Modern Business Strategies",
        "Educational Reforms in the 21st Century: Enhancing Learning Outcomes",
        "Marine Biology: Discoveries in Deep-Sea Ecosystems",
        "Innovations in Agritech: Boosting Crop Yields with Precision Farming",
        "The Future of Space Exploration: Missions to Mars and Beyond",
        "Public Health Strategies to Combat Pandemics: Lessons from COVID-19",
        "The Intersection of Art and Technology: Digital Art Movements",
        "Behavioral Economics: Understanding Human Decision-Making Processes",
        "The Evolution of Cryptocurrencies: Opportunities and Regulatory Challenges",
        "AI-Driven Autonomous Vehicles: The Road to Safe and Efficient Transportation"
    ]

    article_subheadings = [
        "Quantum computing advancements and their implications.",
        "Insights into genetic variations and their significance.",
        "Analyzing the global impact of climate change on biodiversity.",
        "Transforming healthcare through AI-driven technologies.",
        "Exploring future prospects in renewable energy.",
        "Comparative analysis of global trade policies.",
        "Understanding cognitive development through brain imaging.",
        "Integrating green spaces in urban planning.",
        "Medical and industrial applications of nanotechnology.",
        "Strategies to address cybersecurity challenges.",
        "How big data is reshaping business strategies.",
        "Enhancing educational outcomes through reforms.",
        "Discoveries in deep-sea ecosystems.",
        "Precision farming innovations for increased crop yields.",
        "Exploring the future of space missions.",
        "Learning from public health strategies during pandemics.",
        "Exploring digital art movements and technology.",
        "Human decision-making processes through behavioral economics.",
        "Opportunities and challenges in cryptocurrency evolution.",
        "Ensuring safe and efficient autonomous vehicle transportation."
    ]

    st.subheader("Featured Articles")
    for i in range(len(article_headings)):
        col1, col2 = st.columns([1, 3])
        with col1:
            col1.image(image_paths[i], use_column_width=True)  # Dummy path for each article image
        with col2:
            col2.subheader(article_headings[i])
            col2.write(article_subheadings[i])
            col2.button("Learn more", key=f"learn_more_button_{i}")
            col2.write("Audio")
        st.markdown('---')

# Results Page
else:
    st.title("Harvard University Content Store")
    
    query = st.text_input("Search for research content here:", value=st.session_state.search_query, key="search_query")
    if st.button("Search", key="search_button"):
        search()

    st.subheader(f"Search Results for '{st.session_state.search_query}'")
    for title, similarity, text in st.session_state.search_results:
        st.subheader(title)
        st.write(f"{text[:200]}...")  # Displaying a snippet of the text
        st.markdown("[Learn more](#)")

# Footer
st.markdown("""
    <footer>
        <div style="display: flex; justify-content: space-between;">
            <div>
                <h4>Security & Brand</h4>
                <ul>
                    <li>Report Copyright Infringement</li>
                    <li>Report Security Issue</li>
                    <li>Trademark Notice</li>
                </ul>
            </div>
            <div>
                <h4>Website</h4>
                <ul>
                    <li>Accessibility</li>
                    <li>Digital Accessibility</li>
                    <li>Privacy Statement</li>
                </ul>
            </div>
            <div>
                <h4>Get in Touch</h4>
                <ul>
                    <li>Contact Harvard</li>
                    <li>Maps & Directions</li>
                    <li>Jobs</li>
                </ul>
            </div>
        </div>
        <hr />
        <p>© 2024 The President and Fellows of Harvard College</p>
    </footer>
""", unsafe_allow_html=True)
