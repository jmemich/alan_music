
# coding: utf-8

# In[180]:

import os
import hashlib
import pandas as pd
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

    def df_dict(self, verbose = True):
        """turn Library() object into a [dict()] which can be read
        into pandas as a dataframe.
        """

        ## number of columns!
        cols = ['md5'] ## unique ID

        for val in self.songs.values():
            for key in val.keys():
                if key not in cols:
                    cols.append(key)

        ## create appropriate dict() structure
        obs_all = []

        for song in self.songs:
            obs = dict()
            for col in cols:
                if col == 'md5':
                    obs[col] = song
                else:
                    try:
                        obs[col] = self.songs[song][col]
                    except:
                        if verbose == True:
                            print col + ' column missing!'
            obs_all.append(obs)

        return obs_all



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


# In[190]:

#############
## TESTING ##
#############

song_list = file_search("C:\\Users\\User\\Desktop\\music_test\\Air")

lib = Library()

for i in song_list:
    lib.add_song( Song(i) )


# In[191]:

print lib


# In[192]:

lib.songs


# In[193]:

## make data frame
df = pd.DataFrame.from_dict( lib.df_dict(verbose = False) )

df

