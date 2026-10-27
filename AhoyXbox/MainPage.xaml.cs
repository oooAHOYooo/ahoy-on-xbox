using System;
using System.Collections.Generic;
using System.Linq;
using Windows.Data.Json;
using Windows.Media.Core;
using Windows.Media.Playback;
using Windows.Storage;
using Windows.UI.Core;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;

namespace AhoyXbox
{
    public static class SavedStore
    {
        private const string Key = "Ahoy_Saved_Ids";
        private static readonly HashSet<string> savedIds = new HashSet<string>();

        static SavedStore()
        {
            try
            {
                var settings = Windows.Storage.ApplicationData.Current.LocalSettings;
                if (settings.Values.TryGetValue(Key, out var val) && val is string csv && !string.IsNullOrEmpty(csv))
                {
                    foreach (var id in csv.Split(new[] { ',' }, StringSplitOptions.RemoveEmptyEntries))
                        savedIds.Add(id.Trim());
                }
            }
            catch { }
        }

        public static bool Contains(string id) => !string.IsNullOrEmpty(id) && savedIds.Contains(id);

        public static bool Toggle(string id)
        {
            if (string.IsNullOrEmpty(id)) return false;
            bool added = savedIds.Contains(id) ? savedIds.Remove(id) && false : savedIds.Add(id);
            try
            {
                var settings = Windows.Storage.ApplicationData.Current.LocalSettings;
                settings.Values[Key] = string.Join(",", savedIds);
            }
            catch { }
            return added;
        }
    }

    public sealed class Video
    {
        public string Id { get; set; }
        public string Title { get; set; }
        public string Host { get; set; }
        public string Url { get; set; }
        public string Category { get; set; }
        public List<string> Tags { get; set; }
        public bool IsSaved => SavedStore.Contains(Id);
    }
    public sealed class Channel
    {
        public string Name { get; set; }
        public List<Video> Videos { get; set; }
        public string CountLabel => Videos.Count + " videos · continuous queue";
    }
    public sealed partial class MainPage : Page
    {
        private readonly MediaPlayer media = new MediaPlayer();
        private Channel playingChannel;
        private int playingIndex;
        public MainPage()
        {
            InitializeComponent();
            Player.SetMediaPlayer(media);
            media.MediaEnded += Ended;
            media.MediaFailed += Failed;
            Loaded += LoadCatalog;
            Unloaded += Cleanup;
            SystemNavigationManager.GetForCurrentView().BackRequested += Back;
            KeyDown += (s, e) => {
                if (e.Key == Windows.System.VirtualKey.GamepadX || e.Key == Windows.System.VirtualKey.X)
                {
                    if (Programs.SelectedItem is Video v)
                    {
                        bool isSaved = SavedStore.Toggle(v.Id);
                        Status.Text = isSaved ? $"★ {v.Title} saved to Library!" : $"{v.Title} removed from Library.";
                    }
                }
            };
        }
        private async void LoadCatalog(object sender, RoutedEventArgs e)
        {
            string json = null;
            try
            {
                using (var client = new Windows.Web.Http.HttpClient())
                {
                    client.DefaultRequestHeaders.UserAgent.ParseAdd("AhoyTV/1.0");
                    json = await client.GetStringAsync(new Uri("https://raw.githubusercontent.com/oooAHOYooo/ahoy-on-xbox/main/AhoyXbox/Data/catalog.json"));
                }
            }
            catch { }

            if (string.IsNullOrEmpty(json))
            {
                try
                {
                    var file = await StorageFile.GetFileFromApplicationUriAsync(new Uri("ms-appx:///Data/catalog.json"));
                    json = await FileIO.ReadTextAsync(file);
                }
                catch (Exception)
                {
                    Status.Text = "The catalog could not load. Close and reopen Ahoy to retry.";
                    return;
                }
            }

            try
            {
                var root = JsonObject.Parse(json);
                var videos = root.GetNamedArray("videos").Select(value => {
                    var row = value.GetObject();
                    return new Video {
                        Id = row.GetNamedString("id", Guid.NewGuid().ToString()),
                        Title = row.GetNamedString("title", "Untitled"), Host = row.GetNamedString("host", "Ahoy"),
                        Url = row.GetNamedString("url", ""), Category = row.GetNamedString("category", ""),
                        Tags = row.ContainsKey("tags") ? row.GetNamedArray("tags").Select(t => t.GetString()).ToList() : new List<string>()
                    };
                }).Where(v => Uri.TryCreate(v.Url, UriKind.Absolute, out var uri) && uri.Scheme == "https").ToList();
                var channels = new List<Channel> { new Channel { Name = "Ahoy TV (Mix)", Videos = videos } };
                AddChannel(channels, "Wintergreen Studios", videos.Where(v => v.Tags.Contains("wintergreen-sessions") || v.Host.Contains("Wintergreen")));
                AddChannel(channels, "Music Videos", videos.Where(v => v.Tags.Contains("music-video")));
                AddChannel(channels, "Skating", videos.Where(v => v.Category == "skating" || v.Tags.Contains("skating")));
                AddChannel(channels, "Saved", videos.Where(v => SavedStore.Contains(v.Id)));
                Channels.ItemsSource = channels;
                Channels.SelectedIndex = 0;
                Channels.Focus(FocusState.Programmatic);
                Status.Text = "Choose a video to start its channel. Live catalog synced.";
            }
            catch (Exception) { Status.Text = "The catalog could not load. Close and reopen Ahoy to retry."; }
        }
        private static void AddChannel(List<Channel> channels, string name, IEnumerable<Video> videos)
        {
            var list = videos.ToList();
            if (list.Count > 0) channels.Add(new Channel { Name = name, Videos = list });
        }
        private void ChannelChanged(object sender, SelectionChangedEventArgs e)
        {
            if (Channels.SelectedItem is Channel channel) Programs.ItemsSource = channel.Videos;
        }
        private void PlayClicked(object sender, ItemClickEventArgs e)
        {
            if (!(Channels.SelectedItem is Channel channel) || !(e.ClickedItem is Video video)) return;
            playingChannel = channel;
            playingIndex = channel.Videos.IndexOf(video);
            PlayCurrent();
        }
        private void PlayCurrent()
        {
            if (playingChannel == null || playingChannel.Videos.Count == 0) return;
            var video = playingChannel.Videos[playingIndex];
            NowPlaying.Text = video.Title;
            Status.Text = playingChannel.Name + " · " + video.Host + " · Next video plays automatically";
            try { media.Source = MediaSource.CreateFromUri(new Uri(video.Url)); media.Play(); }
            catch (Exception) { Status.Text = "This video could not open. Select another video to continue."; }
        }
        private async void Ended(MediaPlayer sender, object args)
        {
            await Dispatcher.RunAsync(CoreDispatcherPriority.Normal, () => {
                if (playingChannel == null) return;
                playingIndex = (playingIndex + 1) % playingChannel.Videos.Count;
                PlayCurrent();
            });
        }
        private async void Failed(MediaPlayer sender, MediaPlayerFailedEventArgs args)
        {
            await Dispatcher.RunAsync(CoreDispatcherPriority.Normal, () => {
                Status.Text = "Playback stopped. Check your connection, then select a video to retry.";
            });
        }
        private void Back(object sender, BackRequestedEventArgs e)
        {
            if (Player.IsFullWindow) { Player.IsFullWindow = false; e.Handled = true; }
        }
        private void Cleanup(object sender, RoutedEventArgs e)
        {
            SystemNavigationManager.GetForCurrentView().BackRequested -= Back;
            media.MediaEnded -= Ended;
            media.MediaFailed -= Failed;
            media.Dispose();
        }
    }
}
