#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "diskio.h"
#include "ifs.h"


DSTATUS disk_initialize (BYTE pdrv)
{
    FILE *fp = NULL;
    char* device_name;
    printf("<===%s===>\n", __func__);
    printf(">>>>>pdrv:%d\n",pdrv);

    device_name = dev_name_table[pdrv];
    fp = fopen(device_name, "rb+");
    if(!fp)
    {
        printf("%s fopen failed!\n",__func__);
        return RES_ERROR;
    }

    fclose(fp);

    return RES_OK;
}
DSTATUS disk_status (BYTE pdrv)
{
    FILE *fp = NULL;
    char* device_name;
    printf("<===%s===>\n", __func__);
    printf(">>>>>pdrv:%d\n",pdrv);

    device_name = dev_name_table[pdrv];

    fp = fopen(device_name, "rb");
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
    char* device_name;
    printf("<===%s===>\n", __func__);
    printf(">>>>>pdrv:%d\n",pdrv);

    device_name = dev_name_table[pdrv];

    fp = fopen(device_name, "rb");
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
    char* device_name;
    printf("<===%s===>\n", __func__);
    printf(">>>>>pdrv:%d\n",pdrv);

    device_name = dev_name_table[pdrv];

    fp = fopen(device_name, "rb+");
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
    DRESULT res;
    FILE *fp = NULL;
    char* device_name;
    printf("<===%s===>\n", __func__);
    printf(">>>>>pdrv:%d\n",pdrv);

    device_name = dev_name_table[pdrv];

    fp = fopen(device_name, "rb+");
    if(!fp)
    {
        printf("%s fopen failed!",__func__);
        return RES_PARERR;
    }

    switch(cmd)
    {
    case GET_SECTOR_COUNT:
        * (DWORD*)buff = floor((fseek(fp, 0, SEEK_END) - ftell(fp)) / 512);
        break;
    case GET_SECTOR_SIZE:
        * (WORD*)buff = 512;
        break;
    case GET_BLOCK_SIZE:
        * (DWORD*)buff = 512;
        break;
    case CTRL_SYNC:
        res = RES_OK;
        break;
    case CTRL_TRIM:
        res = RES_OK;
        break;
    default:
        res = RES_OK;
        break;
    }

    fclose(fp);

    return res;
}

DWORD get_fattime (void)
{
	return time(0);
}
