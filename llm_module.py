import os
import pandas as pd
from langchain_community.chat_models import ChatOllama
from langchain.schema import SystemMessage, HumanMessage
import json
import xml.etree.ElementTree as ET
import torch
from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent.futures import ProcessPoolExecutor



def parallel_call_llm(texts, max_processes=4):
    with ProcessPoolExecutor(max_workers=max_processes) as executor:
        return list(executor.map(call_llm, texts))



def llm_handler(df, max_processes=4):
    texts = df['text'].tolist()
    predictions = call_llm(texts)
    df['predicted_label'] = [normalize_prediction(pred) for pred in predictions]
    return df


def normalize_prediction(label):

	label = label.strip().lower()
	if "non-cancer" in label:
		return "Non-cancer"
	elif "cancer" in label:
		return "Cancer"
	else:
		return "Unknown"



def call_llm(text):

	n_ctx = 16384
	llm = ChatOllama(model="llama3.1:8b-instruct-q8_0", temperature=0.7, num_ctx=n_ctx)
	
	system_prompt = SystemMessage(content="""
	You are an expert in disease identification based on your training data. 
	Read given content and take action as per given query and apply all instructions given by user.
	If you don't know the answer, just say that you don't know.
	Strictly do not add any commentary, explanation, or additional words from your side.
	""")
	user_message=HumanMessage(content=f'''I have only two classes Cancer and Non-cancer, So for given text to you ,classify them in either of these 2 classes only, Make sure there is no variation of these 2 classes.
		Text : {text}     
		Answer : 
		''')

	response = llm([system_prompt, user_message])
	result = response.content.strip()

	return result


def llm_request_handler(request):
    json_data = request.get_json()
    text = json_data.get('text', [])
    df = pd.DataFrame({'text': text})
    llm_response = llm_handler(df)
    return llm_response.to_dict(orient="records")





