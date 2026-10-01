import os
import re
import json
import urllib.parse
import urllib.request
import requests
from PIL import Image

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

def search_duckduckgo_images(query, max_results=5):
    """Searches DuckDuckGo image endpoint for comic art."""
    search_url = f"https://duckduckgo.com/i.js?l=us-en&o=json&q={urllib.parse.quote(query)}"
    try:
        # First get vqd token
        token_req = requests.get(f"https://duckduckgo.com/?q={urllib.parse.quote(query)}", headers=HEADERS, timeout=8)
        vqd_match = re.search(r'vqd=([0-9-]+)', token_req.text)
        if not vqd_match:
            vqd_match = re.search(r'vqd="([^"]+)"', token_req.text)
        if not vqd_match:
            return []
        vqd = vqd_match.group(1)

        res = requests.get(
            f"https://duckduckgo.com/i.js?l=us-en&o=json&q={urllib.parse.quote(query)}&vqd={vqd}&f=,,,",
            headers=HEADERS,
            timeout=8
        )
        data = res.json()
        results = []
        for r in data.get('results', []):
            img_url = r.get('image')
            if img_url:
                results.append(img_url)
                if len(results) >= max_results:
                    break
        return results
    except Exception as e:
        print(f"Error searching {query}: {e}")
        return []

def search_bing_html(query, max_results=5):
    """Fallback scraping Bing Images HTML."""
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2&first=1"
    try:
        res = requests.get(url, headers=HEADERS, timeout=8)
        # Find murl in m="{...&quot;murl&quot;:&quot;url&quot;...}"
        matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', res.text)
        if not matches:
            matches = re.findall(r'"murl":"(http[^"]+)"', res.text)
        return matches[:max_results]
    except Exception as e:
        print(f"Bing search error: {e}")
        return []

def download_and_validate_image(urls, out_path, min_dim=500):
    """Downloads candidate URLs, validates it's a valid image, and saves."""
    for url in urls:
        try:
            print(f"Trying {url[:70]}...")
            r = requests.get(url, headers=HEADERS, timeout=12)
            if r.status_code == 200 and len(r.content) > 30000:
                with open(out_path, 'wb') as f:
                    f.write(r.content)
                # validate image
                with Image.open(out_path) as im:
                    w, h = im.size
                    if min(w, h) >= 300:
                        # Convert to clean RGB JPEG
                        rgb = im.convert('RGB')
                        rgb.save(out_path, 'JPEG', quality=95)
                        print(f"SUCCESS: Saved {out_path} ({w}x{h})")
                        return True
                    else:
                        print(f"Image too small: {w}x{h}")
        except Exception as e:
            print(f"Failed to fetch {url[:50]}: {e}")
    return False

if __name__ == '__main__':
    targets = {
        'post_07_cap_hail_hydra.jpg': 'captain america steve rogers 1 hail hydra comic panel',
        'post_08_ghost_rider_hulk.jpg': 'ghost rider penance stare world war hulk comic panel johnny blaze',
        'post_09_red_death.jpg': 'batman red death comic panel cosmic batmobile speed force barry',
        'post_12_tower_of_babel.jpg': 'jla tower of babel comic panel batman contingency plan',
        'post_17_spiderman_lifting.jpg': 'amazing spider-man 33 if this be my destiny lifting panel comic',
        'post_18_watchmen_rorschach.jpg': 'watchmen 12 rorschach doctor manhattan do it comic panel',
        'post_19_magneto_wolverine.jpg': 'x-men 25 magneto pulls adamantium wolverine comic panel'
    }

    out_dir = r"C:\Users\Vanes\comics en espanol\assets\facebook_posts"
    os.makedirs(out_dir, exist_ok=True)

    for fn, query in targets.items():
        out_p = os.path.join(out_dir, fn)
        print(f"\n--- Searching for {fn} ({query}) ---")
        urls = search_duckduckgo_images(query, 5)
        if not urls:
            urls = search_bing_html(query, 5)
        print(f"Found {len(urls)} URLs")
        download_and_validate_image(urls, out_p)
