/* Define the SIP wrapper to the ifs library. 
 * http://ftp.ics.uci.edu/pub/centos0/ics-custom-build/BUILD/sip-4.10/doc/html/c_api.html
 */  

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
    int readdir(void *dir_cb,char** entry_name /Out/,int* size /Out/,int* type /Out/);
    %MethodCode
        SIP_SSIZE_T length = 0;
        sipRes = sipCpp->readdir(a0,&a1,&a2,&a3);

        if (a1 != NULL)
        {
            length = strlen(a1);
        }
        PyObject * obj = sipBuildResult(0,"(igii)",sipRes, a1, length, a2, a3);
        if (a1 != NULL)
        {
            free(a1);
        }
        return obj;
    %End
    int rename(const char *old_name,const char *new_name);
    

};
