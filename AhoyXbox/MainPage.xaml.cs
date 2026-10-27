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
        public string Number { get; set; }
        public string Name { get; set; }
        public string Tagline { get; set; }
        public List<Video> Videos { get; set; }
        public string CountLabel => Videos.Count + " in rotation";
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
                    ToggleSaveCurrent();
                }
                else if (e.Key == Windows.System.VirtualKey.GamepadY || e.Key == Windows.System.VirtualKey.Y)
                {
                    Player.IsFullWindow = !Player.IsFullWindow;
                }
                else if (e.Key == Windows.System.VirtualKey.GamepadB || e.Key == Windows.System.VirtualKey.B)
                {
                    if (Player.IsFullWindow)
                    {
                        Player.IsFullWindow = false;
                        e.Handled = true;
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
                        Title = row.GetNamedString("title", "Untitled"),
                        Host = row.GetNamedString("host", "Ahoy"),
                        Url = row.GetNamedString("url", ""),
                        Category = row.GetNamedString("category", ""),
                        Tags = row.ContainsKey("tags") ? row.GetNamedArray("tags").Select(t => t.GetString()).ToList() : new List<string>()
                    };
                }).Where(v => Uri.TryCreate(v.Url, UriKind.Absolute, out var uri) && uri.Scheme == "https").ToList();

                // EXACTLY 4 CANONICAL CHANNELS (Matches app.ahoy.ooo backend /api/live-tv/channels)
                var liveShowsVideos = videos.Where(v => v.Category == "live show" || v.Tags.Contains("wintergreen-sessions") || v.Tags.Contains("live")).ToList();
                if (liveShowsVideos.Count == 0) liveShowsVideos = videos.Take(10).ToList();

                var musicVideos = videos.Where(v => v.Tags.Contains("music-video") || v.Tags.Contains("music")).ToList();
                // Augment Music Videos with audio tracks from music.json
                try
                {
                    var musicFile = await StorageFile.GetFileFromApplicationUriAsync(new Uri("ms-appx:///Data/music.json"));
                    var musicJson = await FileIO.ReadTextAsync(musicFile);
                    var musicRoot = JsonObject.Parse(musicJson);
                    if (musicRoot.ContainsKey("tracks"))
                    {
                        var musicArray = musicRoot.GetNamedArray("tracks");
                        var tracks = musicArray.Select(t => {
                            var row = t.GetObject();
                            return new Video {
                                Id = row.GetNamedString("track_id", Guid.NewGuid().ToString()),
                                Title = row.GetNamedString("title", "Untitled Track"),
                                Host = row.GetNamedString("artist", "Ahoy Music"),
                                Url = row.GetNamedString("audio_url", ""),
                                Category = "music",
                                Tags = new List<string> { "music", "audio" }
                            };
                        }).Where(v => Uri.TryCreate(v.Url, UriKind.Absolute, out var uri) && uri.Scheme == "https").ToList();
                        musicVideos.AddRange(tracks);
                    }
                }
                catch { }
                if (musicVideos.Count == 0) musicVideos = videos;

                var filmVideos = videos.Where(v => v.Category == "film" || v.Category == "skating" || v.Tags.Contains("short-film") || v.Tags.Contains("skating")).ToList();
                if (filmVideos.Count == 0) filmVideos = videos;

                var miscVideos = videos; // Continuous 24/7 Mix

                var channels = new List<Channel>
                {
                    new Channel { Number = "101", Name = "Live Shows", Tagline = "Wintergreen Sessions & Live Concerts", Videos = liveShowsVideos },
                    new Channel { Number = "102", Name = "Music Videos", Tagline = "Premieres, Visuals & Soundscapes", Videos = musicVideos },
                    new Channel { Number = "103", Name = "Films", Tagline = "Skate Tapes, Documentaries & Shorts", Videos = filmVideos },
                    new Channel { Number = "104", Name = "Misc", Tagline = "Continuous Cultural Mix & Curations", Videos = miscVideos }
                };

                Channels.ItemsSource = channels;
                Channels.SelectedIndex = 0;
                Channels.Focus(FocusState.Programmatic);

                // Auto-Play Channel 101 immediately (Pluto TV behavior)
                playingChannel = channels[0];
                playingIndex = 0;
                Programs.ItemsSource = playingChannel.Videos;
                PlayCurrent();
            }
            catch (Exception)
            {
                Status.Text = "The catalog could not load. Close and reopen Ahoy to retry.";
            }
        }

        private void ChannelChanged(object sender, SelectionChangedEventArgs e)
        {
            if (Channels.SelectedItem is Channel channel)
            {
                Programs.ItemsSource = channel.Videos;
                GuideHeader.Text = $"{channel.Name.ToUpperInvariant()} • SCHEDULE ({channel.Videos.Count} IN ROTATION)";

                // Instant Channel Surfing: Switching channels immediately tunes and starts playback
                if (channel.Videos.Count > 0)
                {
                    playingChannel = channel;
                    playingIndex = 0;
                    PlayCurrent();
                }
                else
                {
                    NowPlaying.Text = channel.Name;
                    Status.Text = "Empty queue. Press [X] on any video to add it.";
                    HeaderNowPlaying.Text = "Empty Queue";
                }
            }
        }

        private void PlayClicked(object sender, ItemClickEventArgs e)
        {
            if (!(Channels.SelectedItem is Channel channel) || !(e.ClickedItem is Video video)) return;
            playingChannel = channel;
            playingIndex = channel.Videos.IndexOf(video);
            if (playingIndex < 0) playingIndex = 0;
            PlayCurrent();
        }

        private void PlayCurrent()
        {
            if (playingChannel == null || playingChannel.Videos.Count == 0) return;
            var video = playingChannel.Videos[playingIndex];
            NowPlaying.Text = video.Title;
            HeaderChannel.Text = $"CH {playingChannel.Number} • {playingChannel.Name.ToUpperInvariant()}";
            HeaderNowPlaying.Text = $"{video.Title} ({video.Host})";
            Status.Text = $"{playingChannel.Name} · {video.Host} · Continuous broadcast active";
            UpdateSaveStatus(video.Id);

            try
            {
                media.Source = MediaSource.CreateFromUri(new Uri(video.Url));
                media.Play();
            }
            catch (Exception)
            {
                Status.Text = "Reconnecting to live queue...";
            }
        }

        private void ToggleSaveCurrent()
        {
            Video target = null;
            if (Programs.SelectedItem is Video sel) target = sel;
            else if (playingChannel != null && playingChannel.Videos.Count > playingIndex) target = playingChannel.Videos[playingIndex];

            if (target != null)
            {
                bool isSaved = SavedStore.Toggle(target.Id);
                UpdateSaveStatus(target.Id);
                Status.Text = isSaved ? $"★ '{target.Title}' saved to Library!" : $"'{target.Title}' removed from Library.";
            }
        }

        private void UpdateSaveStatus(string videoId)
        {
            bool isSaved = SavedStore.Contains(videoId);
            SaveIndicator.Text = isSaved ? "★ SAVED IN LIBRARY [X]" : "[X] SAVE TO LIBRARY";
        }

        private void FullscreenClicked(object sender, RoutedEventArgs e)
        {
            Player.IsFullWindow = !Player.IsFullWindow;
        }

        private async void Ended(MediaPlayer sender, object args)
        {
            await Dispatcher.RunAsync(CoreDispatcherPriority.Normal, () => {
                if (playingChannel == null || playingChannel.Videos.Count == 0) return;
                playingIndex = (playingIndex + 1) % playingChannel.Videos.Count;
                PlayCurrent();
            });
        }

        private async void Failed(MediaPlayer sender, MediaPlayerFailedEventArgs args)
        {
            await Dispatcher.RunAsync(CoreDispatcherPriority.Normal, () => {
                Status.Text = "Stream reconnecting...";
                if (playingChannel != null && playingChannel.Videos.Count > 0)
                {
                    playingIndex = (playingIndex + 1) % playingChannel.Videos.Count;
                    PlayCurrent();
                }
            });
        }

        private void Back(object sender, BackRequestedEventArgs e)
        {
            if (Player.IsFullWindow)
            {
                Player.IsFullWindow = false;
                e.Handled = true;
            }
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