"""Matplotlib settings used for all manuscript figures (8/7/6 pt type ladder,
open frame, outward ticks, 300 dpi, embedded TrueType fonts) and two helpers."""
import matplotlib as mpl
from matplotlib.ticker import NullFormatter, NullLocator

METH, BIO, GREY = "#1f6f8b", "#c9852b", "#8a8a8a"   # method topics, biology topics, neutral


def apply_style(base=8, secondary=7, tick=6):
    mpl.rcParams.update({
        "font.family": "sans-serif", "font.size": base, "axes.labelsize": base, "axes.titlesize": base,
        "legend.fontsize": secondary, "xtick.labelsize": tick, "ytick.labelsize": tick,
        "axes.linewidth": 0.6, "xtick.direction": "out", "ytick.direction": "out",
        "xtick.major.size": 3, "ytick.major.size": 3, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "axes.spines.top": False, "axes.spines.right": False, "axes.grid": False, "legend.frameon": False,
        "figure.dpi": 200, "savefig.dpi": 300, "savefig.bbox": "tight", "axes.titlelocation": "left",
        "lines.linewidth": 1.2, "patch.linewidth": 0.6, "pdf.fonttype": 42, "ps.fonttype": 42,
    })


def panel_letter(ax, letter, dx=-0.18, dy=1.02, fontsize=None):
    """Bold lower-case panel letter outside the top-left corner of an axes."""
    fs = fontsize or mpl.rcParams["font.size"] + 1
    ax.text(dx, dy, letter.lower(), transform=ax.transAxes, fontweight="bold", fontsize=fs, va="bottom", ha="left")


def nominor(ax, which="x"):
    a = ax.xaxis if which == "x" else ax.yaxis
    a.set_minor_formatter(NullFormatter()); a.set_minor_locator(NullLocator())


def check(fig):
    """Return pairs of overlapping visible text objects (layout sanity check)."""
    r = fig.canvas.get_renderer()
    T = [(t, t.get_window_extent(r)) for t in fig.findobj(mpl.text.Text) if t.get_text().strip() and t.get_visible()]
    return [(a.get_text()[:25], b.get_text()[:25]) for i, (a, ba) in enumerate(T) for b, bb in T[i + 1:] if ba.overlaps(bb)]
