/* Define the SIP wrapper to the ifs library. 
 * python version 3 -- sip 4.17  
 * python version 2 -- sip 4.16.4 */  

%Module ifs

class ifs {

%TypeHeaderCode
#include "ifs.h"
%End

public:
    explicit ifs(const char* ldn);
    ~ifs();

    void* open(const char *filename, const char *opentype);
    int close(void* stream);
    int read(void *stream,char** buff /Out/, int size);
    %MethodCode
        sipRes = sipCpp->read(a0,&a1,a2);
        PyObject * obj = sipBuildResult(0,"(ig)",sipRes,a1,sipRes);
        free(a1);
        return obj;
    %End
    int write(void *stream,const char* buff, int size);
    int flush(void *stream);
    int seek(void *stream, int offset, int whence);
    int tell(void *stream);
    int mkdir(const char *dirname);
    int rmdir(const char *dirname);
    void* opendir(const char *dirname);
    int readdir(void *dir_cb,char** entry_name /out/);
    %MethodCode
        sipRes = sipCpp->readdir(a0,&a1);
    
        PyObject * obj = sipBuildResult(0,"(ig)",sipRes,a1, strlen(a1));
        free(a1);
        return obj;
    %End
    int rm(const char *old_name,const char *new_name);
    

};
