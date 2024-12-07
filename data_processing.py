import os
import zipfile
import shutil

# Paths to the zip file and extraction folder
zip_file_path = "Arabic_PCM.zip"
extract_folder = "extracted_files"

# Create directories for Arabic and PCM
arabic_folder = os.path.join(extract_folder, "Arabic")
pcm_folder = os.path.join(extract_folder, "PCM")
mismatched_folder = "mismatched_files"

os.makedirs(arabic_folder, exist_ok=True)
os.makedirs(pcm_folder, exist_ok=True)
os.makedirs(mismatched_folder, exist_ok=True)

# Uncompress the zip file
print(f"Uncompressing {zip_file_path}...")
try:
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
    print(f"Files extracted to {extract_folder}")
except Exception as e:
    print(f"Error during extraction: {e}")

# Check if files are extracted and move them to respective folders
extracted_files = os.listdir(extract_folder)
for file in extracted_files:
    if file.startswith("arabic"):
        os.rename(os.path.join(extract_folder, file), os.path.join(arabic_folder, file))
    elif file.startswith("pcm"):
        os.rename(os.path.join(extract_folder, file), os.path.join(pcm_folder, file))

print(f"Arabic files: {os.listdir(arabic_folder)}")
print(f"PCM files: {os.listdir(pcm_folder)}")

# Match files based on suffix
arabic_files = os.listdir(arabic_folder)
pcm_files = os.listdir(pcm_folder)

matched_files = []
mismatched_files = []

# Match files
for arabic_file in arabic_files:
    suffix = arabic_file.split("_")[1]  # Extract the suffix (e.g., "002")
    pcm_file = f"pcm_{suffix}"  # Build corresponding PCM file name
    
    if pcm_file in pcm_files:
        # Check if number of lines match
        with open(os.path.join(arabic_folder, arabic_file), 'r') as arabic_f:
            arabic_lines = arabic_f.readlines()
        
        with open(os.path.join(pcm_folder, pcm_file), 'r') as pcm_f:
            pcm_lines = pcm_f.readlines()
        
        if len(arabic_lines) == len(pcm_lines):
            matched_files.append((arabic_file, pcm_file))
        else:
            mismatched_files.append((arabic_file, pcm_file))
    else:
        print(f"No matching PCM file for {arabic_file}")

# Move mismatched files to a new folder
for arabic_file, pcm_file in mismatched_files:
    shutil.move(os.path.join(arabic_folder, arabic_file), os.path.join(mismatched_folder, arabic_file))
    shutil.move(os.path.join(pcm_folder, pcm_file), os.path.join(mismatched_folder, pcm_file))

# Print matched and mismatched file counts
print(f"Matched files: {len(matched_files)}")
print(f"Mismatched files moved to {mismatched_folder}")

# Concatenate matched files into two master files
with open("Arabic_all.txt", 'w') as arabic_all_f, open("PCM_all.txt", 'w') as pcm_all_f:
    for arabic_file, pcm_file in matched_files:
        with open(os.path.join(arabic_folder, arabic_file), 'r') as arabic_f:
            arabic_lines = arabic_f.readlines()
        
        with open(os.path.join(pcm_folder, pcm_file), 'r') as pcm_f:
            pcm_lines = pcm_f.readlines()
        
        # Write Arabic and PCM lines into their respective master files
        for arabic_line, pcm_line in zip(arabic_lines, pcm_lines):
            arabic_all_f.write(arabic_line)
            pcm_all_f.write(pcm_line)

print("Files concatenated into Arabic_all.txt and PCM_all.txt")
