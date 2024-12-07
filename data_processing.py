import os
import zipfile
import shutil

# files Paths
zip_file_path = "Arabic_PCM.zip"
extracted_folder = "Arabic_PCM"
arabic_folder = "Arabic"
pcm_folder = "PCM"

# first step Uncompress Files
def extract_zip(zip_file_path, extracted_folder):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_folder)

# Step 2: Organize Files into Arabic and PCM folders
def organize_files():
    os.makedirs(arabic_folder, exist_ok=True)
    os.makedirs(pcm_folder, exist_ok=True)

    for filename in os.listdir(extracted_folder):
        if filename.startswith("arabic"):
            shutil.move(os.path.join(extracted_folder, filename), os.path.join(arabic_folder, filename))
        elif filename.startswith("pcm"):
            shutil.move(os.path.join(extracted_folder, filename), os.path.join(pcm_folder, filename))

# Step 3: File Matching Ensure they have the same suffix
def match_files():
    arabic_files = sorted(os.listdir(arabic_folder))
    pcm_files = sorted(os.listdir(pcm_folder))

    # Check if files match by name
    matched_files = []
    for arabic_file in arabic_files:
        pcm_file = arabic_file.replace("arabic", "pcm")
        if pcm_file in pcm_files:
            matched_files.append((os.path.join(arabic_folder, arabic_file), os.path.join(pcm_folder, pcm_file)))
    return matched_files

# Step 4: Line Matching and creating a folder for mismatched files
def line_matching(matched_files):
    mismatched_folder = "Mismatched_Files"
    os.makedirs(mismatched_folder, exist_ok=True)

    for arabic_file, pcm_file in matched_files:
        with open(arabic_file, 'r') as f1, open(pcm_file, 'r') as f2:
            arabic_lines = f1.readlines()
            pcm_lines = f2.readlines()

        if len(arabic_lines) != len(pcm_lines):
            shutil.move(arabic_file, os.path.join(mismatched_folder, os.path.basename(arabic_file)))
            shutil.move(pcm_file, os.path.join(mismatched_folder, os.path.basename(pcm_file)))
    
    return matched_files

# Step 5: Concatenate Files into master files
def concatenate_files(matched_files):
    with open("Arabic_all.txt", 'w') as arabic_output, open("PCM_all.txt", 'w') as pcm_output:
        for arabic_file, pcm_file in matched_files:
            with open(arabic_file, 'r') as f1, open(pcm_file, 'r') as f2:
                arabic_output.write(f1.read())
                pcm_output.write(f2.read())

# Main 
extract_zip(zip_file_path, extracted_folder)
organize_files()
matched_files = match_files()
matched_files = line_matching(matched_files)
concatenate_files(matched_files)

print("Data processing completed. Arabic_all.txt and PCM_all.txt have been created.")
