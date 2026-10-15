# Recomputes series and study-group counts per modality in Table 5 from S3.
import pandas as pd
s3 = pd.read_csv("supplementary/S3_ground_truth_catalogue.csv")
long = s3.assign(m=s3.validation_modalities.str.split(";")).explode("m")
calc = long.groupby("m").agg(series=("gse", "nunique"), study_groups=("study_group", "nunique"),
                             median_samples=("n_samples", "median"))
print("total series:", s3.gse.nunique(), " study groups:", s3.study_group.nunique())
print(calc.sort_values("series", ascending=False))
print(pd.read_csv("tables/Table5_ground_truth.csv")[["modality", "series", "study_groups", "median_samples"]])
