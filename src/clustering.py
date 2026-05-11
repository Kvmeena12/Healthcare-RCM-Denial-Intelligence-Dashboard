from sklearn.cluster import KMeans

def cluster_claims(df):

    features = df[[
        "pc_ClaimAmount"
    ]]

    kmeans = KMeans(
        n_clusters=3,
        random_state=42
    )

    df["cluster"] = kmeans.fit_predict(features)

    return df