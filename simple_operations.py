from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import os

# -------- merge files --------
def merge_files():
    files_path = "path_to_folder_woth_pdfs"
    
    all_files = os.listdir(files_path)
    merger = PdfFileMerger()
    
    for pdf_file in all_files:
        file_path = os.path.join(files_path, pdf_file)
        print(file_path)
        merger.append(PdfFileReader(file_path, 'rb'))
         
    merger.write(os.path.join(files_path, "merged.pdf"))


# -------- add bookmarks --------
def add_bookmarks():
    pdf_file_path = "filepath\\filename.pdf"
    output_file = "result.pdf"
     
    bookmarks_parents = ["bookmark1", "bookmark2", "bookmark3"]
    bookmarks_pages = [[1,2], [1,2,3], [3]]
     
    file_to_open = open(pdf_file_path, 'rb')
    inputpdf = PdfFileReader(file_to_open)
     
    writer = PdfFileWriter()
    
    page_count=0
    for page in range(inputpdf.getNumPages()):
        current_page = inputpdf.getPage(page)
        if page_count==5:
            current_page.rotateCounterClockwise(90)
        current_page.compressContentStreams()
        writer.addPage(current_page)
        page_count+=1
     
    bookmark_count = 0
    for bookmark in bookmarks_pages:
        if len(bookmark)==1:
            writer.addBookmark(bookmarks_parents[bookmark_count], bookmark[0])
        else:
            parent=writer.addBookmark(bookmarks_parents[bookmark_count], bookmark[0])
            for subpage in bookmark:
                writer.addBookmark("page_"+str(subpage+1), subpage, parent)
        bookmark_count+=1
              
       
    with open(output_file, 'wb') as final_file:
        writer.write(final_file)
    file_to_open.close()
merge_files()