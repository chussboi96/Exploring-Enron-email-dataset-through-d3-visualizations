#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
df =pd.read_csv(r"C:\Users\Shabaan\Desktop\V\testemails.csv")


# In[4]:


df.head()


# In[5]:


import email

def get_text_content(msg):
    text_content = ""
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition'))

            # Skip any non-text parts
            if 'text' in content_type and 'attachment' not in content_disposition:
                text_content += part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='ignore') + '\n'
    else:
        text_content = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', errors='ignore')

    return text_content.strip()

# Create a new column 'text_data' in the DataFrame
df['TEXT_CONTENT'] = ""

# Iterate through each row in the DataFrame and extract text content
for index, row in df.iterrows():
    # Assuming 'email_content' is the column containing email content in your DataFrame
    email_content = row['message']

    # Parse the email using email.message_from_string
    msg = email.message_from_string(email_content)

    # Extract text content from the email
    email_text_content = get_text_content(msg)

    # Assign the text content to the 'text_data' column
    df.at[index, 'TEXT_CONTENT'] = email_text_content

# Save the updated DataFrame to a new CSV file or overwrite the existing file
df.to_csv('testemails.csv', index=False)


# In[6]:


df.head()


# In[7]:


import nltk

# Download the punkt tokenizer data
nltk.download('punkt')
nltk.download('stopwords')
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


# Extract the email body
body = df['TEXT_CONTENT']
df['StemmedContent'] = ""
for i in range(0,len(body)):
    # Tokenize the text
    tokens = word_tokenize(body[i])

    # Remove stop words and punctuation
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word.lower() for word in tokens if word.isalnum() and word.lower() not in stop_words]

    # Stemming
    ps = PorterStemmer()
    stemmed_tokens = [ps.stem(word) for word in filtered_tokens]
    df.at[i, 'StemmedContent'] = stemmed_tokens


# In[8]:


df.tail()


# In[9]:


import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

from nltk import word_tokenize, pos_tag, ne_chunk

# Sample text
body = df['TEXT_CONTENT']
df['EntitytText']=""
df['EntityLabel']=""

# Tokenize and part-of-speech tagging
for i in range(0,len(body)):
    tokens = word_tokenize(body[i])
    pos_tags = pos_tag(tokens)

    # Named Entity Recognition using ne_chunk
    named_entities = ne_chunk(pos_tags)

    # Display named entities
    for chunk in named_entities:
        if isinstance(chunk, nltk.Tree):
            entity_label = chunk.label()
            df.at[i,'EntityLabel']=entity_label
            entity_text = " ".join([token[0] for token in chunk.leaves()])
            df.at[i, 'EntityText'] = entity_text
df


# In[10]:


df=df.dropna()


# In[11]:


df.head()


# In[12]:


df=df.dropna()


# In[13]:


df


# In[14]:


# Assuming df is your DataFrame
df.to_csv('output.csv', index=False)


# In[ ]:




