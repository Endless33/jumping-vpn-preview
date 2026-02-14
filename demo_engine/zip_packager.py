import os
import zipfile

class ZipPackager:
    """
    Creates a full lifecycle ZIP archive containing all demo artifacts.
    """

    def __init__(self, source_dir="DEMO_ECOSYSTEM", output_zip="DEMO_PACKAGE.zip"):
        self.source_dir = source_dir
        self.output_zip = output_zip

    def package(self):
        if not os.path.exists(self.source_dir):
            raise FileNotFoundError(f"Source directory not found: {self.source_dir}")

        with zipfile.ZipFile(self.output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.source_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.source_dir)
                    zipf.write(full_path, rel_path)

        return self.output_zip