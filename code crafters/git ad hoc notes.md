### process.argv
The `process.argv` property returns an array containing the command-line arguments passed when the Node.js process was launched. The first element will be [`process.execPath`]  The second element will be the path to the JavaScript file being executed. The remaining elements will be any additional command-line arguments.
### .git folder internals
[What is in that .git directory? (meain.io)](https://blog.meain.io/2023/what-is-in-dot-git/)
### git objects
- Blobs 
    - These are used to store file data.
    - Blobs only store the contents of a file, not its name or permissions.
    - Each Git Blob is stored as a separate file in the `.git/objects` directory. The file contains a header and the contents of the blob object, compressed using Zlib.
    - The format of a blob object file looks like this (after Zlib decompression):
```
  blob <size>\0<content>
```
- `<size>` is the size of the content (in bytes)
- `\0` is a null byte
- `<content>` is the actual content of the file
    For example, if the contents of a file are `hello world`, the blob object file would look like this (after Zlib decompression):
```
  blob 11\0hello world
```
- Trees 
    - These are used to store directory structures.
    - The information stored can include things like what files/directories are in a tree, their names and permissions.
- Commits 
    - These are used to store commit data.
    - The information stored can include things like the commit message, author, committer, parent commit(s) and more.
### git cat-file
```bash
git cat-file -t 4c5b58f323d7b459664b5d3fb9587048bb0296deblob$
git cat-file -s 4c5b58f323d7b459664b5d3fb9587048bb0296de9$ 
git cat-file -p 4c5b58f323d7b459664b5d3fb9587048bb0296demeain.io
```
	-t for type
	-s for size
	-p for content
### hashing and zlib compression
calculating the SHA1
```ts
import crypto from 'crypto';  
  
export function calculateSha1(buffer: Buffer): string {  
  const hash = crypto.createHash('sha1');  
  hash.update(buffer);  
  return hash.digest('hex');  
}
```
zlib Compression and Rarefaction
```ts
import zlib from 'zlib';
const bufferToWrite = fs.readFileSync(compressedFilePath);
const compressedBuffer = zlib.deflateSync(bufferToWrite);
const buffer = zlib.unzipSync(compressedBuffer);
```
### git ls-tree command
used to inspect tree object
a tree object is made up of entries
each entry includes
- a sha hash that point to a blob or tree object
	- if the entry is a file it points to a blob
	- if the entry is a dir it points to another tree object
- name of the file/directory
- mode of the file/directory
	- mode is basically different kinds of permissions 
	- for files we have three options
		- `100644` (regular file)
		- `100755` (executable file)
		- `120000` (symbolic link)
```ts
export function getFileMode(stats: fs.Stats): string {  
  if (stats.isSymbolicLink()) {  
    return '120000'; // symbolic link  
  } else if (stats.mode & 0o111) {  
    return '100755'; // executable file  
  } else {  
    return '100644'; // regular file  
  }  
}
getFileMode(fs.statSync(filePath));
```
	- for dirs the value is `40000`

- For example, if you had a directory structure like this:
```
  your_repo/
    - file1
    - dir1/
      - file_in_dir_1
      - file_in_dir_2
    - dir2/
      - file_in_dir_3
```
The entries in the tree object would look like this:, this is also the output of the git ls-tree command
```
  40000 dir1 <tree_sha_1>
  40000 dir2 <tree_sha_2>
  100644 file1 <blob_sha_1>
```
dir1 and dir 2 are tree objects as well and if we inspect them we will find the files in them
the output is alphabetically sorted
> gist ls-tree --name-only <tree_sha>

this outputs only the name of the files

git cat-file -p tree_sha
the format of the tree object file is like so
```
tree <size>\0
<mode> <name>\0<sha>
<mode> <name>\0<sha>
```
the actual out put doesnt have a new line character

### git write-tree
creates a tree object from the current state of the staging area
outputs the sha of the tree object
iterate over the folder structure in the staging area
- if the entry is a file create a blob object and record its sha
- if directory create a tree object and record its sha

### git index
based on 
- [pygit: Just enough of a Git client to create a repo, commit, and push itself to GitHub (benhoyt.com)](https://benhoyt.com/writings/pygit/#committing)
- [pygit/pygit.py at master · benhoyt/pygit (github.com)](https://github.com/benhoyt/pygit/blob/master/pygit.py#L28)

Also known as staging area
its just a list of file entries ordered by their path
each entry contains the following things
```javascript
[
    'ctime_s', 'ctime_n', 'mtime_s', 'mtime_n', 'dev', 'ino', 'mode', 'uid', 'gid', 'size', 'sha1', 'flags', 'path',
]
```

the index is a single file at .git/index and the data is stored in a binary format
the first 12 bytes of the index are the header, the last 20 are a SHA-1 hash of the index
the bytes in between are the index entries
each index entry is 62 bytes + length of the path and some padding
the index lists are the files in the current tree not just the files being staged
```
100644 33b1de85e344e8b470589e51d7db75e825497e9b 0	not/file2/file1.txt
100644 97b93ecf83935d51486a98b42b5dd8985f60336d 0	path/to/file2.txt
```
this is what the index might look like

so when we create a commit from this it will look like so
```
tree <SHA-1 of root tree>
parent <SHA-1 of parent commit, if any>
author <author name> <author email> <timestamp>
committer <committer name> <committer email> <timestamp>

Add initial files
```
it will contain the single tree sha that will be the common root tree sha for all the files in the index
if we do 
>`git cat-file -p <SHA-1 of root tree>`

```
040000 tree <SHA-1 of a tree>    a
040000 tree <SHA-1 of c tree>    c
```

so the write-tree function must filter for only the paths in the index file
create a function responsible to read the index file
```ts
import * as fs from 'fs';
import * as path from 'path';
import * as crypto from 'crypto';

interface IndexEntry {
    ctimeSeconds: number;
    ctimeNanoseconds: number;
    mtimeSeconds: number;
    mtimeNanoseconds: number;
    dev: number;
    ino: number;
    mode: number;
    uid: number;
    gid: number;
    fileSize: number;
    sha1: string;
    flags: number;
    path: string;
}

function readFile(filePath: string): Buffer {
    return fs.readFileSync(filePath);
}

function readIndex(): IndexEntry[] {
    const indexPath = path.join('.git', 'index');
    let data: Buffer;
    try {
        data = readFile(indexPath);
    } catch (e) {
        if (e.code === 'ENOENT') {
            return [];
        } else {
            throw e;
        }
    }

    const digest = crypto.createHash('sha1').update(data.slice(0, -20)).digest();
    const indexDigest = data.slice(-20);

    if (!digest.equals(indexDigest)) {
        throw new Error('Invalid index checksum');
    }

    const signature = data.toString('ascii', 0, 4);
    if (signature !== 'DIRC') {
        throw new Error(`Invalid index signature ${signature}`);
    }

    const version = data.readUInt32BE(4);
    if (version !== 2) {
        throw new Error(`Unknown index version ${version}`);
    }

    const numEntries = data.readUInt32BE(8);
    let entries: IndexEntry[] = [];
    let offset = 12;

    while (offset < data.length - 20) {
        const entryStart = offset;
        const ctimeSeconds = data.readUInt32BE(offset);
        const ctimeNanoseconds = data.readUInt32BE(offset + 4);
        const mtimeSeconds = data.readUInt32BE(offset + 8);
        const mtimeNanoseconds = data.readUInt32BE(offset + 12);
        const dev = data.readUInt32BE(offset + 16);
        const ino = data.readUInt32BE(offset + 20);
        const mode = data.readUInt32BE(offset + 24);
        const uid = data.readUInt32BE(offset + 28);
        const gid = data.readUInt32BE(offset + 32);
        const fileSize = data.readUInt32BE(offset + 36);
        const sha1 = data.slice(offset + 40, offset + 60).toString('hex');
        const flags = data.readUInt16BE(offset + 60);
        const pathLength = flags & 0x0FFF;  // Path length stored in lower 12 bits
        offset += 62;
        let pathEnd = data.indexOf(0, offset);
        const path = data.toString('utf8', offset, pathEnd);

        entries.push({
            ctimeSeconds,
            ctimeNanoseconds,
            mtimeSeconds,
            mtimeNanoseconds,
            dev,
            ino,
            mode,
            uid,
            gid,
            fileSize,
            sha1,
            flags,
            path
        });

        offset = entryStart + Math.ceil((62 + pathEnd - entryStart + 1) / 8) * 8; // Align to the next 8-byte boundary
    }

    if (entries.length !== numEntries) {
        throw new Error('Number of index entries does not match expected count');
    }

    return entries;
}

import * as fs from 'fs';
import * as path from 'path';
import * as crypto from 'crypto';

interface IndexEntry {
    ctimeSeconds: number;
    ctimeNanoseconds: number;
    mtimeSeconds: number;
    mtimeNanoseconds: number;
    dev: number;
    ino: number;
    mode: number;
    uid: number;
    gid: number;
    fileSize: number;
    sha1: string;
    flags: number;
    path: string;
}

function writeFile(filePath: string, data: Buffer): void {
    fs.writeFileSync(filePath, data);
}

function writeIndex(entries: IndexEntry[]): void {
    const indexPath = path.join('.git', 'index');
    let buffer = Buffer.alloc(12); // Reserve space for header

    // Write header
    buffer.write('DIRC', 0, 4, 'ascii'); // Signature
    buffer.writeUInt32BE(2, 4); // Version
    buffer.writeUInt32BE(entries.length, 8); // Number of entries

    // Write index entries
    let offset = 12; // Start after header
    for (const entry of entries) {
        // Write each field of the entry
        buffer.writeUInt32BE(entry.ctimeSeconds, offset);
        buffer.writeUInt32BE(entry.ctimeNanoseconds, offset + 4);
        buffer.writeUInt32BE(entry.mtimeSeconds, offset + 8);
        buffer.writeUInt32BE(entry.mtimeNanoseconds, offset + 12);
        buffer.writeUInt32BE(entry.dev, offset + 16);
        buffer.writeUInt32BE(entry.ino, offset + 20);
        buffer.writeUInt32BE(entry.mode, offset + 24);
        buffer.writeUInt32BE(entry.uid, offset + 28);
        buffer.writeUInt32BE(entry.gid, offset + 32);
        buffer.writeUInt32BE(entry.fileSize, offset + 36);
        Buffer.from(entry.sha1, 'hex').copy(buffer, offset + 40);
        buffer.writeUInt16BE(entry.flags, offset + 60);

        // Write path (null-terminated)
        buffer.write(entry.path, offset + 62, Buffer.byteLength(entry.path, 'utf8'), 'utf8');
        buffer.writeUInt8(0, offset + 62 + Buffer.byteLength(entry.path, 'utf8')); // Null terminator

        // Move offset to the next entry
        const entryLen = Math.ceil((62 + Buffer.byteLength(entry.path, 'utf8') + 1) / 8) * 8;
        offset += entryLen;
    }

    // Calculate and append SHA-1 checksum
    const digest = crypto.createHash('sha1').update(buffer).digest();
    buffer = Buffer.concat([buffer, digest]);

    // Write buffer to file
    writeFile(indexPath, buffer);
}

// Usage
const indexEntries: IndexEntry[] = [
    {
        ctimeSeconds: 0,
        ctimeNanoseconds: 0,
        mtimeSeconds: 0,
        mtimeNanoseconds: 0,
        dev: 0,
        ino: 0,
        mode: 0o100644, // File mode
        uid: 0,
        gid: 0,
        fileSize: 0,
        sha1: 'b6fc4c620b67d95f953a5c1c1230aaab5db5a1b0', // SHA-1 hash
        flags: 0,
        path: 'a/b/file1.txt' // File path
    },
    {
        ctimeSeconds: 0,
        ctimeNanoseconds: 0,
        mtimeSeconds: 0,
        mtimeNanoseconds: 0,
        dev: 0,
        ino: 0,
        mode: 0o100644, // File mode
        uid: 0,
        gid: 0,
        fileSize: 0,
        sha1: '99f602c87026dfc2c4347c20c8fdb161ac7b1179', // SHA-1 hash
        flags: 0,
        path: 'c/d/file2.txt' // File path
    }
];

writeIndex(indexEntries);

```

### git commit
the format is as follows:
- Top level:
    ```
    commit {size}\0{content}
    ```
    where `{size}` is the number of bytes in `{content}`.
    This follows the same pattern for all object types.
-  `{content}`:
    ```
    tree {tree_sha}
    {parents}
    author {author_name} <{author_email}> {author_date_seconds} {author_date_timezone}
    committer {committer_name} <{committer_email}> {committer_date_seconds} {committer_date_timezone}
    
    {commit message}
    ```
    where:
    - `{tree_sha}`: SHA of the tree object this commit points to.
        This represents the top-level Git repo directory.
        That SHA comes from the format of the tree object: [What is the internal format of a Git tree object?](https://stackoverflow.com/questions/14790681/what-is-the-internal-format-of-a-git-tree-object)
    - `{parents}`: optional list of parent commit objects of form:
        ```
        parent {parent1_sha}
        parent {parent2_sha}
        ...
        ```
        The list can be empty if there are no parents, e.g. for the first commit in a repo.
        Two parents happen in regular merge commits.
        More than two parents are possible with `git merge -Xoctopus`, but this is not a common workflow. Here is an example: [https://github.com/cirosantilli/test-octopus-100k](https://github.com/cirosantilli/test-octopus-100k)
    - `{author_name}`: e.g.: `Ciro Santilli`. Cannot contain `<`, `\n`
    - `{author_email}`: e.g.: `cirosantilli@mail.com`. Cannot contain `>`, `\n`
    - `{author_date_seconds}`: seconds since 1970, e.g. `946684800` is the first second of year 2000
    - `{author_date_timezone}`: e.g.: `+0000` is UTC
    - committer fields: analogous to author fields
    - `{commit message}`: arbitrary.
there should be one new line character between the commit message and the committer

the git-commit tree  command takes in a parent sha a the current sha and a message
```bash
 git commit-tree 5b825dc642cb6eb9a060e54bf8d69288fbee4904 -p 3b18e512dba79e4c8300dd08aeb37f8e728b8dad -m "Second commit"
```
like so

### git clone
