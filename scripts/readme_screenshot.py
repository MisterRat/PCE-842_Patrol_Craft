"""Takes the README screenshot of the game during the GitHub Pages build (headless Chromium, software WebGL).
Writes screenshots/chase_underway.jpg into the published site; the README shows it from there."""
import functools, http.server, os, threading
from playwright.sync_api import sync_playwright

srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8765), functools.partial(http.server.SimpleHTTPRequestHandler, directory="."))
threading.Thread(target=srv.serve_forever, daemon=True).start()
os.makedirs("screenshots", exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    pg.goto("http://127.0.0.1:8765/index.html")
    pg.wait_for_timeout(8000)
    pg.evaluate("()=>{$$('go').click()}")
    pg.wait_for_timeout(800)
    pg.keyboard.press("KeyH")
    pg.evaluate("()=>{SHIP.tel=0.8;ENG.ans=0.8;SHIP.u=SHIP.VMAX*0.8;orbitOn=true;orbYaw=2.3;orbEl=0.18;orbDist=70}")
    pg.wait_for_timeout(6000)
    pg.screenshot(path="screenshots/chase_underway.jpg", type="jpeg", quality=85, clip={"x": 200, "y": 170, "width": 880, "height": 430})
    b.close()
srv.shutdown()
print("screenshot written")
