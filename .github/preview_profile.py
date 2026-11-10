"""Build a local README preview. Optional dependency: pip install markdown."""

from pathlib import Path
import markdown

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "README.md").read_text(encoding="utf-8")
source = source.replace('srcset="./assets/', 'srcset="../assets/').replace('src="./assets/', 'src="../assets/')
source = source.replace("<details>", '<details markdown="1">')
content = markdown.markdown(source, extensions=["md_in_html"])
page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Prakash Palsaniya — GitHub profile preview</title>
<style>
  :root{color-scheme:light;--bg:#fff;--ink:#262a23;--line:#d8ddd0;--muted:#636b5a;--link:#47671e;--panel:#f6f7f2}
  @media(prefers-color-scheme:dark){:root{color-scheme:dark;--bg:#0d100c;--ink:#e5e9dd;--line:#31382b;--muted:#9da792;--link:#c3f467;--panel:#161a13}}
  :root[data-theme=light]{color-scheme:light;--bg:#fff;--ink:#262a23;--line:#d8ddd0;--muted:#636b5a;--link:#47671e;--panel:#f6f7f2}
  :root[data-theme=dark]{color-scheme:dark;--bg:#0d100c;--ink:#e5e9dd;--line:#31382b;--muted:#9da792;--link:#c3f467;--panel:#161a13}
  *{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}
  nav{max-width:896px;margin:28px auto 16px;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:0 12px;font:12px/1.5 monospace;color:var(--muted)}
  nav strong{color:var(--ink)}.switches{display:flex;gap:6px}button{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:5px;font:inherit;padding:7px 12px;cursor:pointer}button[aria-pressed=true]{border-color:var(--link);color:var(--link)}
  article{max-width:896px;margin:0 auto 56px;padding:24px;border:1px solid var(--line);border-radius:9px}
  article>p:first-of-type{margin-top:0}picture{display:block}img{display:block;height:auto;max-width:100%}a{color:var(--link);text-decoration:none}a:hover{text-decoration:underline}a:focus-visible,button:focus-visible,summary:focus-visible{outline:2px solid var(--link);outline-offset:5px}
  h2{font-size:23px;line-height:1.4;font-weight:600;letter-spacing:-.6px;margin:38px 0 18px;padding-bottom:12px;border-bottom:1px solid var(--line)}p{margin:16px 0}p[align=center]{padding:8px 0 14px;font-size:13px}details{font-size:14px;color:var(--muted)}summary{cursor:pointer;color:var(--ink)}details p{padding:0 16px}article>br{display:block;content:"";margin-bottom:14px}
  @media(max-width:600px){nav{margin-top:16px;font-size:10px;gap:6px}.switches button{padding:6px 9px}article{padding:16px 12px;border:0;margin-bottom:20px}body{font-size:14px}h2{font-size:21px}p[align=center]{font-size:11px;line-height:2}article>p{overflow-wrap:break-word}}
</style>
</head>
<body>
<nav><span><strong>PrakashPalsaniya</strong> / README.md</span><div class="switches"><button type="button" data-mode="light">Light</button><button type="button" data-mode="dark">Dark</button></div></nav>
<article>''' + content + '''</article>
<script>
const sources=[...document.querySelectorAll('source')].map(el=>({el,media:el.media}));
function choose(theme){
 document.documentElement.dataset.theme=theme;
 sources.forEach(({el,media})=>el.media=media.replace(/\\(prefers-color-scheme: (dark|light)\\)/g,(_,value)=>value===theme?'(min-width: 0px)':'(max-width: 0px)'));
 document.querySelectorAll('button[data-mode]').forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.mode===theme)));
}
document.querySelectorAll('button[data-mode]').forEach(el=>el.addEventListener('click',()=>choose(el.dataset.mode)));
document.querySelectorAll('button[data-mode]').forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.mode===(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'))));
</script>
</body></html>
'''
preview = ROOT / ".preview"
preview.mkdir(exist_ok=True)
(preview / "index.html").write_text(page, encoding="utf-8")
print(f'Preview: {preview / "index.html"}')
