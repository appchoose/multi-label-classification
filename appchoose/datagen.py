import numpy as np
from keras.utils import Sequence
from cv2 import imread

class DataGenerator(Sequence):
    '''Image Data Generator.
    
    Further improvements can be made here (e.g. data augmentation).
    
    # Arguments
        x_set: A list of file paths.
        y_set: A list of one-hot encoded labels (one label being a list of attributes).
        batch_size: An integer specifying the number of samples to include in a batch.
    
    # Returns
        One tensor storing the batch of images (batch_size, image_height, image_width, 3) and 
        one tensor storing the batch of one-hot encoded labels.
    '''
    def __init__(self, x_set, y_set, batch_size):
        self.x, self.y = x_set, y_set
        self.batch_size = batch_size

    def __len__(self):
        return int(np.ceil(len(self.x) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_x = self.x[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_y = self.y[idx * self.batch_size:(idx + 1) * self.batch_size]
        return np.array([imread(file_name) for file_name in batch_x]), batch_y
