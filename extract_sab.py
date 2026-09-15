import urllib.request

ORIGINAL_URL = "https://premiumplugx.com/VIP/pluglist.php"
OUTPUT_FILE = "sony_sab_sd.m3u"
TARGET_KEYWORD = "sab"


def extract_single_channel():
  print("Fetching latest playlist from provider...")
  try:
    # Add a User-Agent header so the server doesn't block python requests
    req = urllib.request.Request(
        ORIGINAL_URL, headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req) as response:
      playlist_data = response.read().decode("utf-8", errors="ignore")
  except Exception as e:
    print(f"Error fetching playlist: {e}")
    return

  print(f"Total characters downloaded: {len(playlist_data)}")

  lines = playlist_data.splitlines()
  extracted_lines = ["#EXTM3U"]

  found = False
  for i in range(len(lines)):
    if TARGET_KEYWORD.lower() in lines[i].lower() and lines[i].startswith(
        "#EXTINF:"
    ):
      extracted_lines.append(lines[i])
      if i + 1 < len(lines):
        extracted_lines.append(lines[i + 1])
      found = True
      print(f"MATCH FOUND: {lines[i]}")
      break

  if found:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
      f.write("\n".join(extracted_lines))
    print(f"Success! Saved to '{OUTPUT_FILE}'.")
  else:
    print(f"ERROR: Downloaded data, but keyword '{TARGET_KEYWORD}' was not found.")
    # Create a dummy file anyway so git commit doesn't fail while we debug
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
      f.write("#EXTM3U\n#EXTINF:-1,Dummy File\nhttp://error.link")


if __name__ == "__main__":
  extract_single_channel()

