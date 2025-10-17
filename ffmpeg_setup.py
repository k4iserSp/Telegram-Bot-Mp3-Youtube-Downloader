import os
import subprocess
import sys

def ensure_ffmpeg():
    ffmpeg_path = os.path.join("ffmpeg", "bin")
    ffmpeg_exec = os.path.join(ffmpeg_path, "ffmpeg")

    if not os.path.exists(ffmpeg_exec):
        print("📦 Descargando ffmpeg...")
        os.makedirs(ffmpeg_path, exist_ok=True)
        # Descarga y extrae el binario estático desde johnvansickle.com
        subprocess.run(
            "curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz "
            "| tar xJ --strip-components=1 -C ffmpeg/bin",
            shell=True,
            check=True
        )
    else:
        print("✅ ffmpeg ya disponible")

    return ffmpeg_path

if __name__ == "__main__":
    ensure_ffmpeg()
