/*
                                                                        [ Group Number : 21 ]
                                                                          GAUTAM KUMAR MAHAR
                                                                           KanwarRaj Singh
                                                                           
*/

#include <iostream>
#include <cstdlib>
#include <vector>
#include <cmath>
using namespace std;


double headProbability = 0.4; // Probability of getting heads

int numStates = 10; // Number of states

int maxReward = numStates * 2; // Maximum possible reward

double discountFactor = 0.9; // Discount factor

int stateCount = numStates + 1; // Number of states including terminal states

double epsilon = 1e-14; // Convergence threshold

// Define a policy that selects the minimum of steps to reach either end
vector<int> minimumStepPolicy()
{
    vector<int> statePolicy(stateCount);
    int i = 1;
    
    while (i < statePolicy.size())
    {
        statePolicy[i] = min(i, numStates - i);
        i++;
    }
    
    statePolicy[0] = -1; // Exit state
    statePolicy[numStates] = -1; // Exit state
    
    return statePolicy;
}


// Define a policy that always selects a fixed step size
vector<int> fixedStepPolicy()
{
    vector<int> statePolicy(stateCount, 1);
    statePolicy[0] = -1; // Exit state
    statePolicy[numStates] = -1; // Exit state
    return statePolicy;
}

// Check if the difference between two utility vectors is below the threshold
bool convergenceCheck(vector<double> oldUtility, vector<double> newUtility)
{
    double squareDifference = 0;
    int i = 0;
    
    while (i < oldUtility.size())
    {
        squareDifference += pow(oldUtility[i] - newUtility[i], 2);
        i++;
    }

    squareDifference = sqrt(squareDifference);
    return squareDifference < epsilon;
}


// Calculate the utility vector for a given policy
vector<double> policyUtility(vector<int> statePolicy)
{
    vector<double> oldUtility(stateCount, 0);
    vector<double> newUtility(stateCount, 0);
    oldUtility[numStates] = 2 * numStates;
    newUtility[numStates] = 2 * numStates;

    bool converged = false;

    while (!converged)
    {
        oldUtility = newUtility;
        converged = true;

        for (int i = 1; i < statePolicy.size() - 1; i++)
        {
            newUtility[i] = headProbability * (discountFactor * oldUtility[i + statePolicy[i]]) + (1 - headProbability) * (discountFactor * oldUtility[i - statePolicy[i]]);

            // Check for convergence in this state
            if (abs(newUtility[i] - oldUtility[i]) >= epsilon)
            {
                converged = false;
            }
        }
    }

    return newUtility;
}


// Calculate the optimal policy using value iteration
vector<int> optimalValueIterationPolicy()
{
    vector<double> oldUtility(stateCount, 0);
    vector<double> utility(stateCount, 0);
    vector<int> policy(stateCount, 0);

    do
    {
        oldUtility = utility;
        for (int j = 0; j < stateCount; j++)
        {
            if (j == numStates)
            {
                utility[j] = 2 * numStates;
            }
            else if (j == 0)
            {
                utility[j] = 0;
            }
            else
            {
                double maxUtility = -1e37;
                for (int i = 0; i <= min(j, numStates - j); i++)
                {
                    if (maxUtility < (headProbability * (discountFactor * oldUtility[i + j]) + (1 - headProbability) * (discountFactor * oldUtility[j - i])))
                    {
                        policy[j] = i;
                        maxUtility = headProbability * (discountFactor * oldUtility[i + j]) + (1 - headProbability) * (discountFactor * oldUtility[j - i]);
                        utility[j] = maxUtility;
                    }
                }
            }
        }
    } while (!convergenceCheck(utility, oldUtility));

    return policy;
}

// Calculate the optimal policy using policy iteration
vector<int> optimalPolicyIterationPolicy()
{
    vector<double> utility(stateCount, 0);
    vector<int> policy(stateCount, 0);
    vector<int> previousPolicy(stateCount, 0);

    do
    {
        previousPolicy = policy;
        for (int j = 0; j < stateCount; j++)
        {
            double maxUtility = policyUtility(policy)[j];
            for (int i = 0; i <= min(j, numStates - j); i++)
            {
                double actionUtility = (headProbability * (discountFactor * policyUtility(policy)[i + j]) + (1 - headProbability) * (discountFactor * policyUtility(policy)[j - i]));
                if (maxUtility < actionUtility)
                {
                    maxUtility = actionUtility;
                    policy[j] = i;
                }
            }
        }
    } while (!(previousPolicy == policy));

    return policy;
}

int main()
{
    cout << "Using Minimum Step Policy:" << endl;
    cout << "State | Action | Utility" << endl;
    vector<int> minimumStepPolicyResult = minimumStepPolicy();
    vector<double> minimumStepPolicyUtility = policyUtility(minimumStepPolicyResult);
    for (int x = 0; x < minimumStepPolicyResult.size(); x++)
    {
        cout << x << " " << minimumStepPolicyResult[x] << " " << minimumStepPolicyUtility[x] << endl;
    }

    cout << endl;
    cout << "Using Fixed Step Policy:" << endl;
    cout << "State | Action | Utility" << endl;
    vector<int> fixedStepPolicyResult = fixedStepPolicy();
    vector<double> fixedStepPolicyUtility = policyUtility(fixedStepPolicyResult);
    for (int x = 0; x < fixedStepPolicyResult.size(); x++)
    {
        cout << x << " " << fixedStepPolicyResult[x] << " " << fixedStepPolicyUtility[x] << endl;
    }

    cout << endl;
    cout << "Optimal Policy using Value Iteration:" << endl;
    vector<int> optimalValueIterationResult = optimalValueIterationPolicy();
    vector<double> optimalValueIterationUtility = policyUtility(optimalValueIterationResult);
    for (int x = 0; x < optimalValueIterationResult.size(); x++)
    {
        if (x == numStates)
        {
            cout << x << " -1 " << optimalValueIterationUtility[x] << endl;
        }
        else if (x == 0)
        {
            cout << x << " -1 " << optimalValueIterationUtility[x] << endl;
        }
        else
        {
            cout << x << " " << optimalValueIterationResult[x] << " " << optimalValueIterationUtility[x] << endl;
        }
    }

    cout << endl;
    cout << "Optimal Policy Using Policy Iteration:" << endl;
    vector<int> optimalPolicyIterationResult = optimalPolicyIterationPolicy();
    vector<double> optimalPolicyIterationUtility = policyUtility(optimalPolicyIterationResult);
    for (int x = 0; x < optimalPolicyIterationResult.size(); x++)
    {
        if (x == numStates)
        {
            cout << x << " -1 " << optimalPolicyIterationUtility[x] << endl;
        }
        else if (x == 0)
        {
            cout << x << " -1 " << optimalPolicyIterationUtility[x] << endl;
        }
        else
        {
            cout << x << " " << optimalPolicyIterationResult[x] << " " << optimalPolicyIterationUtility[x] << endl;
        }
    }

    return 1;
}
