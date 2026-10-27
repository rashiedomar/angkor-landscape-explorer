"""Loopback-only static preview with restricted downloads from the curated share folder."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit
import mimetypes
import shutil
import html

ROOT=Path(__file__).resolve().parents[1]
SHARE=ROOT.parent/"SHARE_WITH_SCOTT"

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        route=unquote(urlsplit(self.path).path)
        if route.startswith("/downloads/"):
            relative=route[len("/downloads/"):]
            if not relative:
                entries=[p for p in sorted(SHARE.rglob("*")) if p.is_file() and not p.name.startswith(".") and not p.name.endswith("~")]
                listing="<!doctype html><meta charset='utf-8'><title>Research files</title><style>body{font:15px/1.6 Arial;max-width:1000px;margin:45px auto;padding:0 25px;color:#23352f}li{margin:8px 0}a{color:#315f72}</style><h1>Research progress files</h1><p>Current local SHARE_WITH_SCOTT folder. This is not the older ZIP snapshot.</p><ul>"+"".join("<li><a href='/downloads/"+html.escape(p.relative_to(SHARE).as_posix(),quote=True)+"'>"+html.escape(p.relative_to(SHARE).as_posix())+"</a></li>" for p in entries)+"</ul>"
                body=listing.encode("utf-8");self.send_response(200);self.send_header("Content-Type","text/html; charset=utf-8");self.send_header("Content-Length",str(len(body)));self.end_headers();self.wfile.write(body);return
            path=ROOT.parent/"SHARE_WITH_SCOTT.zip" if relative=="SHARE_WITH_SCOTT.zip" else (SHARE/relative).resolve()
            if relative!="SHARE_WITH_SCOTT.zip" and SHARE.resolve() not in path.parents:
                self.send_error(403);return
            if not path.is_file() or any(part.startswith(".") for part in Path(relative).parts):
                self.send_error(404);return
            self.send_response(200);self.send_header("Content-Type",mimetypes.guess_type(path.name)[0] or "application/octet-stream")
            self.send_header("Content-Length",str(path.stat().st_size));self.send_header("Content-Disposition",'attachment; filename="'+path.name+'"');self.end_headers()
            with path.open("rb") as stream:shutil.copyfileobj(stream,self.wfile)
            return
        if any(part.startswith(".") for part in Path(route).parts if part not in {"/"}):
            self.send_error(403);return
        super().do_GET()
    def log_message(self,format,*args):
        if args and str(args[1]) not in {"200","304"}:super().log_message(format,*args)

server=ThreadingHTTPServer(("127.0.0.1",8765),partial(Handler,directory=str(ROOT/"dist")))
print("Angkor explorer: http://127.0.0.1:8765",flush=True)
server.serve_forever()
