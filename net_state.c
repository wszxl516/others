#include <stdio.h>
#include <string.h>
#include <errno.h> 
#include <fcntl.h>
#include <getopt.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <net/if.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>


typedef unsigned short u16;

#include <linux/ethtool.h>
#include <linux/sockios.h>



int get_info(int skfd, char *ifname)
{
        struct ifreq ifr;
        char mac[21] = {0};
	char ip[16] = {0};
	char broadcast[16] = {0};
	char netmask[16] = {0};


        strncpy(ifr.ifr_name, ifname, IFNAMSIZ);
        //mac address
        if (!ioctl(skfd, SIOCGIFHWADDR, &ifr))
        {
            memset(mac, 0, sizeof(mac));
            snprintf(mac, sizeof(mac), "%02x:%02x:%02x:%02x:%02x:%02x",
                (unsigned char)ifr.ifr_hwaddr.sa_data[0],
                (unsigned char)ifr.ifr_hwaddr.sa_data[1],
                (unsigned char)ifr.ifr_hwaddr.sa_data[2],

                (unsigned char)ifr.ifr_hwaddr.sa_data[3],
                (unsigned char)ifr.ifr_hwaddr.sa_data[4],
                (unsigned char)ifr.ifr_hwaddr.sa_data[5]);
            printf("mac: %s\n", mac);

        }
        else
        {
            printf("ioctl: %s [%s:%d]\n", strerror(errno), __FILE__, __LINE__);
            return -1;
        }
	
	 //ip address
        if (!ioctl(skfd, SIOCGIFADDR, &ifr))
        {

            strcpy(ip, inet_ntoa(((struct sockaddr_in*)&(ifr.ifr_addr))->sin_addr));
            printf("ip: %s\n", ip);


        }
        else
        {
            printf("ioctl: %s [%s:%d]\n", strerror(errno), __FILE__, __LINE__);
            return -1;
        }
	//broadcast
	if(!ioctl(skfd, SIOCGIFBRDADDR, &ifr))
	{
		strcpy(broadcast, inet_ntoa(((struct sockaddr_in *)&ifr.ifr_broadaddr)->sin_addr));
		printf("broadcast:%s\n", broadcast);

       }
       //netmask
       if(ioctl(skfd, SIOCGIFNETMASK, &ifr) != -1)
	{
		strcpy(netmask, inet_ntoa(((struct sockaddr_in *)&ifr.ifr_broadaddr)->sin_addr));
		printf("netmask:%s\n", netmask);
	}
}


int detect_mii(int skfd, char *ifname)
{
        struct ifreq ifr;
        u16 *data, mii_val;
        unsigned phy_id;

        /* Get the vitals from the interface. */
        strncpy(ifr.ifr_name, ifname, IFNAMSIZ);
        if (ioctl(skfd, SIOCGMIIPHY, &ifr) < 0) 
        {
                fprintf(stderr, "SIOCGMIIPHY on %s failed: %s\n", ifname,
                strerror(errno));
                (void) close(skfd);
                return 2;
        }

        data = (u16 *)(&ifr.ifr_data);
        phy_id = data[0];
        data[1] = 1;


        if (ioctl(skfd, SIOCGMIIREG, &ifr) < 0)
        {
                fprintf(stderr, "SIOCGMIIREG on %s failed: %s\n", ifr.ifr_name, strerror(errno));
                return 2;
        }

        mii_val = data[3];

        return(((mii_val & 0x0016) == 0x0004) ? 0 : 1);
}

int detect_ethtool(int skfd, char *ifname)
{
        struct ifreq ifr;
        struct ethtool_value edata;
        memset(&ifr, 0, sizeof(ifr));
        edata.cmd = ETHTOOL_GLINK;

        strncpy(ifr.ifr_name, ifname, sizeof(ifr.ifr_name)-1);
        ifr.ifr_data = (char *) &edata;

        if (ioctl(skfd, SIOCETHTOOL, &ifr) == -1) 
        {
                printf("ETHTOOL_GLINK failed: %s\n", strerror(errno));
                return  detect_mii(skfd, ifname);
        }

        return (edata.data ? 0 : 1);
}
int main(int argc, char **argv)
{
        int skfd = -1;
        char *ifname;
        int retval;

        if( argv[1] )
                ifname = argv[1];
        else{    
                printf("Usage:\n\t%s\tethname\n", argv[0]);
                exit(0);
            }
        /* Open a socket. */
        if (( skfd = socket( AF_INET, SOCK_DGRAM, 0 ) ) < 0 )
        {
                printf("socket error\n");
                exit(-1);
        }

	retval = detect_ethtool(skfd, ifname);
	printf("status:");
        if (retval == 2)
                printf("Could not determine status\n"); 

        if (retval == 1)
                printf("Link down\n");

        if (retval == 0)
	{
		printf("Link up\n");
		get_info(skfd, ifname);
	}
	close(skfd);
        return retval;
}
