import os, struct, time
from pathlib import Path


def compile(directory_path, pak_file_path=None):
    start_time = time.time()
    # Get the list of files in the directory and its subdirectories
    file_list = []
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            relative_path = os.path.relpath(root, directory_path)
            file_list.append(
                (os.path.join(relative_path, file_name), os.path.join(root, file_name))
            )
    print("Gotten files...")

    # Sort the file list based on the directory and filename
    # sorted_file_list = sorted(file_list, key=lambda path: (path.count('/'), path))
    def custom_key(path):
        priority_chars = [
            ".",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "\\",
            "-",
            "_",
        ]
        default_priority = 1000

        def get_priority(char):
            if char in priority_chars:
                return priority_chars.index(char)
            return default_priority + ord(char)

        return [get_priority(char) for char in path[0].lower()]

    sorted_file_list = sorted(file_list, key=custom_key)

    debug_list = []

    num_files = len(sorted_file_list)

    if pak_file_path == None:
        pak_file_path = os.path.join(directory_path, ".pak")

    # Open the .pak file in binary mode
    with open(pak_file_path, "wb") as pak_file:
        # Write the number of files to the archive header
        pak_file.write(struct.pack("I", num_files))

        # Write the directory entries for each file
        file_offset = 0  # Offset starts after the archive header
        for file_name, file_path in sorted_file_list:
            if file_name in debug_list:
                print("DOUBLE")
            debug_list.append(file_name)

            # print(file_name)
            # Write the filename (null-terminated)
            pak_file.write(file_name.encode("utf-8"))
            pak_file.write(b"\x00")
            pak_file.write(b"\xcc" * (98 - (len(file_name) - 1)))

            # Write the file offset and length
            pak_file.write(struct.pack("I", file_offset))
            file_size = os.path.getsize(file_path)
            pak_file.write(struct.pack("I", file_size))

            # Update the file offset for the next file
            file_offset += file_size

        # Write the file data for each file
        for _, file_path in sorted_file_list:
            with open(file_path, "rb") as file:
                print(f"Packing {_}...")
                pak_file.write(file.read())

    print(f"Done! Elapsed time: {time.time() - start_time}")


def decompile(pak_file_path, output_directory=os.getcwd()):
    start_time = time.time()
    # Create the output directory if it doesn't exist
    output_directory = os.path.join(output_directory, Path(pak_file_path).stem)
    print(output_directory)

    os.makedirs(output_directory, exist_ok=True)
    print("Made dirs...")

    # Open the .pak file in binary mode
    entries = []
    with open(pak_file_path, "rb") as pak_file:
        # Read the number of files from the archive header
        num_files_bytes = pak_file.read(4)
        num_files = struct.unpack("I", num_files_bytes)[0]
        file_offset = 4 + (108 * num_files)
        # filename_offset = 4

        # Read the directory entries for each file
        for _ in range(num_files - 2):
            # Read the filename (null-terminated)
            filename = b""
            while True:
                char = pak_file.read(1)
                if char == b"\x00":
                    break
                filename += char

            filename_offset = 100 - len(filename) - 1
            pak_file.seek(filename_offset, os.SEEK_CUR)
            print(filename_offset, filename, len(filename))

            file_offset_bytes = pak_file.read(4)
            file_offset = struct.unpack("I", file_offset_bytes)[0]
            file_length_bytes = pak_file.read(4)
            file_length = struct.unpack("I", file_length_bytes)[0]

            entries.append((filename, file_offset, file_length))

        for entry in entries:
            print(f"writing {entry[0]}...")
            pak_file.seek(entry[1])
            file_data = pak_file.read(entry[2])

            # Determine the output path for the file
            output_path = os.path.join(output_directory, entry[0].decode("utf-8"))

            # Create the necessary directories in the output path
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Write the extracted file data to the output file
            with open(output_path, "wb") as output_file:
                output_file.write(file_data)

    print(f"Done! Elapsed time: {time.time() - start_time}")
