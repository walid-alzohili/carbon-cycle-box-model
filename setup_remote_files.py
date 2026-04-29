"""Doandload needed assets from server."""

import httpx

url_ = "https://vormada.com/share/carbon_modeling/assets.zip"
output_path_ = "assets.zip"


def calculate_progress(total_size: int, downloaded: int) -> None:
    """Calculate doanload progress."""
    if total_size > 0:
        percent = (downloaded / total_size) * 100
        print(f"\rDownloading: {round(percent)}%", end="")
    else:
        print(f"\rDownloading: {downloaded} bytes...", end="")


def download_assets(url: str, output_path: str) -> None:
    """Download a remote file."""
    print(f"📦 Downloading assets from {url}")

    try:
        with httpx.stream("GET", url, follow_redirects=True) as response:
            # Ensure the request was successful
            response.raise_for_status()

            total_size = int(response.headers.get("Content-Length", 0))
            downloaded = 0

            with open(output_path, "wb") as f:
                for chunk in response.iter_bytes(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    calculate_progress(total_size, downloaded)

        print("\n✅ Done! Assets are ready in the project root.")

    except httpx.HTTPStatusError as e:
        print(f"\n❌ HTTP Error: {e.response.status_code}")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    download_assets(url_, output_path_)
