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
        private const string TokenKey = "Ahoy_Id_Token";
        private const string HandleKey = "Ahoy_Id_Handle";
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

        public static string AccessToken
        {
            get
            {
                try
                {
                    var settings = Windows.Storage.ApplicationData.Current.LocalSettings;
                    return settings.Values.TryGetValue(TokenKey, out var val) && val is string s ? s : null;
                }
                catch { return null; }
            }
            set
            {
                try
                {
                    var settings = Windows.Storage.ApplicationData.Current.LocalSettings;
                    settings.Values[TokenKey] = value;
                }
                catch { }
            }
        }

        public static string AccountHandle
        {
            get
            {
                try
                {
                    var settings = Windows.Storage.ApplicationData.Current.LocalSettings;
                    return settings.Values.TryGetValue(HandleKey, out var val) && val is string s ? s : null;
                }
                catch { return null; }
            }
            set
            {
                try
                {
                    var settings = Windows.Storage.ApplicationData.Current.LocalSettings;
                    settings.Values[HandleKey] = value;
                }
                catch { }
            }
        }

        public static bool IsPaired => !string.IsNullOrEmpty(AccessToken);

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

            // Sync with AHOY ID if paired
            if (IsPaired)
            {
                _ = SyncToggleAsync(id);
            }

            return added;
        }

        public static async System.Threading.Tasks.Task SyncLibraryAsync()
        {
            var token = AccessToken;
            if (string.IsNullOrEmpty(token)) return;
            try
            {
                using (var client = new Windows.Web.Http.HttpClient())
                {
                    client.DefaultRequestHeaders.Authorization = new Windows.Web.Http.Headers.HttpCredentialsHeaderValue("Bearer", token);
                    var resp = await client.GetAsync(new Uri("https://id.ahoy.ooo/api/v1/me/library"));
                    if (resp.IsSuccessStatusCode)
                    {
                        var text = await resp.Content.ReadAsStringAsync();
                        var root = JsonObject.Parse(text);
                        if (root.ContainsKey("items"))
                        {
                            var items = root.GetNamedArray("items");
                            foreach (var item in items)
                            {
                                savedIds.Add(item.GetString());
                            }
                            var settings = Windows.Storage.ApplicationData.Current.LocalSettings;
                            settings.Values[Key] = string.Join(",", savedIds);
                        }
                    }
                }
            }
            catch { }
        }

        private static async System.Threading.Tasks.Task SyncToggleAsync(string itemId)
        {
            var token = AccessToken;
            if (string.IsNullOrEmpty(token)) return;
            try
            {
                using (var client = new Windows.Web.Http.HttpClient())
                {
                    client.DefaultRequestHeaders.Authorization = new Windows.Web.Http.Headers.HttpCredentialsHeaderValue("Bearer", token);
                    var payload = new JsonObject();
                    payload.SetNamedValue("itemId", JsonValue.CreateStringValue(itemId));
                    var content = new Windows.Web.Http.HttpStringContent(payload.Stringify(), Windows.Storage.Streams.UnicodeEncoding.Utf8, "application/json");
                    await client.PostAsync(new Uri("https://id.ahoy.ooo/api/v1/me/library/toggle"), content);
                }
            }
            catch { }
        }
    }

    public sealed class Video
    {
        public string Id { get; set; }
        public string Title { get; set; }
        public string Host { get; set; }
        public string Description { get; set; }
        public string Duration { get; set; }
        public string DurationLabel => !string.IsNullOrEmpty(Duration) ? Duration : "LIVE";
        public string Url { get; set; }
        public string Thumbnail { get; set; }
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
        private readonly DispatcherTimer guideTimer = new DispatcherTimer();
        private readonly DispatcherTimer pairingPollTimer = new DispatcherTimer();
        private string currentDeviceCode = null;
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

            UpdateAccountIndicator();
            pairingPollTimer.Interval = TimeSpan.FromSeconds(5);
            pairingPollTimer.Tick += PollPairingStatus;

            guideTimer.Interval = TimeSpan.FromSeconds(6);
            guideTimer.Tick += (s, e) => {
                guideTimer.Stop();
                if (GuideDock != null && !Player.IsFullWindow)
                {
                    GuideDock.Visibility = Visibility.Collapsed;
                }
            };

            KeyDown += (s, e) => {
                if (e.Key == Windows.System.VirtualKey.GamepadX || e.Key == Windows.System.VirtualKey.X)
                {
                    WakeGuide();
                    ToggleSaveCurrent();
                }
                else if (e.Key == Windows.System.VirtualKey.GamepadY || e.Key == Windows.System.VirtualKey.Y)
                {
                    WakeGuide();
                    OpenPairingOverlay();
                    e.Handled = true;
                }
                else if (e.Key == Windows.System.VirtualKey.GamepadB || e.Key == Windows.System.VirtualKey.B)
                {
                    if (PairingOverlay != null && PairingOverlay.Visibility == Visibility.Visible)
                    {
                        ClosePairingOverlay();
                        e.Handled = true;
                    }
                    else if (Player.IsFullWindow)
                    {
                        Player.IsFullWindow = false;
                        WakeGuide();
                        e.Handled = true;
                    }
                    else if (GuideDock != null)
                    {
                        if (GuideDock.Visibility == Visibility.Visible)
                        {
                            GuideDock.Visibility = Visibility.Collapsed;
                            guideTimer.Stop();
                        }
                        else
                        {
                            WakeGuide();
                        }
                        e.Handled = true;
                    }
                }
                else if (e.Key == Windows.System.VirtualKey.GamepadRightShoulder)
                {
                    WakeGuide();
                    if (Channels.ItemsSource is System.Collections.IList chs && chs.Count > 0)
                    {
                        Channels.SelectedIndex = (Channels.SelectedIndex + 1) % chs.Count;
                        e.Handled = true;
                    }
                }
                else if (e.Key == Windows.System.VirtualKey.GamepadLeftShoulder)
                {
                    WakeGuide();
                    if (Channels.ItemsSource is System.Collections.IList chs && chs.Count > 0)
                    {
                        Channels.SelectedIndex = (Channels.SelectedIndex - 1 + chs.Count) % chs.Count;
                        e.Handled = true;
                    }
                }
                else
                {
                    WakeGuide();
                }
            };
        }

        private void WakeGuide()
        {
            if (GuideDock != null && GuideDock.Visibility != Visibility.Visible)
            {
                GuideDock.Visibility = Visibility.Visible;
            }
            guideTimer.Stop();
            guideTimer.Start();
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
                var rawVideos = root.GetNamedArray("videos").Select(value => {
                    var row = value.GetObject();
                    var rawThumb = row.ContainsKey("thumbnail") ? row.GetNamedString("thumbnail", "") : "";
                    if (!string.IsNullOrEmpty(rawThumb) && rawThumb.StartsWith("/"))
                        rawThumb = "https://app.ahoy.ooo" + rawThumb;
                    else if (string.IsNullOrEmpty(rawThumb))
                        rawThumb = "https://storage.googleapis.com/ahoy-videos/wintergreen-sessions/web/thumbnails/H6iranjvsNI.jpg";

                    string durationStr = "";
                    if (row.ContainsKey("duration"))
                    {
                        var dVal = row.GetNamedValue("duration");
                        if (dVal.ValueType == JsonValueType.String) durationStr = dVal.GetString();
                    }
                    string descStr = row.ContainsKey("description") ? row.GetNamedString("description", "") : "";

                    return new Video {
                        Id = row.GetNamedString("id", Guid.NewGuid().ToString()),
                        Title = row.GetNamedString("title", "Untitled"),
                        Host = row.GetNamedString("host", "Ahoy"),
                        Description = descStr,
                        Duration = durationStr,
                        Url = row.GetNamedString("url", ""),
                        Thumbnail = rawThumb,
                        Category = row.GetNamedString("category", ""),
                        Tags = row.ContainsKey("tags") ? row.GetNamedArray("tags").Select(t => t.GetString()).ToList() : new List<string>()
                    };
                }).Where(v => Uri.TryCreate(v.Url, UriKind.Absolute, out var uri) && uri.Scheme == "https").ToList();

                var liveShowsVids = rawVideos.Where(v => v.Category == "live show" || v.Tags.Contains("wintergreen-sessions") || v.Tags.Contains("live") || v.Title.ToLowerInvariant().Contains("whatnot")).ToList();
                var musicVids = rawVideos.Where(v => v.Tags.Contains("music-video") || v.Tags.Contains("music") || v.Category == "music").ToList();
                var filmVids = rawVideos.Where(v => v.Category == "film" || v.Category == "skating" || v.Tags.Contains("skating") || v.Tags.Contains("short-film")).ToList();
                var miscVids = rawVideos;

                // Load Radio Tracks into Music
                try
                {
                    var musicFile = await StorageFile.GetFileFromApplicationUriAsync(new Uri("ms-appx:///Data/music.json"));
                    var musicJson = await FileIO.ReadTextAsync(musicFile);
                    var musicRoot = JsonObject.Parse(musicJson);
                    if (musicRoot.ContainsKey("tracks"))
                    {
                        var musicArray = musicRoot.GetNamedArray("tracks");
                        var radioTracks = musicArray.Select(t => {
                            var row = t.GetObject();
                            var cover = row.ContainsKey("cover_art") ? row.GetNamedString("cover_art", "") : "https://i.ytimg.com/vi/XDH0X-dF4GM/maxresdefault.jpg";
                            string trackDuration = row.ContainsKey("duration") ? row.GetNamedString("duration", "") : "";
                            string trackAlbum = row.ContainsKey("album") ? row.GetNamedString("album", "") : "";
                            return new Video {
                                Id = row.GetNamedString("track_id", Guid.NewGuid().ToString()),
                                Title = row.GetNamedString("title", "Untitled Track"),
                                Host = row.GetNamedString("artist", "Ahoy Music"),
                                Description = !string.IsNullOrEmpty(trackAlbum) ? $"Album: {trackAlbum}" : "Ahoy Radio 24/7",
                                Duration = trackDuration,
                                Url = row.GetNamedString("audio_url", ""),
                                Thumbnail = cover,
                                Category = "music",
                                Tags = new List<string> { "music", "audio" }
                            };
                        }).Where(v => Uri.TryCreate(v.Url, UriKind.Absolute, out var uri) && uri.Scheme == "https").ToList();
                        musicVids.AddRange(radioTracks);
                    }
                }
                catch { }

                var channels = new List<Channel>
                {
                    new Channel { Number = "101", Name = "Live Shows", Tagline = "Wintergreen Sessions & Concerts", Videos = liveShowsVids },
                    new Channel { Number = "102", Name = "Music Videos", Tagline = "Premieres & Soundscapes", Videos = musicVids },
                    new Channel { Number = "103", Name = "Films", Tagline = "Skate Tapes & Documentaries", Videos = filmVids },
                    new Channel { Number = "104", Name = "Misc", Tagline = "24/7 Mix & Curations", Videos = miscVids }
                };

                Channels.ItemsSource = channels;
                Channels.SelectedIndex = 0;
                Channels.Focus(FocusState.Programmatic);
                _ = SavedStore.SyncLibraryAsync();

                // Auto-Play Channel 101 immediately (Pluto TV live clock sync)
                playingChannel = channels[0];
                var (initIdx, initOffset) = GetLiveSyncPosition(playingChannel);
                playingIndex = initIdx;
                Programs.ItemsSource = playingChannel.Videos;
                PlayCurrent(initOffset);
            }
            catch (Exception)
            {
                Status.Text = "The catalog could not load. Close and reopen Ahoy to retry.";
            }
        }

        private (int index, double offsetSeconds) GetLiveSyncPosition(Channel channel)
        {
            if (channel == null || channel.Videos == null || channel.Videos.Count == 0) return (0, 0);
            double totalCycle = 0;
            var durations = new double[channel.Videos.Count];
            for (int i = 0; i < channel.Videos.Count; i++)
            {
                durations[i] = ParseDurationSeconds(channel.Videos[i].Duration);
                totalCycle += durations[i];
            }
            if (totalCycle <= 0) return (0, 0);

            double nowSec = DateTime.UtcNow.TimeOfDay.TotalSeconds % totalCycle;
            double accumulated = 0;
            for (int i = 0; i < channel.Videos.Count; i++)
            {
                if (nowSec >= accumulated && nowSec < accumulated + durations[i])
                {
                    return (i, nowSec - accumulated);
                }
                accumulated += durations[i];
            }
            return (0, 0);
        }

        private static double ParseDurationSeconds(string dur)
        {
            if (string.IsNullOrEmpty(dur)) return 240.0;
            var parts = dur.Split(':');
            if (parts.Length == 2 && double.TryParse(parts[0], out var m) && double.TryParse(parts[1], out var s))
                return m * 60.0 + s;
            if (parts.Length == 3 && double.TryParse(parts[0], out var h) && double.TryParse(parts[1], out var m2) && double.TryParse(parts[2], out var s2))
                return h * 3600.0 + m2 * 60.0 + s2;
            return 240.0;
        }

        private void ChannelChanged(object sender, SelectionChangedEventArgs e)
        {
            if (Channels.SelectedItem is Channel channel)
            {
                Programs.ItemsSource = channel.Videos;
                GuideHeader.Text = $"{channel.Name.ToUpperInvariant()} • SCHEDULE ({channel.Videos.Count} IN ROTATION)";

                // Instant Channel Surfing: Switching channels immediately tunes with clock sync
                if (channel.Videos.Count > 0)
                {
                    playingChannel = channel;
                    var (syncIdx, syncOffset) = GetLiveSyncPosition(channel);
                    playingIndex = syncIdx;
                    PlayCurrent(syncOffset);
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
            PlayCurrent(0);
        }

        private void PlayCurrent(double seekSeconds = 0)
        {
            if (playingChannel == null || playingChannel.Videos.Count == 0) return;
            var video = playingChannel.Videos[playingIndex];
            NowPlaying.Text = video.Title;
            HeaderChannel.Text = $"CH {playingChannel.Number} • {playingChannel.Name.ToUpperInvariant()}";
            HeaderNowPlaying.Text = $"{video.Title} ({video.Host})";
            Status.Text = $"{playingChannel.Name} · {video.Host} · Live broadcast active";
            UpdateSaveStatus(video.Id);

            try
            {
                if (!string.IsNullOrEmpty(video.Thumbnail))
                {
                    Player.PosterSource = new Windows.UI.Xaml.Media.Imaging.BitmapImage(new Uri(video.Thumbnail));
                }
                media.Source = MediaSource.CreateFromUri(new Uri(video.Url));
                if (seekSeconds > 5)
                {
                    media.PlaybackSession.Position = TimeSpan.FromSeconds(seekSeconds);
                }
                media.Play();
                WakeGuide();
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
                Status.Text = isSaved ? $"'{target.Title}' saved to Library" : $"'{target.Title}' removed from Library";
            }
        }

        private void UpdateSaveStatus(string videoId)
        {
            bool isSaved = SavedStore.Contains(videoId);
            SaveIndicator.Text = isSaved ? "[X] SAVED" : "[X] SAVE";
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
                PlayCurrent(0);
            });
        }

        private async void Failed(MediaPlayer sender, MediaPlayerFailedEventArgs args)
        {
            await Dispatcher.RunAsync(CoreDispatcherPriority.Normal, () => {
                Status.Text = "Stream reconnecting...";
                if (playingChannel != null && playingChannel.Videos.Count > 0)
                {
                    playingIndex = (playingIndex + 1) % playingChannel.Videos.Count;
                    PlayCurrent(0);
                }
            });
        }

        private void OpenPairingOverlay()
        {
            if (PairingOverlay == null) return;
            PairingOverlay.Visibility = Visibility.Visible;
            StartPairingFlow();
        }

        private void ClosePairingOverlay(object sender = null, RoutedEventArgs e = null)
        {
            pairingPollTimer.Stop();
            if (PairingOverlay != null)
            {
                PairingOverlay.Visibility = Visibility.Collapsed;
            }
        }

        private async void StartPairingFlow()
        {
            PairingCodeDisplay.Text = "REQUESTING...";
            PairingStatusText.Text = "Contacting id.ahoy.ooo...";
            try
            {
                using (var client = new Windows.Web.Http.HttpClient())
                {
                    var req = new JsonObject();
                    req.SetNamedValue("client_id", JsonValue.CreateStringValue("app.ahoy.xbox"));
                    var content = new Windows.Web.Http.HttpStringContent(req.Stringify(), Windows.Storage.Streams.UnicodeEncoding.Utf8, "application/json");
                    var resp = await client.PostAsync(new Uri("https://id.ahoy.ooo/api/v1/auth/device/code"), content);
                    if (resp.IsSuccessStatusCode)
                    {
                        var text = await resp.Content.ReadAsStringAsync();
                        var data = JsonObject.Parse(text);
                        currentDeviceCode = data.GetNamedString("device_code", "");
                        var userCode = data.GetNamedString("user_code", "");
                        PairingCodeDisplay.Text = userCode;
                        PairingStatusText.Text = "Waiting for authorization on phone or browser...";

                        pairingPollTimer.Interval = TimeSpan.FromSeconds(5);
                        pairingPollTimer.Start();
                    }
                    else
                    {
                        PairingCodeDisplay.Text = "ERROR";
                        PairingStatusText.Text = "Could not reach id.ahoy.ooo. Press [B] to close.";
                    }
                }
            }
            catch
            {
                PairingCodeDisplay.Text = "OFFLINE";
                PairingStatusText.Text = "Check network connection. Press [B] to close.";
            }
        }

        private async void PollPairingStatus(object sender, object e)
        {
            if (string.IsNullOrEmpty(currentDeviceCode)) return;
            try
            {
                using (var client = new Windows.Web.Http.HttpClient())
                {
                    var req = new JsonObject();
                    req.SetNamedValue("client_id", JsonValue.CreateStringValue("app.ahoy.xbox"));
                    req.SetNamedValue("device_code", JsonValue.CreateStringValue(currentDeviceCode));
                    var content = new Windows.Web.Http.HttpStringContent(req.Stringify(), Windows.Storage.Streams.UnicodeEncoding.Utf8, "application/json");
                    var resp = await client.PostAsync(new Uri("https://id.ahoy.ooo/api/v1/auth/device/token"), content);
                    var text = await resp.Content.ReadAsStringAsync();
                    var data = JsonObject.Parse(text);

                    if (resp.IsSuccessStatusCode && data.ContainsKey("access_token"))
                    {
                        pairingPollTimer.Stop();
                        var token = data.GetNamedString("access_token");
                        SavedStore.AccessToken = token;

                        string handle = null;
                        if (data.ContainsKey("account"))
                        {
                            var acct = data.GetNamedObject("account");
                            if (acct.ContainsKey("handle") && acct.GetNamedValue("handle").ValueType == JsonValueType.String)
                                handle = acct.GetNamedString("handle");
                            else if (acct.ContainsKey("displayName") && acct.GetNamedValue("displayName").ValueType == JsonValueType.String)
                                handle = acct.GetNamedString("displayName");
                            else if (acct.ContainsKey("ahoyId"))
                                handle = acct.GetNamedString("ahoyId");
                        }
                        SavedStore.AccountHandle = handle;
                        UpdateAccountIndicator();

                        PairingStatusText.Text = $"Paired successfully with {handle ?? "AHOY ID"}!";
                        await SavedStore.SyncLibraryAsync();

                        var closeTimer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(2) };
                        closeTimer.Tick += (s, args) => {
                            closeTimer.Stop();
                            ClosePairingOverlay();
                        };
                        closeTimer.Start();
                    }
                    else if (data.ContainsKey("error"))
                    {
                        var err = data.GetNamedString("error");
                        if (err == "expired_token" || err == "access_denied")
                        {
                            pairingPollTimer.Stop();
                            PairingStatusText.Text = "Code expired or denied. Reopen [Y] to retry.";
                        }
                    }
                }
            }
            catch { }
        }

        private void UpdateAccountIndicator()
        {
            if (AccountIndicator == null) return;
            if (SavedStore.IsPaired)
            {
                var h = SavedStore.AccountHandle;
                AccountIndicator.Text = !string.IsNullOrEmpty(h) ? $"[Y] @{h.Replace("@", "")}" : "[Y] PAIRED";
                AccountIndicator.Foreground = new Windows.UI.Xaml.Media.SolidColorBrush(Windows.UI.Color.FromArgb(255, 52, 199, 89));
            }
            else
            {
                AccountIndicator.Text = "[Y] PAIR ID";
                AccountIndicator.Foreground = new Windows.UI.Xaml.Media.SolidColorBrush(Windows.UI.Color.FromArgb(255, 255, 0, 96));
            }
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