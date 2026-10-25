import re, base64, json, os, shutil
K='../brand/'
s=open('src.html').read()
b64=lambda p: base64.b64encode(open(p,'rb').read()).decode()
wm=open('wordmark.svg').read().replace('viewBox="-124.8 -118.8 1479.2 451.7"','viewBox="-2 4 1234 206"').replace('fill="#3F4A41"','fill="currentColor"').replace('class="mark" ','')
icons=json.load(open('icons.json'))
s=s.replace('{{WORDMARK}}',wm).replace('{{SPIRAL}}',open('spiral.svg').read())
s=re.sub(r'\{\{FONT:([^}]+)\}\}',lambda m:'data:font/woff2;base64,'+b64(K+'fonts/'+m.group(1)),s)
s=re.sub(r'\{\{ICON:(\w+):(\w+)\}\}',lambda m:icons[m.group(1)][m.group(2)].replace('role="img"','aria-hidden="true"'),s)
s=re.sub(r'\{\{IMG:([^}]+)\}\}',lambda m:'data:image/jpeg;base64,'+b64('img/'+m.group(1)+'.jpg'),s)
cats=['c-breakfast','c-omelettes','c-sweet','c-sandwiches','c-dessert','c-drinks']
s=s.replace('{{IMGMAP}}',json.dumps({n:'data:image/jpeg;base64,'+b64('img/'+n+'.jpg') for n in cats}))
s=s.replace('{{ICONMAP}}',json.dumps({'line':{k:v.replace('role="img"','aria-hidden="true"') for k,v in icons['line'].items()}}))
s=s.replace('{{FAVSVG}}','data:image/svg+xml;base64,'+b64('favicon.svg'))
s=re.sub(r'\{\{FAVPNG:(\d+)\}\}',lambda m:'data:image/png;base64,'+b64('favicon-'+m.group(1)+'.png'),s)
assert '{{' not in s, re.findall(r'\{\{.{0,40}',s)[:3]
open('../index.html','w').write(s)
print(len(s)//1024,'KB')
