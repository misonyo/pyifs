#include "ifs.h"
#include <stdio.h>
#include <string.h>

ifs::ifs(const char* ldn)
{
    FRESULT ret;

    drive_num = ldn;
    fs_cb = malloc(sizeof (FATFS));

    ret = f_mount(fs_cb, drive_num, 0);
    if (ret != FR_OK)
    {
        printf("mount failed!\n");
    }
    else
    {
        printf("mount succeed!\n");
    }

    printf("<==%s==>\n", __func__);
}
ifs::~ifs()
{
    FRESULT ret;

    ret = f_unmount(drive_num);
    if (ret != FR_OK)
    {
        printf("unmount failed!\n");
    }
    else
    {
        printf("unmount succeed!\n");
    }

    free(fs_cb);

    printf("<==~%s==>\n", __func__);
}

void* ifs::open(const char *filename, const char *opentype)
{
    BYTE mode;
    static FIL file_cb;

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

    f_open(&file_cb, filename, mode);

    printf("<==%s==>\n", __func__);

    return ((void*)&file_cb);
}
int ifs::close(void* stream)
{
    int ret;

    ret = f_close((FIL*)stream);

    printf("<==%s==>\n", __func__);

    return ret;
}
int ifs::read(void *stream,char* buff, int size, int* num)
{
    int ret;

    ret = f_read((FIL*)stream, (void*)buff, (UINT)size, (UINT*)num);

    printf("<==%s==>\n", __func__);

    return ret;
}
int ifs::write(void *stream,const char* buff, int size, int* num)
{
    int ret;

    ret = f_write((FIL*)stream, (const void*)buff, (UINT)size, (UINT*)num);

    printf("<==%s==>\n", __func__);

    return ret;
}
int ifs::flush (void *stream)
{

    printf("<==%s==>\n", __func__);

    return 0;
}
int ifs::seek (void *stream, int offset, int whence)
{
    int ret;
    int ofs;

    if(0 == whence)
    {
        ofs = offset;
    }
    else if(1 == whence)
    {

        ofs = offset + f_tell((FIL*)stream);
    }
    else
    {
        ofs = f_size((FIL*)stream) + offset;
    }
    ret = f_lseek((FIL*)stream, ofs);

    printf("<==%s==>\n", __func__);

    return ret;
}
int ifs::tell (void *stream)
{
    int ret;

    ret = f_tell((FIL*)stream);

    printf("<==%s==>\n", __func__);

    return ret;
}
