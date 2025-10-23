int main()
{
    int x = 0,
        y = 16;

    // Start Semantic Matching
    switch(x)
    {
        case 0:
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
            y = y - x;
            break;
        default:
            y = y + x;
            break;
    }
    // End Semantic Matching

    return 0;
}
