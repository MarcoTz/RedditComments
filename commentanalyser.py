import praw
import tkinter
import tkinter.messagebox

#analyses comments in entered thread
def analyseComments():
    if linkEntry.get() is not None:
        post = threadByUrl(linkEntry.get())
        wordcount = getWordCounts(post)
        print(wordcount)
        displayWordCount(wordcount)
    
#get thread by Id
def threadByUrl(threadId):
    try:
        post = r.get_submission(url=threadId)
        return post
    except Exception:
        tkinter.messagebox.showerror('404','thread not found, try again')
        return None

#counts occurance of words in reddit thread post, returns dictionary with occurence numbers
def getWordCounts(post):
    wordcount = dict() 
    post.replace_more_comments(None,0)
    for comment in praw.helpers.flatten_tree(post.comments):
        if hasattr(comment,'body'):
            words = str(comment.body.encode('utf-8'))[2:-1].split()
            for word in words:
                if word in wordcount:
                    wordcount[word] = wordcount[word]+1
                else:
                    wordcount[word] = 1
    return wordcount

#displays wordcount dict in seperate window
def displayWordCount(wordcount):
    
    infostring = ''
    
    sortedkeys  = sorted(wordcount, key=wordcount.get)
    sortedkeys.reverse()
    
    for key in sortedkeys:
        infostring += key+':'+str(wordcount[key])+'\n'

    tkinter.messagebox.showinfo('words in comments',infostring)

r=praw.Reddit(user_agent = 'linux:pythonscript:v1.0 by /u/rooxo')

mainWindow = tkinter.Tk()
mainWindow.wm_title('Reddit comment analizer')

explanationLabel = tkinter.Label(mainWindow, text='Enter link to thread:')
explanationLabel.grid(row=0,column=0)

linkEntry = tkinter.Entry(mainWindow)
linkEntry.grid(row=1,column=0)
submit = tkinter.Button(mainWindow, text='analyse comments', command=analyseComments)
submit.grid(row=1,column=1)

mainWindow.mainloop()