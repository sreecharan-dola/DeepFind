import streamlit as st
import os
from engine import *


#st.title("🧐 DocSearch")
st.markdown("""<h1> 🧐 Deep<span style = "color : green";>Find </span> </h1>""", unsafe_allow_html=True)
st.markdown('*- Search meaning, not just words*')
st.markdown('### 1. Add your document')
st.write("*Upload one or more text files to start*")
files = st.file_uploader('', type=['txt'], accept_multiple_files=True)

all_files = []
if files:
    st.write(f"{len(files)}.File upload success")
    for file in files:
        all_files.append(file.name)
        with open(file.name, 'wb') as f:
            f.write(file.getbuffer())
else:
    st.write('⚠️Upload files')



st.markdown('### 2. Enter your query')
st.write("*ask anything - we find most relevant information*")

with st.form("search "):
    query = st.text_input("", placeholder="Ask anything....")
    query_words = query.split()
    with st.columns([2,1,2])[1]:
        button = st.form_submit_button('🔍︎ Search')


top_picks = []

if button:
    if query and all_files:
        #index 0 = chunk , index 1 = filename, index 2 = score
        top_picks = sentence_similarity(set(all_files), query)

    else:
        st.write('⚠️Write something')


st.markdown('### 3. Results')
st.write('*Top results ranked by semantic similarity*')

def highlight(chunk):
    chunk = chunk.title()
    for word in query_words:
        word = word.title()
        if len(word) > 3:
            chunk = chunk.replace(word, f"""<b style = "color:#9AD872; font-size:18px;" >{word}</b> """ )
    return chunk


#[('Title 1', 'In box 1'), ('Title 2', 'In box 2'), ('Title 3', 'In box 3')]
for i in range(len(top_picks)):
    st.markdown(f"""
    <div style = "background-color:black;
     padding:25px;
     border : 1px solid green;
     border-radius:50px;
     margin-bottom:15px"; >

     <h4>📄 {top_picks[i][1]}</h3>
     <p> {highlight(top_picks[i][0])} </p>
     <p> 🎯 Similarity: {str(top_picks[i][2]*100)[:5]}% </p>
     </div>
    """, unsafe_allow_html=True)


st.markdown("""
<style> 
.stApp {background-color :  #050505; color : white;  font-family: Tahoma;}
[data-testid="stFileUploaderDropzone"] {background : black; color : white; border:2px dashed #14532d;}
[data-testid="stBaseButton-secondary"] {border:1px solid green; background-color :#0b0f0d  !important; color : green !important;}
[data-testid="stBaseButton-secondaryFormSubmit"] {border:1px solid green; background-color :#0b0f0d  !important; color : green !important;}
[data-testid="stForm"] {border:2px dashed #14532d; }
.stTextInput input {background : black ; color : white; border : 1px solid gray;}

</style>
""", unsafe_allow_html=True)



for i in all_files:
    os.remove(i)