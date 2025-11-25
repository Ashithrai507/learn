#include<iostream>
#include<stack>
using namespace std;

int main()
{
    stack<int> s;

    s.push(10);
    s.push(20);
    s.push(30);

    for(int i=0;i<3;i++)
    {
        cout << s.top() << endl;
        s.pop();
        
    }
    return 0;
}