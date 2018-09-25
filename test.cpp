#include "ifs.h"

int main(void)
{
    
    ifs img("0:");
    void* fp = img.open("hello.txt","r+");
    char* data;
    int r=img.read(fp, &data, 24);
    for(int i=0; i< r; i++)
    {
        printf("%02X-%c ", data[i], data[i]);
    }

    return 0;
}
