import os
from typing import List, Any
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader

def load_documents(directory: str) -> List[Any]:
    """
    Load documents from a specified directory.

    :param directory: The path to the directory containing documents.
    :return: A list of loaded documents.
    """
    loader = DirectoryLoader(directory)
    documents = loader.load()
    return documents

def split_docs(documents: List[str], chunk_size: int = 1000, chunk_overlap: int = 20) -> List[str]:
    """
    Split documents into chunks based on specified size and overlap.

    :param documents: A list of documents to be split.
    :param chunk_size: The size of each chunk.
    :param chunk_overlap: The overlap size between chunks.
    :return: A list of document chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(documents)
    return docs

def get_db(data_dir: str, embedding: Any, doc_dir: str) -> Chroma:
    """
    Get or create a Chroma database based on the existence of a specified directory.

    :param data_dir: The directory to persist the Chroma database.
    :param embedding: The embedding function to use.
    :param doc_dir: The directory containing documents to load and process.
    :return: An instance of the Chroma database.
    """
    if os.path.isdir(data_dir):
        db = Chroma(persist_directory=data_dir, embedding_function=embedding)
    else:
        documents = load_documents(doc_dir)
        docs = split_docs(documents)
        print(len(docs), "documents have been split.")
        print("Started generating docs.")
        db = Chroma.from_documents(docs, embedding, persist_directory=data_dir)
        print("Finished generating docs.")
        db.persist()
    return db
