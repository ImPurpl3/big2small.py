# big2small.py v2 : ffmpeg toolbox by ImPurpl3

from tkinter import filedialog, Tk

import os
import time
import subprocess
import datetime
import yt_dlp

print("Welcome to ImPurpl3's ffmpeg toolbox : v2.0")
print("Select a file to work on")

root = Tk()
root.withdraw()

if os.name == "nt":
    root.iconbitmap("pack-32.ico")

file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Videos", ["*.mp4", "*.mov", "*.mkv", "*.webm"]), ("All files", "*.*")])

if not file_path:
    print("File dialog closed or cancelled, Closing toolbox!")
    exit()

fpath, fnamext = os.path.split(file_path)   # C:/Users/user/Videos, videofile.mp4
fext = os.path.splitext(file_path)[1]       # .mp4
fname = fnamext.removesuffix(fext)          # videofile
fpname = f"{fpath}/{fname}"                 # C:/Users/user/Videos/videofile

logpth = "./b2smol_logs/"
def close():
    print("\nProcessing done, Closing toolbox!")
    time.sleep(1)
    exit()

def fexists(file):
    f = os.path.isfile(file)

    if f == True:
        print("File already exists with desired output name!")
        again = input("Do you want to overwrite old file? [y/N]: ")
        if again.lower() == "y":
            os.remove(file)
            print("Removed old file!")
            return file
        else:
            addfname = input("Do you want to add to file name (i.e. video_cut_1.mp4)? [y/N]: ")
            if addfname.lower() == "y":
                pth, ext = os.path.splitext(file)
                nm = str(os.path.split(file)[1]).replace(ext, "")
                if len(nm) > 40:
                    addname = input(f"Adding: ...{nm[-40:]}_")
                else:
                    addname = input(f"Adding: {nm}_")

                newname = pth+"_"+addname+ext
                if os.path.isfile(newname) == False:
                    print(f"Running with new name: {newname}")
                    return newname
                else:
                    print("New name already exists! Closing toolbox")
                    exit()

            else:
                print("Ok, closing toolbox")
                exit()
    else:
        return file

def fps():
    '''change fps'''
    userfps = input("Enter desired FPS (30, 60): ")
    usercq = input("Enter desired CQR (4-lossless-19, 20-medium-29, 30-horrible-50): ")

    chkname = f"{fpname}_{userfps}fps.mp4"
    outfname = fexists(chkname)

    print(f"\nWorking on '{outfname}'...")
    os.system(f'ffmpeg -hwaccel cuvid -i "{file_path}" -vf "fps={userfps}" -c:v h264_nvenc -cq {usercq} "{outfname}" > "{logpth}{fname}.log" 2>&1')

def mkv():
    '''change mkv to mp4'''
    usercq = input("Enter desired CQR (4-lossless-19, 20-medium-29, 30-horrible-50): ")

    chkname = f"{fpname}_remuxed.mp4"
    outfname = fexists(chkname)

    print(f"\nWorking on '{outfname}'...")
    os.system(f'ffmpeg -hwaccel cuda -i "{file_path}" -map 0 -c:v h264_nvenc -rc vbr -cq {usercq} -qmin 14 -qmax 14 -b:v 0 -c:a copy "{outfname}" > "{logpth}{fname}.log" 2>&1')

def mp4():
    '''change anything to mp4'''
    usercq = input("Enter desired CQR (4-lossless-19, 20-medium-29, 30-horrible-50): ")

    chkname = f"{fpname}_remuxed.mp4"
    outfname = fexists(chkname)

    print(f"\nWorking on '{outfname}'...")
    os.system(f'ffmpeg -hwaccel cuda -i "{file_path}" -c:v h264_nvenc -cq {usercq} -c:a copy "{outfname}" > "{logpth}{fname}.log" 2>&1')

def webm():
    '''encode to webm with target quality'''
    usercq = input("Enter desired CQR (4-lossless-19, 20-medium-29, 30-horrible-50): ")

    chkname = f"{fpname}.webm"
    outfname = fexists(chkname)
    print(f"\nWorking on '{outfname}'...")

    os.system(f'ffmpeg -i "{file_path}" -c:v libvpx-vp9 -cq {usercq} "{outfname}" > "{logpth}{fname}.log" 2>&1')

def shorten():
    '''shorten'''
    ffdur = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path], capture_output=True, text=True)
    dur = float(ffdur.stdout.strip())

    fdur = str(datetime.timedelta(seconds=dur))
    if dur < 3600: fdur = fdur[2:]

    print(f"Duration: {fdur[:-3]}")

    ttstart = input("Enter start timestamp (hh:mm:ss): ")
    ttend = input("Enter end timestamp (hh:mm:ss): ")

    chkname = f"{fpname}_cut{fext}"
    outfname = fexists(chkname)
    print(f"\nWorking on '{outfname}'...")

    os.system(f'ffmpeg -ss {ttstart} -to {ttend} -i "{file_path}" -map 0:v -map 0:a -c copy -map_metadata 0 "{outfname}" > "{logpth}{fname}.log" 2>&1')

    delold = input("Delete old file? [y/N]: ")
    if delold.lower() == "y":
        os.remove(file_path)
        print(f"Deleted {file_path}")
    else:
        print("Keeping old file, closing toolbox")
        time.sleep(1)
        exit()

def flatten():
    '''flatten audio tracks'''
    pass

def boost():
    '''boost specific audio track'''
    pass

def concat():
    '''concat two videos'''
    file_path2 = filedialog.askopenfilename(title="Select a File", filetypes=[("Videos", ["*.mp4", "*.mov", "*.mkv", "*.webm"]), ("All files", "*.*")])

    if not file_path2:
        print("File dialog closed or cancelled, Closing toolbox!")
        exit()

    fpath2, fnamext2 = os.path.split(file_path2)   # C:/Users/user/Videos, videofile.mp4
    fext2 = os.path.splitext(file_path2)[1]        # .mp4
    fname2 = fnamext2.removesuffix(fext2)          # videofile
    fpname2 = f"{fpath2}/{fname2}"                 # C:/Users/user/Videos/videofile

    if fext2 != fext:
        print("Must use two files of same container type, Closing toolbox!")
        exit()

    concat_file = os.path.join(logpth, "concat.txt")

    if os.path.exists(concat_file):
        open(concat_file, "w").close()

    # Write the file paths of the input videos to concat.txt
    with open(concat_file, "a") as file:
        file.write(f"file '{file_path}'\n")
        file.write(f"file '{file_path2}'\n")

    os.system(f'ffmpeg -f concat -safe 0 -i "{logpth}/concat.txt" -c copy "{fpname}_joined{fext}" > "{logpth}{fname}.log" 2>&1')
    close()

def test():
    '''test cases'''
    print("Nothing to test")
    pass

def ytdlp():
    '''simple yt-dlp download best quality'''
    vid_url = input("Enter video url: ")

    with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True, 'no_warnings': True, 'extract_flat': True}) as ytvid:
        try:
            info = ytvid.extract_info(vid_url, download=False)
        except:
            close()
        vid_title = info.get('title', 'Title not found')

    print(f'Downloading "{vid_title}"...')

    keepcharacters = (' ','.','_')
    clean_title = "".join(c for c in vid_title if c.isalnum() or c in keepcharacters).rstrip()

    os.system(f'yt-dlp -f "(bv*[vcodec^=av01][format_id!*=-sr]/bv*[vcodec^=vp09][format_id!*=-sr]/bv*[vcodec^=vp9][format_id!*=-sr]/bv*[vcodec^=avc1][format_id!*=-sr]/bv*)+bestaudio" -S "vbr,asr,abr" -o "{fpath}/{clean_title}.%(ext)s" -w -v {vid_url} > "{logpth}{clean_title}.log" 2>&1')
    close()

def folder():
    '''batch convert folder'''
    convtype = input("File type to convert all files of: .")

    videos = [f for f in os.listdir(fpath) if os.path.isfile(os.path.join(fpath, f)) and os.path.splitext(f)[1] == f".{convtype}"]
    if len(videos) == 0:
        print(f"No files with .{convtype} extension detected in this folder, closing toolbox")
        exit()
    
    usercq = input("Enter desired CQR (4-lossless-19, 20-medium-29, 30-horrible-50): ")

    for video in videos:
        infname = f"{fpath}/{video}"
        jname = os.path.splitext(video)[0]
        chkname = f"{fpath}/{jname}.mp4"
        # chkname = f"{fpath}/{jname}.jpg"
        outfname = fexists(chkname)
        print(f'Converting "{video}"... [{videos.index(video)+1}/{len(videos)}]')
        os.system(f'ffmpeg -hwaccel cuda -i "{infname}" -c:v h264_nvenc -cq {usercq} -c:a copy "{outfname}" > "{logpth}{jname}.log" 2>&1')
        # os.system(f'magick "{infname}" -quality 98 "{outfname}"')
    
    exit()

# now lets ask what process we want to invoke!!!!
userproc = input("Which process do you want? (fps, mp4, mkv, webm, shorten, flatten, boost, join, yt-dlp, folder): ")
print()
match userproc:
    case "fps":
        fps()
    case "mp4":
        mp4()
    case "mkv":
        mkv()
    case "webm":
        webm()
    case "shorten":
        shorten()
    case "flatten":
        flatten()
    case "boost":
        boost()
    case "join":
        concat()
    case "folder":
        folder()
    case "yt-dlp":
        ytdlp()
    case "test":
        test()
    case _:
        print("Invalid input! Closing toolbox")
        exit()

close()
