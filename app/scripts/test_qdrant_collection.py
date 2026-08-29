from app.services.qdrant_service import (
    create_collection,
    get_collection_info
)


create_collection(768)

info = get_collection_info()

print("Qdrant collection info:")
print(info)