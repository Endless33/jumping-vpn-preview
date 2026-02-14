from packager import EcosystemPackager

if __name__ == "__main__":
    pkg = EcosystemPackager()
    path = pkg.package()
    print(f"Ecosystem packaged into: {path}")