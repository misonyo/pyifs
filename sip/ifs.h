#ifndef _IFS_H
#define _IFS_H

#include <stdio.h>
#include "ff.h"

class ifs
{
public:
    explicit ifs(const char* ldn);
    ~ifs();

    void* open(const char *filename, const char *opentype);
    int close(void* stream);
    int read(void *stream,char** buff, int size);
    int write(void *stream,const char* buff, int size);
    int flush(void *stream);
    int seek(void *stream, int offset, int whence);
    int tell(void *stream);
    int mkdir(const char *dirname);
    int rmdir(const char *dirname);
    void* opendir(const char *dirname);
    int readdir(void *dir_cb,char** entry_name,int* size,int* type);
    int rename(const char *old_name,const char *new_name);

private:
    const char* drive_num;
    FATFS* fs_cb;
};
#endif

