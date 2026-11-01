import sys
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

urls = [
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFpZl2c_2-g-L-67CWvZtWxJbUNh24Zs0rDjlXxEKpjZuoLHFlM4iNt6P-kZCkTn3U1zirvUg-YxS16IJQfilyc2USCplmMTcyLBS9LVQb_9pju1S56ztHT1wvfJ0fi1xdywZF7qRBV6pN8IrXIuiutXfGU1YmFWx8sEFs9pGlHRHTsBARCjuBgvIyQcSV-Ge1x88gS",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF1NTqU9lr1VJ6QX1heAU9b3ORdRQOciPrLLKSpcrcwEx5XU2mIpwP6xC-QMhCUbA81Kar-IUAXmAd-zpNtWdJCt665uvrIPHGwaZiCMJf3l9NhTThTn9hkinU9LgWxCBEmhZVjgXoAjV5q9DGb0UxHjStng6XY11YQZalwaxVucXgr7OzRqHMlM64biEYKmRdngHLwuSbGneE_",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEeg0MLSUNpETq3VZGbmfDArfgG-VAMsO_Wp9Nd8LKdTOzKPvCsB4aKikpWbdt8XbRzDQKNNvespbmvsArkbCG680MybRtkxTweKPebiLyzZvVpyjXdzyyQSR0PrqU_PS_bWAk2JHJJ5Cf9T7HHeG5uQGhCdeo-oN9kgic0ezHi-UZw9g6LstAcPMZSK94puhE="
]

for u in urls:
    r = requests.get(u, allow_redirects=False, timeout=10)
    print("Location:", r.headers.get('Location'))
