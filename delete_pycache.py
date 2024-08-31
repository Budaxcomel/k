import os
import shutil

def delete_pycache(directory):
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                pycache_dir = os.path.join(root, dir_name)
                shutil.rmtree(pycache_dir)
                print(f"Deleted {pycache_dir}")

# Gantikan '.' dengan path ke direktori projek anda jika perlu
delete_pycache('.')
