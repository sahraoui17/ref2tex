import sys
import getopt
import re
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase



#given a file that contains a list of IEEE references, return the reference line
def get_reference_line(referencesFile,numberInBrackets):   
    with open(referencesFile, "rt",encoding="utf-8") as inputFile:
        for line in inputFile:
            if line.startswith(numberInBrackets):
                return line
    return 0

def get_title(referenceLine):
    if(len(referenceLine)>0):#skip empty lines
        try:
            title=re.search('“(.*),”', referenceLine).group(1)
            return title
        except IndexError:
            print(referenceLine,'was not processed')
            return 0

#given a reference number, get its title, and return the correspondng bib key
def get_reference_key(referenceLine,bib_database):
    title=get_title(referenceLine) #get the reference title
    title=title.replace('’',"'")  #MS word have different ' with bib/txt.  ’ and ' are different    
    if title[-1]=='.':#some references has . (dot) at the end, it must be removed before searching in bib file
        title=title[:-1]
    try:
        return next(entry for entry in bib_database.entries if entry['title'][1:-1]==title)['ID']
    except StopIteration:
        print('Reference NOT FOUND in bib file:',title)
        return False

#read a document that contain inline citation in IEEE, i.e. ([7]) and relace it with tex citation command \cite{key_in_bib_file}
def ieee2tex(inputRefs,inputTexFile,bibFile,outputTexFile='output_cited.tex'):

    bib_database = BibDatabase()
    with open(bibFile,encoding="utf-8") as bibtex_file:
        print(bibFile,bibtex_file)
        bib_database = bibtexparser.load(bibtex_file)

    with open(inputTexFile, "rt",encoding="utf-8") as inputFile:
        with open(outputTexFile, "wt",encoding="utf-8") as outputFile:
            for line in inputFile:
                citations= re.findall(r'\[\d+\]',line)
                for citation in citations:
                    try:
                        line=line.replace(citation,'\cite{'+get_reference_key(get_reference_line(inputRefs,citation),bib_database)+'}')
                    except StopIteration:
                        print('reference not found')    
                outputFile.write(line)


def main(RefsFile,inputFile,bibFile,outputFile='cited_tex.tex'):
    import os.path
    
    #check if refFile exists
    if not os.path.isfile(RefsFile):
        print(RefsFile,'does not exist')
        sys.exit()    
    #check if inputFile exists
    if not os.path.isfile(inputFile):
        print(inputFile,'does not exist')
        sys.exit()
    #check if bibFile exists 
    if not os.path.isfile(bibFile):
        print(bibFile,'does not exist')
        sys.exit()
    ieee2tex(RefsFile,inputFile,bibFile,outputFile)
    
if __name__ == "__main__":

    for opt, arg in getopt.getopt(sys.argv[1:],'r:b:i:o:',[])[0]:
        print(opt,arg)
        if opt=='-r':
           RefsFile=arg
        if opt=='-b':
           bibFile=arg
        if opt=='-i':
           inputFile=arg
        if opt=='-o':
           outputFile=arg
        
    try:
        main(RefsFile,inputFile,bibFile,outputFile)
    except NameError:
        main(RefsFile,inputFile,bibFile)