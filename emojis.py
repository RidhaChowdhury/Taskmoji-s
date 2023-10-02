import csv
import emoji

# Get emojis and their names
emoji_dict = emoji.EMOJI_DATA
emoji_list = [(emj, name["en"]) for emj, name in emoji_dict.items()]

# Save to CSV file
with open('unicode_emojis_and_names.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Emoji', 'Name'])  # Write header
    for emj, name in emoji_list:
        cleaned_name = name[1:-1].replace('_', ' ')  # Remove colons and replace underscores
        writer.writerow([emj, cleaned_name])
