/*Implement the code to find out the additive and multiplicative inverse pairs of set Zn.
Consider the linear equation in the form ax ≡ b (mod n ).*/
#include<bits/stdc++.h>
using namespace std;
int main()
{
    cout<<"Enter Zn: ";
    int zn;cin>>zn;
    vector<pair<int,int>>v;
    unordered_map<int, int> mp;
    for(int i=0;i<zn/2;i++){
        for(int j=zn/2-1;j<zn;j++){
        if(i+j==zn){
          v.push_back({i,j});
        }
       }
    }
cout<<"Additive inverse pairs are:"<<endl;
for(auto i:v){
    cout<<i.first<<","<<i.second<<endl;
}
for(int i=0;i<zn;i++){
    for(int j=0;j<zn;j++){
        int a;
        int b;
        if(i>j){
           a=i;
           b=j;
        }
        else{
            a=j;
            b=i;
        }
        if(__gcd(zn,a)!=1){
            continue;}
        if((a*b)%zn==1){
                 mp.insert({a,b});
        }
   }
}
cout<< "Multiplicative inverse pairs are:"<<endl;
for (auto x : mp)
    cout << x.first <<","<<x.second << endl;
return 0;
}