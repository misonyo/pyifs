#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "diskio.h"

DSTATUS disk_initialize (BYTE pdrv)
{
    FILE *fp = NULL;
    char dir[10];
    printf("<===%s===>\n", __func__);

    snprintf(dir, 10,"sd%d.bin", pdrv);

    fp = fopen(dir, "rb+");
    if(!fp)
    {
        printf("%s fopen failed!",__func__);
        return RES_ERROR;
    }

    fclose(fp);

    return RES_OK;
}
DSTATUS disk_status (BYTE pdrv)
{
    FILE *fp = NULL;
    char dir[10];
    printf("<===%s===>\n", __func__);

    snprintf(dir, 10,"sd%d.bin", pdrv);

    fp = fopen(dir, "rb");
    if(!fp)
    {
        printf("%s fopen failed!",__func__);
        return STA_NODISK;
    }

    fclose(fp);

    return RES_OK;
}
DRESULT disk_read (BYTE pdrv, BYTE* buff, DWORD sector, UINT count)
{
    FILE *fp = NULL;
    char dir[10];
    printf("<===%s===>\n", __func__);

    snprintf(dir, 10,"sd%d.bin", pdrv);

    fp = fopen(dir, "rb");
    if(!fp)
    {
        printf("%s fopen failed!",__func__);
        return RES_NOTRDY;
    }
    fseek(fp,512 * sector,SEEK_SET);
    fread(buff,sizeof(char),512 * count,fp);
    fclose(fp);

    return RES_OK;
}
DRESULT disk_write (BYTE pdrv, const BYTE* buff, DWORD sector, UINT count)
{
    FILE *fp = NULL;
    char dir[10];
    printf("<===%s===>\n", __func__);

    snprintf(dir, 10,"sd%d.bin", pdrv);

    fp = fopen(dir, "rb+");
    if(!fp)
    {
        printf("%s fopen failed!",__func__);
        return RES_NOTRDY;
    }
    fseek(fp,512 * sector,SEEK_SET);
    fwrite(buff,sizeof(char),512 * count,fp);
    fclose(fp);

    return RES_OK;
}
DRESULT disk_ioctl (BYTE pdrv, BYTE cmd, void* buff)
{
    FILE *fp = NULL;
    char dir[10];
    printf("<===%s===>\n", __func__);

    snprintf(dir, 10,"sd%d.bin", pdrv);

    fp = fopen(dir, "rb+");
    if(!fp)
    {
        printf("%s fopen failed!",__func__);
        return RES_PARERR;
    }

    switch(cmd)
    {
    case GET_SECTOR_COUNT:
        * buff = (DWORD)floor((fseek(fp, 0, SEEK_END) - ftell(fp)) / 512);
        break;
    case GET_SECTOR_SIZE:
        * buff = (WORD)512;
        break;

    }
    return 0;
}

DWORD get_fattime (void)
{
	return time(0);
}
