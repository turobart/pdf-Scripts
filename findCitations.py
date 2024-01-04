# -*- coding: utf-8 -*-

import fitz

fname = "filename.pdf"  # filename

doc = fitz.open(fname)

start_page = 0
end_page = 100
numberOfRomanPages = 9
    
allRefs = []
for page in doc:  # scan through the pages
    if int(page.number) <= start_page or int(page.number) >= end_page:
        continue
    found = 0
    word_bold = False
    refBlock = ''
    pageRefs = []
    pageSingleRef = []
    blocks = page.get_text("dict", flags=11)["blocks"]
    for b in blocks:  # iterate through the text blocks
        for l in b["lines"]:  # iterate through the text lines
            for s in l["spans"]:  # iterate through the text spans
                if "[" in s["text"] or "]" in s["text"]:
                    if s["flags"] & 2 ** 4:  # is bold - for bold citations
                        if not s["flags"] & 2 ** 1: # is not itallic
                            refBlock = s["text"].strip('[]')
#                             print(refBlock)
                            if not '-' in refBlock:
                                pageSingleRef = [s for s in refBlock.split(', ') if s.isdigit()]

                            else:
                                pageSingleRef = []
                                tempPageRefs = refBlock.split(', ')
                                for ref in tempPageRefs:
                                    if '-' in ref and not 'Sn' in ref: # rare case of α-Sn in textblock with citation
                                        tempPageRefs.remove(ref)
                                        temp_range = ref.split('-')
                                        range_delta = int(temp_range[-1])-int(temp_range[0])
                                        for citation in range(range_delta+1):
                                            tempPageRefs.append(str(int(temp_range[0])+citation))
                                        pageSingleRef = tempPageRefs
                            for Ref in pageSingleRef:
                                if len(Ref)>0:
                                    pageRefs.append(int(Ref))

          
    refsSorted = sorted(set(pageRefs))    
    print(refsSorted, " page %s" %( (page.number+1) - start_page))
# #     print('---PAGE BREAK---')
    allRefs.append(refsSorted)
numberOfRefs = max([sublist[-1] for sublist in allRefs if len(sublist)>0])

refsInPage=[]
refsPerPage = []

# print(allRefs)

for ref in range(1, numberOfRefs+1):
    refsInPage=[]
    for sublist in allRefs:
        if ref in sublist: 
            pageOfOccurance = allRefs.index(sublist)+1        
            refsInPage.append(pageOfOccurance-numberOfRomanPages+2)
    refsPerPage.append(refsInPage)

# wite pages on which the reference occurs
with open('refsPages.txt', 'w') as file:
    ref_count=0
    for pages in refsPerPage:
        ref_count+=1
        file.write("Ref [%s] on pages:\t" %(ref_count))
        for page in pages:
            file.write(str(page))
            if len(pages)>1: file.write(', ')
        file.write('\n')
