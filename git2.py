import argparse
import hashlib
import io
import os
import pathlib
import sys
import time
import zlib
from enum import Enum
from os.path import isfile
from typing import Optional
from urllib.parse import urlparse
from urllib.request import urlopen, Request
def _object_path(sha):
class ObjType(Enum):
    COMMIT = 1
    TREE = 2
    BLOB = 3
    TAG = 4
    __RESERVED = 5
    OFS_DELTA = 6
    REF_DELTA = 7
obj_names = {
    ObjType.COMMIT: b"commit",
    ObjType.TREE: b"tree",
    ObjType.BLOB: b"blob",
    ObjType.TAG: b"tag",
}
_verbose = False
def _object_path(sha: str) -> str:
    return f"./.git/objects/{sha[:2]}/{sha[2:]}"
def _read_object(sha, mode="rb"):
def _read_object(sha: str, mode="rb"):
    with open(_object_path(sha), mode) as f:
        return zlib.decompress(f.read())
def _debug(msg, end="\n"):
    if _verbose:
        print(msg, file=sys.stderr, end=end)
def init(args):
    os.mkdir(".git")
    os.mkdir(".git/objects")
    os.mkdir(".git/refs")
    os.mkdir(".git/refs/heads")
    with open(".git/HEAD", "w") as f:
        f.write("ref: refs/heads/master\n")
    print("Initialized git directory")
def cat_file(args):
    blob = _read_object(args.sha)
    print(_cat_file(args.sha)[1].decode("utf8"), end="")
    file_type = blob[:4]
    size_i = blob.index(b"\x00", 5)
    size = int(blob[5:size_i])
def _cat_file(sha: str) -> tuple[bytes, bytes]:
    blob = _read_object(sha)
    space_i = blob.index(b" ")
    file_type = blob[:space_i]
    size_i = blob.index(b"\x00", space_i)
    size = int(blob[space_i + 1 : size_i])
    data = blob[size_i + 1 : size_i + size + 1]
    print(data.decode("utf8"), end="")
    return file_type, data
def hash_object(args):
    print(_hash_object(args.path, args.to_write))
def _hash_object(path: str, to_write: bool) -> str:
    hash = hashlib.sha1()
    hash.update(b"blob ")
    stat = os.stat(path)
    num_bytes = str(stat.st_size).encode("utf8")
    hash.update(num_bytes)
    hash.update(b"\x00")
    with open(path, "rb") as f:
        hash.update(f.read())
    hex = hash.hexdigest()
    opath = _object_path(hex)
    if to_write and not os.path.exists(opath):
        pathlib.Path(f".git/objects/{hex[:2]}").mkdir(exist_ok=True)
        with open(opath, "wb") as out:
            compress = zlib.compressobj()
            out.write(compress.compress(b"blob "))
            out.write(compress.compress(num_bytes))
            out.write(compress.compress(b"\x00"))
            with open(path, "rb") as f:
                out.write(compress.compress(f.read()))
            out.write(compress.flush())
    return hex
def ls_tree(args):
    def print_sha_type(sha):
        data = _read_object(sha)
        print(data[: data.index(b" ")].decode("utf8"), end=" ")
    data = _read_object(args.tree_sha)
    null_index = data.index(b"\x00")
    size = int(data[4:null_index])
    index = null_index + 1
    for entry in _ls_tree(_cat_file(args.tree_sha)[1]):
        if not args.name_only:
            mode = entry["mode"]
            print("0" * (6 - len(mode)), end="")
            print(mode.decode("utf8"), end=" ")
            sha = entry["sha"]
            print_sha_type(sha)
            print(sha, end="\t")
        print(entry["name"].decode("utf8"))
def _ls_tree(data):
    index = 0
    while index < len(data):
        mode_end = data.index(b" ", index)
        mode = data[index:mode_end]
        null_index = data.index(b"\x00", index)
        name = data[mode_end + 1 : null_index]
        sha = data[null_index + 1 : null_index + 21].hex()
        if not args.name_only:
            print("0" * (6 - len(mode)), end="")
            print(mode.decode("utf8"), end=" ")
            print_sha_type(sha)
            print(sha, end="\t")
        print(name.decode("utf8"))
        index = null_index + 21
        yield {
            "mode": mode,
            "name": name,
            "sha": sha,
        }
def write_tree(args):
    print(_write_tree("."))
def _write_tree(path: str) -> Optional[str]:
    path = os.path.normpath(path)
    if path == ".git":
        return None
    items = []
    for f in sorted(os.listdir(path)):
        base = os.path.basename(f)
        fullname = os.path.join(path, f)
        if isfile(fullname):
            sha = _hash_object(fullname, True)
            items.append(
                {
                    "mode": b"100755" if os.access(fullname, os.X_OK) else b"100644",
                    "type": b"blob",
                    "sha": sha,
                    "name": base.encode("utf8"),
                }
            )
        else:
            sha = _write_tree(fullname)
            if sha is None:
                continue
            items.append(
                {
                    "mode": b"40000",
                    "type": b"tree",
                    "sha": sha,
                    "name": base.encode("utf8"),
                }
            )
    bf = io.BytesIO()
    size = 0
    for item in items:
        size += bf.write(
            b"%b %b\x00%b" % (item["mode"], item["name"], bytes.fromhex(item["sha"]))
        )
    hex = hashlib.sha1(b"tree ")
    size_bytes = str(size).encode("utf8")
    hex.update(size_bytes)
    hex.update(b"\x00")
    hex.update(bf.getvalue())
    sha = hex.hexdigest()
    pathlib.Path(f".git/objects/{sha[:2]}").mkdir(exist_ok=True)
    with open(_object_path(sha), "wb") as out:
        compress = zlib.compressobj()
        out.write(compress.compress(b"tree "))
        out.write(compress.compress(size_bytes))
        out.write(compress.compress(b"\x00"))
        out.write(compress.compress(bf.getvalue()))
        out.write(compress.flush())
    return sha
def commit_tree(args):
    tree_sha = _write_tree(".") or ""
    print(f"tree_sha: {tree_sha}", file=sys.stderr)
    _debug(f"tree_sha: {tree_sha}")
    bf = io.BytesIO()
    size = 0
    size += bf.write(b"tree %s\n" % tree_sha.encode("utf8"))
    if args.parent_sha:
        size += bf.write(b"parent %s\n" % args.parent_sha.encode("utf8"))
    current_time = int(time.time())
    size += bf.write(b"author Foo Bar <foo.bar@gmail.com> %d -0700\n" % current_time)
    size += bf.write(
        b"committer Foo Bar <foo.bar@gmail.com> %d -0700\n\n" % current_time
    )
    size += bf.write(args.message.encode("utf8"))
    size += bf.write(b"\n")
    size_bytes = str(size).encode("utf8")
    hex = hashlib.sha1(b"commit %s\x00" % size_bytes)
    hex.update(bf.getvalue())
    sha = hex.hexdigest()
    pathlib.Path(f".git/objects/{sha[:2]}").mkdir(exist_ok=True)
    with open(_object_path(sha), "wb") as out:
        compress = zlib.compressobj()
        out.write(compress.compress(b"commit "))
        out.write(compress.compress(size_bytes))
        out.write(compress.compress(b"\x00"))
        out.write(compress.compress(bf.getvalue()))
        out.write(compress.flush())
    print(sha)
def parse_pkt_line(f):
    pkt_len = int(f.read(4), 16)
    if pkt_len == 0:
        return b""
    return f.read(pkt_len - 4)
def make_pkt_line(b: bytes) -> bytes:
    return b"%04x" % (len(b) + 4) + b
def parse_ref_list(f):
    pkt_line = parse_pkt_line(f)
    if pkt_line[:40] == b"0" * 40:
        raise Exception("empty ref list not currently supported")
    obj_id = pkt_line[:40]
    _debug(f"obj_id: {obj_id}")
    null_index = pkt_line.index(b"\x00", 41)
    name = pkt_line[41:null_index]
    _debug(f"name: {name}")
    cap_list = pkt_line[null_index + 1 :].strip().split(b" ")
    _debug(f"cap_list: {cap_list}")
    return {
        "obj-id": obj_id,
        "name": name,
        "cap_list": cap_list,
    }
def parse_upload_pack(resp):
    if (
        resp.status != 200
        or resp.getheader("Content-Type")
        != "application/x-git-upload-pack-advertisement"
    ):
        _debug("Bad response")
        sys.exit(2)
        return
    service_line = parse_pkt_line(resp)[1:].strip()
    _debug(f"service_line: {service_line}")
    assert resp.read(4) == b"0000"
    ref_list = parse_ref_list(resp)
    ref_list["refs"] = {}
    _debug(f"ref_list: {ref_list}")
    ref_record = parse_pkt_line(resp)
    _debug(f"ref_record: {ref_record}")
    if ref_record:
        obj_id = ref_record[:40]
        null_index = ref_record.index(b"\n", 41)
        name = ref_record[41:null_index]
        ref_list["refs"][obj_id] = name
    assert parse_pkt_line(resp) == b""
    return ref_list
def compute_request(sha: bytes) -> bytes:
    bf = io.BytesIO()
    # want_list
    want = b"want " + sha
    want_list = want + b"\n"
    bf.write(make_pkt_line(want_list))
    # have_list
    pass
    # request_end
    bf.write(b"0000")
    bf.write(make_pkt_line(b"done\n"))
    return bf.getvalue()
def parse_pack_object(f):
    b = int.from_bytes(f.read(1))
    _debug("pack object: {0:08b}".format(b), end="")
    index = 1
    has_more_bytes = bool(b & 0b10000000)
    o_type = ObjType((b & 0b01110000) >> 4)
    size = b & 0b00001111
    shift = 4
    while has_more_bytes:
        b = int.from_bytes(f.read(1))
        _debug(" {0:08b}".format(b))
        index += 1
        has_more_bytes = bool(b & 0b10000000)
        size += (b & 0b01111111) << shift
        shift += 7
    _debug("")
    return o_type, size, index
def parse_pack_num(f):
    b = int.from_bytes(f.read(1))
    index = 1
    num = b & 127
    shift = 7
    while bool(b & 128):
        b = int.from_bytes(f.read(1))
        num += (b & 127) << shift
        shift += 7
        index += 1
    return num, index
def decompress_obj_data(f):
    data = b""
    index = 0
    decompress = zlib.decompressobj()
    while True:
        c = f.read(1)
        data += decompress.decompress(c)
        index += 1
        if decompress.eof:
            break
    return data, index
def rebuild_object(base_sha: str, delta: bytes):
    df = io.BytesIO(delta)
    base_size, _ = parse_pack_num(df)
    _debug(f"base_size: {base_size}")
    obj_size, _ = parse_pack_num(df)
    _debug(f"obj_size: {obj_size}")
    base_type, base_data = _cat_file(base_sha)
    _debug(f"base object type: {base_type}")
    header = b"%s %d\x00" % (base_type, obj_size)
    _debug(f"header: {header}")
    of = io.BytesIO()
    of.write(header)
    f = io.BytesIO(base_data)
    while c := df.read(1):
        b = c[0]
        _debug(f"command: {b:#010b}")
        if b & 0b10000000:
            # copy
            offsets = b & 0b00001111
            _debug(f"offsets: {offsets:#010b}")
            shift = 0
            offset = 0
            while offsets:
                if offsets & 1:
                    offset += df.read(1)[0] << shift
                shift += 8
                offsets >>= 1
            sizes = (b & 0b01110000) >> 4
            _debug(f"sizes: {sizes:#010b}")
            shift = 0
            size = 0
            while sizes:
                if sizes & 1:
                    size += df.read(1)[0] << shift
                shift += 8
                sizes >>= 1
            _debug(f"Copy: offset: {offset}, size: {size}")
            f.seek(offset)
            of.write(f.read(size))
        else:
            # insert
            size = b & 0b01111111
            _debug(f"copy size: {size}")
            data = df.read(size)
            _debug(f"data: {data}")
            of.write(data)
    target_sha = hashlib.sha1(of.getvalue()).hexdigest()
    _debug(f"Deltified sha: {target_sha}\ndata:\n{of.getvalue()}")
    pathlib.Path(f".git/objects/{target_sha[:2]}").mkdir(exist_ok=True)
    with open(_object_path(target_sha), "wb") as f:
        f.write(zlib.compress(of.getvalue()))
def parse_pack(f):
    signature = f.read(4)
    index = 4
    _debug(signature.decode("utf8"))
    assert signature == b"PACK"
    version = int.from_bytes(f.read(4))
    index += 4
    _debug(f"version = {version}")
    num_objects = int.from_bytes(f.read(4))
    index += 4
    _debug(f"number of objects: {num_objects}")
    objects = {}  # key: offset, val: decompressed data
    for i in range(num_objects):
        start_index = index
        o_type, size, bytes_read = parse_pack_object(f)
        index += bytes_read
        _debug(f"ObjType: {o_type}\nsize: {size}")
        if o_type.value < 5:
            data, bytes_read = decompress_obj_data(f)
            objects[start_index] = data
            _debug(data)
            assert len(data) == size
            index += size
            object_data = b"%s %d\x00%s" % (obj_names[o_type], len(data), data)
            sha = hashlib.sha1(object_data).hexdigest()
            _debug(f"sha: {sha}")
            pathlib.Path(f".git/objects/{sha[:2]}").mkdir(exist_ok=True)
            with open(_object_path(sha), "wb") as of:
                of.write(zlib.compress(object_data))
        elif o_type == ObjType.OFS_DELTA:
            raise Exception("OFS_DELTA unsupported")
        elif o_type == ObjType.REF_DELTA:
            sha = f.read(20).hex()
            _debug(f"base sha: {sha}")
            data, bytes_read = decompress_obj_data(f)
            _debug(data)
            assert len(data) == size
            rebuild_object(sha, data)
        else:
            raise Exception("Unknown object type")
def make_tree(data: bytes, parent_dir: bytes = b""):
    for entry in _ls_tree(data):
        name = entry["name"]
        sha = entry["sha"]
        otype, data = _cat_file(sha)
        if otype == b"blob":
            with open(os.path.join(parent_dir, name), "wb") as f:
                f.write(data)
        elif otype == b"tree":
            new_dir = os.path.join(parent_dir, name)
            os.mkdir(new_dir)
            make_tree(data, new_dir)
        else:
            raise Exception("Unhandled object type %s" % otype)
def checkout_commit(sha: str):
    _, tree_data = _cat_file(sha)
    tree_sha = tree_data[tree_data.index(b" ") + 1 : tree_data.index(b"\n")].decode(
        "utf8"
    )
    _debug(f"checkout tree sha: {tree_sha}")
    make_tree(_cat_file(tree_sha)[1])
def clone(args):
    def parse_dir(url):
        o = urlparse(url)
        last = o.pat.split("/")[-1]
        if last.endswith(".git"):
            return last[:-4]
        return last
    git_upload_pack_url: str = args.url + "/info/refs?service=git-upload-pack"
    resp = urlopen(git_upload_pack_url)
    ref_list = parse_upload_pack(resp)
    data = compute_request(ref_list["obj-id"])
    _debug(data)
    resp = urlopen(
        Request(
            args.url + "/git-upload-pack",
            data=data,
            headers={"Content-Type": "application/x-git-upload-pack-request"},
        )
    )
    parse_pkt_line(resp)  # NAK
    repo = args.dir or parse_dir(args.url)
    os.mkdir(repo)
    os.chdir(repo)
    init(None)
    if ref_list["name"] == "HEAD":
        with open(".git/HEAD", "w") as f:
            ref = ref_list["refs"][ref_list["obj-id"]]
            f.write(f"ref: {ref}")
    for obj_id, name in ref_list["refs"].items():
        with open(b".git/%s" % name, "wb") as f:
            f.write(obj_id)
            f.write(b"\n")
    parse_pack(resp)
    checkout_commit(ref_list["obj-id"].decode("utf8"))
def main():
    parser = argparse.ArgumentParser("mygit")
    parser.add_argument("-v", action="store_true", help="Show debug information")
    subparsers = parser.add_subparsers(required=True)
    parser_init = subparsers.add_parser("init", help="Create new repo")
    parser_init.set_defaults(func=init)
    parser_cat_file = subparsers.add_parser("cat-file", help="Print blob")
    parser_cat_file.add_argument("-p", dest="sha", required=True, help="Blob hash")
    parser_cat_file.set_defaults(func=cat_file)
    parser_hash_object = subparsers.add_parser("hash-object", help="Print hash of file")
    parser_hash_object.add_argument("path", help="The path to the file")
    parser_hash_object.add_argument(
        "-w",
        dest="to_write",
        action="store_true",
        help="Write file to objects directory",
    )
    parser_hash_object.set_defaults(func=hash_object)
    parser_ls_tree = subparsers.add_parser(
        "ls-tree", help="List the contents of a tree object"
    )
    parser_ls_tree.add_argument("tree_sha", help="SHA of the tree")
    parser_ls_tree.add_argument(
        "--name-only", action="store_true", help="List only the filenames"
    )
    parser_ls_tree.set_defaults(func=ls_tree)
    parser_write_tree = subparsers.add_parser(
        "write-tree", help="Create a tree object from the current files"
    )
    parser_write_tree.set_defaults(func=write_tree)
    parser_commit_tree = subparsers.add_parser(
        "commit-tree", help="Create a new commit object"
    )
    parser_commit_tree.add_argument("sha", help="An existing tree object")
    parser_commit_tree.add_argument(
        "-m", dest="message", required=True, help="The commit message"
    )
    parser_commit_tree.add_argument(
        "-p", dest="parent_sha", help="The sha of the parent commit objectr"
        "-p", dest="parent_sha", help="The sha of the parent commit object"
    )
    parser_commit_tree.set_defaults(func=commit_tree)
    parser_clone = subparsers.add_parser(
        "clone", help="Clone a repository into a new directory"
    )
    parser_clone.add_argument("url", help="The remote repository to clone from")
    parser_clone.add_argument(
        "dir", nargs="?", default=None, help="Name of the new directory to clone into."
    )
    parser_clone.set_defaults(func=clone)
    args = parser.parse_args()
    global _verbose
    _verbose = args.v
    args.func(args)
