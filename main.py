import os
import pickle


if not os.path.exists('assets/token.pickle'):
    os.system('python signin/signin.py')
 
else:
    f = open('assets/token.pickle', 'rb')
    try:
        if pickle.load(f) == 'signedout':
            os.system('python signin/signin.py')
        else:
            os.system('python guimain/guimain.py')
    except EOFError:
        os.system('python signin/signin.py')
