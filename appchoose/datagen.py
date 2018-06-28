import numpy as np
from keras.utils import Sequence
from cv2 import imread

class DataGenerator(Sequence):
    '''Image Data Generator.
    
    Further improvements can be made here (e.g. data augmentation).
    
    # Arguments
        x: A list of file paths.
        y: A list of one-hot encoded labels (one label being a list of attributes).
        batch_size: An integer specifying the number of samples to include in a batch.
        shuffle: A boolean specifying whether the samples should be shuffled or not.
    
    # Returns
        One tensor storing the batch of images (batch_size, image_height, image_width, 3) and 
        one tensor storing the batch of one-hot encoded labels.
    '''
    def __init__(self, x, y, batch_size, shuffle = True):
        self.x, self.y = x, y
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        return int(np.ceil(len(self.x) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_indexes = self.indexes[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_x = self.x[batch_indexes]
        batch_y = self.y[batch_indexes]
        return np.array([imread(file_name) for file_name in batch_x]), batch_y
    
    def on_epoch_end(self):
        self.indexes = np.arange(len(self.x))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)
