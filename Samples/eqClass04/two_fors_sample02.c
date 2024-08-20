int main()
{
    int arr[10][10];

    for(int j = 0; j < 10; ++j)
    {
        for(int i = 0; i < 10; ++i)
        {
            arr[i][j] = i + j;
        }
    }

    return 0;
}