#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "diskio.h"

DSTATUS disk_initialize (BYTE pdrv)
{
    DRESULT ret = RES_OK;
    FILE *fp = NULL;
    char dir[10];

    snprintf(dir, 10,"sd%d.bin", pdrv);

    do{
        fp = fopen(dir, "ab+");
        if(!fp)
        {
            ret = RES_ERROR;
            printf("%s fopen failed!",__func__);
            break;
        }

        fclose(fp);
    }while(0);

    printf("this is :%s\n", __func__);

    return ret;
}
DSTATUS disk_status (BYTE pdrv)
{
    DRESULT ret = RES_OK;
    FILE *fp = NULL;
    char dir[10];

    snprintf(dir, 10,"sd%d.bin", pdrv);

    fp = fopen(dir, "rb");
    if(!fp)
    {
        ret = STA_NODISK;
    }

    fclose(fp);

    printf("this is :%s\n", __func__);

    return ret;
}
DRESULT disk_read (BYTE pdrv, BYTE* buff, DWORD sector, UINT count)
{
    DRESULT ret = RES_OK;
    FILE *fp = NULL;
    char dir[10];

    snprintf(dir, 10,"sd%d.bin", pdrv);

    do{
        fp = fopen(dir, "rb+");
        if(!fp)
        {
            ret = RES_NOTRDY;
            break;
        }
        fseek(fp,512 * sector,SEEK_SET);
        fread(buff,sizeof(char),512 * count,fp);
        fclose(fp);
    }while(0);

    printf("this is :%s\n", __func__);

    return ret;
}
DRESULT disk_write (BYTE pdrv, const BYTE* buff, DWORD sector, UINT count)
{
    DRESULT ret = RES_OK;
    FILE *fp = NULL;
    char dir[10];

    snprintf(dir, 10,"sd%d.bin", pdrv);

    do{
        fp = fopen(dir, "rb+");
        if(!fp)
        {
            ret = RES_NOTRDY;
            break;
        }
        fseek(fp,512 * sector,SEEK_SET);
        fwrite(buff,sizeof(char),512 * count,fp);
        fclose(fp);
    }while(0);

    printf("this is :%s\n", __func__);

    return ret;
}
DRESULT disk_ioctl (BYTE pdrv, BYTE cmd, void* buff)
{
	printf("%s to be implemented\n", __func__); return 0;
}

DWORD get_fattime (void)
{
	return time(0);
}
