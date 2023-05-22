## imports
import PyPDF2

def write_to_file(path):
    pdf = open(path, 'rb')
    pdf = PyPDF2.PdfFileReader(pdf, strict=False)
    text = str()
    for page in range(pdf.numPages):
        page_obj = pdf.getPage(page)
        text += page_obj.extract_text()
    text = text.split('\n')
    path2 = './text_files/' + path.split('/')[-1].split('.')[0] + '.txt'
    with open(path2, 'w') as f:
        f.writelines(text)

file_path = list()
file_path.append('/home/hitesh/Documents/IIIT-H/Honours 2/IR/journeys/1810 Survey for Discovering Sources of the Ganges by Raper from ARv11 s.pdf')
file_path.append('/home/hitesh/Documents/IIIT-H/Honours 2/IR/journeys/1820 Journey to Sources of Jumna and Bhagirathi Rivers by Fraser from ARv13 s.pdf')
file_path.append('/home/hitesh/Documents/IIIT-H/Honours 2/IR/journeys/1825 Course and Levels of River Setlej or Satudra in 1819 by Herbert from ARv15 s.pdf')
# map_path = '/home/hitesh/Documents/IIIT-H/Honours 2/IR/wb_countries_admin0_10m/WB_countries_Admin0_10m/WB_countries_Admin0_10m.shp'
for i in file_path:
    write_to_file(i)