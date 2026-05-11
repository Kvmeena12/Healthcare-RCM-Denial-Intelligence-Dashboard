from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def build_similarity(df):

    df["combined_text"] = (
        df["ec_PayerName"].astype(str)
        + " "
        + df["pcl_ProcedureCode"].astype(str)
        + " "
        + df["ec_PrincipalDiagnosis"].astype(str)
    )

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        df["combined_text"]
    )

    similarity_matrix = cosine_similarity(vectors)

    return similarity_matrix