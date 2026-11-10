using System;
using System.Collections.Generic;
using Windows.Data.Json;

namespace AhoyXbox
{
    internal static partial class PublishedMediaCatalog
    {
        internal static List<Video> Audio(JsonArray rows, bool radio)
        {
            var result = new List<Video>();
            foreach (var value in rows)
            {
                if (value.ValueType != JsonValueType.Object) continue;
                var row = value.GetObject();
                var url = PublishedVideoCatalog.Text(row, "audio_url");
                if (string.IsNullOrWhiteSpace(url)) url = PublishedVideoCatalog.Text(row, "stream_url");
                Uri uri;
                if (!Uri.TryCreate(url, UriKind.Absolute, out uri) || uri.Scheme != "https") continue;
                var id = PublishedVideoCatalog.Text(row, "id");
                if (string.IsNullOrWhiteSpace(id)) continue;
                var thumb = PublishedVideoCatalog.Text(row, "cover_art");
                if (string.IsNullOrWhiteSpace(thumb)) thumb = PublishedVideoCatalog.Text(row, "thumbnail");
                if (thumb.StartsWith("/")) thumb = new Uri(new Uri("https://app.ahoy.ooo"), thumb).AbsoluteUri;
                var duration = row.GetNamedNumber("duration_seconds", 0);
                if (duration < 0 || duration > int.MaxValue || double.IsNaN(duration)) duration = 0;
                var seconds = (int)duration;
                result.Add(new Video {
                    Id = id, Title = PublishedVideoCatalog.Text(row, "title", "Untitled Track"),
                    Host = PublishedVideoCatalog.Text(row, "artist", "Ahoy"),
                    Description = PublishedVideoCatalog.Text(row, "description", PublishedVideoCatalog.Text(row, "album")),
                    Url = url, Thumbnail = thumb, Duration = seconds > 0 ? $"{seconds / 60}:{seconds % 60:00}" : "",
                    Category = radio ? "radio" : "music", Tags = new List<string> { radio ? "radio" : "music", "audio" }
                });
            }
            if (rows.Count > 0 && result.Count == 0) throw new FormatException("No playable audio in feed.");
            return result;
        }

        internal static List<Channel> Channels(JsonObject root)
        {
            var result = new List<Channel>();
            foreach (var value in root.GetNamedArray("channels"))
            {
                var row = value.GetObject();
                // Reuse the public-video adapter for schedule items; keep repeats and server ordering.
                var videos = new List<Video>();
                foreach (var item in row.GetNamedArray("items"))
                {
                    var normalized = PublishedVideoCatalog.Normalize(new JsonObject {
                        ["shows"] = new JsonArray { item }
                    }.Stringify());
                    foreach (var entry in normalized)
                    {
                        var video = entry.GetObject();
                        videos.Add(new Video {
                            Id = video.GetNamedString("id"), Title = video.GetNamedString("title"),
                            Host = video.GetNamedString("host"), Description = video.GetNamedString("description"),
                            Duration = video.GetNamedString("duration"), Url = video.GetNamedString("url"),
                            Thumbnail = video.GetNamedString("thumbnail"), Category = video.GetNamedString("category"),
                            Tags = new List<string>()
                        });
                    }
                }
                var id = PublishedVideoCatalog.Text(row, "id");
                result.Add(new Channel {
                    Number = id == "live-shows" ? "101" : id == "music-videos" ? "102" : id == "films" ? "103" : id == "misc" ? "104" : (105 + result.Count).ToString(),
                    Name = PublishedVideoCatalog.Text(row, "name", "Ahoy"),
                    Tagline = "AHOY TV rotation", Videos = videos
                });
            }
            return result;
        }
    }
}
