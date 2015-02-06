
# coding: utf-8

# In[7]:

import os
import hashlib
from mutagen.easyid3 import EasyID3



class Song(object):
    """ create Song object from file path.
    """
    
    def __init__(self, path = ''):
        self.path = path
        
    def __str__(self):
        return str(self.get_metadata()['title'])
        
    def get_md5(self):
        con = open(self.path, 'rb')
        return hashlib.md5(con.read()).hexdigest()
    
    def get_metadata(self):
        return EasyID3(self.path)
    
    def keys_num(self):
        return len(self.get_metadata().keys())

    
    
class Library(object):
    """Creates a song library.
    """
     
    def __init__(self, song = None):
        self.songs = dict()
        
    def __str__(self):
        return 'Song Library has %i song(s)' % len(self.songs.keys()) 
        
    def add_song(self, Song):
        """NOTE: potentially problematic if two songs have same md5
        data! Will overwrite 1st!?
        """
        
        self.songs.update( {Song.get_md5() : Song.get_metadata()} )

        

def file_search(filepath, results_list = []):
    """ recursive function to list all files in all subfolders.
    Note list creation as argument in function!
    """
    
    # loop over each item in directory
    for item in os.listdir(filepath):
        
        path = os.path.join(filepath, item)

        if os.path.isfile(path):
            results_list.append(path)
        else:
            file_search(path) ## recursive call

    return results_list


# In[8]:

song_list = file_search("C:\\Users\\User\\Desktop\\music_test\\Air")


# In[9]:

song_list


# In[11]:

for i in song_list:
    print Song(i)


# In[12]:

lib = Library()


# In[13]:

for i in song_list:
    lib.add_song( Song(i) )


# In[15]:

print lib


# In[16]:

lib.songs


# In[ ]:



