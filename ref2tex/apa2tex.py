import re
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase




bib_database = BibDatabase()
with open('refs.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)


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
    with open(referencesFile, "rt") as inputFile:
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
def get_reference_key(referenceLine):
    title=parse_reference(referenceLine)[2] #get the reference title
    title=title.replace('’',"'")  #MS word have different ' with bib/txt.  ’ and ' are different
    #print(title)
    
    return next(entry for entry in bib_database.entries if entry['title'][1:-1]==title)['ID']


#read a document that contain inline citation in APA, i.e. (Saha et al. 2023) and relace it with tex citation command \cite{key_in_bib_file}
def apa2tex(inputRefs,inputTexFile,outputTexFile='cited_tex.tex'):    
    with open(inputTexFile, "rt") as inputFile:
        with open(outputTexFile, "wt") as outputFile:
            for line in inputFile:
                citations= re.findall(r"\((?:[A-Z][A-Za-z\.\s\&'`-]+), (?:19|20)[0-9][0-9]\)",line)
                for citation in citations:
                    try:
                        #print(citation)
                        reference_line=get_reference_line(inputRefs,get_APA_author_name(citation[1:-1]))
                        #get_reference_key(ref[1:-1])
                        line=line.replace(citation,'\cite{'+get_reference_key(reference_line)+'}')
                    except StopIteration:
                        print('reference not found')    
                print(line)    
                # #outputFile.write(line)

apa2tex('inputRefs.txt','input.tex','someout')

#print(get_reference_key('Mendu, S., Boukhechba, M., Baglione, A., Baee, S., Wu, C., & Barnes, L. (2019). SocialText: A Framework for Understanding the Relationship Between Digital Communication Patterns and Mental Health. 2019 IEEE 13th International Conference on Semantic Computing (ICSC), 428–433. '))

#print(get_reference_key('Wongkoblap, A., Vadillo, M. A., & Curcin, V. (2019). Modeling Depression Symptoms from Social Network Data through Multiple Instance Learning. AMIA Joint Summits on Translational Science Proceedings. AMIA Joint Summits on Translational Science, 2019, 44–53. https://pubmed.ncbi.nlm.nih.gov/31258955'))


# citations=['(T. Liu et al., 2022)', '(S. Li et al., 2020)', '(Hou et al., 2020)', '(Wongkoblap et al., 2019)', '(Mendu et al., 2019)', '(Wan et al., 2019)']
# for citation in citations:
#     print(get_APA_author_name(citation[1:-1]))

#     with open('s.txt', "rt") as inputFile:
#         for line in inputFile:
#             if line.startswith(get_APA_author_name(citation[1:-1])):
#                 print(line)
    
#"s.txt"
