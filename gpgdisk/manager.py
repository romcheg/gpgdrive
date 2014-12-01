# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import subprocess

import llfuse

from gpgdisk import utils


class MountManager(llfuse.Operations):
    def init(self):
        '''Initialize FS

        Attaches required amount of RAM as a devise and
        initializes GPG.

        '''
        self.volume_label = 'GPG Disk'

        cmd = 'hdiutil attach -nomount ram://1048576'
        ret_code, stdout, stderr = utils.execute(cmd)

        if ret_code != 0:
            raise Exception('Attaching RAM failed. %s' % stderr)

        self.device_path = stdout.strip()

        cmd = 'diskutil erasevolume HFS+ "{label}" {dev}'
        cmd = cmd.format(dev=self.device_path, label=self.volume_label)

        ret_code, stdout, stderr = utils.execute(cmd)

        self.mount_path = '/Volumes/%s' % self.volume_label

    def destroy(self):
        '''Clean up operations.

        Unmounts volume and detaches RAM disk.

        '''

        cmd = 'diskutil umount %s' % self.volume_label
        utils.execute(cmd)

        cmd = 'hdiutil detach %s' % self.device_path
        utils.execute(cmd)

    def lookup(self, parent_inode, name):
        '''Look up a directory entry by name and get its attributes.

        If the entry *name* does not exist in the directory with inode
        *parent_inode*, this method must raise `FUSEError` with an
        errno of `errno.ENOENT`. Otherwise it must return an
        `EntryAttributes` instance.

        Once an inode has been returned by `lookup`, `create`,
        `symlink`, `link`, `mknod` or `mkdir`, it must be kept by the
        file system until it receives a `forget` request for the
        inode. If `unlink` or `rmdir` requests are received prior to
        the `forget` call, they are expect to remove only the
        directory entry for the inode and defer removal of the inode
        itself until the `forget` call.

        The file system must be able to handle lookups for :file:`.`
        and :file:`..`, no matter if these entries are returned by
        `readdir` or not.
        '''

        raise FUSEError(errno.ENOSYS)

    def forget(self, inode_list):
        '''Notify about inodes being removed from the kernel cache

        *inode_list* is a list of ``(inode, nlookup)`` tuples. This
        method is called when the kernel removes the listed inodes
        from its internal caches. *nlookup* is the number of times
        that the inode has been looked up by calling either of the
        `lookup`, `create`, `symlink`, `mknod`, `link` or `mkdir`
        methods.

        The file system is expected to keep track of the number of
        times an inode has been looked up and forgotten. No request
        handlers other than `lookup` will be called for an inode with
        a lookup count of zero.

        If the lookup count reaches zero after a call to `forget`, the
        file system is expected to check if there are still directory
        entries referring to this inode and, if not, delete the inode
        itself.

        If the file system is unmounted, it will may not receive
        `forget` calls for inodes that are still cached. The `destroy`
        method may be used to clean up any remaining inodes for which
        no `forget` call has been received.
        '''

        pass

    def getattr(self, inode):
        '''Get attributes for *inode*

        This method should return an `EntryAttributes` instance with
        the attributes of *inode*. The
        `~EntryAttributes.entry_timeout` attribute is ignored in this
        context.
        '''

        raise FUSEError(errno.ENOSYS)

    def setattr(self, inode, attr):
        '''Change attributes of *inode*

        *attr* is an `EntryAttributes` instance with the new
        attributes. Only the attributes `~EntryAttributes.st_size`,
        `~EntryAttributes.st_mode`, `~EntryAttributes.st_uid`,
        `~EntryAttributes.st_gid`, `~EntryAttributes.st_atime` and
        `~EntryAttributes.st_mtime` are relevant. Unchanged attributes
        will have a value `None`.

        The method should return a new `EntryAttributes` instance
        with the updated attributes (i.e., all attributes except for
        `~EntryAttributes.entry_timeout` should be set).
        '''

        raise FUSEError(errno.ENOSYS)

    def readlink(self, inode):
        '''Return target of symbolic link

        The return value must have type `bytes`.
        '''

        raise FUSEError(errno.ENOSYS)

    def mknod(self, parent_inode, name, mode, rdev, ctx):
        '''Create (possibly special) file

        *ctx* will be a `RequestContext` instance. The method must
        return an `EntryAttributes` instance with the attributes of
        the newly created directory entry.

        Once an inode has been returned by `lookup`, `create`,
        `symlink`, `link`, `mknod` or `mkdir`, it must be kept by the
        file system until it receives a `forget` request for the
        inode. If `unlink` or `rmdir` requests are received prior to
        the `forget` call, they are expect to remove only the
        directory entry for the inode and defer removal of the inode
        itself until the `forget` call.
        '''

        raise FUSEError(errno.ENOSYS)

    def mkdir(self, parent_inode, name, mode, ctx):
        '''Create a directory

        *ctx* will be a `RequestContext` instance. The method must
        return an `EntryAttributes` instance with the attributes of
        the newly created directory entry.

        Once an inode has been returned by `lookup`, `create`,
        `symlink`, `link`, `mknod` or `mkdir`, it must be kept by the
        file system until it receives a `forget` request for the
        inode. If `unlink` or `rmdir` requests are received prior to
        the `forget` call, they are expect to remove only the
        directory entry for the inode and defer removal of the inode
        itself until the `forget` call.
        '''

        raise FUSEError(errno.ENOSYS)

    def unlink(self, parent_inode, name):
        '''Remove a (possibly special) file

        If the file system has received a `lookup`, but no `forget`
        call for this file yet, `unlink` is expected to remove only
        the directory entry and defer removal of the inode with the
        actual file contents and metadata until the `forget` call is
        received.

        Note that an unlinked file may also appear again if it gets a
        new directory entry by the `link` method.
        '''

        raise FUSEError(errno.ENOSYS)

    def rmdir(self, inode_parent, name):
        '''Remove a directory

        If the file system has received a `lookup`, but no `forget`
        call for this file yet, `unlink` is expected to remove only
        the directory entry and defer removal of the inode with the
        actual file contents and metadata until the `forget` call is
        received.
        '''

        raise FUSEError(errno.ENOSYS)

    def symlink(self, inode_parent, name, target, ctx):
        '''Create a symbolic link

        *ctx* will be a `RequestContext` instance. The method must
        return an `EntryAttributes` instance with the attributes of
        the newly created directory entry.

        Once an inode has been returned by `lookup`, `create`,
        `symlink`, `link`, `mknod` or `mkdir`, it must be kept by the
        file system until it receives a `forget` request for the
        inode. If `unlink` or `rmdir` requests are received prior to
        the `forget` call, they are expect to remove only the
        directory entry for the inode and defer removal of the inode
        itself until the `forget` call.
        '''

        raise FUSEError(errno.ENOSYS)

    def rename(self, inode_parent_old, name_old, inode_parent_new, name_new):
        '''Rename a directory entry

        If *name_new* already exists, it should be overwritten.

        If the file system has received a `lookup`, but no `forget`
        call for the file that is about to be overwritten, `rename` is
        expected to only overwrite the directory entry and defer
        removal of the old inode with the its contents and metadata
        until the `forget` call is received.
        '''

        raise FUSEError(errno.ENOSYS)

    def link(self, inode, new_parent_inode, new_name):
        '''Create a hard link.

        The method must return an `EntryAttributes` instance with the
        attributes of the newly created directory entry.

        Once an inode has been returned by `lookup`, `create`,
        `symlink`, `link`, `mknod` or `mkdir`, it must be kept by the
        file system until it receives a `forget` request for the
        inode. If `unlink` or `rmdir` requests are received prior to
        the `forget` call, they are expect to remove only the
        directory entry for the inode and defer removal of the inode
        itself until the `forget` call.
        '''

        raise FUSEError(errno.ENOSYS)

    def open(self, inode, flags):
        '''Open a file.

        *flags* will be a bitwise or of the open flags described in
        the :manpage:`open(2)` manpage and defined in the `os` module
        (with the exception of ``O_CREAT``, ``O_EXCL``, ``O_NOCTTY``
        and ``O_TRUNC``)

        This method should return an integer file handle. The file
        handle will be passed to the `read`, `write`, `flush`, `fsync`
        and `release` methods to identify the open file.
        '''

        raise FUSEError(errno.ENOSYS)

    def read(self, fh, off, size):
        '''Read *size* bytes from *fh* at position *off*

        This function should return exactly the number of bytes
	requested except on EOF or error, otherwise the rest of the
	data will be substituted with zeroes.
        '''

        raise FUSEError(errno.ENOSYS)

    def write(self, fh, off, buf):
        '''Write *buf* into *fh* at *off*

        This method should return the number of bytes written. If no
        error occured, this should be exactly :samp:`len(buf)`.
        '''

        raise FUSEError(errno.ENOSYS)

    def flush(self, fh):
        '''Handle close() syscall.

        This method is called whenever a file descriptor is closed. It
        may be called multiple times for the same open file (e.g. if
        the file handle has been duplicated).

        If the file system implements locking, this method must clear
        all locks belonging to the file handle's owner.
        '''

        raise FUSEError(errno.ENOSYS)

    def release(self, fh):
        '''Release open file

        This method will be called when the last file descriptor of
        *fh* has been closed. Therefore it will be called exactly once
        for each `open` call.
        '''

        raise FUSEError(errno.ENOSYS)

    def fsync(self, fh, datasync):
        '''Flush buffers for open file *fh*

        If *datasync* is true, only the file contents should be
        flushed (in contrast to the metadata about the file).
        '''

        raise FUSEError(errno.ENOSYS)

    def opendir(self, inode):
        '''Open a directory.

        This method should return an integer file handle. The file
        handle will be passed to the `readdir`, `fsyncdir`
        and `releasedir` methods to identify the directory.
        '''

        raise FUSEError(errno.ENOSYS)


    def readdir(self, fh, off):
        '''Read directory entries

        This method should return an iterator over the contents of
        directory *fh*, starting at the entry identified by *off*.
        Directory entries must be of type `bytes`.

        The iterator must yield tuples of the form :samp:`({name}, {attr},
        {next_})`, where *attr* is an `EntryAttributes` instance and
        *next_* gives an offset that can be passed as *off* to start
        a successive `readdir` call at the right position.

        Iteration may be stopped as soon as enough elements have been
        retrieved. The method should be prepared for this case.

        If entries are added or removed during a `readdir` cycle, they
        may or may not be returned. However, they must not cause other
        entries to be skipped or returned more than once.

        :file:`.` and :file:`..` entries may be included but are not
        required.
        '''

        raise FUSEError(errno.ENOSYS)

    def releasedir(self, fh):
        '''Release open directory

        This method must be called exactly once for each `opendir` call.
        '''

        raise FUSEError(errno.ENOSYS)

    def fsyncdir(self, fh, datasync):
        '''Flush buffers for open directory *fh*

        If *datasync* is true, only the directory contents should be
        flushed (in contrast to metadata about the directory itself).
        '''

        raise FUSEError(errno.ENOSYS)

    def statfs(self):
        '''Get file system statistics

        The method is expected to return an appropriately filled
        `StatvfsData` instance.
        '''

        raise FUSEError(errno.ENOSYS)


