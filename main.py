import streamlit as st
import pandas as pd
import re
import pickle
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import time
from litellm import completion
import logging
logging.basicConfig(level=logging.INFO)
import os


def main():
    
    
    
    st.title("Wikipeida Search Engine")
    
    OLLAMA_HOST = os.environ.get('OLLAMA_HOST', 'host.docker.internal')
    OLLAMA_PORT = os.environ.get('OLLAMA_PORT', '11434')
    OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'orca-mini')
    
    st.sidebar.title("Settings")
    is_debugging = st.sidebar.checkbox("Debugging")
    using_ai = st.sidebar.checkbox("Generate answer using AI")
    
    user_input = st.text_input("Enter your query")
    
    
    if st.button("Search") or user_input:
        
        with st.spinner("Searching..."):
            
            time.sleep(1)
            
            with open('corpus_weight.pkl', 'rb') as f:
                matrix_vec = pickle.load(f)

            with open('vectorizer.pkl', 'rb') as f:
                vectorizer = pickle.load(f)
                            
            logging.info("Processing query")
            stop_words = stopwords.words('english')
            query = ' '.join([word for word in user_input.split() if word not in (stop_words)])
            query = re.sub(r'[^\w\s]','', query)
            query = re.sub(' +', ' ', query)
            query = query.lower()
            query_vec = vectorizer.transform([query])
            logging.info("Processed query")
            
            logging.info("Calculating similarity")
            similarity = cosine_similarity(matrix_vec, query_vec).flatten()
            index_similarity = [(i, s) for i, s in enumerate(similarity)]
            index_similarity = sorted(index_similarity, key=lambda k: k[1], reverse=True)
            top_10 = index_similarity[:10]
            logging.info("Calculated similarity")
        
            logging.info("Collecting documents")
            df = pd.read_parquet('prod.parquet', columns=['title', 'url', 'summary'])
            documents_data = [] 
            for i, s in top_10:
                data = [df['title'][i], df['url'][i], df['summary'][i]]
                documents_data.append(data)
            documents_df = pd.DataFrame(documents_data, columns=['title', 'url', 'summary'])
            if documents_df.duplicated(subset=['url']).sum() > 1:
                documents_df.drop_duplicates(subset=['url'], inplace=True)
                documents_df.reset_index(drop=True, inplace=True)
            logging.info("Collected documents")
            
            if using_ai:
                logging.info("Creating prompt")
                model_name = 'orca-mini'
                prompt = 'You are search engine. You are tasked to answer a question or query that will be given to you in a short paragraph or small set of instructions. Your answer will only be based on the 5 document given to you and nothing else. Even though sometimes it may be a query try to think in a way of question. Please keep your answer as short as possible like 1 paragraph without leaving important details.\n'
                prompt += 'The question/query is:\n\n'
                prompt += f'"{user_input}"\n\n'
                prompt += f'Here are the 5 documents that you can use to answer the question/query:\n\n'
                for document_index in range(5 if documents_df.shape[0] > 5 else documents_df.shape[0]):
                    prompt += f'{documents_df["summary"][document_index]}\n\n'
                logging.info("Created prompt")
                            
                logging.info("Generating answer")
                response = completion(
                    model=f"ollama/{OLLAMA_MODEL}",
                    messages=[{ "content": prompt, "role": "user"}], 
                    api_base=f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"
                )
                logging.info("Generated answer")
        
        if using_ai:
            with st.expander("See AI generated answer:"):
                st.write(response.choices[0].message.content)    

        for document_index in range(5 if documents_df.shape[0] > 5 else documents_df.shape[0]):
            title = documents_df['title'][document_index]
            url = documents_df['url'][document_index]
            summary = documents_df['summary'][document_index]
            st.write("[{}]({})\n[{}]({})".format(title, url, url, url))
            st.write("**Summary:**\n{}\n".format(summary[:250]))
            st.write(' ')
            st.write(' ')
        
        if is_debugging:
            st.write("Debugging:")
            st.write("User input: {}".format(user_input))
            st.write("Query: {}".format(query))
            st.write("Duplicated Results Count by title: {}".format(documents_df.duplicated(subset=['title']).sum()))
            st.write("Duplicated Results Count by url: {}".format(documents_df.duplicated(subset=['url']).sum()))
            for i in top_10:
                st.write(i)
                

main()