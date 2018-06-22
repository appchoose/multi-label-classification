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

list_items = data.load_data('list_items', credentials = credentials)
```
