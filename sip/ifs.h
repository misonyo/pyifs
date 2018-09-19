#ifndef _IFS_H
#define _IFS_H

#include <stdio.h>
class ifs
{
public:
    explicit ifs();
    ~ifs();

    void* open(const char *filename, const char *opentype);
    int close(void* stream);
    int read(char* data, int size, void *stream);
    int write(const char *data, int size, void *stream);
    int flush(void *stream);
    int seek(void *stream, int offset, int whence);
    int tell(void *stream);
};
#endif

