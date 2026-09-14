import urllib.request

# Your dynamic provider link
ORIGINAL_URL = "https://premiumplugx.com/VIP/pluglist.php"
OUTPUT_FILE = "sony_sab_sd.m3u"

# Search term for the channel you want to extract
TARGET_CHANNEL = "Sony SAB SD"


def extract_single_channel():
  print("Fetching latest playlist from provider...")
  try:
    req = urllib.request.urlopen(ORIGINAL_URL)
    playlist_data = req.read().decode("utf-8")
  except Exception as e:
    print(f"Error fetching playlist: {e}")
    return

  lines = playlist_data.splitlines()
  extracted_lines = ["#EXTM3U"]  # M3U header

  found = False
  for i in range(len(lines)):
    # Look for the target channel in the metadata line
    if TARGET_CHANNEL.lower() in lines[i].lower() and lines[i].startswith(
        "#EXTINF:"
    ):
      # Grab the metadata line and the very next line (which is the stream URL)
      extracted_lines.append(lines[i])
      if i + 1 < len(lines):
        extracted_lines.append(lines[i + 1])
      found = True
      break

  if found:
    # Save only this channel to the output file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
      f.write("\n".join(extracted_lines))
    print(
        f"Success! '{TARGET_CHANNEL}' was found and saved to '{OUTPUT_FILE}'."
    )
  else:
    print(
        f"Could not find '{TARGET_CHANNEL}' in the playlist. Check the exact"
        " name."
    )


if __name__ == "__main__":
  extract_single_channel()

