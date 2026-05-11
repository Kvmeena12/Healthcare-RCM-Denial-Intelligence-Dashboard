def merge_claims(df835, df837):

    merged = df835.merge(
        df837,
        left_on="pc_ClaimID",
        right_on="ec_ClaimNo",
        how="left"
    )

    return merged