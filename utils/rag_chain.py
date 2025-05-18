# File: utils/rag_chain.py

from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

def create_qa_chain(vectorstore, system_prompt: str = None):
    """
    Creates a RetrievalQA chain that uses your system_prompt as a prefix.
    """
    # 1) Chat model
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    # 2) Prompt şablonu oluştur
    if system_prompt:
        template = (
            system_prompt
            + "\n\n"
            + "Context:\n{context}\n\n"
            + "Question: {question}\n"
            + "Answer:"
        )
    else:
        template = "Context:\n{context}\n\nQuestion: {question}\nAnswer:"

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    # 3) RetrievalQA zincirini inşa et
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        return_source_documents=False,
        verbose=False,
        chain_type_kwargs={"prompt": prompt}
    )

    return chain
