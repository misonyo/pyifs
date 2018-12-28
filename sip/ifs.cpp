#include "ifs.h"
#include <stdio.h>
#include <string.h>
#include <stdint.h>

ifs::ifs(const char* ldn)
{
    FRESULT res;
    printf("<===%s===>\n", __func__);

    drive_num = ldn;
    printf(">>>>>>>[ldn]%s\n",ldn);
    fs_cb = (FATFS*)malloc(sizeof (FATFS));
    if(fs_cb == NULL)
    {
        printf("ifs malloc failed!\n");
    }
    else
    {
        res = f_mount(fs_cb, drive_num, 0);
        if (res != FR_OK)
        {
            printf("mount %s failed,return value is:%d!\n",drive_num,res);
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
    FRESULT res;
    printf("<===%s===>\n", __func__);

    res = f_unmount(drive_num);
    if (res != FR_OK)
    {
        printf("unmount %s failed,return value is:%d!\n",drive_num,res);
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
    FRESULT res;
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
    res = f_open(file_cb, filename, open_flag);
    if(res)
    {
        printf("f_open %s failed,return value is %d!\n",filename,res);
        free(file_cb);
        return NULL;
    }

    return ((void*)file_cb);
}
int ifs::close(void* stream)
{
    FRESULT res;
    printf("<===%s===>\n", __func__);

    res = f_close((FIL*)stream);

    return res;
}
int ifs::read(void *stream,char** buff, int size)
{
    FRESULT res;
    int num = 0;
    printf("<===%s===>\n", __func__);

    *buff = (char*)malloc(size);
    res = f_read((FIL*)stream, (void*)*buff, (UINT)size, (UINT*)&num);
    if(res)
    {
        printf("f_read failed,return value is:%d!\n",res);
        num = 0;
    }

    printf("<===%s %d===>\n", __func__, num);
    return num;
}
int ifs::write(void *stream,const char* buff, int size)
{
    FRESULT res;
    int num = 0;
    printf("<===%s===>\n", __func__);

    res = f_write((FIL*)stream, (const void*)buff, (UINT)size, (UINT*)&num);
    if(res)
    {
        printf("f_write failed,return value is:%d!\n",res);
        num = 0;
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
    FRESULT res;
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
    res = f_lseek((FIL*)stream, ofs);

    return res;
}
int ifs::tell (void *stream)
{
    printf("<===%s===>\n", __func__);

    return f_tell((FIL*)stream);
}
int ifs::mkdir(const char *dirname)
{
    printf("<===%s===>\n", __func__);

    return f_mkdir(dirname);
}

int ifs::rmdir(const char *dirname)
{
    printf("<===%s===>\n", __func__);

    return f_unlink(dirname);
}

void* ifs::opendir(const char *dirname)
{
    FRESULT res;
    DIR* dir_cb;

    printf("<===%s===>\n", __func__);
    dir_cb = (DIR*)malloc(sizeof (DIR));
    res = f_opendir(dir_cb, dirname);
    if (res)
    {
        printf("f_opendir failed,return value is:%d!\n",res);
        free(dir_cb);
        return NULL;
    }

    return dir_cb;
}

int ifs::readdir(void *dir_cb,char** entry_name,int* size,int* type)
{
    FRESULT res;
    FILINFO fno;
    printf("<===%s===>\n", __func__);

    res = f_readdir((DIR*)dir_cb, &fno);
    if (res != FR_OK)
    {
        *entry_name = NULL;
        *size = 0;
        *type = 0;
        return res;
    }
   else
    {
       *entry_name = (char*)malloc(strlen(fno.fname) + 1);
       strcpy(*entry_name,fno.fname);
       *size = fno.fsize;
       *type = fno.fattrib;
    }

    return res;
}

int ifs::rename(const char *old_name,const char *new_name)
{
    FRESULT res;
    printf("<===%s===>\n", __func__);

    res = f_rename(old_name,new_name);
    if (res)
    {
        printf("f_rename failed,return value is:%d!\n",res);
    }
    return res;
}
