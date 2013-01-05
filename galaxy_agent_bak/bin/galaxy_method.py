#!/usr/bin/env python
# - * - coding: utf-8 -*-

import time,os
import errno
import subprocess
import paramiko
from galaxy_agent_bak.bin.globaldef import blog,config

class Todo(object):
    def __init__(self):
        """
        Init config parameters
        """
        self.__tmp_dir = config.getGalaxy('tmp_dir')
        ##ssh log
        self.__ssh_log = config.getGalaxy('ssh_log')
        ##mysql
        self.__user = config.getMysql('user')
        self.__password = config.getMysql('password')
        #self.__socket = config.getMysql('socket')
        self.__mysql_bin = config.getMysql('mysql_bin_path')
        ##remote host
        self.__remote_user = config.getRemote('remote_user')
        self.__remote_port = int(config.getRemote('remote_port'))
        self.__remote_password = config.getRemote('remote_password')
        self.__remote_timeout = int(config.getRemote('remote_timeout'))
        ##rsync
        self.__rsync_bin = config.getRsync('rsync_bin')
        self.__rsync_port = int(config.getRsync('rsync_port'))
        self.__rsync_password_file = config.getRsync('rsync_password_file')
        self.__rsync_user = config.getRsync('rsync_user')
        #self.__rsync_module = config.getRsync('rsync_module')

        blog.info('Initialization parameter finish...')


    def __mysqldumpCommand(self,alias,host,port,database = None,table = None):
        """
        生成mysqldump备份数据库命令
        注：
            最好备份的表都是innodb存储引擎
        """

        #        key_set = set(args.keys())
        #       var_set = set(['pool_name','host_ip','mysql_port','db','tb','backup_host','backup_dir'])
        #        diff_set = var_set - key_set
        #        def DiffSet(arg1,arg2):
        #            diff_num = len(arg1)
        #            if diff_num == 0:
        #                return True
        #            elif diff_num ==1:
        #                if arg2 in arg1:
        #                    return True
        #
        #            return False

        #        if key_set.issubset(var_set) and DiffSet(diff_set,'tb'):
        back_time = time.strftime('%Y%m%d%H%M%S',time.localtime())
        back_file = alias + "-mysqldump-" + back_time
        dump_cmd = '%s%smysqldump -h%s -u%s -p%s -P%s --single-transaction --master-data=2 --flush-logs' % (
            self.__mysql_bin,os.sep,host,self.__user,self.__password,port)
        if database:
            if  database == 'all':
                dump_cmd = dump_cmd + ' ' + '--all-databases'
                back_file = back_file + '-all'
                blog.info("Start backup all database...")
            else:
                db_list = database.split(',')
                if len(db_list) == 1:
                    dump_cmd = dump_cmd + ' ' + db_list[0]
                    back_file = back_file + '-' + db_list[0]
                    blog.info("backup database: %s" % (str(db_list)))
                    if table:
                        tb_list = table.split(',')
                        blog.info("backup designated table: %s" % (str(tb_list)))
                        for i in range(0,len(tb_list)):
                            dump_cmd = dump_cmd + ' ' + tb_list[i]
                            back_file = back_file + '-' + tb_list[i]

                else:
                    for i in range(0,len(db_list)):
                        dump_cmd = dump_cmd + ' ' + db_list[i]
                        back_file = back_file + '-' + db_list[i]
                    blog.info("backup multiple databases: %s" % (str(db_list)))
        else:
            blog.error("Backup database can't for empty,such as:all or db1 or db2 etc.")
            return [None,None]

        return [dump_cmd,back_file]

        #            self.isBackupDirExist(args['backup_host'],args['backup_dir'])

    #            blog.info("Begin to use [MysqlDump] methods perform backup...")
    #            (e_res,file_name) = self.runBackupCommand(dump_cmd,back_file)
    #            if e_res:
    #            blog.info("Backup success...")
    #            else:
    #                blog.info("Backup failed...")
    #        else:
    #            blog.error("The client transfer parameter wrong!")
    #            return [None,None]

    def __isBackupDirExist(self,remote_host,backup_dir):
        """
        判断远程备份机备份目录是否存在
        参数1：远程备份机IP
        参数2：远程备份机存放备份的目录
        """

        def exists(path):
            """
            Return True if the remote path exists
            """
            try:
                sftpclient.stat(path)
            except IOError,e:
                if e.errno == errno.ENOENT:
                    return False
                raise
            else:
                return True

        backup_dir = backup_dir + os.sep + time.strftime('%Y%m%d',time.localtime())

        try:
            paramiko.util.log_to_file(self.__ssh_log)
            info = open(self.__ssh_log,'a')
            #open one ssh connect
            sshclient = paramiko.SSHClient()
            sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            sshclient.connect(remote_host,self.__remote_port,self.__remote_user,self.__remote_password,
                              timeout = self.__remote_timeout)
            #open one sftp tunnel
            sftpclient = sshclient.open_sftp()
            ##Detected on the backup machine backup directory exists
            if not exists(backup_dir):
                sftpclient.mkdir(new_backup_dir,mode = 0755)
                #executive command
            sftpclient.close()
            sshclient.close()
            info.close()
            return True

        except Exception,e:
            blog.error('ssh connect error: %s' % (e))
            return False

    def __initBackupDir(self):
        """
        初始化备份目录，按日期，比如：20121212
        如果占用则从1开始递增，比如20121212_1,20121212_2
        """
        backup_dir = self.__tmp_dir + os.sep + 'galaxy_backup' + time.strftime('%Y%m%d',time.localtime())
        try:
            if not os.path.isdir(backup_dir):
                os.mkdir(backup_dir)
        except Exception,e:
            blog.error("Create directory failure: ",e)
            return [False,None]
        return [True,backup_dir]

    def __runBackupCommand(self,basepath,backup_cmd,filename):
        """
        执行备份命令，备份的文件放到galaxy。cfg中tmp指定的目录下
        参数1：备份文件名称
        参数2：备份命令
        """
        try:
            if backup_cmd and filename:
                filename = basepath + os.sep + filename
                fp = file(filename,'a')
                proc = subprocess.Popen(backup_cmd,
                                        shell = True,
                                        stdout = fp,
                                        stderr = subprocess.PIPE)
                stderr_value = proc.communicate()[0]
                if proc.wait() == 0:
                    blog.info('Backup command executed successfully...')
                else:
                    blog.error('Backup command execution process encounters an error.\n%s' % (stderr_value))

                fp.close()
                file_size = int(os.stat(filename)[6])
                return [True,file_size]
            else:
                blog.error("Executive backup command is empty!!!")
                return [False,None]
        except Exception,e:
            blog.error("Backup command execution failed!!!\n%s" % (str(e)))
            return [False,None]

    def __backupFileCompression(self,basepath,compressfile,rmswitch = 0,mode = None):
        """
        备份完成后，备份文件压缩的方式gzip或bz2或不压缩
        参数mode：压缩方式
        参数backupfile：需要压缩的备份文件
        """
        import tarfile

        compress_mode = {1: 'targz',
                         2: 'tarbz2',
                         3: 'tar'
        }

        if compress_mode[mode] == 'targz':
            tar_filename = compressfile + '.tar.gz'
            tar_mode = 'w|gz'
        elif compress_mode[mode] == 'tarbz2':
            tar_filename = compressfile + '.tar.bz2'
            tar_mode = 'w|bz2'
        elif compress_mode[mode] == 'tar':
            tar_filename = compressfile + '.tar'
            tar_mode = 'w'
        else:
            blog.error("You specify of packing compression way does not exist or does not support...")
            return [False,None,0]

        workdir = os.path.dirname(__file__)
        if not workdir:
            workdir = os.getcwd()
        os.chdir(basepath)
        try:
            blog.info("Began to compression packing...")
            tar = tarfile.open(tar_filename,tar_mode)
            tar.add(compressfile)
            tar.close()
        except Exception,e:
            blog.error("Packing compression failure!!!")
            return [False,None,0]

        if int(rmswitch):
            os.remove(compressfile)
        tar_size = int(os.stat(tar_filename)[6])
        os.chdir(workdir)
        return [True,tar_filename,tar_size]


    def __rsyncStandbyServer(self,desthost,source,m,bandwidth = None):
        """
        使用rsync工具同步在备份存储机器上去
        参数1：目的主机IP
        参数2: 需同步的备份文件或备份目录
        参数3：备份存储机存储目录
        参数4：带宽限制
        """
        #source = basepath + os.sep + source
        if not os.path.exists(source):
            blog.error("Synchronous path does not exist.")

        rsync_cmd = "%s -auvzP --port=%d --password-file=%s " % (
            self.__rsync_bin,self.__rsync_port,self.__rsync_password_file)
        if bandwidth:
            rsync_cmd = rsync_cmd + "--bwlimit=%d " % (bandwidth)
        rsync_cmd = rsync_cmd + source + '%s@%s::%s' % (self.__rsync_user,desthost,m)
        p = subprocess.Popen(rsync_cmd,
                             shell = True,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE
        )
        (out,err) = p.communicate()
        if out:
            blog.info(out.rstrip())
        if err:
            blog.error(err.rstrip())
            return False
        return True

    def mysqldump(self,**args):
        (a_status,bpath) = self.__initBackupDir()
        if a_status:
            (dumpcmd,backfilename) = self.__mysqldumpCommand(args['HostAlias'],args['HostIp'],args['HostPort'],
                                                             args['DatabaseList'],args['TableList'])
            (b_status,fsize) = self.__runBackupCommand(bpath,dumpcmd,backfilename)
            if b_status:
                blog.info("Backup success!!!")
                if int(args['CompressType']) in range(1,4):
                    (c_status,tfile,tsize) = self.__backupFileCompression(bpath,backfilename,args['RmSwitch'],
                                                                          args['CompressType'])
                    if c_status:
                        blog.info("Compression success...")
                        #insert
                    else:
                        blog.info("Compression failure...")
                else:
                    blog.info("Compression type is not exists...")
                    #insert
            else:
                blog.error("Backup failure!!!")
                #insert
        else:
            blog.error("Backup failure!!!")
            #insert

    def mysqldumpRsync(self,**args):
        (a_status,bpath) = self.__initBackupDir()
        if a_status:
            (dumpcmd,backfilename) = self.__mysqldumpCommand(args['HostAlias'],args['HostIp'],args['HostPort'],
                                                             args['DatabaseList'],args['TableList'])
            (b_status,fsize) = self.__runBackupCommand(bpath,dumpcmd,backfilename)
            if b_status:
                blog.info("Backup success!!!")
                if int(args['CompressType']) in range(1,4):
                    (c_status,backfilename,tsize) = self.__backupFileCompression(bpath,backfilename,args['RmSwitch'],
                                                                                 args['CompressType'])
                    if c_status:
                        blog.info("Compression success...")
                        #insert
                    else:
                        blog.info("Compression failure...")
                else:
                    blog.info("Compression type is not exists...")
                    #insert
                blog.info("rsync sync start...")
                d_status = self.__rsyncStandbyServer(args['StorageIP'],bpath,args['RsyncModule'],args['BandWidth'])
                if d_status:
                    blog.info("rsync sync success...")
                else:
                    blog.error("rsync sync failure..")
            else:
                blog.error("Backup failure!!!")
                #insert
        else:
            blog.error("Backup failure!!!")
            #insert

    def error(self,args):
        return 'not function!'


Method = Todo()

if __name__ == '__main__':
    dump_args = {"StorageIP": '172.20.150.87',
                 'RsyncModule': '/backup',
                 'HostAlias': 'test1',
                 'BandWidth': 0,
                 'CompressType': 1,
                 'RmSwitch': 0,
                 'HostIp': '172.20.150.3',
                 'HostPort': 3306,
                 'DatabaseList': 'valentine0606',
                 'TableList': 'ms_user,ms_retailer'
    }
    Method.mysqldump(**dump_args)
