import torch
import os
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")


# check if models/summarizer exists and is not empty
if os.path.isdir('models/summarizer') and os.listdir('models/summarizer'):
   print("Summarizer model already downloaded.")
else: 
    summarizer_hf = "pszemraj/led-base-book-summary"
    summarizer_pipeline = pipeline(
        "summarization",
        summarizer_hf,
        device=0 if torch.cuda.is_available() else -1,
    )
    summarizer_pipeline.save_pretrained('models/summarizer')
    print("Summarizer model downloaded.")

if os.path.isdir('models/topic_model') and os.listdir('models/topic_model'):
   print("Topic model already downloaded.")
else:   
    topic_hf = "cardiffnlp/tweet-topic-21-multi"
    topic_tokenizer = AutoTokenizer.from_pretrained(topic_hf)
    topic_model = AutoModelForSequenceClassification.from_pretrained(topic_hf)
    topic_class_mapping = topic_model.config.id2label
    topic_model.save_pretrained('models/topic_model')
    topic_tokenizer.save_pretrained('models/topic_model')
    print("Topic model downloaded.")

if os.path.isdir('models/sentiment_pipeline') and os.listdir('models/sentiment_pipeline'):
    print("Sentiment model already downloaded.")
else:
    sentiment_hf = "cardiffnlp/twitter-roberta-base-sentiment"

    sentiment_pipeline = pipeline(
        task='sentiment-analysis',
        model=sentiment_hf,
        device=0 if torch.cuda.is_available() else -1
        )
    sentiment_pipeline.save_pretrained('models/sentiment_pipeline')
    print("Sentiment model downloaded.")