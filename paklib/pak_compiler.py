import os
import struct
import pathlib


class PAKCompiler:
    def __init__(self):
        self.file_entries = []

    def add_file(self, file_path):
        if os.path.isfile(file_path):
            relative_path = os.path.relpath(file_path, os.getcwd())
            file_size = os.path.getsize(file_path)
            file_data = open(file_path, "rb").read()
            self.file_entries.append((relative_path, file_data, file_size))

    def add_directory(self, directory_path):
        for root, _, files in os.walk(directory_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                self.add_file(file_path)

    def compile(self, output_file):
        with open(output_file, "wb") as pak_file:
            # Write the number of file entries
            pak_file.write(struct.pack("<I", len(self.file_entries)))

            metadata_size = len(self.file_entries) * (
                100 + 1 + 3
            )  # file paths + null bytes + padding

            offset = (
                0  # Initial offset calculation (relative to the end of the metadata)
            )

            for file_entry in self.file_entries:
                relative_path, file_data, file_size = file_entry

                # Write the relative file path (up to 100 bytes)
                encoded_path = relative_path.encode("utf-8")[:100]
                pak_file.write(encoded_path)

                # Write the null byte after the file name
                pak_file.write(b"\x00")

                # Write the padding (remaining bytes in the 100-byte field)
                pak_file.write(b"\xCC" * (100 - len(encoded_path) - 1))

                # Write the offset of the file data
                pak_file.write(struct.pack("<I", offset))

                # Write the file size
                pak_file.write(struct.pack("<I", file_size))

                # Update the offset for the next file entry
                offset += len(file_data)

            # Write the file data for each file entry
            for file_entry in self.file_entries:
                relative_path, file_data, file_size = file_entry
                pak_file.write(file_data)

        print(
            f"Successfully compiled {len(self.file_entries)} files into {output_file}."
        )
