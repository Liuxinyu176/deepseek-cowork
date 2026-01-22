import sys
import subprocess
import os

def _ensure_dependency(package_name):
    """
    Ensure a python package is installed.
    """
    try:
        __import__(package_name)
    except ImportError:
        print(f"Installing missing dependency: {package_name}...")
        
        # Determine the correct python executable
        # In PyInstaller frozen environment, sys.executable is the .exe itself, 
        # which usually cannot run 'pip'. We need to find the underlying python interpreter 
        # or bundle pip within the exe (complex). 
        # For this v2.0 simplification, if frozen, we assume standard system python might be available
        # or we gracefully fail if we can't find a pip-capable python.
        
        python_exe = sys.executable
        if getattr(sys, 'frozen', False):
            # Try to find a system python fallback
            # This is a limitation of PyInstaller onefile/onedir without embedded python runtime for pip
            # A common workaround is to assume 'python' is in PATH
            import shutil
            if shutil.which("python"):
                python_exe = "python"
            else:
                 raise RuntimeError("Cannot install dependencies in frozen mode without system Python. Please install 'yt-dlp' manually or ensure 'python' is in your PATH.")

        try:
            # On Windows, we want to suppress the new window for the subprocess
            startupinfo = None
            if sys.platform == 'win32':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                
            subprocess.check_call(
                [python_exe, "-m", "pip", "install", package_name],
                startupinfo=startupinfo
            )
            print(f"Successfully installed {package_name}.")
            # In frozen mode, even if we install to system python, we might not be able to import it 
            # if the frozen app is isolated. 
            # However, since we are dynamically importing, if we installed to the *same* environment 
            # that the app is running in (not possible for frozen), or if we are just calling a subprocess later...
            # 
            # Wait, if we are in frozen mode, we CANNOT easily 'import' a newly installed package 
            # into the running process because sys.path is fixed to the MEIPASS/executable.
            # 
            # CORRECTION for V3.0 Architecture:
            # Skills that require new dependencies should ideally run as *subprocesses* using the system python,
            # rather than trying to import them into the frozen Agent process.
            # 
            # But for this specific 'import yt_dlp' style, it only works reliably in source mode.
            # For frozen mode compatibility, we should probably prefer the CLI wrapper approach 
            # or warn the user.
            
            # For now, let's try to let the import happen if possible (e.g. if not frozen),
            # or re-raise if we are frozen and can't import.
            if getattr(sys, 'frozen', False):
                 print("Warning: Dependency installed to system Python, but frozen app may not see it. It is recommended to run from source for dynamic dependency management.")

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to install {package_name}: {str(e)}")

def download_video(url, output_dir=None):
    """
    Download a video from YouTube or other sites using yt-dlp.
    Automatically installs yt-dlp if missing.

    Args:
        url (str): The URL of the video or playlist.
        output_dir (str, optional): Directory to save the video. Defaults to 'downloads' in current workspace.
    
    Returns:
        str: Result message indicating success or failure.
    """
    # 1. Dependency Check & Auto-Install
    try:
        # Check for yt_dlp (package name uses underscore)
        _ensure_dependency("yt_dlp")
        import yt_dlp
    except Exception as e:
        return f"Error: Failed to install or import yt-dlp. {str(e)}"

    # 2. Setup Output Directory
    if not output_dir:
        # Get the workspace root from where the script is likely running, or just use current cwd
        output_dir = os.path.join(os.getcwd(), "downloads")
    
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except OSError as e:
            return f"Error: Could not create output directory '{output_dir}'. {str(e)}"

    # 3. Configure yt-dlp
    ydl_opts = {
        'format': 'best', # Download best single file (avoids ffmpeg merge requirement for simple use cases)
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True, # Keep going if one video in playlist fails
    }

    # 4. Execute Download
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # extract_info with download=True performs the download
            info = ydl.extract_info(url, download=True)
            
            # Handle playlist vs single video
            if 'entries' in info:
                return f"Successfully processed playlist: {info.get('title', 'Unknown')}. Saved to {output_dir}"
            else:
                filename = ydl.prepare_filename(info)
                return f"Successfully downloaded: {os.path.basename(filename)} to {output_dir}"
                
    except Exception as e:
        return f"Error during download: {str(e)}"
