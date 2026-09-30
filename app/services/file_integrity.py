import hashlib


def calculate_bytes_hash(file_data):
    """
    Calculate SHA-256 hash of file data.
    """

    sha256 = hashlib.sha256()
    sha256.update(file_data)

    return sha256.hexdigest()


def check_file_integrity(current_hash, original_hash):
    """
    Compare current file hash with the stored baseline hash.
    """

    if current_hash == original_hash:
        return {
            "status": "SAFE",
            "message": "File has not been modified.",
            "hash": current_hash
        }

    return {
        "status": "CHANGED",
        "message": "File has been modified.",
        "hash": current_hash
    }