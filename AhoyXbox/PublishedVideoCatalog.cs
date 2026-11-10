using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Windows.Data.Json;
using Windows.Storage;

namespace AhoyXbox
{
    internal static class PublishedVideoCatalog
    {
        private const string CacheFile = "published-videos-v1.json";

        internal static string Text(JsonObject row, string key, string fallback = "")
        {
            IJsonValue value;
            return row.TryGetValue(key, out value) && value.ValueType == JsonValueType.String
                ? value.GetString() : fallback;
        }

        internal static JsonArray Normalize(string json)
        {
            var shows = JsonObject.Parse(json).GetNamedArray("shows");
            var videos = new JsonArray();
            var ids = new HashSet<string>();
            foreach (var value in shows)
            {
                if (value.ValueType != JsonValueType.Object) continue;
                var row = value.GetObject();
                var id = Text(row, "id", Text(row, "video_id"));
                var url = Text(row, "video_url");
                if (string.IsNullOrWhiteSpace(url)) url = Text(row, "url");
                Uri uri;
                if (string.IsNullOrWhiteSpace(id) || !Uri.TryCreate(url, UriKind.Absolute, out uri)
                    || uri.Scheme != "https" || !ids.Add(id)) continue;
                var category = Text(row, "category").ToLowerInvariant();
                if (category == "skateboarding") category = "skating";
                if (category == "music video") category = "music";
                var tags = new JsonArray();
                IJsonValue tagValue;
                if (row.TryGetValue("tags", out tagValue) && tagValue.ValueType == JsonValueType.Array)
                    foreach (var tag in tagValue.GetArray())
                        if (tag.ValueType == JsonValueType.String) tags.Add(tag);
                var duration = Text(row, "duration");
                IJsonValue seconds;
                if (row.TryGetValue("duration_seconds", out seconds) && seconds.ValueType == JsonValueType.Number)
                {
                    var count = seconds.GetNumber();
                    if (count >= 0 && count <= int.MaxValue)
                    {
                        var total = (int)count;
                        duration = total >= 3600 ? $"{total / 3600}:{total / 60 % 60:00}:{total % 60:00}"
                            : $"{total / 60}:{total % 60:00}";
                    }
                }
                var thumbnail = Text(row, "thumbnail");
                if (thumbnail.StartsWith("/")) thumbnail = new Uri(new Uri("https://app.ahoy.ooo"), thumbnail).AbsoluteUri;
                videos.Add(new JsonObject {
                    ["id"] = JsonValue.CreateStringValue(id),
                    ["title"] = JsonValue.CreateStringValue(Text(row, "title", "Untitled")),
                    ["host"] = JsonValue.CreateStringValue(Text(row, "host", "Ahoy")),
                    ["description"] = JsonValue.CreateStringValue(Text(row, "description")),
                    ["duration"] = JsonValue.CreateStringValue(duration),
                    ["url"] = JsonValue.CreateStringValue(url),
                    ["thumbnail"] = JsonValue.CreateStringValue(thumbnail),
                    ["category"] = JsonValue.CreateStringValue(category),
                    ["tags"] = tags
                });
            }
            if (shows.Count > 0 && videos.Count == 0)
                throw new FormatException("Published catalog contains no playable videos.");
            return videos;
        }

        internal static async Task<JsonArray> LoadAsync()
        {
            try
            {
                using (var client = new Windows.Web.Http.HttpClient())
                using (var timeout = new CancellationTokenSource(TimeSpan.FromSeconds(10)))
                {
                    client.DefaultRequestHeaders.UserAgent.ParseAdd("AhoyTV/0.4.1");
                    client.DefaultRequestHeaders.CacheControl.TryParseAdd("no-cache");
                    var json = await client.GetStringAsync(new Uri("https://app.ahoy.ooo/api/shows")).AsTask(timeout.Token);
                    var videos = Normalize(json);
                    try
                    {
                        var cache = await ApplicationData.Current.LocalFolder.CreateFileAsync(CacheFile, CreationCollisionOption.ReplaceExisting);
                        await FileIO.WriteTextAsync(cache, json);
                    }
                    catch { /* A full disk must not prevent using the current feed. */ }
                    return videos;
                }
            }
            catch
            {
                try
                {
                    var cache = await ApplicationData.Current.LocalFolder.GetFileAsync(CacheFile);
                    return Normalize(await FileIO.ReadTextAsync(cache));
                }
                catch { return null; } // Caller retains the packaged fallback.
            }
        }
    }
}
