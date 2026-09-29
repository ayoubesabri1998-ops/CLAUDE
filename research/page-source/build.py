"""Build the report page (HTML) and the repo copy (Markdown) from one source.

Inputs (next to this file):
  content.md  narrative in Markdown; headings may carry {#id data-nav="Label"};
              a paragraph containing only @@CATALOG@@ marks where the catalog goes
  data.json   {"meta": {...}, "categories": [...], "tools": [...]}
  style.css, app.js, template.html
Outputs:
  edit-toolkit.html   page to publish
  report.md           GitHub-friendly Markdown copy
"""
import html
import json
import pathlib
import re

import markdown

ROOT = pathlib.Path(__file__).parent
LIC = {"ok": "Commercial use OK", "nc": "Non-commercial only", "check": "Check license", "paid": "Paid"}


def load():
    content = (ROOT / "content.md").read_text(encoding="utf-8")
    data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    order = [c["key"] for c in data["categories"]]
    tools = []
    for f in sorted((ROOT / "tools").glob("*.json")):
        tools.extend(json.loads(f.read_text(encoding="utf-8")))
    unknown = {t["c"] for t in tools} - set(order)
    if unknown:
        raise SystemExit(f"unknown categories: {unknown}")
    tools.sort(key=lambda t: order.index(t["c"]))
    data["tools"] = tools
    return content, data


def catalog_html():
    return """<div class="catalog" id="catalog-app">
  <div class="filters">
    <label class="search" for="q"><span class="sr">Search the catalog</span><input id="q" type="search" placeholder="Search: depth, Fusion, Blender, whoosh, rotoscope…" autocomplete="off"></label>
    <div class="chips" id="cat-chips" role="group" aria-label="Filter by category"></div>
    <div class="toggles">
      <label for="f-commercial"><input type="checkbox" id="f-commercial"> Commercial use OK</label>
      <label for="f-gui"><input type="checkbox" id="f-gui"> No coding needed</label>
      <label for="f-nogpu"><input type="checkbox" id="f-nogpu"> Works without an NVIDIA GPU</label>
    </div>
  </div>
  <p class="count" id="count" aria-live="polite"></p>
  <div class="grid" id="grid"></div>
  <noscript><p>The catalog needs JavaScript. The same list is in the Markdown copy of this report.</p></noscript>
</div>"""


def md_cell(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")


def catalog_md(data):
    out = []
    for cat in data["categories"]:
        rows = [t for t in data["tools"] if t["c"] == cat["key"]]
        if not rows:
            continue
        out.append(f"### {cat['label']}\n")
        if cat.get("blurb"):
            out.append(cat["blurb"] + "\n")
        out.append("| Tool | What it does | Use it for | Interface | Hardware | License | Stars · updated |")
        out.append("|---|---|---|---|---|---|---|")
        for t in rows:
            lic = LIC[t["lk"]] + (f" ({t['l']})" if t.get("l") else "")
            su = " · ".join(x for x in [("★ " + t["s"]) if t.get("s") else "", t.get("d", "")] if x)
            name = md_cell(t["n"]) + (" (unverified)" if t.get("v") is False else "")
            out.append(
                f"| [{name}]({t['u']}) | {md_cell(t['w'])} | {md_cell(t.get('f'))} | "
                f"{md_cell(t.get('i'))} | {md_cell(t.get('h'))} | {md_cell(lic)} | {md_cell(su)} |"
            )
        out.append("")
    return "\n".join(out)


def build_html(content, data):
    md = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list", "toc", "sane_lists"])
    body = md.convert(content)
    body = body.replace("<table>", '<div class="table-scroll"><table>').replace("</table>", "</table></div>")
    body = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', body)
    body = body.replace("<p>@@CATALOG@@</p>", catalog_html())

    nav = []
    for m in re.finditer(r"<h2([^>]*)>(.*?)</h2>", body):
        attrs = m.group(1)
        hid = re.search(r'id="([^"]+)"', attrs)
        label = re.search(r'data-nav="([^"]+)"', attrs)
        if hid:
            text = label.group(1) if label else re.sub(r"<[^>]+>", "", m.group(2))
            nav.append(f'<li><a href="#{hid.group(1)}">{text}</a></li>')

    meta = data["meta"]
    n_tools = len(data["tools"])
    n_cats = len({t["c"] for t in data["tools"]})
    facts = [
        f"<li><strong>{meta['tracks']}</strong> research tracks</li>",
        f"<li><strong>{n_tools}</strong> tools in the catalog</li>",
        f"<li><strong>{n_cats}</strong> categories</li>",
        "<li>Licenses checked for monetized channels</li>",
    ]
    payload = json.dumps({"categories": data["categories"], "tools": data["tools"]}, ensure_ascii=False)
    payload = payload.replace("</", "<\\/")

    page = (ROOT / "template.html").read_text(encoding="utf-8")
    repl = {
        "%%CSS%%": (ROOT / "style.css").read_text(encoding="utf-8"),
        "%%JS%%": (ROOT / "app.js").read_text(encoding="utf-8"),
        "%%DESCRIPTION%%": html.escape(meta["description"]),
        "%%DATE%%": html.escape(meta["date"]),
        "%%LEDE%%": meta["lede_html"],
        "%%FACTS%%": "".join(facts),
        "%%NAV%%": "".join(nav),
        "%%CONTENT%%": body,
        "%%FOOTER%%": meta["footer_html"],
        "%%DATA%%": payload,
    }
    for k, v in repl.items():
        page = page.replace(k, v)
    (ROOT / "edit-toolkit.html").write_text(page, encoding="utf-8")
    return page


def build_md(content, data):
    meta = data["meta"]
    text = re.sub(r"[ \t]*\{#[^}]*\}[ \t]*$", "", content, flags=re.M)
    text = text.replace("@@CATALOG@@", catalog_md(data))
    lede = re.sub(r"<[^>]+>", "", meta["lede_html"])
    head = f"# 2D→3D Edit Toolkit\n\n_{meta['date']} · deep research on GitHub and the web_\n\n{lede}\n\n"
    foot = "\n---\n\n" + re.sub(r"<[^>]+>", "", meta["footer_html"]).strip() + "\n"
    (ROOT / "report.md").write_text(head + text.strip() + "\n" + foot, encoding="utf-8")


if __name__ == "__main__":
    c, d = load()
    page = build_html(c, d)
    build_md(c, d)
    print(f"html {len(page):,} bytes, tools {len(d['tools'])}")
