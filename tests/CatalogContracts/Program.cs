using System;
using System.Collections.Generic;
using AhoyXbox;
using Windows.Data.Json;

namespace AhoyXbox
{
    public sealed class Video
    {
        public string Id, Title, Host, Description, Duration, Url, Thumbnail, Category;
        public List<string> Tags;
    }
    public sealed class Channel
    {
        public string Number, Name, Tagline;
        public List<Video> Videos;
    }
}

internal static class Program
{
    private static int checks;
    private static void Check(bool condition, string message)
    {
        if (!condition) throw new Exception(message);
        checks++;
    }
    private static void Reject(Action action, string message)
    {
        try { action(); }
        catch { checks++; return; }
        throw new Exception(message);
    }
    private static void Main()
    {
        const string duo = "{\"id\":\"duo\",\"title\":\"DUO 4K\",\"video_url\":\"https://media.example/duo.mp4\",\"thumbnail\":\"/static/duo.jpg\",\"category\":\"Skateboarding\",\"duration_seconds\":187,\"tags\":[\"skating\",null,5]}";
        var videos = PublishedVideoCatalog.Normalize("{\"shows\":[" + duo + "," + duo + ",{\"id\":\"unsafe\",\"video_url\":\"http://example/a\"},null]}");
        Check(videos.Count == 1, "Deduplicate video IDs and skip invalid entries");
        var video = videos[0].GetObject();
        Check(video.GetNamedString("duration") == "3:07", "Duration conversion");
        Check(video.GetNamedString("category") == "skating", "DUO skating category");
        Check(video.GetNamedString("thumbnail") == "https://app.ahoy.ooo/static/duo.jpg", "Relative image resolution");
        Check(video.GetNamedArray("tags").Count == 1, "Ignore non-string tags");
        Check(PublishedVideoCatalog.Normalize("{\"shows\":[]}").Count == 0, "Respect authoritative empty feed");
        Reject(() => PublishedVideoCatalog.Normalize("{\"shows\":[{\"id\":\"a\",\"video_url\":\"http://example/a\"}]}"), "Reject unusable feed before caching");
        Reject(() => PublishedVideoCatalog.Normalize("{\"tracks\":[]}"), "Reject wrong feed schema");
        var audio = PublishedMediaCatalog.Audio(JsonArray.Parse("[{\"id\":\"a\",\"audio_url\":\"https://media.example/a.mp3\",\"cover_art\":\"/art.jpg\",\"duration_seconds\":190},{\"id\":\"b\",\"stream_url\":\"https://media.example/b.mp3\"}]"), false);
        Check(audio.Count == 2, "Support API and bundled audio formats");
        Check(audio[0].Duration == "3:10" && audio[0].Thumbnail == "https://app.ahoy.ooo/art.jpg", "Music metadata");
        Check(PublishedMediaCatalog.Audio(new JsonArray(), true).Count == 0, "Respect empty radio feed");
        Reject(() => PublishedMediaCatalog.Audio(JsonArray.Parse("[{\"id\":\"bad\",\"audio_url\":\"file:///a.mp3\"}]"), false), "Reject unsafe audio feed");
        var channels = PublishedMediaCatalog.Channels(JsonObject.Parse("{\"channels\":[{\"id\":\"live-shows\",\"name\":\"Renamed by API\",\"items\":[" + duo + "," + duo + "]}]}"));
        Check(channels[0].Name == "Renamed by API", "Channel names come from API");
        Check(channels[0].Videos.Count == 2, "Preserve rotation repeats and order");
        Check(PublishedMediaCatalog.Channels(JsonObject.Parse("{\"channels\":[]}")).Count == 0, "Respect empty channel feed");
        Console.WriteLine(checks + " catalog contract checks passed.");
    }
}
