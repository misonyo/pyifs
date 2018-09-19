#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "diskio.h"

char* name_cat(BYTE pdrv)
{
    char num[2];
    char dev_name[10] = "sd";
    char dir[16] = "/d/misonyo/test/";

    itoa(pdrv, num, 10);
    strcat(dev_name,num);
    strcat(dev_name,".bin");
    strcat(dir, dev_name);

    return dir;
}

DSTATUS disk_initialize (BYTE pdrv)
{
    DRESULT ret = RES_OK;
    FILE *fp = NULL;
    char dir = name_cat(pdrv);

    do{
        fp = fopen(dir, "ab+");
        if(!fp)
        {
            ret = RES_ERROR;
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
    char dir = name_cat(pdrv);

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
    char dir = name_cat(pdrv);

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
    char dir = name_cat(pdrv);

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
