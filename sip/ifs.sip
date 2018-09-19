/* Define the SIP wrapper to the ifs library. 
 * python version 3 -- sip 4.17  
 * python version 2 -- sip 4.16.4 */  

%Module ifs

class ifs {

%TypeHeaderCode
#include "ifs.h"
%End

public:
    /* operations for file */
    void* open (const char *filename, const char *opentype);
    int close (void* stream);
    int read  (char* data /Out/, int size, void *stream);
    int write (const char *data, int size, void *stream);
    int flush (void *stream);
    int seek (void *stream, int offset, int whence);
    int tell  (void *stream);
};
