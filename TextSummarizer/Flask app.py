from __future__ import unicode_literals
from flask import Flask,url_for,render_template,request,flash,redirect,send_from_directory
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
#NLP Packages
from spacy_summarization import text_summarizer
from nltk_summarization import nltk_summarizer
import gensim
from gensim.summarization import summarize
import spacy
nlp = spacy.load('en_core_web_sm')
import time
from googletrans import Translator, LANGUAGES
import PyPDF2
from PyPDF2 import PdfFileReader
import docx
#Web Scraping Packages
from bs4 import BeautifulSoup
from urllib.request import urlopen


hdr={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}




app=Flask(__name__)
SESSION_TYPE = "redis"
PERMANENT_SESSION_LIFETIME = 1800

app.config.update(SECRET_KEY=os.urandom(24))
#Home[2]
#Compare[2]

#Sumy Package
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


#functions
def readingTime(mytext):
    total_words=len([token.text for token in nlp(mytext)])
    estimated_time=total_words/265.0
    return estimated_time

def size_summ(final_summary):
    return (len(final_summary))

def size_inn(raw_docx):
    raw_text = raw_docx
    return len(raw_text)

def get_text(url):
    page=urlopen(url)
    soup=BeautifulSoup(page,"lxml")
    fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
    return fetched_text


#sumy
def sumy_summary(docx):
    parser=PlaintextParser.from_string(docx,Tokenizer("english"))
    lex_summarizer=LexRankSummarizer()
    summary =lex_summarizer(parser.document,3)
    summary_list = [str(sentence) for sentence in summary]
    result=''.join(summary_list)
    return result

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze',methods=['GET','POST'])
def analyze():
    start=time.time()
    if request.method=='POST':
        rawtext=request.form['rawtext']
        final_reading_time= readingTime(rawtext)
        #summarization
        final_summary=text_summarizer(rawtext)
        #Reading Time
        summary_reading_time= readingTime(final_summary)
        end=time.time()
        final_time= end-start
        Length_Input=size_inn(rawtext)
        Length_Output=size_summ(final_summary)
    return render_template('index.html',ctext=rawtext,Length_Input=Length_Input,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,Length_Output=Length_Output,summary_reading_time=summary_reading_time)



@app.route('/use_url')
def use_url():
    return render_template('use_url.html')


@app.route('/analyze_url',methods=['GET','POST'])
def analyze_url():
    start=time.time()
    if request.method=='POST':
        raw_url = request.form['raw_url']
        rawtext = get_text(raw_url)

        final_reading_time= readingTime(rawtext)
        #summarization
        final_summary=text_summarizer(rawtext)
        #Reading Time
        summary_reading_time= readingTime(final_summary)
        end=time.time()
        final_time= end-start
        Length_Input=size_inn(rawtext)
        Length_Output=size_summ(final_summary)
    return render_template('use_url.html',ctext=rawtext,Length_Input=Length_Input,Length_Output=Length_Output,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)



@app.route('/use_file')
def use_file():
    return render_template('use_file.html')

#app.config["IMAGE_UPLOADS"]=r"C:\Users\lenovo\Desktop\TextSummarizer\static\img\uploads"
app.config["IMAGE_UPLOADS"] = r'C:\Users\lenovo\Desktop\TextSummarizer'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PDF", "TXT", "DOC", "DOCX"]

def allowed_image(filename):

    # We only want files with a . in the filename
    if not "." in filename:
        return False

    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route('/upload-image',methods=['GET','POST'])
def upload_image():
    start=time.time()
    if request.method=='POST':
        if request.files:
            image=request.files["image"]
            if image.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"],filename))

                flash("File saved")

                #return redirect(request.url)
                name= image.filename
                ext = filename.rsplit(".", 1)[1]
                if ext=='txt':


                    f=open(image.filename,'r')
                    #f=open(r'C:\Users\lenovo\Desktop\TextSummarizer\static\img\uploads\image.filename','r')
                    read_text =f.read()

                    #f=open(r'static\img\uploads','r')
                    #contents=f.read()
                    flash("read_text")
                    final_reading_time= readingTime(read_text)
                    #summarization
                    final_summary=text_summarizer(read_text)
                    #Reading Time
                    summary_reading_time= readingTime(final_summary)
                    end=time.time()
                    final_time= end-start
                    Length_Input=size_inn(read_text)
                    Length_Output=size_summ(final_summary)
                    return render_template('use_file.html',ctext=read_text,Length_Input=Length_Input,Length_Output=Length_Output,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)

                if ext=='pdf':
                    pdfFileObj = open(image.filename, 'rb')

                    # creating a pdf reader object
                    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)


                    # printing number of pages in pdf file
                    print(pdfReader.numPages)

                    # creating a page object
                    pageObj = pdfReader.getPage(0)



                    # extracting text from page
                    p=(pageObj.extractText())

                    flash("read_text")
                    final_reading_time= readingTime(p)
                    #summarization
                    final_summary=text_summarizer(p)
                    #Reading Time
                    summary_reading_time= readingTime(final_summary)
                    end=time.time()
                    final_time= end-start
                    Length_Input=size_inn(p)
                    Length_Output=size_summ(final_summary)
                    return render_template('use_file.html',ctext=p,Length_Input=Length_Input,Length_Output=Length_Output,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)


                if ext == "docx":
                    doc = docx.Document(image.filename)
                    fullText = []
                    for para in doc.paragraphs:
                        fullText.append(para.text)
                        data='\n'.join(fullText)
                        final_reading_time= readingTime(data)
                    #summarization
                        final_summary=text_summarizer(data)
                    #Reading Time
                        summary_reading_time= readingTime(final_summary)
                        end=time.time()
                        final_time= end-start
                        Length_Input=size_inn(data)
                        Length_Output=size_summ(final_summary)
                    return render_template('use_file.html',ctext=data,Length_Input=Length_Input,Length_Output=Length_Output,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)

                    #print (readtxt('path\Tutorialspoint.docx'))










                    return render_template('use_file.html',ctext=read_text,Length_Input=Length_Input,Length_Output=Length_Output,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)







                return redirect(request.url)











            else:
                error="Invalid file type. Please upload .doc,.docx,.txt,.pdf files"
                return render_template('use_file.html',error=error)
                #return redirect(request.url)


            return redirect(request.url)



    return render_template('use_file.html')





































#Compare Tab
@app.route('/compare_summary')
def compare_summary():
    return render_template('compare_summary.html')

@app.route('/comparer',methods=['GET','POST'])
def comparer():
    start = time.time()
    if request.method == 'POST':
            rawtext = request.form['rawtext']
            Length_Input=size_inn(rawtext)
            final_reading_time = readingTime(rawtext)
            final_summary_spacy = text_summarizer(rawtext)
            summary_reading_time = readingTime(final_summary_spacy)
            Length_Input=size_inn(rawtext)
            Length_Output_Spacy=size_summ(final_summary_spacy)
    #Sumy summary
            final_summary_sumy = sumy_summary(rawtext)
            summary_reading_time_sumy = readingTime(final_summary_sumy)
            Length_Input=size_inn(rawtext)
            Length_Output_LexRank=size_summ(final_summary_sumy)

		        #Nltk summary
            final_summary_nltk = nltk_summarizer(rawtext)
            summary_reading_time_nltk = readingTime(final_summary_nltk)
            Length_Input=size_inn(rawtext)
            Length_Output_NLTK=size_summ(final_summary_nltk)
    #Gensim summary
            final_summary_gensim = summarize(rawtext)
            summary_reading_time_gensim = readingTime(final_summary_gensim)
            Length_Input=size_inn(rawtext)
            Length_Output_TextRank=size_summ(final_summary_gensim)


    #reading
            end = time.time()
            final_time = end-start
    return render_template('compare_summary.html',ctext=rawtext,Length_Input=Length_Input,Length_Output_Spacy=Length_Output_Spacy,Length_Output_LexRank=Length_Output_LexRank,Length_Output_NLTK=Length_Output_NLTK,Length_Output_TextRank=Length_Output_TextRank,final_summary_spacy=final_summary_spacy,final_summary_gensim=final_summary_gensim,final_summary_nltk=final_summary_nltk,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time,summary_reading_time_gensim=summary_reading_time_gensim,final_summary_sumy=final_summary_sumy,summary_reading_time_sumy=summary_reading_time_sumy,summary_reading_time_nltk=summary_reading_time_nltk )

@app.route('/about')
def about():
    return render_template('index.html')

@app.route('/translate_summary')
def translate_summary():
    return render_template('translate_summary.html')

@app.route('/predict', methods=['POST'])
def predict():
    translator=Translator()
    message = request.form['message']
    lang=request.form['languages']
    lang=lang.lower()

    if(lang=="afrikaans"):
	    dest_code='af'
    if(lang=="albanian"):
    	dest_code='sq'
    if(lang=="amharic"):
    	dest_code='am'
    if(lang=="arabic"):
    	dest_code='ar'
    if(lang=="armenian"):
    	dest_code='hy'
    if(lang=="azerbaijani"):
    	dest_code='az'
    if(lang=="basque"):
    	dest_code='eu'
    if(lang=="belarusian"):
    	dest_code='be'
    if(lang=="bengali"):
    	dest_code='bn'
    if(lang=="bosnian"):
    	dest_code='bs'
    if(lang=="bulgarian"):
    	dest_code='bg'
    if(lang=="catalan"):
    	dest_code='ca'
    if(lang=="cebuano"):
    	dest_code='ceb'
    if(lang=="chichewa"):
    	dest_code='ny'
    if(lang=="chinese(simplified) "):
    	dest_code='zh-cn'
    if(lang=="chinese(traditional) "):
    	dest_code='zh-tw'
    if(lang=="corsican"):
    	dest_code='co'
    if(lang=="croatian"):
    	dest_code='hr'
    if(lang=="czech"):
    	dest_code='cs'
    if(lang=="danish"):
    	dest_code='da'
    if(lang=="dutch"):
    	dest_code='nl'
    if(lang=="english"):
    	dest_code='en'
    if(lang=="esperanto"):
    	dest_code='eo'
    if(lang=="estonian"):
    	dest_code='et'
    if(lang=="filipino"):
    	dest_code='tl'
    if(lang=="finnish"):
    	dest_code='fi'
    if(lang=="french"):
    	dest_code='fr'
    if(lang=="frisian"):
    	dest_code='fy'
    if(lang=="galician"):
    	dest_code='gl'
    if(lang=="georgian"):
    	dest_code='ka'
    if(lang=="german"):
    	dest_code='de'
    if(lang=="greek"):
    	dest_code='el'
    if(lang=="gujarati"):
    	dest_code='gu'
    if(lang=="haitian"):
    	dest_code='ht'
    if(lang=="hausa"):
    	dest_code='ha'
    if(lang=="hawaiian"):
    	dest_code='haw'
    if(lang=="hebrew"):
    	dest_code='iw'
    if(lang=="hindi"):
    	dest_code='hi'
    if(lang=="hmong"):
    	dest_code='hmn'
    if(lang=="hungarian"):
    	dest_code='hu'
    if(lang=="icelandic"):
    	dest_code='is'
    if(lang=="igbo"):
    	dest_code='ig'
    if(lang=="indonesian"):
    	dest_code='id'
    if(lang=="irish"):
    	dest_code='ga'
    if(lang=="italian"):
    	dest_code='it'
    if(lang=="japanese"):
    	dest_code='ja'
    if(lang=="javanese"):
    	dest_code='jw'
    if(lang=="kannada"):
    	dest_code='kn'
    if(lang=="kazakh"):
    	dest_code='kk'
    if(lang=="khmer"):
    	dest_code='km'
    if(lang=="korean"):
    	dest_code='ko'
    if(lang=="kurdish(kurmanji) "):
    	dest_code='ku'
    if(lang=="kyrgyz"):
    	dest_code='ky'
    if(lang=="lao"):
    	dest_code='lo'
    if(lang=="latin"):
    	dest_code='la'
    if(lang=="latvian"):
    	dest_code='lv'
    if(lang=="lithuanian"):
    	dest_code='lt'
    if(lang=="luxembourgish"):
    	dest_code='lb'
    if(lang=="macedonian "):
            dest_code='mk'
    if(lang==" malagasy "):
            dest_code='mg'
    if(lang==" malay "):
            dest_code='ms'
    if(lang==" malayalam "):
            dest_code='ml'
    if(lang==" maltese "):
            dest_code='mt'
    if(lang==" maori "):
            dest_code='mi'
    if(lang==" marathi "):
            dest_code='mr'
    if(lang=="mongolian "):
            dest_code='mn'
    if(lang==" myanmar (burmese) "):
            dest_code='my'
    if(lang==" nepali "):
            dest_code='ne'
    if(lang==" norwegian "):
            dest_code='no'
    if(lang==" pashto "):
            dest_code='ps'
    if(lang==" persian "):
            dest_code='fa'
    if(lang==" polish "):
            dest_code='pl'
    if(lang==" portuguese "):
            dest_code='pt'
    if(lang==" punjabi "):
            dest_code='pa'
    if(lang==" romanian "):
            dest_code='ro'
    if(lang==" russian "):
            dest_code='ru'
    if(lang==" samoan "):
            dest_code='sm'
    if(lang==" scots gaelic "):
            dest_code='gd'
    if(lang==" serbian "):
            dest_code='sr'
    if(lang==" sesotho "):
            dest_code='st'
    if(lang==" shona "):
            dest_code='sn'
    if(lang==" sindhi "):
            dest_code='sd'
    if(lang==" sinhala "):
            dest_code='si'
    if(lang==" slovak "):
            dest_code='sk'
    if(lang==" slovenian "):
            dest_code='sl'
    if(lang==" somali "):
            dest_code='so'
    if(lang==" spanish "):
            dest_code='es'
    if(lang==" sundanese "):
            dest_code='su'
    if(lang==" swahili "):
            dest_code='sw'
    if(lang==" swedish "):
            dest_code='sv'

    if(lang==" tajik"):
            dest_code='tg'

    if(lang==" tamil"):
            dest_code='ta'

    if(lang==" telugu"):
            dest_code='te'

    if(lang==" thai"):
            dest_code='th'

    if(lang==" turkish"):
            dest_code='tr'

    if(lang==" ukrainian"):
            dest_code='uk'

    if(lang==" urdu"):
            dest_code='ur'

    if(lang==" uzbek"):
            dest_code='uz'

    if(lang==" vietnamese"):
            dest_code='vi'

    if(lang==" welsh"):
            dest_code='cy'

    if(lang==" xhosa"):
            dest_code='xh'

    if(lang==" yiddish"):
            dest_code='yi'

    if(lang==" yoruba"):
            dest_code='yo'

    if(lang==" zulu"):
            dest_code='zu'

    if(lang==" Filipino"):
            dest_code='fi'

    if(lang==" Hebrew"):
            dest_code='he'

    text_to_translate = translator.translate(message, src= 'en', dest= dest_code)
    text = text_to_translate.text
    return render_template('translate_summary.html', prediction=text)




@app.route('/help')
def help():
    return render_template('help.html')





if __name__== '__main__':
    app.run(debug=True)
