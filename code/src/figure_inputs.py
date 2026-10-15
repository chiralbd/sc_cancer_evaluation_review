"""Load the figure-input snapshot written at the end of the analysis session.

Each object is the exact in-memory input that the figure code consumed when the
published figures were rendered (15 October 2026). The derivation of every object
is in provenance/ (main_session.py) and, for the statistical inputs, in
src/03_statistics.py.
"""
import json, os
import numpy as np, pandas as pd
from io import StringIO

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "..", "data", "figure_inputs")

def _fromj(o):
    if isinstance(o, dict):
        if "__df__" in o:
            d = pd.read_json(StringIO(json.dumps(o["__df__"])), orient="split")
            d.index.name = o.get("index_name"); return d
        if "__series__" in o:
            s = pd.read_json(StringIO(json.dumps(o["__series__"])), orient="split", typ="series")
            s.index.name = o.get("index_name"); return s
        if "__nd__" in o: return np.array(o["__nd__"], dtype=o["dtype"])
        if "__tuple__" in o: return tuple(_fromj(v) for v in o["__tuple__"])
        if "__dict__" in o: return {_key(_fromj(k)): _fromj(v) for k, v in o["__dict__"]}
        if "__range__" in o: return range(*o["__range__"])
        if "__csv__" in o: return pd.read_csv(os.path.join(SNAP, o["__csv__"]))
    if isinstance(o, list): return [_fromj(v) for v in o]
    return o

def _key(k): return tuple(k) if isinstance(k, list) else k

def load_figure_inputs():
    with open(os.path.join(SNAP, "figure_inputs.json")) as f:
        raw = json.load(f)
    return {k: _fromj(v) for k, v in raw.items()}
