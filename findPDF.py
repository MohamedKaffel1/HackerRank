from PyPDF2 import PdfFileReader
from pprint import pprint
from f1fileOpen import f1file


def walk(obj, fnt, emb):
    '''
    If there is a key called 'BaseFont', that is a font that is used in the document.
    If there is a key called 'FontName' and another key in the same dictionary object
    that is called 'FontFilex' (where x is null, 2, or 3), then that fontname is 
    embedded.
    
    We create and add to two sets, fnt = fonts used and emb = fonts embedded.
    '''
    if not hasattr(obj, 'keys'):
        return None, None
    fontkeys = set(['/FontFile', '/FontFile2', '/FontFile3'])
    if '/BaseFont' in obj:
        fnt.add(obj['/BaseFont'])
    if '/FontName' in obj:
        if [x for x in fontkeys if x in obj]:# test to see if there is FontFile
            emb.add(obj['/FontName'])

    for k in obj.keys():
        walk(obj[k], fnt, emb)

    return fnt, emb# return the sets for each page


def OCRized(fname):
    
    pdf = PdfFileReader(fname)
    fonts = set()
    embedded = set()
    for page in pdf.pages:
        
        obj = page.getObject()
        f, e = walk(obj['/Resources'], fonts, embedded)
        fonts = fonts.union(f)
        embedded = embedded.union(e)
    
    if not fonts :
       return  False
       #print "There's no fonts" 
    else:
       #print "Actually there's fonts"
       return  True
       '''
    unembedded = fonts - embedded
    #print 'Font List'
    pprint(sorted(list(fonts)))
    if unembedded:
        print '\nUnembedded Fonts'
        pprint(unembedded)



fname = f1file()
a=OCRized(fname)
print a   
'''
