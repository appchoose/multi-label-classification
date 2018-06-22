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

X = []
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
        X.append(imgpath)
        labels.append(tmp)
```

## Train on dataset

Now that we have our labels and our images ready, we can train our multilabel classifier on
our images.

#### One-hot encoding of the labels

We use the `MultiLabelBinarizer` function from `sklearn` to transform our labels.

```python
from sklearn.preprocessing import MultiLabelBinarizer

mlb = MultiLabelBinarizer()
y = mlb.fit_transform(labels)
```

#### Splitting the dataset into a train set and a test set

Define the size of the test set.

```python
from sklearn.model_selection import train_test_split

(X_train, X_test, y_train, y_test) = train_test_split(X, y, test_size = 0.2)
```

#### Loading a model architecture

A very simple model for multilabel classification is available in this repo. It
is built upon a MobileNet architecture.

```
import tensorflow as tf
import keras
from keras.utils import multi_gpu_model
from appchoose.choosemultilabel import ChooseMultiLabel 

with tf.device("/cpu:0"):
    model = ChooseMultiLabel(classes = len(mlb.classes_), trainable_layers = 10)

multi_model = multi_gpu_model(model, gpus = 2)
``` 

#### Compile both models (required to save a multiGPU model)

We use custom metrics for multilabel classification as keras default metrics are not suitable for this classification problem. 

*I really think this is important since it now feels a bit like flying blind without having per class metrics on multi class classification.*

```
from appchoose.metrics import fmeasure, recall, precision

model.compile(optimizer = 'Adam', loss = 'binary_crossentropy')
multi_model.compile(optimizer = 'Adam', loss = 'binary_crossentropy', metrics = [fmeasure, recall, precision])
```

#### Train the model

You need to use a data generator to generate the batches of samples that are going to be fed into
the model. Our data generator takes a list of file paths and a list of one-hot encoded labels as inputs. 

```
from appchoose.datagen import DataGenerator

training_generator = DataGenerator(X_train, y_train, batch_size = 128)
validation_generator = DataGenerator(X_test, y_test, batch_size = 128)

multi_model.fit_generator(generator = training_generator, validation_data = validation_generator,
                          use_multiprocessing = True, workers = 6, epochs = 10)

#### Save the model

As `multi_model` can't be saved, you actually need to save `model`.

```
model.save('multilabel.h5')
```
