#include "ifs.h"
#include <stdio.h>
#include <string.h>
#include <stdint.h>

ifs::ifs(const char* ldn)
{
    FRESULT ret;
    printf("<===%s===>\n", __func__);

    drive_num = ldn;

    fs_cb = (FATFS*)malloc(sizeof (FATFS));
    if(fs_cb == NULL)
    {
        printf("ifs malloc failed!\n");
    }
    else
    {
        ret = f_mount(fs_cb, drive_num, 0);
        if (ret != FR_OK)
        {
            printf("mount %s failed,return value is:%d!\n",drive_num,ret);
            free(fs_cb);
        }
        else
        {
            printf("mount %s succeed!\n",drive_num);
        }
    }
}
ifs::~ifs()
{
    FRESULT ret;
    printf("<===%s===>\n", __func__);

    ret = f_unmount(drive_num);
    if (ret != FR_OK)
    {
        printf("unmount %s failed,return value is:%d!\n",drive_num,ret);
    }
    else
    {
        printf("unmount %s succeed!\n",drive_num);
    }

    free(fs_cb);
}

void* ifs::open(const char *filename, const char *opentype)
{
    FIL* file_cb;
    FRESULT ret;
    BYTE open_flag;
    printf("<===%s===>\n", __func__);

    for(open_flag = 0;(*opentype) != '\0';opentype ++)
    {
        if('r' == (*opentype))
        {
            open_flag |= FA_READ;
        }
        else if('w' == (*opentype))
        {
            open_flag |= (FA_CREATE_ALWAYS | FA_WRITE);
        }
        else if('a' == (*opentype))
        {
            open_flag |= (FA_OPEN_APPEND | FA_WRITE);
        }
        else if('x' == (*opentype))
        {
            open_flag |= FA_CREATE_NEW;
            open_flag &= ~FA_CREATE_ALWAYS;
        }
        else if('+' == (*opentype))
        {
            open_flag |= (FA_READ | FA_WRITE);
        }
        else
        {
            printf("wrong open type!\n");
            return NULL;
        }
    }

    file_cb = (FIL*)malloc(sizeof (FIL));
    if(file_cb == NULL)
    {
        return NULL;
    }
    ret = f_open(file_cb, filename, open_flag);
    if(ret)
    {
        printf("f_open %s failed,return value is %d!\n",filename,ret);
        free(file_cb);
        return NULL;
    }

    return ((void*)file_cb);
}
int ifs::close(void* stream)
{
    FRESULT ret;
    printf("<===%s===>\n", __func__);

    ret = f_close((FIL*)stream);

    return ret;
}
int ifs::read(void *stream,char** buff, int size)
{
    FRESULT ret;
    int num = -1;
    printf("<===%s===>\n", __func__);

    *buff = (char*)malloc(size);
    ret = f_read((FIL*)stream, (void*)*buff, (UINT)size, (UINT*)&num);
    if(ret)
    {
        printf("f_read failed,return value is:%d!\n",ret);
    }

    printf("<===%s %d===>\n", __func__, num);
    return num;
}
int ifs::write(void *stream,const char* buff, int size)
{
    FRESULT ret;
    int num = -1;
    printf("<===%s===>\n", __func__);

    ret = f_write((FIL*)stream, (const void*)buff, (UINT)size, (UINT*)&num);
    if(ret)
    {
        printf("f_write failed,return value is:%d!\n",ret);
    }
    return num;
}
int ifs::flush (void *stream)
{

    printf("<==%s==>\n", __func__);

    return 0;
}
int ifs::seek (void *stream, int offset, int whence)
{
    FRESULT ret;
    int ofs;
    printf("<===%s===>\n", __func__);

    if(0 == whence)
    {
        ofs = offset;
    }
    else if((1 == whence) && (offset >= 0))
    {

        ofs = f_tell((FIL*)stream) + offset;
    }
    else if((2 == whence) && (offset < 0))
    {
        ofs = f_size((FIL*)stream) + offset;
    }
    else
    {
        printf("wrong whence or offset!\n");
        return FR_INVALID_PARAMETER;
    }
    ret = f_lseek((FIL*)stream, ofs);

    return ret;
}
int ifs::tell (void *stream)
{
    printf("<===%s===>\n", __func__);

    return f_tell((FIL*)stream);
}

