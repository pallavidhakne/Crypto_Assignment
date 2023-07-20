//find out the multiplicative inverse of an integer b using extended Euclidean
//algorithm of set Zn.
//gcd(a,b)=ax+by;
#include<bits/stdc++.h>
using namespace std;
tuple<int, int, int> extended_gcd(int a, int b) //for implementing extended Euclidean
{
    if (a == 0) {
        return make_tuple(b, 0, 1);
    }
 
    int gcd, x, y;

    tie(gcd, x, y) = extended_gcd(b % a, a);
 
    return make_tuple(gcd, (y - (b/a) * x), x);
}
int main()
{
   int a,M;
   cin>>a>>M;
    tuple<int, int, int> t = extended_gcd(a, M);
     int gc = get<0>(t);
    int x = get<1>(t);
    int y = get<2>(t);
    if (gc != 1)
        cout << "Inverse doesn't exist";
    else {
 
        // m is added to handle negative x
        int res = (x % M + M) % M;
        cout << "Modular multiplicative inverse is " << res;
    }
   return 0; 
}