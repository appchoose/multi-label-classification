# Multilabel classification

```bash
git clone https://github.com/appchoose/multi-label-classification.git
```

## Load the data

Define the parameters required to retrieve the data with Elasticsearch, then 
use the helper function to load the data.

```python
credentials = {
    'ES_HOST': ['...'],
    'ES_USR': '...',
    'ES_PWD': '...',
    'ES_PORT': ...,
    'ES_SCHEME': '...',
}
```

```
from appchoose import data
list_items = data.load_data('list_items', credentials = credentials)
```

## Download and resize the images

Downloading images straight from the Internet will probably leave you with images 
of different size. Since most neural networks are fed with images that share the 
same size, storing a resized version of each image is likely to speed up the training. 
One of the biggest bottlenecks that we have experienced came from resizing our images.

```python
from appchoose import download
from tqdm import tqdm 

target_dir = '/home/...'
aws = 'https://...'

list(map(lambda x: download.img_downloader(x['_source'], target_dir = target_dir, aws = aws), tqdm(list_items)))
```

## Generate the labels

Probably the most important task. The code presented here is far from being perfect, but
it gives a simple workflow of how this can be done. Tags (categories and colors) we are
interested in are defined in separate files (`files/categories` and `files/webcolors`). 
Corrected and/or simplified versions of these tags are also stored in pickled files 
(`files/valid_categories` and `files/valid_colors`).

```python
import os
import re
import pickle
from appchoose import tag

with open ('files/categories', 'rb') as fp:
    categories = pickle.load(fp)
    
with open ('files/webcolors', 'rb') as fp:
    wbcolors = re.compile('|'.join(pickle.load(fp)))
    
with open ('files/valid_colors', 'rb') as fp:
    valid_colors = pickle.load(fp)
    
with open ('files/valid_categories', 'rb') as fp:
    valid_categories = pickle.load(fp)

valid_img = []
labels = []

for idx in tqdm_notebook(range(len(list_items))):
    obj = download.extract_filepath(source = list_items[idx]['_source'], aws = aws)
    imgpath = '/'.join([target_dir, obj[0], obj[1]])
    tmp = tag.tag_image(source = list_items[idx]['_source'], 
                        categories = categories, 
                        wbclrs = wbcolors, 
                        valid_colors = valid_colors, 
                        valid_categories = valid_categories, 
                        target_dir = target_dir)
    if (len(tmp) > 0 and os.path.exists(imgpath)):
        valid_img.append(imgpath)
        labels.append(tmp)
```
