// WAP to perform
// brute force attack on the cipher text “dvvkzecfssprkkve”.
#include <iostream>
using namespace std;
string decrypt(string text, int s)
{
    string result = "";
    for (int i = 0; i < text.length(); i++)
    {
        if (isupper(text[i]))
            result += char(int(text[i] + s - 65) % 26 + 65);
        else
            result += char(int(text[i] + s - 97) % 26 + 97);
    }
    return result;
}
int main()
{
    string s = "dvvkzecfssprkkve";
    for (int key = 1; key < 26; key++)
    {
        string result = decrypt(s, key);
        cout << result << endl;
    }
    return 0;
}