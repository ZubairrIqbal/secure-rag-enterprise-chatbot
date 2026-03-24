from app.access_control import get_allowed_departments


def retrieve_documents(vectorstore, query, role, k=3):
    allowed_departments = get_allowed_departments(role)

    results = vectorstore.similarity_search(
        query,
        k=k,
        filter={"department": {"$in": allowed_departments}}
    )

    return results