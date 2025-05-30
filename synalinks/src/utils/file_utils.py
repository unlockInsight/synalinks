# Modified from: keras/src/utils/file_utils.py
# Original authors: François Chollet et al. (Keras Team)
# License Apache 2.0: (c) 2025 Yoan Sallami (Synalinks Team)

import hashlib
import os
import re
import shutil
import tarfile
import urllib
import warnings
import zipfile
from urllib.request import urlretrieve

from synalinks.src.api_export import synalinks_export
from synalinks.src.backend import config
from synalinks.src.utils import io_utils
from synalinks.src.utils.progbar import Progbar


def path_to_string(path):
    """Convert `PathLike` objects to their string representation.

    If given a non-string typed path object, converts it to its string
    representation.

    If the object passed to `path` is not among the above, then it is
    returned unchanged. This allows e.g. passthrough of file objects
    through this function.

    Args:
        path: `PathLike` object that represents a path

    Returns:
        A string representation of the path argument, if Python support exists.
    """
    if isinstance(path, os.PathLike):
        return os.fspath(path)
    return path


def resolve_path(path):
    return os.path.realpath(os.path.abspath(path))


def is_path_in_dir(path, base_dir):
    return resolve_path(os.path.join(base_dir, path)).startswith(base_dir)


def is_link_in_dir(info, base):
    tip = resolve_path(os.path.join(base, os.path.dirname(info.name)))
    return is_path_in_dir(info.linkname, base_dir=tip)


def filter_safe_paths(members):
    base_dir = resolve_path(".")
    for finfo in members:
        valid_path = False
        if is_path_in_dir(finfo.name, base_dir):
            valid_path = True
            yield finfo
        elif finfo.issym() or finfo.islnk():
            if is_link_in_dir(finfo, base_dir):
                valid_path = True
                yield finfo
        if not valid_path:
            warnings.warn(
                f"Skipping invalid path during archive extraction: '{finfo.name}'.",
                stacklevel=2,
            )


def extract_archive(file_path, path=".", archive_format="auto"):
    """Extracts an archive if it matches a support format.

    Supports `.tar`, `.tar.gz`, `.tar.bz`, and `.zip` formats.

    Args:
        file_path: Path to the archive file.
        path: Where to extract the archive file.
        archive_format: Archive format to try for extracting the file.
            Options are `"auto"`, `"tar"`, `"zip"`, and `None`.
            `"tar"` includes `.tar`, `.tar.gz`, and `.tar.bz` files.
            The default `"auto"` uses `["tar", "zip"]`.
            `None` or an empty list will return no matches found.

    Returns:
        `True` if a match was found and an archive extraction was completed,
        `False` otherwise.
    """
    if archive_format is None:
        return False
    if archive_format == "auto":
        archive_format = ["tar", "zip"]
    if isinstance(archive_format, str):
        archive_format = [archive_format]

    file_path = path_to_string(file_path)
    path = path_to_string(path)

    for archive_type in archive_format:
        if archive_type == "tar":
            open_fn = tarfile.open
            is_match_fn = tarfile.is_tarfile
        elif archive_type == "zip":
            open_fn = zipfile.ZipFile
            is_match_fn = zipfile.is_zipfile
        else:
            raise NotImplementedError(archive_type)

        if is_match_fn(file_path):
            with open_fn(file_path) as archive:
                try:
                    if zipfile.is_zipfile(file_path):
                        # Zip archive.
                        archive.extractall(path)
                    else:
                        # Tar archive, perhaps unsafe. Filter paths.
                        archive.extractall(path, members=filter_safe_paths(archive))
                except (tarfile.TarError, RuntimeError, KeyboardInterrupt):
                    if os.path.exists(path):
                        if os.path.isfile(path):
                            os.remove(path)
                        else:
                            shutil.rmtree(path)
                    raise
            return True
    return False


@synalinks_export("synalinks.utils.get_file")
def get_file(
    fname=None,
    origin=None,
    untar=False,
    md5_hash=None,
    file_hash=None,
    cache_subdir="datasets",
    hash_algorithm="auto",
    extract=False,
    archive_format="auto",
    cache_dir=None,
    force_download=False,
    progbar=True,
):
    """Downloads a file from a URL if it not already in the cache.

    By default the file at the url `origin` is downloaded to the
    cache_dir `~/.synalinks`, placed in the cache_subdir `datasets`,
    and given the filename `fname`. The final location of a file
    `example.txt` would therefore be `~/.synalinks/datasets/example.txt`.
    Files in `.tar`, `.tar.gz`, `.tar.bz`, and `.zip` formats can
    also be extracted.

    Passing a hash will verify the file after download. The command line
    programs `shasum` and `sha256sum` can compute the hash.

    Example:

    ```python
    path_to_downloaded_file = get_file(
        origin="https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz",
        extract=True,
    )
    ```

    Args:
        fname: If the target is a single file, this is your desired
            local name for the file.
            If `None`, the name of the file at `origin` will be used.
            If downloading and extracting a directory archive,
            the provided `fname` will be used as extraction directory
            name (only if it doesn't have an extension).
        origin: Original URL of the file.
        untar: Deprecated in favor of `extract` argument.
            Boolean, whether the file is a tar archive that should
            be extracted.
        md5_hash: Deprecated in favor of `file_hash` argument.
            md5 hash of the file for file integrity verification.
        file_hash: The expected hash string of the file after download.
            The sha256 and md5 hash algorithms are both supported.
        cache_subdir: Subdirectory under the Keras cache dir where the file is
            saved. If an absolute path, e.g. `"/path/to/folder"` is
            specified, the file will be saved at that location.
        hash_algorithm: Select the hash algorithm to verify the file.
            options are `"md5'`, `"sha256'`, and `"auto'`.
            The default 'auto' detects the hash algorithm in use.
        extract: If `True`, extracts the archive. Only applicable to compressed
            archive files like tar or zip.
        archive_format: Archive format to try for extracting the file.
            Options are `"auto'`, `"tar'`, `"zip'`, and `None`.
            `"tar"` includes tar, tar.gz, and tar.bz files.
            The default `"auto"` corresponds to `["tar", "zip"]`.
            None or an empty list will return no matches found.
        cache_dir: Location to store cached files, when None it
            defaults ether `$KERAS_HOME` if the `KERAS_HOME` environment
            variable is set or `~/.synalinks/`.
        force_download: If `True`, the file will always be re-downloaded
            regardless of the cache state.

    Returns:
        Path to the downloaded file.

    **⚠️ Warning on malicious downloads ⚠️**

    Downloading something from the Internet carries a risk.
    NEVER download a file/archive if you do not trust the source.
    We recommend that you specify the `file_hash` argument
    (if the hash of the source file is known) to make sure that the file you
    are getting is the one you expect.
    """
    if origin is None:
        raise ValueError(
            'Please specify the "origin" argument (URL of the file to download).'
        )

    if cache_dir is None:
        cache_dir = config.synalinks_home()
    if md5_hash is not None and file_hash is None:
        file_hash = md5_hash
        hash_algorithm = "md5"
    datadir_base = os.path.expanduser(cache_dir)
    if not os.access(datadir_base, os.W_OK):
        datadir_base = os.path.join("/tmp", ".synalinks")
    datadir = os.path.join(datadir_base, cache_subdir)
    os.makedirs(datadir, exist_ok=True)

    provided_fname = fname
    fname = path_to_string(fname)

    if not fname:
        fname = os.path.basename(urllib.parse.urlsplit(origin).path)
        if not fname:
            raise ValueError(
                "Can't parse the file name from the origin provided: "
                f"'{origin}'."
                "Please specify the `fname` argument."
            )
    else:
        if os.sep in fname:
            raise ValueError(
                "Paths are no longer accepted as the `fname` argument. "
                "To specify the file's parent directory, use "
                f"the `cache_dir` argument. Received: fname={fname}"
            )

    if extract or untar:
        if provided_fname:
            if "." in fname:
                download_target = os.path.join(datadir, fname)
                fname = fname[: fname.find(".")]
                extraction_dir = os.path.join(datadir, fname + "_extracted")
            else:
                extraction_dir = os.path.join(datadir, fname)
                download_target = os.path.join(datadir, fname + "_archive")
        else:
            extraction_dir = os.path.join(datadir, fname)
            download_target = os.path.join(datadir, fname + "_archive")
    else:
        download_target = os.path.join(datadir, fname)

    if force_download:
        download = True
    elif os.path.exists(download_target):
        # File found in cache.
        download = False
        # Verify integrity if a hash was provided.
        if file_hash is not None:
            if not validate_file(download_target, file_hash, algorithm=hash_algorithm):
                io_utils.print_msg(
                    "A local file was found, but it seems to be "
                    f"incomplete or outdated because the {hash_algorithm} "
                    "file hash does not match the original value of "
                    f"{file_hash} so we will re-download the data."
                )
                download = True
    else:
        download = True

    if download:
        if progbar:
            io_utils.print_msg(f"Downloading data from {origin}")

        class DLProgbar:
            """Manage progress bar state for use in urlretrieve."""

            def __init__(self):
                self.progbar = None
                self.finished = False

            def __call__(self, block_num, block_size, total_size):
                if total_size == -1:
                    total_size = None
                if not self.progbar:
                    self.progbar = Progbar(total_size)
                current = block_num * block_size

                if total_size is None:
                    self.progbar.update(current)
                else:
                    if current < total_size:
                        self.progbar.update(current)
                    elif not self.finished:
                        self.progbar.update(self.progbar.target)
                        self.finished = True

        error_msg = "URL fetch failure on {}: {} -- {}"
        try:
            try:
                if progbar:
                    urlretrieve(origin, download_target, DLProgbar())
                else:
                    urlretrieve(origin, download_target)
            except urllib.error.HTTPError as e:
                raise Exception(error_msg.format(origin, e.code, e.msg))
            except urllib.error.URLError as e:
                raise Exception(error_msg.format(origin, e.errno, e.reason))
        except (Exception, KeyboardInterrupt):
            if os.path.exists(download_target):
                os.remove(download_target)
            raise

        # Validate download if succeeded and user provided an expected hash
        # Security conscious users would get the hash of the file from a
        # separate channel and pass it to this API to prevent MITM / corruption:
        if os.path.exists(download_target) and file_hash is not None:
            if not validate_file(download_target, file_hash, algorithm=hash_algorithm):
                raise ValueError(
                    "Incomplete or corrupted file detected. "
                    f"The {hash_algorithm} "
                    "file hash does not match the provided value "
                    f"of {file_hash}."
                )

    if extract or untar:
        if untar:
            archive_format = "tar"

        status = extract_archive(download_target, extraction_dir, archive_format)
        if not status:
            warnings.warn("Could not extract archive.", stacklevel=2)
        return extraction_dir

    return download_target


def resolve_hasher(algorithm, file_hash=None):
    """Returns hash algorithm as hashlib function."""
    if algorithm == "sha256":
        return hashlib.sha256()

    if algorithm == "auto" and file_hash is not None and len(file_hash) == 64:
        return hashlib.sha256()

    # This is used only for legacy purposes.
    return hashlib.md5()


def hash_file(fpath, algorithm="sha256", chunk_size=65535):
    """Calculates a file sha256 or md5 hash.

    Example:

    >>> hash_file('/path/to/file.zip')
    'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

    Args:
        fpath: Path to the file being validated.
        algorithm: Hash algorithm, one of `"auto"`, `"sha256"`, or `"md5"`.
            The default `"auto"` detects the hash algorithm in use.
        chunk_size: Bytes to read at a time, important for large files.

    Returns:
        The file hash.
    """
    if isinstance(algorithm, str):
        hasher = resolve_hasher(algorithm)
    else:
        hasher = algorithm

    with open(fpath, "rb") as fpath_file:
        for chunk in iter(lambda: fpath_file.read(chunk_size), b""):
            hasher.update(chunk)

    return hasher.hexdigest()


def validate_file(fpath, file_hash, algorithm="auto", chunk_size=65535):
    """Validates a file against a sha256 or md5 hash.

    Args:
        fpath: path to the file being validated
        file_hash:  The expected hash string of the file.
            The sha256 and md5 hash algorithms are both supported.
        algorithm: Hash algorithm, one of `"auto"`, `"sha256"`, or `"md5"`.
            The default `"auto"` detects the hash algorithm in use.
        chunk_size: Bytes to read at a time, important for large files.

    Returns:
        Boolean, whether the file is valid.
    """
    hasher = resolve_hasher(algorithm, file_hash)

    if str(hash_file(fpath, hasher, chunk_size)) == str(file_hash):
        return True
    else:
        return False


def is_remote_path(filepath):
    """
    Determines if a given filepath indicates a remote location.

    This function checks if the filepath represents a known remote pattern
    such as GCS (`/gcs`), CNS (`/cns`), CFS (`/cfs`), HDFS (`/hdfs`)

    Args:
        filepath (str): The path to be checked.

    Returns:
        bool: True if the filepath is a recognized remote path, otherwise False
    """
    if re.match(r"^(/cns|/cfs|/gcs|/hdfs|/readahead|.*://).*$", str(filepath)):
        return True
    return False


def _raise_remote_path_error(path):
    raise ValueError(f"Handling remote paths is not supported. Received path: {path}")


def exists(path):
    if is_remote_path(path):
        _raise_remote_path_error(path)
    return os.path.exists(path)


def File(path, mode="r"):
    if is_remote_path(path):
        _raise_remote_path_error(path)
    return open(path, mode=mode)


def join(path, *paths):
    if is_remote_path(path):
        _raise_remote_path_error(path)
    return os.path.join(path, *paths)


def isdir(path):
    if is_remote_path(path):
        _raise_remote_path_error(path)
    return os.path.isdir(path)


def remove(path):
    if is_remote_path(path):
        _raise_remote_path_error(path)
    return os.remove(path)


def rmtree(path):
    if is_remote_path(path):
        _raise_remote_path_error(path)
    return shutil.rmtree(path)


def listdir(path):
    if is_remote_path(path):
        _raise_remote_path_error(path)
    return os.listdir(path)


def copy(src, dst):
    if is_remote_path(src) or is_remote_path(dst):
        _raise_remote_path_error(f"src={src} dst={dst}")
    return shutil.copy(src, dst)


def makedirs(path):
    if is_remote_path(path):
        _raise_remote_path_error(path)
    return os.makedirs(path)
