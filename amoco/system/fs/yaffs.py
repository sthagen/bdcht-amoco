from amoco.system.structs import StructDefine, StructFormatter

YAFFS_OK = 1
YAFFS_FAIL = 0

YAFFS_LOSTNFOUND_NAME = "lost+found"
YAFFS_LOSTNFOUND_PREFIX = "obj"

YAFFS_ROOT_MODE = 0o755
YAFFS_LOSTNFOUND_MODE = 0o700

YAFFS_MAGIC = 0x5941FF53

YAFFS_NTNODES_LEVEL0 = 16
YAFFS_TNODES_LEVEL0_BITS = 4
YAFFS_TNODES_LEVEL0_MASK = 0xF
YAFFS_NTNODES_INTERNAL = YAFFS_NTNODES_LEVEL0 / 2
YAFFS_TNODES_INTERNAL_BITS = YAFFS_TNODES_LEVEL0_BITS - 1
YAFFS_TNODES_INTERNAL_MASK = 0x7
YAFFS_TNODES_MAX_LEVEL = 8
YAFFS_TNODES_MAX_BITS = (
    YAFFS_TNODES_LEVEL0_BITS + YAFFS_TNODES_INTERNAL_BITS * YAFFS_TNODES_MAX_LEVEL
)
YAFFS_MAX_CHUNK_ID = (1 << YAFFS_TNODES_MAX_BITS) - 1
YAFFS_MAX_FILE_SIZE_32 = 0x7FFFFFFF
YAFFS_BYTES_PER_SPARE = 16
YAFFS_BYTES_PER_CHUNK = 512
YAFFS_CHUNK_SIZE_SHIFT = 9
YAFFS_CHUNKS_PER_BLOCK = 32
YAFFS_BYTES_PER_BLOCK = YAFFS_CHUNKS_PER_BLOCK * YAFFS_BYTES_PER_CHUNK
YAFFS_MIN_YAFFS2_CHUNK_SIZE = 1024
YAFFS_MIN_YAFFS2_SPARE_SIZE = 32
YAFFS_ALLOCATION_NOBJECTS = 100
YAFFS_ALLOCATION_NTNODES = 100
YAFFS_ALLOCATION_NLINKS = 100
YAFFS_NOBJECT_BUCKETS = 256
YAFFS_OBJECT_SPACE = 0x40000
YAFFS_MAX_OBJECT_ID = YAFFS_OBJECT_SPACE - 1
YAFFS_SUMMARY_VERSION = 1


@StructDefine(
    """
    B: _f
    """
)
class yaffs_obj(StructFormatter):
    def __init__(self, data="", offset=0):
        if data:
            self.unpack(data, offset)
            assert self.fs_magic == 0x011954
