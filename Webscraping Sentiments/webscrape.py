import os
import re
import sys
import urllib

DEBUG = True
COMMENT_SEARCH_URL = "https://www.youtube.com/all_comments"
COMMENT_TAG_HEAD = '<div class="comment-text-content">'
COMMENT_TAG_TAIL = '</div>'
NUM_OF_COMMENTS = None
HAPPY_LIST = ['love','loved','like','liked','awesome','amazing','good','great','excellent','best','wonderful','cool']
SAD_LIST = ['hate','hated','dislike','disliked','awful','terrible','bad','painful','worst','sucks','sucked','stupid','dumb','asshole','shitty','dogshit','failure','idiot']

SEP_RE = re.compile(r'[\s\W]')
HTML_RE = re.compile(r'<.+>')
WEB_PATH_RE = re.compile(r'https://www\.youtube\.com/watch\?v=[\w\-]+')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[0] == __file__ or sys.argv[0] == os.path.basename(__file__):
        web_path = sys.argv[1]
        if DEBUG: print web_path
    else:
        web_path = raw_input("Enter a valid URL to a Youtube video: ")
    
    if WEB_PATH_RE.search(web_path) == None:
        print "Invalid path! Program is shutting down."
        sys.exit()

    happy_count = 0
    sad_count = 0
    comments = {}
    
    html_file = urllib.urlopen("".join([COMMENT_SEARCH_URL, web_path[web_path.find('?'):]]))
    html_source = html_file.read()
    html_file.close()

    index = 0
    end_index = 0
    while NUM_OF_COMMENTS == None or len(comments) < NUM_OF_COMMENTS:
        index = html_source.find(COMMENT_TAG_HEAD, end_index)
        if index == -1:
            break
        end_index = html_source.find(COMMENT_TAG_TAIL, index)

        cm = html_source[index+len(COMMENT_TAG_HEAD):end_index]
        cm = "".join(HTML_RE.split(cm))
        if cm in comments:
            cm_count = 1
            while True:
                cm_copy = "".join([cm, '(', str(cm_count), ')'])
                if cm_copy not in comments:
                    cm = cm_copy
                    break
                cm_count += 1
        #Index0 is the happy count for the comment; Index1 is the sad count
        comments[cm] = [0,0]
        
        for word in SEP_RE.split(cm):
            if word.lower() in HAPPY_LIST:
                happy_count += 1
                comments[cm][0] += 1
            elif word.lower() in SAD_LIST:
                sad_count += 1
                comments[cm][1] += 1

    print "From a sample size of {0}:\n".format(len(comments))
    for cm in comments.keys():
        print cm
        if comments[cm][0] > comments[cm][1]:
            mood_single = "Happy"
        elif comments[cm][0] < comments[cm][1]:
            mood_single = "Sad"
        else:
            mood_single = "Neutral"
        print "This sentence is mostly {0}. It contained {1} amount of Happy keywords and {2} amount of Sad keywords\n".format(mood_single, comments[cm][0], \
                                                                                                                               comments[cm][1])
    if happy_count > sad_count:
        mood = "Happy"
    elif happy_count < sad_count:
        mood = "Sad"
    else:
        mood = "Neutral"

    print "The general feelings towards this video was {0}\n".format(mood)
    print "The number of Happy keywords is {0} and the number of Sad keywords is {1}".format(happy_count, sad_count)
