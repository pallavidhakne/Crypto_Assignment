//  Consider the linear equation in the form ax ≡ b (mod n ).
// Check how many solutions are exists for the equation and also find the
// possible solutions. (Values of a, b and n must be taken from the user)
//The Chinese Remainder Theorem
#include <bits/stdc++.h>
using namespace std;

int ExtendedEuclidAlgo(int a, int b,int &x, int &y)
{
    if (b == 0)
    {
        x = 1;
        y = 0;
        return a;
    }
    else
    {
        int x1, y1;
        int gcd = ExtendedEuclidAlgo(b, a % b, x1, y1);

        x = y1;
        y = x1 - floor(a / b) * y1;

        return gcd;
    }
}

void solve(int A, int B, int N)
{
    A = A % N;
    B = B % N;

    int u = 0, v = 0;

    int d = ExtendedEuclidAlgo(A, N, u, v);

    if (B % d != 0)
    {
        cout << -1 << endl;
        return;
    }

    int x0 = (u * (B / d)) % N;
    if (x0 < 0)
        x0 += N;

    for (int i = 0; i <= d - 1; i++)
        cout << (x0 + i * (N / d)) % N << " ";
}

int main()
{
    int A;
    int B;
    int N;
    cout << "Enter A:";
    cin >> A;
    cout << "Enter B:";
    cin >> B;
    cout << "Enter N:";
    cin >> N;
    solve(A, B, N);
    // 15 9 18
    // 9 21 30
    return 0;
}