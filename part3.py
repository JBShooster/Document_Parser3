#Document Parser v3: Final Version
#This version of parser gives the user the ability to determine keywords she/he would like
#the parser to use when sifting through the meta-data. Here we append sys.argv  with those words.
#This parser also splits the program into functions to simplify the process.

import sys
import os
import re
 
sys.argv.append(raw_input("Welcome to Document Tagger Part 3! Today we will be \ntaking keywords chosen by you and using the parser to search \nthrough the metadata of Project Gutenberg texts to find your words. \nEnter the first word: "))
sys.argv.append(raw_input("Great! Now let's try a second word: "))
sys.argv.append(raw_input("A third word: "))
sys.argv.append(raw_input("Okay! This is the final word: "))

print sys.argv
 
title_ptn = re.compile(r'(?:title:\s*)(?P<title>((\S*( )?)+)' + 
                          r'((\n(\ )+)(\S*(\ )?)*)*)', 
                          re.IGNORECASE)
author_ptn = re.compile(r'(author:)(?P<author>.*)', 
    re.IGNORECASE)
translator_ptn = re.compile(r'(translator:)(?P<translator>.*)', 
    re.IGNORECASE)
illustrator_ptn = re.compile(r'(illustrator:)(?P<illustrator>.*)', 
    re.IGNORECASE)
 
meta_search_dict = dict(author=author_ptn,
                    title=title_ptn,
                    translator=translator_ptn,
                    illustrator=illustrator_ptn,
                    )
 
def meta_search(meta_search_dict, text):
    """Returns results of search for metadata from text"""
    results = {}
    for k in meta_search_dict:
        result = re.search(meta_search_dict[k], text)
        if result:
            results[k] = result.group(k)
        else:
            results[k] = None
    return results
 
 
def file_opener(fl_path):
    """Given a full path to a file, opens that file and returns its contents"""
    with open(fl_path, 'r') as f:
        return f.read()
 
def file_path_maker(directory, fl_name):
    return os.path.join(directory, fl_name)
 
def kw_pattern_maker(kws):
    """Returns dictionary of keyword regular expression patterns"""
    result = {kw: re.compile(r'\b' + kw + r'\b') for kw in kws}
    return result
 
def kw_counter(pattern, text):
    """Returns the number of matches for a keyword in a given text"""
    matches = re.findall(pattern, text)
    return len(matches)
 
def doc_tag_reporter(directory, kws):
    """
    This will iterate through the text documents in Project Gutenberg and reveal the data we ask of it
    """
    for fl in os.listdir(directory):
        if fl.endswith('.txt'):
            fl_path = file_path_maker(directory, fl)
            text = file_opener(fl_path)
            meta_searches = meta_search(meta_search_dict, text)
            kw_searches = kw_pattern_maker(kws)
            print "Here's the info for {}:".format(fl)
            for k in meta_searches:
                print "{0}: {1}".format(k.capitalize(), meta_searches[k])
            print "\n****KEYWORD REPORT****\n\n"
            for kw in kw_searches:
                print "\"{0}\": {1}".format(kw, kw_counter(kw_searches[kw], text))
            print '\n\n'
            print "***" * 25


def main():
    directory = "C:\Python27\projects\document_tagger\part3"
    kws = [i for i in sys.argv[1:]]
    doc_tag_reporter(directory, kws)

if __name__ == '__main__':
    main()

raw_input("\n\nPress any key to exit...")

