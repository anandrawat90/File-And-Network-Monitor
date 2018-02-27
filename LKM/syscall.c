#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/errno.h>
#include <linux/types.h>
#include <asm/current.h>
#include <linux/sched.h>
#include <linux/syscalls.h>
#include <linux/slab.h>
#include <linux/socket.h>
#include <linux/in.h>
#include <net/sock.h>
#include <linux/file.h>
#include <linux/net.h>
#include <linux/proc_fs.h>
#include <asm/uaccess.h>
#include <linux/stat.h>


#define LICENSE "GPL"
#define DESCRIPTION "CSc 239 Project"
#define AUTHOR "Anand Rawat"
#define MAX_NUMBER_FILES 100
#define MAX_FILE_NAME 100
#define BLOCK_FILE_CONFIG "/home/anand/LKM/file_ds"
#define MAX_LEN       4096

MODULE_LICENSE(LICENSE);
MODULE_DESCRIPTION(DESCRIPTION);
MODULE_AUTHOR(AUTHOR);

/** Original System Calls **/
asmlinkage long (*original_open)(const char *,int,int);
asmlinkage int (*original_close)(unsigned int);
asmlinkage size_t (*original_read)(int, char *, size_t);
asmlinkage int (*original_write)(unsigned int, const char __user*, size_t);

/**Hacked System Calls **/
asmlinkage long our_sys_open(const char *filename,int flags,int mode);

/** Utility Functions **/
ssize_t read_proc(struct file *filp,char *buf,size_t count,loff_t *offp );
ssize_t write_proc(struct file *filp,const char *buf,size_t count,loff_t *offp);
void print_time(char []);
int get_username(char *);
void write_file(char *,char *);
int init_file_ds(void);

/** Constants and data structures **/
char USER_NAME[7]="USRNAM\0";
char USER_TIME[11]="###:##:###";
char log_filename[11]="##_##_####";
const char PROC_FILE_PATH[13] = "Project_Logs";
/*assign the system  call  table  base  address  to  syscall_table*/
unsigned long *syscall_table = (unsigned long *) 0xffffffff81a001c0;
/*static int write_index;
static int read_index;*/
int len, temp;
char *msg;
struct file_operations proc_fops =
{
read:
    read_proc,
write:
    write_proc
};

char BLOCKED_FILE_LIST[MAX_NUMBER_FILES][MAX_FILE_NAME];
unsigned int NUMBER_OF_FILES;


ssize_t read_proc(struct file *filp,char *buf,size_t count,loff_t *offp )
{
    if(count>temp)
    {
        count=temp;
    }
    temp=temp-count;
    copy_to_user(buf,msg, count);
    if(count==0)
        temp=len;

    return count;

    /*int len;
    /*if(read_index >= write_index)
    {
    	read_index=0;
    	return 0;
    }
    len =
    if(len!=0)
    	read_index += count - len;

    return count;
    copy_to_user(buf,msg, write_index+1);
    return write_index+1;
    int len;
    if (off > 0)
    {
    	*eof = 1;
    	return 0;
    }

    if (read_index >= write_index)
    	read_index = 0;

    len = sprintf(page, "%s\n", &msg[read_index]);
    read_index += len;
    return len;*/
}

ssize_t write_proc(struct file *filp,const char *buf,size_t count,loff_t *offp)
{
    /*int capacity = (MAX_LEN - write_index)+1;
    if (count > capacity)
    {
    	printk	(KERN_INFO "No space to write in Project_logs!\n");
    	return -1;
    }
    if (copy_from_user( &msg[write_index], buf, count ))
    {
    	return -2;
    }

    write_index += count;
    msg[write_index-1] = '\0';
    return count;*/
    copy_from_user(msg,buf,count);
    len=count;
    temp=len;
    return count;
}

asmlinkage long our_sys_open(const char *filename,int flags,int mode)
{
    //printk(KERN_INFO "file - %s",filename);
    char fileinfo_buff[200], path[120];
    int ret = 0, i = 0;

    int found = 0;
    while(i < NUMBER_OF_FILES)
    {
        found = strcmp(filename, BLOCKED_FILE_LIST[i]);
        if(found == 0)
        {
            printk(KERN_INFO"The matched filename is %s\n",filename);
            break;
        }
        i++;
    }

    if(found!=0)
    {
        //printk(KERN_INFO "Allowing %d access %s",found,filename);
        return (*original_open)(filename, flags, mode);
    }

    print_time(USER_TIME);
    // Get Current Time
    strcpy(fileinfo_buff,USER_TIME+1);// Store Time in Log Array
    ret=get_username(USER_NAME);
    printk(KERN_ALERT "\n get_username retrived %s",USER_NAME);
    if(ret < 0)
    {
        printk(KERN_ALERT "\n error in get_username");
    }
    else
    {
        strcat(fileinfo_buff,USER_NAME);
    }
    if(flags & (O_WRONLY|O_APPEND))
    {
        strcat(fileinfo_buff,"#WR#");
    }
    else
    {
        strcat(fileinfo_buff,"#RD#");
    }
    strcat(fileinfo_buff,filename);
    strcat(fileinfo_buff,"\n");
    strcpy(path,"/proc/Project_Logs");
    //strcat(path,PROC_FILE_PATH);
    if((USER_NAME[0]>='A' && USER_NAME[0]<='Z')||(USER_NAME[0]>='a' && USER_NAME[0]<='z'))
    {
        write_file(fileinfo_buff,path);
    }
    else
    {
        printk("missing write in file %s\n",filename);
    }
    return -EACCES; /* call the original function */
}

void create_new_proc_entry(void)
{
    proc_create(PROC_FILE_PATH,O_RDWR|O_APPEND|O_LARGEFILE,NULL,&proc_fops);
    msg=kmalloc(10 * sizeof(char),GFP_KERNEL);
}

int my_init(void)
{
    create_new_proc_entry();
    int fd;
    printk(KERN_INFO "I am Hacking the system call\n");
    write_cr0 (read_cr0 () & (~ 0x10000));
    /*  Save  the  original system calls addresses, so we can call the original system functions */
    original_read=(void *)syscall_table[__NR_read];
    original_write= (void *)syscall_table[__NR_write];
    original_close=(void *)syscall_table[__NR_close];
    original_open=(void *)syscall_table[__NR_open];

    /* Hack the table with our implemention */
    /*  change  the  system  call base table entry of sys_open to our_sys_open function */
    syscall_table[__NR_open]  =  (void  *) our_sys_open;
    /* Reset the write protect bits*/
    write_cr0 (read_cr0 () | 0x10000);
    int i = init_file_ds();
    printk(KERN_ALERT"Configuration: %s\n",BLOCK_FILE_CONFIG);
    for(i = 0; i < NUMBER_OF_FILES; i++)
        printk(KERN_ALERT" Entry No. %d is %s\n", i, BLOCKED_FILE_LIST[i]);
    return 0;
    //			while ((c = getc(file)) != EOF)
    //		        putchar(c);
}

void my_exit(void)
{
    /* This check is must because if this is the case then somebody else also played with syscall_table's sys_open */
    if(syscall_table[__NR_open] != our_sys_open)
    {
        printk(KERN_ALERT "Somebody else also played with system call table\n");
        printk(KERN_ALERT "The system may be left in unstable state\n");
    }
    write_cr0 (read_cr0 () & (~ 0x10000));
    syscall_table[__NR_open] = (void *)original_open;
    write_cr0 (read_cr0 () | 0x10000);
    /*  assign the original address for system integrity */
    kfree(msg);
    remove_proc_entry(PROC_FILE_PATH,NULL);
    printk(KERN_INFO "Leaving the kernel\n");
}

/** Utility Functions **/
// Used for Getting the name
void print_time(char char_time[])
{
    struct timeval my_tv;
    int sec, hr, min, tmp1, tmp2;
    int days,years,days_past_currentyear;
    int i=0,month=0,date=0;
    unsigned long get_time;
    char_time[11]="#00:00:00#";
    do_gettimeofday(&my_tv);                    // GetSystem Time From Kernel Mode
    get_time = my_tv.tv_sec;                   // Fetch System time in Seconds
// printk(KERN_ALERT "\n %ld",get_time);
    get_time = get_time + 43200;
    sec = get_time % 60;                       // Convert into Seconds
    tmp1 = get_time / 60;
    min = tmp1 % 60;                          // Convert into Minutes
    tmp2 = tmp1 / 60;
    hr = (tmp2+4) % 24;                      // Convert into Hours
    hr=hr+1;
    char_time[1]=(hr/10)+48;                // Convert into Char from Int
    char_time[2]=(hr%10)+48;
    char_time[4]=(min/10)+48;
    char_time[5]=(min%10)+48;
    char_time[7]=(sec/10)+48;
    char_time[8]=(sec%10)+48;
    char_time[10]='\0';
    /* calculating date from time in seconds */
    days = (tmp2+4)/24;
    days_past_currentyear = days % 365;
    years = days / 365;
    for(i=1970; i<=(1970+years); i++)
    {
        if ((i % 4) == 0)
            days_past_currentyear--;
    }
    if((1970+years % 4) != 0)
    {
        if(days_past_currentyear >=1 && days_past_currentyear <=31)
        {
            month=1; //JAN
            date = days_past_currentyear;
        }
        else if (days_past_currentyear >31 && days_past_currentyear <= 59)
        {
            month = 2;
            date = days_past_currentyear - 31;
        }
        else if (days_past_currentyear >59 && days_past_currentyear <= 90)
        {
            month = 3;
            date = days_past_currentyear - 59;
        }
        else if (days_past_currentyear >90 && days_past_currentyear <= 120)
        {
            month = 4;
            date = days_past_currentyear - 90;
        }
        else if (days_past_currentyear >120 && days_past_currentyear <= 151)
        {
            month = 5;
            date = days_past_currentyear - 120;
        }
        else if (days_past_currentyear >151 && days_past_currentyear <= 181)
        {
            month = 6;
            date = days_past_currentyear - 151;
        }
        else if (days_past_currentyear >181 && days_past_currentyear <= 212)
        {
            month = 7;
            date = days_past_currentyear - 181;
        }
        else if (days_past_currentyear >212 && days_past_currentyear <= 243)
        {
            month = 8;
            date = days_past_currentyear - 212;
        }
        else if (days_past_currentyear >243 && days_past_currentyear <= 273)
        {
            month = 9;
            date = days_past_currentyear - 243;
        }
        else if (days_past_currentyear >273 && days_past_currentyear <= 304)
        {
            month = 10;
            date = days_past_currentyear - 273;
        }
        else if (days_past_currentyear >304 && days_past_currentyear <= 334)
        {
            month = 11;
            date = days_past_currentyear - 304;
        }
        else if (days_past_currentyear >334 && days_past_currentyear <= 365)
        {
            month = 12;
            date = days_past_currentyear - 334;
        }
        // printk(KERN_ALERT "month=%d date=%d year=%d",month,date,(1970+years));
    }
// for leap years..
    else
    {
        if(days_past_currentyear >=1 && days_past_currentyear <=31)
        {
            month=1; //JAN
            date = days_past_currentyear;
        }
        else if (days_past_currentyear >31 && days_past_currentyear <= 60)
        {
            month = 2;
            date = days_past_currentyear - 31;
        }
        else if (days_past_currentyear >60 && days_past_currentyear <= 91)
        {
            month = 3;
            date = days_past_currentyear - 60;
        }
        else if (days_past_currentyear >91 && days_past_currentyear <= 121)
        {
            month = 4;
            date = days_past_currentyear - 91;
        }
        else if (days_past_currentyear >121 && days_past_currentyear <= 152)
        {
            month = 5;
            date = days_past_currentyear - 121;
        }
        else if (days_past_currentyear >152 && days_past_currentyear <= 182)
        {
            month = 6;
            date = days_past_currentyear - 152;
        }
        else if (days_past_currentyear >182 && days_past_currentyear <= 213)
        {
            month = 7;
            date = days_past_currentyear - 182;
        }
        else if (days_past_currentyear >213 && days_past_currentyear <= 244)
        {
            month = 8;
            date = days_past_currentyear - 213;
        }
        else if (days_past_currentyear >244 && days_past_currentyear <= 274)
        {
            month = 9;
            date = days_past_currentyear - 244;
        }
        else if (days_past_currentyear >274 && days_past_currentyear <= 305)
        {
            month = 10;
            date = days_past_currentyear - 274;
        }
        else if (days_past_currentyear >305 && days_past_currentyear <= 335)
        {
            month = 11;
            date = days_past_currentyear - 305;
        }
        else if (days_past_currentyear >335 && days_past_currentyear <= 366)
        {
            month = 12;
            date = days_past_currentyear - 335;
        }
// printk(KERN_ALERT "\nmonth=%d date=%d year=%d",month,date,(1970+years));
    }
    log_filename[0]=(month/10)+48;                //Convert into Char from Int
    log_filename[1]=(month%10)+48;
    log_filename[3]=(date/10)+48;
    log_filename[4]=(date%10)+48;
    tmp1 = ((1970+years) % 10) + 48;
    log_filename[9]= tmp1;
    tmp1 = (1970+years)/ 10;
    tmp2 = tmp1 % 10;
    log_filename[8]= tmp2 + 48;
    tmp1 = tmp1 / 10;
    tmp2 = tmp1 % 10;
    log_filename[7]=tmp2 + 48;
    tmp1 = tmp1 / 10;
    log_filename[6]= tmp1+48;
    log_filename[10]='\0';
}

int get_username(char *name)
{
    char *read_buff,*path,*tk,*tk1;
    char tmp_buff[12];
    int fd,ret,my_i,error=0;
    mm_segment_t old_fs_username;
    memset(name,0,7);
    read_buff = (char *)kmalloc(2024,GFP_ATOMIC);
    if(!read_buff)
    {
        printk(KERN_ALERT "\n kmalloc error");
        return -1;
    }

    path = (char *)kmalloc(120,GFP_ATOMIC);
    if(!path)
    {
        printk(KERN_ALERT "\n kmalloc error for path");
        return -1;
    }

    strcpy(path,"/proc/");
    snprintf(tmp_buff,12,"%u",current->pid);
    strcat(path,tmp_buff);
    strcat(path,"/environ");

    old_fs_username = get_fs();
    set_fs(KERNEL_DS);

    fd = original_open(path, O_RDONLY|O_LARGEFILE,0700); // Original Stolenaddress of sys_open system call
    if(fd < 0)
    {
        printk(KERN_ALERT "\n error in sys_open in get_username function");
        error = -1;
        goto my_error;
    }
    else
    {
        if((ret=original_read(fd,read_buff,2024)) < 0)
        {
            printk(KERN_ALERT "\nError in sys_read in get_username function");
            error = -1;
            goto my_error;
        }
        else
        {
            for(my_i=0; my_i<ret; my_i++)
            {
                if(read_buff[my_i] == '\0')
                    read_buff[my_i] = ' ';
            }
            read_buff[ret-1] = '\0';

            tk = strstr(read_buff,"USER=");
            //printk("\ntk is %s",tk);
            if(!tk)
            {
                printk(KERN_ALERT "Error in strstr");
                error = -1;
                goto my_error;
            }
            tk1 = strsep(&tk," ");
            tk1 = tk1+5;
            strncpy(name,tk1,strlen(tk1));
            //printk("\nname is %s",name);
        }
        original_close(fd);
    }
my_error:
    set_fs(old_fs_username);
    kfree(read_buff);
    kfree(path);
    return error;
}

void write_file(char *buffer,char *path)
{
    mm_segment_t old_fs;
    int fd;
    old_fs=get_fs();
    set_fs(KERNEL_DS);
    fd = original_open(path, O_WRONLY|O_APPEND,0777);
    // printk(cd " %d %s",fd,buffer);

    if(fd >= 0)
    {
        original_write(fd,buffer,strlen(buffer));
        original_close(fd);
        printk("Writing into %s with %s\n", path, buffer);
    }
    else
    {
        printk(KERN_ALERT "\n Errro in write_file() while opening a file with fd =%d",fd);
    }
    set_fs(old_fs);
    return;
}
//pases file and populates the data structure
int init_file_ds(void)
{
    mm_segment_t old_fs;
    old_fs= get_fs();
    set_fs(KERNEL_DS);

    char c;
    int current_index = 0;
    int current_file_index = 0;

    int fd = original_open(BLOCK_FILE_CONFIG, O_RDWR|O_LARGEFILE,0700);
    printk(KERN_ALERT"file decriptor: %d\n",fd);
    if(fd < 0)
        return -1;

    while(1)
    {
        ssize_t temp = original_read(fd, &c, 1);
        if(temp == 0)	//finish parsing for this file
            break;
        else if(c == '\n') 	//finish parsing one entry
        {
            BLOCKED_FILE_LIST[current_file_index][current_index] = '\0';
            current_file_index++;
            current_index = 0;
        }
        else BLOCKED_FILE_LIST[current_file_index][current_index++] = c;

    }
    set_fs(old_fs);
    NUMBER_OF_FILES = current_file_index;
    return 0;
}

/** Utility Functions **/

module_init(my_init);
module_exit(my_exit);
