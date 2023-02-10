### endpoints

* Get company details:
```
curl 'https://appservices.contabilizei.com/plataforma/rest/authentication/login' \
  -H 'authority: appservices.contabilizei.com' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -H 'cookie: _hjSessionUser_21654=$SESSION_USER_TOKEN' \
  -H 'origin: https://app.contabilizei.com.br' \
  -H 'pragma: no-cache' \
  -H 'referer: https://app.contabilizei.com.br/' \
  -H 'sec-ch-ua: "Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'strinfs-token: $SESSION_TOKEN' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36' \
  -H 'userid: [object Object]' \
  --data-raw '$SESSION_TOKEN' \
  --compressed
```