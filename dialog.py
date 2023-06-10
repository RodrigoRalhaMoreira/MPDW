from models.model_utils import get_model
from transformers import AutoTokenizer
import config
import transformers
import random

import search
import response

# Set the transformer verbosity to hide the annoying warnings
transformers.logging.set_verbosity_error()

# load model and tokenizer
checkpoint_name = 'bert-base-uncased'
config.model_name = 'bertdsti'
config.start_by_loading = True
config.max_len = 128
config.load_path = 'trained-models/bert-dsti-ff-new.ptbert-base-uncased'
tokenizer = AutoTokenizer.from_pretrained(checkpoint_name, truncation_side='left')
model, input_function, dataloading_function = get_model(checkpoint_name, tokenizer, None)


def add_special_tokens_to_model_and_tokenizer(model, tokenizer, special_tokens, embeddings):
    # TODO instead of checking for the shared param you should really just have a good way to tell whether the model has some sort of decoder
    if model is None or hasattr(model, 'shared'):
        if model is None:
            for special_token in special_tokens:
                tokenizer.add_tokens(special_token)
        return

print("Loaded early iFetch slot filling and intent detector...")
    
add_special_tokens_to_model_and_tokenizer(
    None,
    tokenizer,
    [' Dontcare', '[sys]', '[usr]', '[intent]'],
    ['I don\'t care', '[SEP]', '[SEP]', '[CLS]']
)

UTTERANCE1 = "find me a black suit please"
UTTERANCE2 = "what kind of suit should i wear to my sister's wedding"

GREETING = ["Hello! How can I help you?", "Hi, I'm here to help you!"]
GOODBYE = ["Bye!"]

def get_human_readable_output(utterance: str):
  o = input_function(tokenizer=tokenizer, question=utterance)
  tokens = tokenizer.convert_ids_to_tokens(o["input_ids"][0])
  return model.get_human_readable_output(o, tokens)
  

def get_key_value_parameters(utterance: str):
  result = []
  a = get_human_readable_output(utterance)
  
  for key in a.value.keys():
      value = a.get_slot_value_from_key(key)
      result.append((key,value))
  
  return result
      

def get_all_possible_intents():
  return model.intent_keys

  
def get_utterance_intent(utterance: str):
  return get_human_readable_output(utterance).get_intent()


# print(get_key_value_parameters(UTTERANCE2))
# print(get_utterance_intent("Help me to find a prada blue suit"))
# print(get_key_value_parameters("Help me to find a prada blue suit"))

def get_bot_response(utterance: str, product_found: any):
  user_intent = get_utterance_intent(utterance)
  
  if(user_intent == 'user_neutral_greeting'):
    return GREETING[random.randint(0, len(GREETING)-1)]
  
  elif(user_intent == 'user_neutral_goodbye'):
    return GOODBYE[random.randint(0, len(GOODBYE)-1)]
    
  elif(user_intent == 'user_request_get_products'):
    result = search.search_natural_text(utterance)
    if result["hits"]["total"]["value"] > 0:
      print("product_found!")
      print(get_key_value_parameters(utterance))
    else:
      print('I cant retrieve products right now')
    
    return result
    
  elif(user_intent == 'user_qa_product_description'):
    if(product_found is None):
      return 'You must choose a product before.'
      print('You must choose a product before.')
    else:
      product_index = get_product_index(utterance)
      if (product_index == -1):
        return "unknown ordinality"
      # return product_found["hits"]["hits"][product_index]
      return "Here are some details:\n"+response.response_to_details(product_found["hits"]["hits"][product_index])
 

def get_product_index( utterance: str):
  if(utterance.find("first")>0):
    return 0
  if(utterance.find("second")>0):
    return 1
  if(utterance.find("third")>0):
    return 2
  return -1


    