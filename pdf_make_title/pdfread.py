import PyPDF2
import os
import shutil

inpath = './input/'
outpath = './output/'

non_file = []

for i in range(2, 720):
    filename = inpath + '{:04}.pdf'.format(i)
    print(filename)
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            # print(reader.numPages)
            page = reader.getPage(0)
            text = page.extractText()
            split_t = text.split('\n')
            # print(split_t)
            index = 0
            non_flag = True
            for s in split_t:
                if s == '' or index > 10:
                    non_file.append(filename)
                    non_flag = False
                    break
                if s[0] == '1':
                    break
                index+=1
            if non_flag:
                name = ' '.join(split_t[:index-1])
                outfilename = outpath + name + '.pdf'
                outfilename.replace(':', ' ')
                os.rename(filename, outfilename)
                # shutil.copyfile(filename, outfilename)
print(non_file)