int main()
{
    int arr[10][10];

    // Start Semantic Matching
    for(int i = 0; i < 10; ++i)
    {
        for(int j = 0; j < 10; ++j)
        {
            arr[i][j] = i + j;
        }
    }
    // End Semantic Matching
    
    return 0;
}