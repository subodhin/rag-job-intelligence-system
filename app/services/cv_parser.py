from langchain_community.document_loaders import PyPDFLoader


def parse_cv(file_path: str):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # for doc in documents:
    #     print("PAGE:::::::::::::::::::::::::", doc.metadata.get("page"))
    #     print(doc.page_content[:500])
    #     print("-" * 50)

    for doc in documents:
      print("PAGE:::::::::::::::::::::::::", doc.metadata.get("page"))
      print("CHARACTERS:", len(doc.page_content))
      print(doc.page_content)
      print("-" * 80)

      return documents