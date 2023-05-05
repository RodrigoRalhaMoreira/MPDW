import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from bertviz import model_view, head_view
import transformers
from transformers import *

import numpy as np
import pprint

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from transformers import BertTokenizer, BertModel
import torch
import re
from transformers import AutoTokenizer, AutoModel

model_path = 'bert-base-uncased'
CLS_token = "[CLS]"
SEP_token = "[SEP]"

# transformers.logging.set_verbosity_warning()

tokenizer = AutoTokenizer.from_pretrained(model_path)
config = AutoConfig.from_pretrained(model_path,  output_hidden_states=True, output_attentions=True)  
model = AutoModel.from_pretrained(model_path, config=config)


sentence_a = "cat cat cat cat cat cat cat cat cat cat cat cat cat cat cat cat cat cat cat cat"

inputs = tokenizer.encode_plus(sentence_a, return_tensors='pt', add_special_tokens=True, max_length = 512, truncation = True)
pprint.pprint(inputs)

input_ids = inputs['input_ids']

input_id_list = input_ids[0].tolist() # Batch index 0
tokens = tokenizer.convert_ids_to_tokens(input_id_list)

with torch.no_grad():
    outputs = model(**inputs)

hidden_states = outputs['hidden_states']

pprint.pprint(hidden_states)

layer = 1

# rows = 3
# cols = 4
# fig, ax_full = plt.subplots(rows, cols)
# fig.set_figheight(rows*4)
# fig.set_figwidth(cols*4+3)

# plt.rcParams.update({'font.size': 10})

# j = 0
# for r in range(rows):
#     for c in range(cols):
       
#         ax = ax_full[r,c]
        
#         plt.rcParams.update({'font.size': 10})
#         model = hidden_states[j][0].detach().numpy()
        
#         if model.shape[1] == 2:
#             twodim = model
#         else:
#             twodim = PCA().fit_transform(model)[:,:2]

#         plt.style.use('default') # https://matplotlib.org/3.5.1/gallery/style_sheets/style_sheets_reference.html
#         im = ax.scatter(twodim[:,0], twodim[:,1], edgecolors='k', c='r')
#         for word, (x,y) in zip(tokens, twodim):
#             ax.text(x+0.05, y+0.05, word)
        
#         # Show all ticks and label them with the respective list entries
#         ax.set_title("Layer " + str(j))
            
#         # Loop over data dimensions and create text annotations.
#         j = j + 1

# fig.suptitle("Title")
# plt.show()


def display_scatterplot(model, words):
    if model.shape[1] == 2:
        twodim = model
    else:
        twodim = PCA().fit_transform(model)[:,:2]
    
    # plt.style.use('default') # https://matplotlib.org/3.5.1/gallery/style_sheets/style_sheets_reference.html
    plt.figure(figsize=(6,6))
    plt.scatter(twodim[:,0], twodim[:,1], edgecolors='k', c='r')
    for word, (x,y) in zip(words, twodim):
        plt.text(x+0.05, y+0.05, word)

    plt.show()
    return

display_scatterplot(hidden_states[0][0].detach().numpy(), tokens)