#include <bits/stdc++.h>
#include <omp.h>
using namespace std;

int main() {
    vector<int> v = {1,2,3,4,5,6,7,8,9,10};
    int odd_sum = 0;
    int even_sum = 0;

    omp_set_num_threads(4); // it sets the 
    #pragma omp parallel for
    for (int i = 0; i < v.size(); i++) {
        if (v[i] % 2 == 0){
        cout << i << " ";
            even_sum += v[i];}
        else{
            odd_sum += v[i];
            cout << i << " ";
        }
    }

    cout << "Odd sum: " << odd_sum << endl;
    cout << "Even sum: " << even_sum << endl;
}
// correct ans: 