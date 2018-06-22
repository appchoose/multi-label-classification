from appchoose import download
import os
import re
import webcolors

def get_gender(source):
    """Extract item gender. 
    
    # Arguments
        source: A dictionary listing an item's attributes.
    
    # Returns:
        An item gender.
    """
    try:
        gender = source['cat'].lower().split("-")[-1]
    except KeyError: 
        gender = None
    return gender

def rectify_tag(tag, valid_tags):
    """Rectify item tag (category, color, etc). 
    
    # Arguments
        tag: An item attribute.
        valid_tags: A dictionary listing the non-valid keys and the
                    values they should be replaced with.
        
    # Returns:
        A valid item tag.
    """
    if tag is not None:
        if tag in valid_tags:
            return valid_tags[tag]
        else:
            return tag
    else:
        return None

def get_category(source, valid_tags):
    """Extract item category. 
    
    # Arguments
        source: A dictionary listing an item's attributes.
        valid_tags: A dictionary listing the non-valid keys and the
                    values they should be replaced with.
                    
    # Returns:
        An item category.
    """
    try:
        cat = source['catText'].lower().split(" ")[0]
    except KeyError:
        try:
            cat = source['doc']['catText'].lower().split(" ")[0]
        except KeyError:
            cat = None
    
    return rectify_tag(cat, valid_tags)


def get_colors(source):
    """Extract item colors. 
    
    # Arguments
        source: A dictionary listing an item's attributes.
                    
    # Returns:
        A list of colors.
    """
    if 'color' in source:
        clr = source['color'].lower().split("/")
    return clr

def parse_color(clr, wbclrs):
    """Extract item colors. 
    
    # Arguments
        clr: A color name.
        wbclrs: A list of colors.
    # Returns:
        A valid item color.
    """
    try:
        x = clr
        webcolors.name_to_rgb(clr)
    except ValueError:
        try:
            x = clr.replace(" ", "")
            webcolors.name_to_rgb(clr)
        except ValueError:
            x = re.search(wbclrs, clr).group()
    else:
        x = None
    return x
            
def tag_image(source, categories, wbclrs, valid_colors, valid_categories, target_dir):
    """Extract and assign multiple attributes to an image. 
    
    # Arguments
        source: A dictionary listing an item's attributes.
        categories: A list of all categories of interest.
        wbclrs: A list of valid CSS colors.
        valid_colors: A dictionary listing the non-valid colors and the
                      values they should be replaced with.
        valid_categories: A dictionary listing the non-valid categories and the
                          values they should be replaced with.
        target_dir: A directory path where the image have been saved.
        
    # Returns:
        A list of valid tags.
    """
    img_labels = []
    
    try:
        g = get_gender(source)
        if g is not None:
            img_labels.append(g)
    except:
        pass
    
    try:
        cat = get_category(source, valid_categories)
        if cat is not None:
            img_labels.append(cat)
    except:
        pass
    
    try: 
        clrs = get_colors(source)
        for c in clrs:
            pc = parse_color(c, wbclrs)
            if pc is not None:
                img_labels.append(rectify_tag(pc, valid_colors))
    except:
        pass
    
    if cat in categories:
        return img_labels
    else:
        return []
