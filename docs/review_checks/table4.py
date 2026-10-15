# Recomputes Table 4 from S1 and compares with tables/Table4_benchmark_classes.csv.
import pandas as pd
s1 = pd.read_csv("supplementary/S1_benchmark_catalogue.csv")
t4 = pd.read_csv("tables/Table4_benchmark_classes.csv").set_index("method_class")
gt = s1.ground_truth_strategy.fillna("").str.lower()
flags = {
    "cancer_specific": s1.cancer_specific.astype(str) == "True",
    "gt_simulation": gt.str.contains("simulation"),
    "gt_orthogonal": gt.str.contains("orthogonal assay"),
    "gt_genotype": gt.str.contains("genotype multiplexing"),
    "gt_mixture": gt.str.contains("cell-line mixture"),
    "gt_heldout": gt.str.contains("held-out"),
    "gt_expert": gt.str.contains("expert annotation"),
    "gt_unclear": gt.str.contains("unclear"),
    "robust_params": s1.assessed_robustness_to_parameters.astype(str) == "True",
    "calibration": s1.assessed_calibration_or_uncertainty.astype(str) == "True",
    "metric_validity": s1.assessed_metric_validity.astype(str) == "True",
}
calc = pd.DataFrame({k: v.groupby(s1.method_class).sum() for k, v in flags.items()})
calc.insert(0, "n", s1.groupby("method_class").size())
diff = calc - t4[calc.columns].reindex(calc.index)
print("column totals from S1:", calc.sum().to_dict())
bad = diff[(diff != 0).any(axis=1)]
print("cells that differ from Table 4:", "none" if bad.empty else "\n" + bad.loc[:, (bad != 0).any()].to_string())
