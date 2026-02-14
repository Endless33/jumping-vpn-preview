from zip_packager import ZipPackager

if __name__ == "__main__":
    zp = ZipPackager()
    path = zp.package()
    print(f"Full demo package created: {path}")