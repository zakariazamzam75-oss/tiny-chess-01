import json,os,sys,urllib.request,urllib.error
U=os.environ.get('MAKEFUN_ENV_URL') or sys.exit('MAKEFUN_ENV_URL is not set')
V={'p':100,'n':320,'b':330,'r':500,'q':900,'k':20000}
P={'p':(0,0,2,4,4,2,0,0),'n':(-10,-5,0,5,5,0,-5,-10),'b':(-5,0,2,5,5,2,0,-5),'r':(0,0,2,5,5,2,0,0),'q':(-5,0,2,3,3,2,0,-5),'k':(10,5,-5,-10,-10,-5,5,10)}
def post(path,x):
 r=urllib.request.Request(U+path,data=json.dumps(x).encode(),headers={'content-type':'application/json'})
 try:return json.load(urllib.request.urlopen(r))
 except urllib.error.HTTPError as e:sys.exit('%s: HTTP %s'%(path,e.code))
def bd(f):
 a={};
 for y,row in enumerate(f.split()[0].split('/')):
  x=0
  for c in row:
   if c.isdigit():x+=int(c)
   else:a['abcdefgh'[x]+str(8-y)]=c;x+=1
 return a
def att(b,sq,ow):
 tx,ty=ord(sq[0])-97,int(sq[1])
 for s,c in b.items():
  if c.isupper()==ow:
   sx,sy=ord(s[0])-97,int(s[1]); l=c.lower(); dx,dy=abs(tx-sx),abs(ty-sy)
   if l=='p' and dx==1 and ty==(sy+1 if ow else sy-1): return 1
   if l=='n' and (dx,dy) in ((1,2),(2,1)): return 1
   if l=='k' and dx<=1 and dy<=1: return 1
   if (l=='b' and dx==dy) or (l=='r' and (dx==0 or dy==0)) or (l=='q' and (dx==dy or dx==0 or dy==0)):
    mx=0 if tx==sx else (1 if tx>sx else -1); my=0 if ty==sy else (1 if ty>sy else -1)
    cx,cy=sx+mx,sy+my; bl=0
    while (cx,cy)!=(tx,ty):
     if chr(cx+97)+str(cy) in b: bl=1; break
     cx+=mx; cy+=my
    if not bl: return 1
 return 0
def choose(fen,ms):
 parts=fen.split(); b=bd(parts[0]); white=parts[1]=='w'
 def score(m):
  a,z=m[:2],m[2:4]; pc=b.get(a,'p'); q=pc.lower(); cap=b.get(z)
  if not cap and q=='p' and a[0]!=z[0]:cap='p'
  s=V.get(cap.lower(),0)*10 - min(V.get(q,0),900) if cap else 0
  if len(m)>4:s+=V.get(m[4].lower(),0)*15
  tx,ty=ord(z[0])-97,int(z[1])-1; ax,ay=ord(a[0])-97,int(a[1])-1
  s+=P.get(q,(0,0,0,0,0,0,0,0))[ty if white else 7-ty]*2
  s+=28-(abs(3.5-tx)+abs(3.5-ty))*4
  if q=='p':s+=(ty if white else 7-ty)*4
  if q in 'nb' and (ay==0 if white else ay==7):s+=20
  if q=='k' and abs(tx-ax)>1:s+=40
  if q=='q' and (ay==0 if white else ay==7) and not cap:s-=30
  bn=b.copy(); bn.pop(a,None); bn[z]=pc.upper() if white else pc.lower()
  if not cap and q=='p' and a[0]!=z[0]: bn.pop(z[0]+a[1], None)
  if q=='k' and abs(tx-ax)>1:
   if z=='g1': bn.pop('h1'); bn['f1']='R'
   elif z=='c1': bn.pop('a1'); bn['d1']='R'
   elif z=='g8': bn.pop('h8'); bn['f8']='r'
   elif z=='c8': bn.pop('a8'); bn['d8']='r'
  if q!='k' and att(bn, z, not white): s-=V.get(q,0)//2
  return (-s,m)
 return min(ms,key=score)
while 1:
 g=post('/game',{})
 if g['status']=='done':break
 while g['status']=='your_move':g=post('/move',{'game':g['game'],'move':choose(g['fen'],g['legal_moves'])})
 print('game %s: %s by %s'%(g['game'],g['outcome'],g['reason']),file=sys.stderr)
print('done: %s won, %s draws, %s lost'%(g.get('wins'),g.get('draws'),g.get('losses')),file=sys.stderr)
