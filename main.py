from fastapi import FastAPI
import yt_dlp

app = FastAPI()

@app.get("/search_and_play")
def search_and_play(query: str):
    # 'ytmusicsearch1:' memaksa yt-dlp mencari langsung di database YouTube Music
    # dan hanya mengambil 1 hasil paling atas yang paling akurat
    search_query = f"ytmusicsearch1:{query}"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True  # Menyembunyikan log berantakan di server
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Mengekstrak informasi lagu secara langsung dari YouTube Music tanpa download file
            info = ydl.extract_info(search_query, download=False)
            
            if 'entries' in info and len(info['entries']) > 0:
                track = info['entries'][0]
                return {
                    "status": "success",
                    "title": track.get('title'),
                    "artist": track.get('uploader'),
                    "stream_url": track.get('url')  # Ini URL audio mentah yang sudah didekripsi
                }
            else:
                return {"status": "error", "message": "Lagu tidak ditemukan"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
