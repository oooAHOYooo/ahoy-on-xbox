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
using Windows.UI.Xaml.Media;

namespace AhoyXbox
{
    public enum AppSection
    {
        Channels,
        OnDemand,
        Music,
        Radio
    }

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
        public Windows.UI.Xaml.Media.ImageSource Artwork { get; set; }
        public string CountLabel => Videos.Count + " in rotation";
    }

    public sealed partial class MainPage : Page
    {
        private readonly MediaPlayer media = new MediaPlayer();
        private readonly DispatcherTimer guideTimer = new DispatcherTimer();
        private readonly DispatcherTimer pairingPollTimer = new DispatcherTimer();
        private string currentDeviceCode = null;

        private double radioEpochMs = 1767225600000;
        private bool hasRadioManifest;
        private string radioStationName = "Ahoy Radio";
        private double pendingSeekSeconds;

        private AppSection currentSection = AppSection.Channels;
        private readonly List<Channel> allChannels = new List<Channel>();
        private readonly List<Video> onDemandVideos = new List<Video>();
        private readonly List<Video> musicTracks = new List<Video>();
        private readonly List<Video> radioTracks = new List<Video>();

        private Channel playingChannel;
        private int playingIndex;
        private Video currentPlayingVideo;

        private readonly SolidColorBrush accentBrush = new SolidColorBrush(Windows.UI.Color.FromArgb(255, 255, 0, 96));
        private readonly SolidColorBrush inactiveBrush = new SolidColorBrush(Windows.UI.Color.FromArgb(255, 20, 21, 26));
        private readonly SolidColorBrush tabBorderBrush = new SolidColorBrush(Windows.UI.Color.FromArgb(255, 36, 38, 46));
        private readonly SolidColorBrush whiteBrush = new SolidColorBrush(Windows.UI.Color.FromArgb(255, 255, 255, 255));
        private readonly SolidColorBrush grayBrush = new SolidColorBrush(Windows.UI.Color.FromArgb(255, 160, 160, 168));

        public MainPage()
        {
            InitializeComponent();
            try
            {
                // Draw edge-to-edge across TV display (disables OS overscan black letterboxing)
                Windows.UI.ViewManagement.ApplicationView.GetForCurrentView().SetDesiredBoundsMode(Windows.UI.ViewManagement.ApplicationViewBoundsMode.UseCoreWindow);
            }
            catch { }

            Player.SetMediaPlayer(media);
            media.MediaOpened += MediaOpened;
            media.MediaEnded += Ended;
            media.MediaFailed += Failed;
            Loaded += LoadCatalog;
            Unloaded += Cleanup;

            // Handle Xbox OS back navigation (B button / system back)
            SystemNavigationManager.GetForCurrentView().BackRequested += Back;

            UpdateAccountIndicator();
            pairingPollTimer.Interval = TimeSpan.FromSeconds(5);
            pairingPollTimer.Tick += PollPairingStatus;

            // Big-screen TV cinema timer: 10s idle timeout dims chrome for cinematic viewing
            guideTimer.Interval = TimeSpan.FromSeconds(10);
            guideTimer.Tick += (s, e) => {
                guideTimer.Stop();
                if (GuideDock != null && !Player.IsFullWindow)
                {
                    GuideDock.Visibility = Visibility.Collapsed;
                }
                if (TopHeader != null)
                {
                    TopHeader.Opacity = 0.25;
                }
            };

            PointerMoved += (s, e) => WakeGuide();

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
                    // NEVER CLOSE APP ON B BUTTON
                    e.Handled = true;
                    HandleBackNavigation();
                }
                else if (e.Key == Windows.System.VirtualKey.GamepadRightTrigger)
                {
                    CycleSection(1);
                    e.Handled = true;
                }
                else if (e.Key == Windows.System.VirtualKey.GamepadLeftTrigger)
                {
                    CycleSection(-1);
                    e.Handled = true;
                }
                else if (e.Key == Windows.System.VirtualKey.GamepadRightShoulder)
                {
                    WakeGuide();
                    if (currentSection == AppSection.Channels && Channels.ItemsSource is System.Collections.IList chs && chs.Count > 0)
                    {
                        Channels.SelectedIndex = (Channels.SelectedIndex + 1) % chs.Count;
                        e.Handled = true;
                    }
                }
                else if (e.Key == Windows.System.VirtualKey.GamepadLeftShoulder)
                {
                    WakeGuide();
                    if (currentSection == AppSection.Channels && Channels.ItemsSource is System.Collections.IList chs && chs.Count > 0)
                    {
                        Channels.SelectedIndex = (Channels.SelectedIndex - 1 + chs.Count) % chs.Count;
                        e.Handled = true;
                    }
                }
                else if (e.Key == Windows.System.VirtualKey.GamepadDPadDown || e.Key == Windows.System.VirtualKey.Down)
                {
                    WakeGuide();
                    if (currentSection == AppSection.Channels)
                    {
                        if (GuideDock != null && GuideDock.Visibility != Visibility.Visible)
                        {
                            GuideDock.Visibility = Visibility.Visible;
                        }
                        Channels.Focus(FocusState.Keyboard);
                    }
                }
                else if (e.Key == Windows.System.VirtualKey.Number1)
                {
                    SetSection(AppSection.Channels);
                    e.Handled = true;
                }
                else if (e.Key == Windows.System.VirtualKey.Number2)
                {
                    SetSection(AppSection.OnDemand);
                    e.Handled = true;
                }
                else if (e.Key == Windows.System.VirtualKey.Number3)
                {
                    SetSection(AppSection.Music);
                    e.Handled = true;
                }
                else if (e.Key == Windows.System.VirtualKey.Number4)
                {
                    SetSection(AppSection.Radio);
                    e.Handled = true;
                }
                else
                {
                    WakeGuide();
                }
            };
        }

        private void CycleSection(int direction)
        {
            var sections = new[] { AppSection.Channels, AppSection.OnDemand, AppSection.Music, AppSection.Radio };
            int idx = Array.IndexOf(sections, currentSection);
            int next = (idx + direction + sections.Length) % sections.Length;
            SetSection(sections[next]);
        }

        private void HandleBackNavigation()
        {
            // 1. Close pairing overlay if open
            if (PairingOverlay != null && PairingOverlay.Visibility == Visibility.Visible)
            {
                ClosePairingOverlay();
                return;
            }

            // 2. Exit fullscreen if in fullscreen
            if (Player.IsFullWindow)
            {
                Player.IsFullWindow = false;
                WakeGuide();
                return;
            }

            // 3. Return to Live TV if in another section (On Demand / Music / Radio)
            if (currentSection != AppSection.Channels)
            {
                SetSection(AppSection.Channels);
                return;
            }

            // 4. Wake guide if collapsed
            if (GuideDock != null && GuideDock.Visibility != Visibility.Visible)
            {
                WakeGuide();
                return;
            }

            // 5. Already at root Live TV with guide visible:
            // NEVER let OS terminate app. Guide user gracefully.
            Status.Text = "Press the Xbox Guide button on your controller to exit to Dashboard.";
            WakeGuide();
        }

        private void WakeGuide()
        {
            if (GuideDock != null && GuideDock.Visibility != Visibility.Visible)
            {
                GuideDock.Visibility = Visibility.Visible;
            }
            if (TopHeader != null && TopHeader.Opacity < 1.0)
            {
                TopHeader.Opacity = 1.0;
            }
            guideTimer.Stop();
            guideTimer.Start();
        }

        private static Windows.UI.Xaml.Media.ImageSource ChannelArtwork(List<Video> videos)
        {
            var thumbnail = videos?.FirstOrDefault(v => !string.IsNullOrEmpty(v.Thumbnail))?.Thumbnail;
            if (string.IsNullOrEmpty(thumbnail)) return null;
            try { return new Windows.UI.Xaml.Media.Imaging.BitmapImage(new Uri(thumbnail)); }
            catch { return null; }
        }

        // Section Navigation Button Click Handlers
        private void TabChannels_Click(object sender, RoutedEventArgs e) => SetSection(AppSection.Channels);
        private void TabOnDemand_Click(object sender, RoutedEventArgs e) => SetSection(AppSection.OnDemand);
        private void TabMusic_Click(object sender, RoutedEventArgs e) => SetSection(AppSection.Music);
        private void TabRadio_Click(object sender, RoutedEventArgs e) => SetSection(AppSection.Radio);

        public void SetSection(AppSection sec)
        {
            currentSection = sec;

            // Highlight active tab pill
            TabChannels.Background = sec == AppSection.Channels ? accentBrush : inactiveBrush;
            TabChannels.Foreground = sec == AppSection.Channels ? whiteBrush : grayBrush;
            TabChannels.BorderBrush = sec == AppSection.Channels ? accentBrush : tabBorderBrush;

            TabOnDemand.Background = sec == AppSection.OnDemand ? accentBrush : inactiveBrush;
            TabOnDemand.Foreground = sec == AppSection.OnDemand ? whiteBrush : grayBrush;
            TabOnDemand.BorderBrush = sec == AppSection.OnDemand ? accentBrush : tabBorderBrush;

            TabMusic.Background = sec == AppSection.Music ? accentBrush : inactiveBrush;
            TabMusic.Foreground = sec == AppSection.Music ? whiteBrush : grayBrush;
            TabMusic.BorderBrush = sec == AppSection.Music ? accentBrush : tabBorderBrush;

            TabRadio.Background = sec == AppSection.Radio ? accentBrush : inactiveBrush;
            TabRadio.Foreground = sec == AppSection.Radio ? whiteBrush : grayBrush;
            TabRadio.BorderBrush = sec == AppSection.Radio ? accentBrush : tabBorderBrush;

            switch (sec)
            {
                case AppSection.Channels:
                    Channels.Visibility = Visibility.Visible;
                    Programs.Visibility = Visibility.Collapsed;
                    Channels.ItemsSource = allChannels;
                    if (playingChannel == null && allChannels.Count > 0)
                    {
                        playingChannel = allChannels.FirstOrDefault();
                    }
                    if (playingChannel != null)
                    {
                        Programs.ItemsSource = playingChannel.Videos;
                        GuideHeader.Text = $"{playingChannel.Name.ToUpperInvariant()} • SCHEDULE";
                        PlayCurrent();
                    }
                    break;

                case AppSection.OnDemand:
                    Channels.Visibility = Visibility.Collapsed;
                    Programs.Visibility = Visibility.Visible;
                    GuideHeader.Text = $"ON DEMAND VIDEO • {onDemandVideos.Count} INDIE FILMS & SHOWS";
                    Programs.ItemsSource = onDemandVideos;
                    if (onDemandVideos.Count > 0)
                    {
                        PlayVideo(onDemandVideos[0]);
                    }
                    break;

                case AppSection.Music:
                    Channels.Visibility = Visibility.Collapsed;
                    Programs.Visibility = Visibility.Visible;
                    GuideHeader.Text = $"MUSIC • {musicTracks.Count} AHOY TRACKS & ALBUMS";
                    Programs.ItemsSource = musicTracks;
                    if (musicTracks.Count > 0)
                    {
                        PlayVideo(musicTracks[0]);
                    }
                    break;

                case AppSection.Radio:
                    Channels.Visibility = Visibility.Collapsed;
                    Programs.Visibility = Visibility.Visible;
                    GuideHeader.Text = $"{radioStationName.ToUpperInvariant()} • {radioTracks.Count} TRACKS IN ROTATION";
                    Programs.ItemsSource = radioTracks;
                    if (radioTracks.Count > 0)
                    {
                        PlayRadio();
                    }
                    break;
            }

            WakeGuide();
        }

        private async void LoadCatalog(object sender, RoutedEventArgs e)
        {
            try
            {
                // Fetch independent public feeds concurrently; retain cached or bundled data on failure.
                var file = await StorageFile.GetFileFromApplicationUriAsync(new Uri("ms-appx:///Data/catalog.json"));
                var root = JsonObject.Parse(await FileIO.ReadTextAsync(file));
                var videoTask = PublishedVideoCatalog.LoadAsync();
                var musicTask = PublishedMediaCatalog.LoadAsync("/api/music", "music-api-v1.json",
                    data => PublishedMediaCatalog.Audio(data.GetNamedArray("tracks"), false));
                var radioTask = PublishedMediaCatalog.LoadAsync("/api/radio/live", "radio-api-v1.json",
                    data => { PublishedMediaCatalog.Audio(data.GetNamedArray("items"), true); data.GetNamedObject("station").GetNamedNumber("epoch_ms"); });
                var channelsTask = PublishedMediaCatalog.LoadAsync("/api/live-tv/channels", "channels-api-v1.json",
                    data => PublishedMediaCatalog.Channels(data));
                await System.Threading.Tasks.Task.WhenAll(videoTask, musicTask, radioTask, channelsTask);
                var publishedVideos = await videoTask;
                if (publishedVideos != null) root["videos"] = publishedVideos;

                // 1. Parse On Demand Videos
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

                onDemandVideos.Clear();
                onDemandVideos.AddRange(rawVideos);

                // 2. Parse Channels
                var liveShowsVids = rawVideos.Where(v => v.Category == "live show" || v.Tags.Contains("wintergreen-sessions") || v.Tags.Contains("live") || v.Title.ToLowerInvariant().Contains("whatnot")).ToList();
                var musicVids = rawVideos.Where(v => v.Tags.Contains("music-video") || v.Tags.Contains("music") || v.Category == "music").ToList();
                var filmVids = rawVideos.Where(v => v.Category == "film" || v.Category == "skating" || v.Tags.Contains("skating") || v.Tags.Contains("short-film")).ToList();
                var miscVids = rawVideos;

                allChannels.Clear();
                allChannels.Add(new Channel { Number = "101", Name = "Live Shows", Tagline = "Wintergreen Sessions & Concerts", Videos = liveShowsVids, Artwork = ChannelArtwork(liveShowsVids) });
                allChannels.Add(new Channel { Number = "102", Name = "Music Videos", Tagline = "Premieres & Soundscapes", Videos = musicVids, Artwork = ChannelArtwork(musicVids) });
                allChannels.Add(new Channel { Number = "103", Name = "Films & Skate", Tagline = "Skate Tapes & Documentaries", Videos = filmVids, Artwork = ChannelArtwork(filmVids) });
                allChannels.Add(new Channel { Number = "104", Name = "The Mix 24/7", Tagline = "24/7 Round-Robin Eclectic Stream", Videos = miscVids, Artwork = ChannelArtwork(miscVids) });

                var publishedChannels = await channelsTask;
                if (publishedChannels != null)
                {
                    allChannels.Clear();
                    allChannels.AddRange(PublishedMediaCatalog.Channels(publishedChannels));
                    allChannels.Sort((left, right) => string.CompareOrdinal(left.Number, right.Number));
                    foreach (var channel in allChannels) channel.Artwork = ChannelArtwork(channel.Videos);
                }

                musicTracks.Clear();
                var publishedMusic = await musicTask;
                musicTracks.AddRange(PublishedMediaCatalog.Audio(publishedMusic != null
                    ? publishedMusic.GetNamedArray("tracks") : root.GetNamedArray("music", new JsonArray()), false));

                radioTracks.Clear();
                var publishedRadio = await radioTask;
                hasRadioManifest = publishedRadio != null;
                if (hasRadioManifest)
                {
                    radioEpochMs = publishedRadio.GetNamedObject("station").GetNamedNumber("epoch_ms");
                    radioStationName = PublishedVideoCatalog.Text(publishedRadio.GetNamedObject("station"), "name", "Ahoy Radio");
                    radioTracks.AddRange(PublishedMediaCatalog.Audio(publishedRadio.GetNamedArray("items"), true));
                }
                else
                    radioTracks.AddRange(PublishedMediaCatalog.Audio(root.GetNamedArray("radio", new JsonArray()), true));

                // Initialize Channels view
                Channels.ItemsSource = allChannels;
                Channels.SelectedIndex = allChannels.Count > 0 ? 0 : -1;
                Channels.Focus(FocusState.Programmatic);
                _ = SavedStore.SyncLibraryAsync();

                // Auto-Play Channel 101 immediately (Pluto TV live clock sync)
                playingChannel = allChannels.FirstOrDefault();
                var (initIdx, initOffset) = GetLiveSyncPosition(playingChannel);
                playingIndex = initIdx;
                Programs.ItemsSource = playingChannel?.Videos;
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
            if (currentSection == AppSection.Channels && Channels.SelectedItem is Channel channel)
            {
                GuideHeader.Text = $"{channel.Name.ToUpperInvariant()} • SCHEDULE ({channel.Videos.Count} IN ROTATION)";
                HeaderChannel.Text = $"CH {channel.Number} • {channel.Name.ToUpperInvariant()}";
                if (channel.Videos.Count > 0)
                {
                    var (previewIndex, _) = GetLiveSyncPosition(channel);
                    var preview = channel.Videos[previewIndex];
                    NowPlaying.Text = preview.Title;
                    HeaderNowPlaying.Text = $"{preview.Title} ({preview.Host})";
                    Status.Text = $"{channel.Name} · {preview.Host} · Select to tune";
                }
                else
                {
                    NowPlaying.Text = channel.Name;
                    Status.Text = "Empty queue. Press [X] on any video to add it.";
                    HeaderNowPlaying.Text = "Empty Queue";
                }
            }
        }

        private void ChannelClicked(object sender, ItemClickEventArgs e)
        {
            if (e.ClickedItem is Channel channel && channel.Videos.Count > 0)
            {
                playingChannel = channel;
                var (syncIdx, syncOffset) = GetLiveSyncPosition(channel);
                playingIndex = syncIdx;
                Programs.ItemsSource = channel.Videos;
                PlayCurrent(syncOffset);
            }
        }

        private void PlayClicked(object sender, ItemClickEventArgs e)
        {
            if (e.ClickedItem is Video video)
            {
                if (currentSection == AppSection.Channels && Channels.SelectedItem is Channel channel)
                {
                    playingChannel = channel;
                    playingIndex = channel.Videos.IndexOf(video);
                    if (playingIndex < 0) playingIndex = 0;
                    PlayCurrent(0);
                }
                else
                {
                    PlayVideo(video);
                }
            }
        }

        private void PlayCurrent(double seekSeconds = 0)
        {
            if (playingChannel == null || playingChannel.Videos.Count == 0) return;
            var video = playingChannel.Videos[playingIndex];
            currentPlayingVideo = video;
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
                pendingSeekSeconds = seekSeconds;
                media.Source = MediaSource.CreateFromUri(new Uri(video.Url));
                media.Play();
                WakeGuide();
            }
            catch (Exception)
            {
                Status.Text = "Reconnecting to live queue...";
            }
        }

        private void MediaOpened(MediaPlayer sender, object args)
        {
            var seek = pendingSeekSeconds;
            pendingSeekSeconds = 0;
            if (seek > 0 && sender.PlaybackSession.CanSeek)
                sender.PlaybackSession.Position = TimeSpan.FromSeconds(seek);
        }

        private void PlayRadio()
        {
            if (radioTracks.Count == 0) return;
            var total = radioTracks.Sum(video => ParseDurationSeconds(video.Duration));
            var elapsed = (DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() - radioEpochMs) / 1000.0;
            var position = total > 0 ? ((elapsed % total) + total) % total : 0;
            foreach (var video in radioTracks)
            {
                var duration = ParseDurationSeconds(video.Duration);
                if (position < duration)
                {
                    PlayVideo(video, hasRadioManifest ? position : 0);
                    return;
                }
                position -= duration;
            }
        }

        private void PlayVideo(Video video, double seekSeconds = 0)
        {
            if (video == null) return;
            currentPlayingVideo = video;
            NowPlaying.Text = video.Title;

            string secLabel = "AHOY TV";
            switch (currentSection)
            {
                case AppSection.OnDemand:
                    secLabel = "ON DEMAND";
                    break;
                case AppSection.Music:
                    secLabel = "AHOY MUSIC";
                    break;
                case AppSection.Radio:
                    secLabel = "RADIO";
                    break;
                default:
                    secLabel = "AHOY TV";
                    break;
            }

            HeaderChannel.Text = secLabel;
            HeaderNowPlaying.Text = $"{video.Title} • {video.Host}";
            Status.Text = $"{video.Title} · {video.Host} · Independent Media";
            UpdateSaveStatus(video.Id);

            try
            {
                if (!string.IsNullOrEmpty(video.Thumbnail))
                {
                    Player.PosterSource = new Windows.UI.Xaml.Media.Imaging.BitmapImage(new Uri(video.Thumbnail));
                }
                pendingSeekSeconds = seekSeconds;
                media.Source = MediaSource.CreateFromUri(new Uri(video.Url));
                media.Play();
                WakeGuide();
            }
            catch (Exception)
            {
                Status.Text = "Stream connecting...";
            }
        }

        private void ToggleSaveCurrent()
        {
            Video target = null;
            if (Programs.SelectedItem is Video sel) target = sel;
            else if (currentPlayingVideo != null) target = currentPlayingVideo;
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
            if (Player.IsFullWindow && GuideDock != null)
            {
                GuideDock.Visibility = Visibility.Collapsed;
            }
            else
            {
                WakeGuide();
            }
        }

        private async void Ended(MediaPlayer sender, object args)
        {
            await Dispatcher.RunAsync(CoreDispatcherPriority.Normal, () => {
                if (currentSection == AppSection.Channels)
                {
                    if (playingChannel == null || playingChannel.Videos.Count == 0) return;
                    playingIndex = (playingIndex + 1) % playingChannel.Videos.Count;
                    PlayCurrent(0);
                }
                else if (currentSection == AppSection.OnDemand && onDemandVideos.Count > 0)
                {
                    int nextIdx = (onDemandVideos.IndexOf(currentPlayingVideo) + 1) % onDemandVideos.Count;
                    PlayVideo(onDemandVideos[nextIdx]);
                }
                else if (currentSection == AppSection.Music && musicTracks.Count > 0)
                {
                    int nextIdx = (musicTracks.IndexOf(currentPlayingVideo) + 1) % musicTracks.Count;
                    PlayVideo(musicTracks[nextIdx]);
                }
                else if (currentSection == AppSection.Radio && radioTracks.Count > 0)
                {
                    int nextIdx = (radioTracks.IndexOf(currentPlayingVideo) + 1) % radioTracks.Count;
                    PlayVideo(radioTracks[nextIdx]);
                }
            });
        }

        private async void Failed(MediaPlayer sender, MediaPlayerFailedEventArgs args)
        {
            await Dispatcher.RunAsync(CoreDispatcherPriority.Normal, () => {
                Status.Text = "Stream reconnecting...";
                if (currentSection == AppSection.Channels && playingChannel != null && playingChannel.Videos.Count > 0)
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
                AccountIndicator.Text = !string.IsNullOrEmpty(h) ? $"@{h.Replace("@", "")}" : "PAIRED";
                AccountIndicator.Foreground = new Windows.UI.Xaml.Media.SolidColorBrush(Windows.UI.Color.FromArgb(255, 52, 199, 89));
                if (AccountKeycapText != null) AccountKeycapText.Text = "✓";
            }
            else
            {
                AccountIndicator.Text = "PAIR ID";
                AccountIndicator.Foreground = new Windows.UI.Xaml.Media.SolidColorBrush(Windows.UI.Color.FromArgb(255, 208, 208, 216));
                if (AccountKeycapText != null) AccountKeycapText.Text = "Y";
            }
        }

        private void Back(object sender, BackRequestedEventArgs e)
        {
            // CRITICAL: NEVER ALLOW e.Handled TO BE FALSE ON XBOX
            // If false, Xbox OS will terminate the application to Dashboard
            e.Handled = true;
            HandleBackNavigation();
        }

        private void Cleanup(object sender, RoutedEventArgs e)
        {
            SystemNavigationManager.GetForCurrentView().BackRequested -= Back;
            media.MediaOpened -= MediaOpened;
            media.MediaEnded -= Ended;
            media.MediaFailed -= Failed;
            media.Dispose();
        }
    }
}
