import re
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
import sys
import getopt

#take an inline citation (i.e. Saha et al. 2023) and find how the author name will be in the reference list accoring to APA, 
def get_APA_author_name(citation):
    splited=citation.split('.')
    if(len(splited[0])==1):
        return citation.split(' ')[1]+', '+splited[0]+'.'
    elif(len(splited[0])>1):
        return citation.split(' ')[0]+','
    else:
        return 'Not APA'

#given a file that contains a list of APA references, 
def get_reference_line(referencesFile,firstAuthor):   
    with open(referencesFile, "rt",encoding="utf-8") as inputFile:
        for line in inputFile:
            if line.startswith(firstAuthor):
                return line
    return 0

def parse_reference(referenceLine):#get apa ref as string and return [authors,year,title]
    if(len(referenceLine)>0):#skip empty lines
        try:
            year_parenthesis=re.findall(r'\(\d+\).',referenceLine)[0]
            year=year_parenthesis[1:-2]
            title=referenceLine.split(year_parenthesis,1)[1].split('.')[0][1:]
            authors=referenceLine.split(year_parenthesis,1)[0][:-1]
            return [authors,year,title]
        except IndexError:
            print(referenceLine,'was not processed')
            return ['Author Not Found','Year Not Found','Title Not Found']
            #print('line:'+str(index)+' was not processed: '+ref)

#given a reference number, get its title, and return the correspondng bib key
def get_reference_key(referenceLine,bib_database):
    title=parse_reference(referenceLine)[2] #get the reference title
    title=title.replace('’',"'")  #MS word have different ' with bib/txt.  ’ and ' are different    
    return next(entry for entry in bib_database.entries if entry['title'][1:-1]==title)['ID']


#read a document that contain inline citation in APA, i.e. (Saha et al. 2023) and relace it with tex citation command \cite{key_in_bib_file}
def apa2tex(inputRefs,inputTexFile,bibFile,outputTexFile='cited_tex.tex'):    

    bib_database = BibDatabase()
    with open(bibFile,encoding="utf-8") as bibtex_file:
        print(bibFile,bibtex_file)
        bib_database = bibtexparser.load(bibtex_file)

    with open(inputTexFile, "rt",encoding="utf-8") as inputFile:
        with open(outputTexFile, "wt",encoding="utf-8") as outputFile:
            for line in inputFile:
                citations= re.findall(r"\((?:[A-Z][A-Za-z\.\s\&'`-]+), (?:19|20)[0-9][0-9]\)",line)
                for citation in citations:
                    try:
                        #print(citation)
                        reference_line=get_reference_line(inputRefs,get_APA_author_name(citation[1:-1]))
                        #get_reference_key(ref[1:-1])
                        line=line.replace(citation,'\cite{'+get_reference_key(reference_line,bib_database)+'}')
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
    apa2tex(RefsFile,inputFile,bibFile,outputFile)
    
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
