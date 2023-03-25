# ref2tex: Covert Inline Citations to Latex Cite Command
## Introduction
Converting inline citations in a Word document to Latex is not an easy task. Even if you have all the references in bibtex, you still need to replace each citation, which requires searching for each reference in the list of biblography then finding that reference's bibtex entry and getting its key, then finally replacing the citation i.e. [1] to \cite{bibkey}.

This repository contains the code of ref2tex package that automaticaly coverts inline citations (e.g. [1] or (Sahraoui et al. 2023)) to latex cite command (e.g. \cite{refkey2023}).

Input:
1-File that contains orginal text with inline citations 
2-Text file that contains list of references (biblography)
3-Bibtex file that contains all bib entries of the references listed in biblography file
Output:
The orginal text where inline citations are replaced with \cite commands

## Supported styles
The following styles are supported:

- APA (which uses (AuthorName Year) format)
- IEEE (which uses ([number]) format)
If your source documents is in difference style, convertying it to APA or IEEE styles should be straight forward using reference management software such as Mendeley or Endnote.

## Usage
You can directly run the script corresponding to the source citation style, for example, if the source document is using APA style:
```
apa2tex.py -i sourceFile -r refsFile -b bibtexFile [-o OutputFile]

-i input file that contains orginal text with inline citations (e.g. [1] for IEEE or (Sahraoui et al. 2023) for APA)
-r txt file that contains list of references (biblography)
-b bib file that contains all bib entries of the references listed in biblography file
-o [optional] the output tex file that will contain the converted inline citations (e.g. \cite{keyX2023}). If not specified output file is named output_cited.tex
```
Example:
```
apa2tex.py -i myFile.tex -r myRefs.txt -b mybib.bib
```


## Instalation
```
pip install ref2tex
```
```
import apa2tex
apa2tex('inputRefs.txt','inputFile.tex','bibFile.bib')
```

## Ongoing improvements
- bibtex entry generation, in case it is missing in the provided bibtex library.
- Deep learning based reference identification (author,year,journal/conference ...etc.) rather than parsing
- provide a web-based service for online citation converting

## Licence
Licensed under the MIT license.

