import os
import struct
import pathlib


class PAKDecompiler:
    def __init__(self):
        self.file_entries = []

    def decompile(self, archive_file, output_directory):
        self.file_entries = []

        with open(archive_file, "rb") as pak_file:
            # Read the number of file entries
            num_entries = struct.unpack("<I", pak_file.read(4))[0]

            for _ in range(num_entries):
                # Read the file path
                file_path = pak_file.read(100).split(b"\x00", 1)[0].decode("utf-8")

                # Read the offset and file size
                offset = struct.unpack("<I", pak_file.read(4))[0]
                file_size = struct.unpack("<I", pak_file.read(4))[0]

                self.file_entries.append((file_path, offset, file_size))

            # Create the output directory with the same name as the PAK file
            pak_file_name = os.path.basename(archive_file)
            pak_name_without_extension = os.path.splitext(pak_file_name)[0]
            output_directory_path = os.path.join(
                output_directory, pak_name_without_extension
            )
            pathlib.Path(output_directory_path).mkdir(parents=True, exist_ok=True)

            for file_entry in self.file_entries:
                file_path, offset, file_size = file_entry

                # Seek to the file data position
                pak_file.seek(offset, os.SEEK_SET)

                # Read the file data
                file_data = pak_file.read(file_size)

                # Write the file data to the output file
                output_file_path = os.path.join(output_directory_path, file_path)

                # Create parent directories if needed
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

                # Write the file data to the output file
                with open(output_file_path, "wb") as output_file:
                    output_file.write(file_data)

        print(
            f"Successfully decompiled {len(self.file_entries)} files from {archive_file}."
        )
