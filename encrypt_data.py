import base64, gzip, io, os, tarfile
from cryptography.fernet import Fernet


def make_tar_gz(dir_path: str) -> bytes:
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
        with tarfile.open(fileobj=gz, mode="w") as tar:
            tar.add(dir_path, arcname=os.path.basename(dir_path))
    return buf.getvalue()


def encrypt_bytes(data: bytes, key_b64: bytes) -> bytes:
    f = Fernet(key_b64)
    return f.encrypt(data)


if __name__ == "__main__":
    src = "data"  # your plaintext folder
    out = "secure/data.tar.gz.enc"
    os.makedirs(os.path.dirname(out), exist_ok=True)

    # Generate a new key (one-time). Save it securely (NOT in git).
    key_b64 = Fernet.generate_key()
    with open("FERNET_KEY.txt", "wb") as key_file:
        key_file.write(key_b64)
    print("Key saved to FERNET_KEY.txt (keep this secret!)")

    tar_gz = make_tar_gz(src)
    enc = encrypt_bytes(tar_gz, key_b64)
    with open(out, "wb") as out_file:
        out_file.write(enc)

    print(f"Encrypted archive written to {out} ({len(enc)} bytes)")
