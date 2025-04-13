import json
import requests
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from datasets import Dataset, DatasetDict
from transformers import BertForSequenceClassification



def predict_labels(text, tokenizer, model):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    
    # Tokenize and move inputs to the same device
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()

    return "Cancer" if predicted_class == 1 else "Non-cancer"


def predictor(text):
	response = {}
	tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
	model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
	model.load_state_dict(torch.load("bert-cancer-classifier.pth"))
	label = predict_labels(text, tokenizer, model)
	response['Text'] = text
	response['Predicted Class'] = label
	return response




def detect(request):
	response = {}
	json_data = request.get_json()
	text = json_data.get('text', [])
	response = predictor(text)
	return response