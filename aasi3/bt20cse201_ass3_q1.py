import string
key="COMMONLOUNGE"

# remove duplicates
visited=set()
new_key=''
for ch in key:
    if ch not in visited:
        new_key+=ch
    visited.add(ch)
# print(new_key)

# form the playfair matrix
k=0
m=0
mat=[]
alphabet = list(string.ascii_uppercase)
char_list=[]
for ch in alphabet:
    if ch not in visited and ch!='J':
        char_list.append(ch)
# print(char_list)
for i in range(5):
    row=[]
    for j in range(5):
        if(k<len(new_key)):
             row.append(new_key[k])
             k+=1
        elif m<len(alphabet):
             row.append(char_list[m])
             m+=1
    mat.append(row)
        
# print(mat)
# for row in mat:
#  print(row)
# search in a matrix
def search(mat,c):
    ans=[0]*2
    for i in range(5):
        for j in range(5):
            if(mat[i][j]==c):
                ans[0]=i
                ans[1]=j
    return ans
p_text="PLAYFAIRMESXSAGE"
ans=""
# print(p_text)
for i in range(0,len(p_text),2):
    f=p_text[i]
    s=p_text[i+1]
    p1=search(mat,f)
    p2=search(mat,s)
    if p1[0]==p2[0]:
        ans+=mat[p1[0]][(p1[1]+1)%5]
        ans+=mat[p2[0]][(p2[1]+1)%5]
    elif(p1[1]==p2[1]):
        ans+=mat[(p1[0]+1)%5][p1[1]]
        ans+=mat[(p2[0]+1)%5][p2[1]]
    else:
        ans+=mat[p1[0]][p2[1]]
        ans+=mat[p2[0]][p1[1]]
print(ans)