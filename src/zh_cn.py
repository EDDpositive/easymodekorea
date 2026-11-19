"""Simplified Chinese (mainland visitors) derived from the Traditional text.
Imported by build.py after data and data_extra; edit zh-tw text, then rebuild."""
import copy
from t2s import t2s
import data, data_extra as x


def conv(o):
    if isinstance(o, str): return t2s(o)
    if isinstance(o, dict): return {k: conv(v) for k, v in o.items()}
    if isinstance(o, list): return [conv(v) for v in o]
    if isinstance(o, tuple): return tuple(conv(v) for v in o)
    return o


L = conv(copy.deepcopy(data.LANGS["zh-tw"]))
L.update({"html_lang": "zh-CN", "dir": "zh-cn/", "name": "简体中文"})
data.LANGS["zh-cn"] = L
data.CHECKED["zh-cn"] = data.CHECKED["zh-tw"]
for name in ("X", "SHORT", "UX", "PLAN", "QUESTION", "HELP", "FEEDBACK"):
    getattr(x, name)["zh-cn"] = conv(getattr(x, name)["zh-tw"])
for lst in x.PHRASES.values():
    for ko, m in lst: m["zh-cn"] = t2s(m["zh-tw"])
for ko, m in x.HELP_PHRASES: m["zh-cn"] = t2s(m["zh-tw"])
x.HELP["zh-cn"]["nums"][2][1] = "旅游咨询热线(中文24小时)。用国外SIM请拨 +82-2-1330"
for k in list(x.KEYWORDS): x.KEYWORDS[k] = x.KEYWORDS[k] + " " + t2s(x.KEYWORDS[k])

import deep  # noqa: E402
for _g in deep.DEEP.values():
    if "zh-tw" in _g: _g["zh-cn"] = conv(_g["zh-tw"])
deep.HEAD["zh-cn"] = conv(deep.HEAD["zh-tw"])
deep.PAGES["zh-cn"] = conv(deep.PAGES["zh-tw"])
deep.PAGES["zh-cn"]["hosts"] = "给房东(韩文)"
