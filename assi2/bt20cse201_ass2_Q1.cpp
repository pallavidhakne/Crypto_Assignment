// Ashu is writing
// his diary and he want to encrypt the text in his diary with a simple way such
// that every letter in a word is written in its mirror image form ( if the mirror
// image of letter exist i. e. it is also a letter ).


#include<bits/stdc++.h>
using namespace std;
#define MAX_WORD_LEN 6000
int main()
{
    char word[MAX_WORD_LEN];
    cout<<"enter the words:"<<endl;
    cin.getline(word,MAX_WORD_LEN);
    for(int i=0;i<MAX_WORD_LEN;i++)
    {
        if(word[i]=='b')
        {
            word[i]='d';
        }
        else if(word[i]=='d')
        {
            word[i]='b';
        }
        else if(word[i]=='p')
        {
            word[i]='q';
        }
        else if(word[i]=='q')
        {
            word[i]='p';
        }
    }
    cout<<endl;
    cout<<"The changing words are :"<<endl;
    cout<<word<<endl;
return 0;
}