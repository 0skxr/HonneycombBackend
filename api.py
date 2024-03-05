from flask import Flask, request
from flask_cors import CORS, cross_origin
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.chains import ConversationChain
from colorama import Fore, Style
from colorama import init as colorinit
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import OllamaEmbeddings
import chromaDb
from langchain.chains.question_answering import load_qa_chain
import template
import Comb
import pickle


comb1 = Comb.Comb()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/invoke')
def hello_name():
    promt = request.args.get('promt')  
    text = comb1.run(promt)
    returnDict = {"content": text}
    return returnDict

if __name__ == '__main__':
    app.run(debug=True)
