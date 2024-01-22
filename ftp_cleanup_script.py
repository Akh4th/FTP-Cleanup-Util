import time
from ftplib import FTP, error_temp


ftp_host = "ftp.host.com" # Your FTP Hostname
ftp_port = 21 # Your FTP Port
ftp_user = "Username" # Your FTP Username
ftp_pswd = "P4$$W0rd" # Your FTP Password


def is_file(ftp, item):
    try:
        original_directory = ftp.pwd()
        ftp.cwd(item)
        ftp.cwd(original_directory)
        return False
    except Exception:
        return True


def list_files(ftp, path):
    files = []
    directories = []
    original_directory = ftp.pwd()
    try:
        ftp.cwd(path)
        items = ftp.nlst()
        for item in items:
            if item in [".", ".."]:
                continue
            item_path = f"{path}/{item}" if path != "/" else f"/{item}"
            if is_file(ftp, item_path):
                files.append(item_path)
            else:
                directories.append(item_path)
    finally:
        ftp.cwd(original_directory)
    return files, directories


def delete_directory(ftp, path):
    files, directories = list_files(ftp, path)
    for file in files:
        print(f"Deleting file: {file}")
        ftp.delete(file)
    for directory in directories:
        delete_directory(ftp, directory)
    print(f"Deleting directory: {path}")
    ftp.rmd(path)


def clear_directory(ftp, path):
    try:
        files, directories = list_files(ftp, path)
        for file in files:
            print(f"Deleting file: {file}")
            ftp.delete(file)
        for directory in directories:
            print(f"Deleting {directory}")
            delete_directory(ftp, directory)
    except Exception as e:
        print(f"Error clearing directory {path}: {e}")


def find_unnecessary_files(ftp, path, attempt=1):
    print(f"Working on the directory: '{path}'")
    try:
        ftp.voidcmd("NOOP")
        files, directories = list_files(ftp, path)
        for file in files:
            if file.endswith('.txt') or file.endswith('.zip') or file.endswith('.gzip'):
                print(f"Unnecessary file found: {file}")
                ftp.delete(file)
        for directory in directories:
            if 'backup' in directory or 'tmp' in directory:
                print(f"Deleting backup directory: {directory}")
                delete_directory(ftp, directory)
            else:
                find_unnecessary_files(ftp, directory)
    except (error_temp, ConnectionAbortedError) as e:
        print(f"Error: {e}")
        if attempt <= 3:
            time.sleep(5)
            print(f"Attempting to reconnect, attempt {attempt}")
            ftp = reconnect(ftp)
            find_unnecessary_files(ftp, path, attempt + 1)
        else:
            print("Failed to reconnect after several attempts.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def ftp_session():
    ftp = FTP(ftp_host)
    ftp.login(ftp_user, ftp_pswd)
    ftp.set_pasv(True)
    print("Successfully connected with FTP")
    return ftp


def reconnect(ftp):
    try:
        ftp.quit()
    except Exception:
        pass
    return ftp_session()


def main():
    ftp = ftp_session()
    try:
        clear_directory(ftp, '/tmp')
        find_unnecessary_files(ftp, '/')
    except Exception as e:
        print(f"An error occurred in main: {e}")
    finally:
        try:
            ftp.quit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
