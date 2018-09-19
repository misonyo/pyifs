#include "ifs.h"
#include <fatfs/ff.h>
#include <stdio.h>
#include <string.h>

ifs::ifs()
{
    FRESULT ret;
    FATFS fs;     /* Ponter to the filesystem object */

    ret = f_mount(&fs, "/d/misonyo/test/sd0.bin", 0);
    if (ret != FR_OK)
    {
        printf("挂载文件系统失败 (%s)\r\n", FR_Table[result]);
    }
    else
    {
        printf("挂载文件系统成功 (%s)\r\n", FR_Table[result]);
    }

    printf("<==%s==>\n", __func__);
}
ifs::~ifs()
{
    FRESULT ret;

    ret = f_mount(0, "/d/misonyo/test/sd0.bin", 0);
    if (ret != FR_OK)
    {
        printf("卸载文件系统失败 (%s)\r\n", FR_Table[result]);
    }
    else
    {
        printf("卸载文件系统成功 (%s)\r\n", FR_Table[result]);
    }
    printf("<==~%s==>\n", __func__);
}

void* ifs::open (const char *filename, const char *opentype)
{
    static FIL fil = NULL;
    BYTE mode;

    if(strcmp("r",opentype) == 0)
    {
        mode = FA_READ;
    }
    else if(strcmp("r+",opentype) == 0)
    {
        mode = FA_READ | FA_WRITE;
    }
    else if(strcmp("w",opentype) == 0)
    {
        mode = FA_CREATE_ALWAYS | FA_WRITE;
    }
    else if(strcmp("w+",opentype) == 0)
    {
        mode = FA_CREATE_ALWAYS | FA_WRITE | FA_READ;
    }
    else if(strcmp("a",opentype) == 0)
    {
        mode = FA_OPEN_APPEND | FA_WRITE;
    }
    else if(strcmp("a+",opentype) == 0)
    {
        mode = FA_OPEN_APPEND | FA_WRITE | FA_READ;
    }
    else if(strcmp("wx",opentype) == 0)
    {
        mode = FA_CREATE_NEW | FA_WRITE;
    }
    else if(strcmp("w+x",opentype) == 0)
    {
        mode =  FA_CREATE_NEW | FA_WRITE | FA_READ;
    }
    else
    {
        printf("wrong open type!\n");
    }

    f_open(&fil, filename, mode);

    printf("<==%s==>\n", __func__);

    return ((void*)&fil);
}
int ifs::close (void* stream)
{
    int ret;

    ret = f_close((FIL*)stream);

    printf("<==%s==>\n", __func__);

    return ret;
}
int ifs::read  (char* data, int size, void *stream)
{
    int ret;

    ret = f_close((FIL*)stream);

    printf("<==%s==>\n", __func__);

    return ret;
}
int ifs::write (const char *data, int size, void *stream)
{
    int ret;

    ret = f_close((FIL*)stream);

    printf("<==%s==>\n", __func__);

    return ret;
}
int ifs::flush (void *stream)
{
    int ret;

    ret = f_close((FIL*)stream);

    printf("<==%s==>\n", __func__);

    return ret;
}
int ifs::seek (void *stream, int offset, int whence)
{
    int ret;

    ret = f_close((FIL*)stream);

    printf("<==%s==>\n", __func__);

    return ret;
}
int ifs::tell (void *stream)
{
    int ret;

    ret = f_close((FIL*)stream);

    printf("<==%s==>\n", __func__);

    return ret;
}
