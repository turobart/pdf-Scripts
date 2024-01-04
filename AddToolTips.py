import fitz
import re

fname = "filename.pdf"  # filename
# text = "CL"  # search string
doc = fitz.open(fname)
regex = re.compile('[^0-9a-zA-Z-]')
start_page = 1
abbrev_page = 6
end_page = 100
new_doc = False  # indicator if anything found

new_properties = {"title": u'NewTitle',
                  "subject" : 'subjest',
                  "keywords" :'tag1 ; tag2 ',
                  "creationDate" : "D:20240101090000+02'00'", # date in formt yyyymmddhhmmss+timezone
                  "modDate" : "D:20240101090000+02'00'"} # date in formt yyyymmddhhmmss+timezone

# labels of pages in pdf; r gives roman labels
pageLabels = [{'startpage': 8, 'prefix': '', 'style': 'D', 'firstpagenum': 1},
              {'startpage': 0, 'prefix': '', 'style': 'r', 'firstpagenum': 1}]


# open file with abbreviations
with open("abbrevs.txt") as abbrev_file:
    abbrev_list = [line.rstrip() for line in abbrev_file]

# open file with fill names
with open("full_names.txt") as names_file:
    names_list = [line.rstrip() for line in names_file]

for page in doc:  # scan through the pages
    if page.number <start_page:
        continue
    if page.number == abbrev_page:
        continue
    found = 0
    wlist = page.get_text("words")  # make the word list
    for abbrev in abbrev_list:
        tooltip_text = names_list[abbrev_list.index(abbrev)]
        for w in wlist:  # scan through all words on page
            word_itallic = False
            word_bold = False
            tooBig = False
            current_word = regex.sub('', w[4])
            
            if abbrev == current_word:  # w[4] is the word's string
                blocks = page.get_text("dict", flags=11)["blocks"]
                for b in blocks:  # iterate through the text blocks
                    if b['number']!=w[5]:
                        continue
                    for l in b["lines"]:  # iterate through the text lines
                        for s in l["spans"]:  # iterate through the text spans
                            if s["flags"] & 2 ** 4 and current_word in s["text"]:
                                word_bold = True
                            if s["size"]>12:
                                tooBig = True
                if word_bold:
                    continue
                if tooBig:
                    continue

                if len(abbrev) == 1 and len(current_word) !=1:
                    continue
                elif len(abbrev) == 1 and len(current_word) == 1:
                    blocks = page.get_text("dict", flags=11)["blocks"]
                    for b in blocks:  # iterate through the text blocks
                        if b['number']!=w[5]:
                            continue
                        for l in b["lines"]:  # iterate through the text lines
                            for s in l["spans"]:  # iterate through the text spans
                                if s["flags"] & 2 ** 1 and current_word in s["text"]:
                                    word_itallic = True
                if len(current_word) == 1 and not word_itallic:
                    continue
                    
                if current_word[-1] == 's':
                    tooltip_text_to_insert = tooltip_text +'s'
                else:
                    tooltip_text_to_insert = tooltip_text

                found += 1  # count
                r = fitz.Rect(w[:4])  # make rect from word bbox
#                 page.insert_textbox(r, "ToolTip", align=fitz.TEXT_ALIGN_RIGHT)
                
                # add ToolTip as an invisible button
                widget = fitz.Widget()
                widget.field_name = "Button-%s%s" %(page.number, found)
                widget.field_label = tooltip_text_to_insert
                widget.field_type = fitz.PDF_WIDGET_TYPE_BUTTON
                widget.fill_color = None #make button transparent
#                 widget.fill_color = (1,1,1) 
                widget.border_color = None
                widget.rect = r
    #             widget.text_font = "TiRo"
                widget.field_value = True
                annot = page.add_widget(widget)
                print("Added field '%s'" % abbrev)
        if found:  # if anything found ...
            new_doc = True
            doc.set_metadata(new_properties)
            doc.set_page_labels(pageLabels)
#             print("found '%s' %i times on page %i" % (abbrev, found, page.number + 1))

if new_doc:
    doc.save("ToolTips-" + doc.name)