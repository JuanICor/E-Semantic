int main()
{
    int x = 0,
        y = 16;

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
    
    return 0;
}