import os
import re
import urllib
import urllib.request
import urllib.parse
from PIL import Image
from resizeimage import resizeimage

def resize_img(imgpath, target_size = 224):
    """Resize an image.
    
    If for some reason the image cannot be resized, it is deleted.
    
    # Arguments
        imgpath: A file path pointing to an image.
        target_size: An integer specifying the resized image dimensions.
    
    # Returns
        A square image with the desired dimensions.
    """
    try:
        with open(imgpath, 'r+b') as f:
            with Image.open(f) as img:
                img = resizeimage.resize_cover(img, [target_size, target_size])
                img.save(imgpath, img.format)
    except: 
        os.remove(imgpath)
        print("Impossible to resize file {0}. Deleting file...".format(imgpath))
            
def replace(string, substitutions):
    """Replace all non-desired substrings. 
    
    # Arguments
        string: A string to be processed.
        substitutions: A dictionary listing the values the non-desired substrings 
                       should be replaced with.
    
    # Returns
        A processed string with no non-desired substrings.
    """
    substrings = sorted(substitutions, key = len, reverse = True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)

def extract_filepath(source, aws):
    """Extract item brand and file name. 
    
    # Arguments
        source: A dictionary listing an item's attributes.
        aws: A string corresponding to the part of the url to be ignored.
    
    # Returns
        A list containing the item brand and the file name.
    """
    d_str = {"-": "_", " ": "_", "'": "", ".": "", "?": "", "!": "", "%20": "_"}
    imgpath = urllib.parse.unquote(source['img'].replace(aws, ''))
    brd = replace(imgpath.split("/")[0].lower(), d_str)
    filename = imgpath.split("/")[-1]
    return([brd, filename])
    
def img_downloader(source, 
                   target_dir, 
                   aws,
                   target_size = 224):
    """Download an image.
    
    # Arguments
        source: A dictionary listing an item's attributes.
        target_dir: A directory path where the image should be saved.
        aws: A string corresponding to the part of the url to be ignored.
        target_size: An integer specifying the resized image dimensions.
    """
    filepath = extract_filepath(source = source, aws = aws)
    
    if not os.path.exists('/'.join([target_dir, filepath[0]])):
        os.makedirs('/'.join([target_dir, filepath[0]]))
    
    if not os.path.exists('/'.join([target_dir, filepath[0], filepath[1]])):
        if 'img' in source:
            try:
                urllib.request.urlretrieve(source['img'], '/'.join([target_dir, filepath[0], filepath[1]]))
            except:
                0
                
    if os.path.exists('/'.join([target_dir, filepath[0], filepath[1]])):
        resize_img('/'.join([target_dir, filepath[0], filepath[1]]), target_size = target_size)