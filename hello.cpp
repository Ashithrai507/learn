#include<iostream>
using namespace std;
int main(){
    string cars[10] ={};
    int n=0;
    cout << "enter the number of cars you want to enter: ";
    cin >> n;
    cin.ignore(); 
    for(int i=0; i<n; i++){
        cout << "enter the name of car " << i+1 << ": ";
        getline(cin, cars[i]);
    }
    cout << "the cars you entered are: " << endl;
    for(int i=0; i<n; i++){
        cout << cars[i] << endl;
}
    return 0;
}