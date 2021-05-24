import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *
import tkinter.filedialog
import nltk
import gensim
from gensim.summarization import summarize
import  time

timestr=time.strftime("%Y%m%d-%H%M%S")
import tkinter as GUI
from googletrans import Translator, LANGUAGES

#Import diff methods of summarisation
from spacy_summarization import text_summarizer
from spacy_summarization import size_summ
from spacy_summarization import size_inn
from gensim.summarization import summarize
from nltk_summarization import nltk_summarizer


#WebScraping pckg
from bs4 import BeautifulSoup
from urllib.request import urlopen

#Sumy Package
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

#sumy

def sumy_summary(docx):
    parser=PlaintextParser.from_string(docx,Tokenizer("english"))
    lex_summarizer=LexRankSummarizer()
    summary =lex_summarizer(parser.document,3)
    summary_list = [str(sentence) for sentence in summary]
    result=''.join(summary_list)
    return result

#Main window
root=tk.Tk()
root.title(" Automatic Text Summarizer")
root.config(bg='#e8f6fa')
root.geometry('700x600')

#Style
style= ttk.Style(root)
style.configure('lefttab.TNotebook',tabposition='wn')

#Creating Tabs
tab_control=ttk.Notebook(root,style='lefttab.TNotebook')

tab6=ttk.Frame(tab_control,)
tab1=ttk.Frame(tab_control)
tab2=ttk.Frame(tab_control)
tab3=ttk.Frame(tab_control)
tab4=ttk.Frame(tab_control)
tab5=ttk.Frame(tab_control)

#Adding Tabs to window
tab_control.add(tab6,text=f'{"Home":^20s}')
tab_control.add(tab1,text=f'{"Text":^20s}')
tab_control.add(tab2,text=f'{"URL":^20s}')
tab_control.add(tab3,text=f'{"File":^20s}')
tab_control.add(tab4,text=f'{"Algorithms":^20s}')
tab_control.add(tab5,text=f'{"Translator":^20s}')


#Labels
label1=Label(tab6,text='\tWelcome to \n\n\n  \tAutomatic Text Summarizer !',font = "cheque 20 bold",padx=5,pady=5)
label1.grid(column=0,row=0)

label9=Label(tab6,text='\n\n\nSummarization is the task of condensing\n a piece of text to a shorter version,\n reducing the size of the initial text while at the same time preserving key informational elements and the meaning of content.',font = "cheque 10 bold",padx=5,pady=5)
label9.grid(column=0,row=3)


label1=Label(tab1,text='Summarizer',font=12,bg="#e8f6fa",padx=5,pady=5)
label1.grid(column=0,row=0)

label2=Label(tab2,text='URL',bg="#e8f6fa",padx=5,pady=5)
label2.grid(column=0,row=0)

label3=Label(tab3,text='File Processing',bg="#e8f6fa",padx=5,pady=5)
label3.grid(column=0,row=0)

label4=Label(tab4,text='Compare different methods to summarize',bg="#e8f6fa",padx=5,pady=5)
label4.grid(column=0,row=0)

label5=Label(tab5,text='Translator',bg="#e8f6fa",padx=5,pady=5)
label5.grid(column=0,row=0)


tab_control.pack(expand=1,fill='both')


#functions for Home
def get_summary():
    raw_text =str(entry.get('1.0',tk.END))
    final_text =text_summarizer(raw_text)
    fi=size_summ(final_text)
    inn=size_inn(raw_text)

    print(inn)
    print(fi)
    print(final_text)

    result = '\nSummary:{}'.format(final_text)

    tab1_display.insert(tk.END,result)
    tab1_display2.insert(tk.END,fi)
    tab1_display1.insert(tk.END,inn)



def clear_text():
    entry.delete('1.0',END)
    tab1_display1.delete('1.0',END)

def clear_display_result():
    tab1_display.delete('1.0',END)
    tab1_display2.delete('1.0',END)


def save_summary():
    raw_text=str(entry.get('1.0',tk.END))
    final_text = text_summarizer(raw_text)
    file_name='youursummary'+timestr+'.txt'
    with open(file_name,'w') as f:
        f.write(final_text)
    result='\nName of File: {},\n Summary: {} '.format(file_name,final_text)
    tab1_display.insert(tk.END,result)





#Home Tab
l1= Label(tab1,text='Enter text to summarize',font="Helvetica 15",padx=5,pady=5)
l1.grid(column=0,row=1)
entry= ScrolledText(tab1,height=10)
entry.grid(row=2,column=0,columnspan=2,padx=5,pady=5)
l9=Label(tab1,text='Length of input',font="Helvetica 10",padx=5,pady=5)
l9.grid(column=0,row=4)
l8=Label(tab1,text='Length of summary',font="Helvetica 10",padx=5,pady=5)
l8.grid(column=0,row=8)




#Buttons
button1=Button(tab1,text='Reset Input',command=clear_text,width=12,font="arial 8 bold",bg="#9AD7F5")#add bg and fg colors
button1.grid(row=1,column=1,padx=10,pady=5)

button2=Button(tab1,text='Summarize',command=get_summary,font="arial 8 bold",width=12,bg="#9AD7F5")#add bg and fg colors
button2.grid(row=4,column=1,padx=10,pady=5)

button3=Button(tab1,text='Clear Text',command=clear_display_result,font="arial 8 bold",width=12,bg="#9AD7F5")#add bg and fg colors
button3.grid(row=8,column=1,padx=10,pady=5)

button4=Button(tab1,text='Save',command=save_summary,font="arial 8 bold",width=12,bg="#9AD7F5")#add bg and fg colors
button4.grid(row=5,column=1,padx=10,pady=5)

#Display for result
tab1_display = ScrolledText(tab1,height=10)
tab1_display.grid(row=7,column=0, columnspan=3,padx=5,pady=5)

tab1_display1 = Text(tab1,height=1,width=10)
tab1_display1.grid(row=5,column=0,padx=5,pady=5)

tab1_display2 = Text(tab1,height=1,width=10)
tab1_display2.grid(row=9,column=0,padx=5,pady=5)




#URL Tab
l1=Label(tab2,text="Enter URL To Summarize",font="Helvetica 15")
l1.grid(row=1,column=0)

l10=Label(tab2,text='Length of input',font="Helvetica 12",padx=5,pady=5)
l10.grid(column=0,row=2)
l11=Label(tab2,text='Length of summary',font="Helvetica 12",padx=5,pady=5)
l11.grid(column=0,row=11)

raw_entry=StringVar()
url_entry=Entry(tab2,textvariable=raw_entry,width=50)
url_entry.grid(row=1,column=1)


# Display Screen For Result
url_display = ScrolledText(tab2,height=10)
url_display.grid(row=7,column=0, columnspan=3,padx=5,pady=5)

tab2_display_text = ScrolledText(tab2,height=10)
tab2_display_text.grid(row=10,column=0, columnspan=3,padx=5,pady=5)

tab2_len1 = Text(tab2,height=1,width=10)
tab2_len1.grid(row=2,column=1,padx=5,pady=5)

tab2_len2 = Text(tab2,height=1,width=10)
tab2_len2.grid(row=11,column=1,padx=5,pady=5)
#Funcations for URL

def clear_url_entry():
    url_entry.delete(0,END)
    tab2_len1.delete('1.0',END)

def clear_url_display():
    tab2_display_text.delete('1.0',END)
    tab2_len2.delete('1.0',END)

def get_text():
	raw_text = str(url_entry.get())
	page = urlopen(raw_text)
	soup = BeautifulSoup(page,'lxml')
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	url_display.insert(tk.END,fetched_text)

def get_url_summary():
    raw_text =url_display.get('1.0',tk.END)
    final_text =text_summarizer(raw_text)
    fi=size_summ(final_text)
    inn=size_inn(raw_text)

    print(inn)
    print(fi)
    print(final_text)

    result = '\nSummary:{}'.format(final_text)

    tab2_display_text.insert(tk.END,result)
    tab2_len2.insert(tk.END,fi)
    tab2_len1.insert(tk.END,inn)






# BUTTONS
button1=Button(tab2,text="Reset Input",command=clear_url_entry,font="arial 10 bold",bg="#9AD7F5")#,bg='#03A9F4',fg='#fff')
button1.grid(row=1,column=2,padx=10,pady=10)

button2=Button(tab2,text="Get Text",command=get_text,font="arial 10 bold", bg="#9AD7F5")#,bg='#03A9F4',fg='#fff')
button2.grid(row=2,column=2,padx=10,pady=10)

button3=Button(tab2,text="Clear Result", command=clear_url_display,font="arial 10 bold",bg="#9AD7F5")#,bg='#03A9F4',fg='#fff')
button3.grid(row=5,column=0,padx=10,pady=10)

button4=Button(tab2,text="Summarize",command=get_url_summary,font="arial 10 bold",bg="#9AD7F5")#,bg='#03A9F4',fg='#fff')
button4.grid(row=5,column=1,padx=10,pady=10)














#File Processing Tab
l1=Label(tab3,text="Open File To Summarize",font="Helvetica 15")
l1.grid(row=1,column=1)

displayed_file = ScrolledText(tab3,height=7)# Initial was Text(tab2)
displayed_file.grid(row=2,column=0, columnspan=3,padx=5,pady=3)


l12=Label(tab3,text='Length of input',font="Helvetica 10",padx=5,pady=5)
l12.grid(column=0,row=8)
l13=Label(tab3,text='Length of summary',font="Helvetica 10",padx=5,pady=5)
l13.grid(column=0,row=9)


tab3_len1 = Text(tab3,height=1,width=10)
tab3_len1.grid(row=8,column=1,padx=5,pady=5)

tab3_len2 = Text(tab3,height=1,width=10)
tab3_len2.grid(row=9,column=1,padx=5,pady=5)


#functions
def openfiles():
	file1 = tkinter.filedialog.askopenfilename(filetypes=(("Text Files",".txt"),("All files","*")))
	read_text = open(file1).read()
	displayed_file.insert(tk.END,read_text)

def clear_text_file():
    displayed_file.delete('1.0',END)
    tab3_len1.delete('1.0',END)

# Clear Result of Functions
def clear_text_result():
    tab3_display_text.delete('1.0',END)
    tab3_len2.delete('1.0',END)

def get_file_summary():
    raw_text =displayed_file.get('1.0',tk.END)
    final_text =text_summarizer(raw_text)
    fi=size_summ(final_text)
    inn=size_inn(raw_text)

    print(inn)
    print(fi)
    print(final_text)

    result = '\nSummary:{}'.format(final_text)

    tab3_display_text.insert(tk.END,result)
    tab3_len2.insert(tk.END,fi)
    tab3_len1.insert(tk.END,inn)



# Buttons
b0=Button(tab3,text="Open File", width=12,command=openfiles,font="arial 12 bold",bg="#9AD7F5")#,bg='#c5cae9')
b0.grid(row=3,column=0,padx=10,pady=10)

b1=Button(tab3,text="Reset Input ", width=12,command=clear_text_file,font="arial 12 bold",bg="#9AD7F5")#,bg="#b9f6ca")
b1.grid(row=3,column=1,padx=10,pady=10)

b2=Button(tab3,text="Summarize", width=12,command=get_file_summary,font="arial 12 bold",bg="#9AD7F5")#,bg='blue',fg='#fff')
b2.grid(row=3,column=2,padx=10,pady=10)

b3=Button(tab3,text="Clear Result", width=12,command=clear_text_result,font="arial 12 bold",bg="#9AD7F5")
b3.grid(row=5,column=1,padx=10,pady=10)

b4=Button(tab3,text="Close", width=12,command=root.destroy,font="arial 12 bold",bg="#9AD7F5")
b4.grid(row=5,column=2,padx=10,pady=10)

# Display Screen
# tab2_display_text = Text(tab2)
tab3_display_text = ScrolledText(tab3,height=10)
tab3_display_text.grid(row=7,column=0, columnspan=3,padx=5,pady=5)
tab3_display_text.config(state=NORMAL)




#Compare Tab
l1=Label(tab4,text="Enter Text To Summarize",font="Helvetica 15")
l1.grid(row=1,column=0)

entry1=ScrolledText(tab4,height=10)
entry1.grid(row=2,column=0,columnspan=3,padx=5,pady=3)

l13=Label(tab4,text='Length of input',font="Helvetica 10",padx=5,pady=5)
l13.grid(column=0,row=8)
l14=Label(tab4,text='Length of summary',font="Helvetica 10",padx=5,pady=5)
l14.grid(column=0,row=9)

tab4_len1 = Text(tab4,height=1,width=10)
tab4_len1.grid(row=8,column=1,padx=5,pady=5)

tab4_len2 = Text(tab4,height=1,width=10)
tab4_len2.grid(row=9,column=1,padx=5,pady=5)




#functions
def use_spacy():
    raw_text =entry1.get('1.0',tk.END)
    final_text =text_summarizer(raw_text)
    fi=size_summ(final_text)
    inn=size_inn(raw_text)

    print(inn)
    print(fi)
    print(final_text)

    result = '\n Spacy Summary:{}'.format(final_text)

    tab4_display.insert(tk.END,result)
    tab4_len2.insert(tk.END,fi)
    tab4_len1.insert(tk.END,inn)






def use_nltk():
    raw_text =entry1.get('1.0',tk.END)
    final_text =nltk_summarizer(raw_text)
    fi=size_summ(final_text)
    inn=size_inn(raw_text)

    print(inn)
    print(fi)
    print(final_text)

    result = '\n Nltk Summary:{}'.format(final_text)

    tab4_display.insert(tk.END,result)
    tab4_len2.insert(tk.END,fi)
    tab4_len1.insert(tk.END,inn)

def use_gensim():
    raw_text =entry1.get('1.0',tk.END)
    final_text =summarize(raw_text)
    fi=len(final_text)
    inn=len(raw_text)

    print(inn)
    print(fi)
    print(final_text)

    result = '\n TextRank Summary:{}'.format(final_text)

    tab4_display.insert(tk.END,result)
    tab4_len2.insert(tk.END,fi)
    tab4_len1.insert(tk.END,inn)


def use_sumy():
    raw_text =entry1.get('1.0',tk.END)
    final_text =sumy_summary(raw_text)
    fi=size_summ(final_text)
    inn=size_inn(raw_text)

    print(inn)
    print(fi)
    print(final_text)

    result = '\n LexRank Summary:{}'.format(final_text)

    tab4_display.insert(tk.END,result)
    tab4_len2.insert(tk.END,fi)
    tab4_len1.insert(tk.END,inn)

def clear_compare_text():
    entry1.delete('1.0',END)
    tab4_len1.delete('1.0',END)


def clear_compare_display_result():
    tab4_display.delete('1.0',END)
    tab4_len2.delete('1.0',END)


# BUTTONS
button1=Button(tab4,text="Reset Input",command=clear_compare_text,font="arial 12 bold", width=12,bg="#9AD7F5")#,bg='#03A9F4',fg='#fff')
button1.grid(row=4,column=0,padx=10,pady=10)

button2=Button(tab4,text="SpaCy",command=use_spacy,font="arial 12 bold", width=12,bg="#9AD7F5")#,bg='red',fg='#fff')
button2.grid(row=4,column=1,padx=10,pady=10)

button3=Button(tab4,text="Clear Result", command=clear_compare_display_result,font="arial 12 bold",width=12,bg="#9AD7F5")#,bg='#03A9F4',fg='#fff')
button3.grid(row=5,column=0,padx=5,pady=5)

button4=Button(tab4,text="NLTK",command=use_nltk,font="arial 12 bold", width=12,bg="#9AD7F5")#,bg='#03A9F4',fg='#fff')
button4.grid(row=4,column=2,padx=5,pady=5)

button4=Button(tab4,text="TextRank",command=use_gensim,font="arial 12 bold", width=12,bg="#9AD7F5")#,bg='#03A9F4',fg='#fff')
button4.grid(row=5,column=1,padx=5,pady=5)

button4=Button(tab4,text="LexRank",command=use_sumy,font="arial 12 bold", width=12,bg="#9AD7F5")#,bg='#03A9F4',fg='#fff')
button4.grid(row=5,column=2,padx=10,pady=10)


# variable = StringVar()
# variable.set("SpaCy")
# choice_button = OptionMenu(tab4,variable,"SpaCy","Gensim","NLTK")
# choice_button.grid(row=6,column=1)


# Display Screen For Result
tab4_display = ScrolledText(tab4,height=15)
tab4_display.grid(row=7,column=0, columnspan=3,padx=5,pady=5)




#Translator Tab
l1= Label(tab5,text='Enter Text to translate',font="Helvetica 15",padx=5,pady=5)
l1.grid(column=1,row=1)

entry2= ScrolledText(tab5,height=10)
entry2.grid(row=2,column=0,columnspan=2,padx=5,pady=5)


def clear_display_result():
	tab5_display.delete('1.0',END)

def clear_text():
	entry2.delete('1.0',END)

def translate_text():
    translator = Translator()
    translated=translator.translate(text=entry2.get(1.0, END) , src = src_lang.get(), dest = dest_lang.get())
    # tab1_display.delete(1.0, END)
    tab5_display.insert(END, translated.text)


language = list(LANGUAGES.values())
src_lang = ttk.Combobox(tab5, values= language, width =22)
src_lang.place(x=20,y=40)
src_lang.set('choose input language')

dest_lang = ttk.Combobox(tab5, values= language, width =22)
dest_lang.place(x=20,y=300)
dest_lang.set('choose output language')






#buttons
button3=Button(tab5,text='Clear Result',command=clear_display_result,font="arial 12 bold",width=12,bg="#9AD7F5")#add bg and fg colors
button3.grid(row=4,column=0,padx=10,pady=10)

button1=Button(tab5,text='Reset Input',command=clear_text,font="arial 12 bold",width=12,bg="#9AD7F5")#add bg and fg colors
button1.grid(row=5,column=1,padx=10,pady=10)

button1=Button(tab5,text='Translate',command=translate_text,font="arial 12 bold",width=12,bg="#9AD7F5")#add bg and fg colors
button1.grid(row=4,column=1,padx=10,pady=10)


tab5_display = ScrolledText(tab5,height=10)
tab5_display.grid(row=7,column=0, columnspan=3,padx=5,pady=5)
# root.mainloop()





root.mainloop()
