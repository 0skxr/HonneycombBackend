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

class Comb:
    def __init__(self):
        colorinit()
        self.directory = "Documents"
        self.persist_directory = "chroma_db"
        self.initialize_components()
    
    def initialize_components(self):
        print("Starting Embeddings")
        self.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        print("Finished Embeddings")
        
        self.db = chromaDb.get_db(self.persist_directory, self.embeddings, self.directory)
        self.llm = ChatOllama(model="starling-lm")
        
        self.prompt = PromptTemplate(
            input_variables=["chat_history", "human_input", "context"], template=template.template
        )
        
        self.memory = ConversationBufferMemory(memory_key="chat_history", input_key="human_input")
        self.chain = load_qa_chain(
            self.llm, chain_type="stuff", memory=self.memory, prompt=self.prompt
        )
    
    def run(self,query):
        matching_docs = self.db.similarity_search(query)
        self.chain({"input_documents": matching_docs, "human_input": query}, return_only_outputs=True)
        

        chat_dict  = self.chain.memory.dict()


        messages = chat_dict['chat_memory']['messages']

        newest_ai_message = None
        for message in reversed(messages):
            if message['type'] == 'ai':
                newest_ai_message = message['content']
                break

        return newest_ai_message.replace("<|end_of_turn|>","")

if __name__ == "__main__":
    comb_instance = Comb()
    comb_instance.run("Hi")
    print(comb_instance.run("tell me about the spi pins"))