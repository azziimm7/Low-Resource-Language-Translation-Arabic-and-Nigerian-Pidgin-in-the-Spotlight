import zipfile
import os
import shutil

# File paths
zip_file_path = 'Arabic_PCM.zip'
extract_folder = 'Arabic_PCM_extracted'
arabic_folder = os.path.join(extract_folder, 'Arabic')
pcm_folder = os.path.join(extract_folder, 'PCM')
mismatch_folder = os.path.join(extract_folder, 'Mismatches')

# Create necessary folders
os.makedirs(arabic_folder, exist_ok=True)
os.makedirs(pcm_folder, exist_ok=True)
os.makedirs(mismatch_folder, exist_ok=True)

# Extract ZIP file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_folder)

# Move files to corresponding folders
arabic_source = os.path.join(extract_folder, 'arbwbtc_readaloud')
pcm_source = os.path.join(extract_folder, 'pcm_readaloud')

for file in os.listdir(arabic_source):
    shutil.move(os.path.join(arabic_source, file), os.path.join(arabic_folder, file))

for file in os.listdir(pcm_source):
    shutil.move(os.path.join(pcm_source, file), os.path.join(pcm_folder, file))

# Function to extract the full suffix from filenames
def extract_suffix(filename):
    return "_".join(filename.split("_")[1:4]) + "_read.txt"

# Create lookup dictionaries
arabic_dict = {extract_suffix(f): f for f in os.listdir(arabic_folder)}
pcm_dict = {extract_suffix(f): f for f in os.listdir(pcm_folder)}

# Open master files
arabic_master = open('Arabic_all.txt', 'w', encoding='utf-8')
pcm_master = open('PCM_all.txt', 'w', encoding='utf-8')

# Match files and compare line counts
matched_files = 0
for suffix, arabic_file in arabic_dict.items():
    if suffix in pcm_dict:
        arabic_path = os.path.join(arabic_folder, arabic_file)
        pcm_path = os.path.join(pcm_folder, pcm_dict[suffix])

        with open(arabic_path, 'r', encoding='utf-8') as a_file, open(pcm_path, 'r', encoding='utf-8') as p_file:
            arabic_lines = a_file.readlines()
            pcm_lines = p_file.readlines()

            if len(arabic_lines) == len(pcm_lines):
                arabic_master.writelines(arabic_lines)
                pcm_master.writelines(pcm_lines)
                matched_files += 1
            else:
                shutil.move(arabic_path, os.path.join(mismatch_folder, arabic_file))
                shutil.move(pcm_path, os.path.join(mismatch_folder, pcm_dict[suffix]))
    else:
        print(f"No matching PCM file for {arabic_file}")

# Close master files
arabic_master.close()
pcm_master.close()

print(f"Matched files: {matched_files}")
print("Mismatched files moved to mismatched_files")
print("Files concatenated into Arabic_all.txt and PCM_all.txt")
