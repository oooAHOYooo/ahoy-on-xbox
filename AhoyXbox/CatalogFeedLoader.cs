using System;
using System.Threading;
using System.Threading.Tasks;
using Windows.Data.Json;
using Windows.Storage;

namespace AhoyXbox
{
    internal static partial class PublishedVideoCatalog
    {
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

    internal static partial class PublishedMediaCatalog
    {
        internal static async Task<JsonObject> LoadAsync(string path, string cacheName, Action<JsonObject> validate)
        {
            try
            {
                using (var client = new Windows.Web.Http.HttpClient())
                using (var timeout = new CancellationTokenSource(TimeSpan.FromSeconds(10)))
                {
                    client.DefaultRequestHeaders.CacheControl.TryParseAdd("no-cache");
                    var json = await client.GetStringAsync(new Uri("https://app.ahoy.ooo" + path)).AsTask(timeout.Token);
                    var root = JsonObject.Parse(json);
                    validate(root);
                    try
                    {
                        var file = await ApplicationData.Current.LocalFolder.CreateFileAsync(cacheName, CreationCollisionOption.ReplaceExisting);
                        await FileIO.WriteTextAsync(file, json);
                    }
                    catch { }
                    return root;
                }
            }
            catch
            {
                try
                {
                    var file = await ApplicationData.Current.LocalFolder.GetFileAsync(cacheName);
                    var root = JsonObject.Parse(await FileIO.ReadTextAsync(file));
                    validate(root);
                    return root;
                }
                catch { return null; }
            }
        }

    }
}
