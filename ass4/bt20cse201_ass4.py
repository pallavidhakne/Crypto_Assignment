from collections import Counter
cprtxt="XLILSYWIMWRSAAJSVWEPIJSVJSYVQMPPMSRHSPPEVWMXMWASVXLQSVILYVVCFIJSVIXLIWIPPIVVIGIMZIWQSVISJJIVW"
mp=Counter(cprtxt)
l=['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U', 'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'Q', 'X', 'Z']
print(mp)
r_mp=[]
i=0
for key in sorted(mp, key=mp.get, reverse=True):
      r_mp.append(key)

key=ord(r_mp[0])-ord(l[0])
# print(key)
# print(r_mp)
ans=""

for ch in cprtxt:
            ans+=chr((ord(ch) - key-65) % 26 + 65)
 
print(ans)