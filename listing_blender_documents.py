import shutil
from pathlib import Path

def transfer_blender_file():
    # 1. Locate the source directory (Documents/Blender)
    source_dir = Path.home().joinpath("Documents", "Blender")
    
    # 2. Locate your current working directory
    current_dir = Path.cwd()
    
    if not source_dir.exists() or not source_dir.is_dir():
        print(f"Error: The source directory '{source_dir}' does not exist.")
        return

    # 3. Gather all files in the Blender folder
    files = [item for item in source_dir.iterdir() if item.is_file()]
    
    if not files:
        print(f"No files found in {source_dir}")
        return

    # 4. Display the files with a numbered menu
    print(f"\n--- Available files in {source_dir} ---")
    for index, file in enumerate(files, start=1):
        print(f"[{index}] {file.name}")
    print("[0] Cancel and Exit")

    # 5. Get the user's choice
    while True:
        try:
            choice = int(input("\nEnter the number of the file you want to copy: "))
            if choice == 0:
                print("Operation cancelled.")
                return
            if 1 <= choice <= len(files):
                selected_file = files[choice - 1]
                break
            else:
                print(f"Please enter a number between 1 and {len(files)} (or 0 to cancel).")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # 6. Define the destination path
    destination_path = current_dir.joinpath(selected_file.name)

    # Check if a file with the same name already exists in the current folder
    if destination_path.exists():
        overwrite = input(f"'{selected_file.name}' already exists here. Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            print("Transfer cancelled. File not overwritten.")
            return

    # 7. Copy the file
    try:
        shutil.copy2(selected_file, destination_path)
        print(f"\nSuccess! Successfully copied '{selected_file.name}' to:")
        print(f"-> {destination_path}")
    except Exception as e:
        print(f"An error occurred during the file transfer: {e}")

if __name__ == "__main__":
    transfer_blender_file()