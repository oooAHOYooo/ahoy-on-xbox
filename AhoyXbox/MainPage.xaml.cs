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
    public sealed class Video
    {
        public string Title { get; set; }
        public string Host { get; set; }
        public string Url { get; set; }
        public string Category { get; set; }
        public List<string> Tags { get; set; }
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
        }
        private async void LoadCatalog(object sender, RoutedEventArgs e)
        {
            try
            {
                var file = await StorageFile.GetFileFromApplicationUriAsync(new Uri("ms-appx:///Data/catalog.json"));
                var root = JsonObject.Parse(await FileIO.ReadTextAsync(file));
                var videos = root.GetNamedArray("videos").Select(value => {
                    var row = value.GetObject();
                    return new Video {
                        Title = row.GetNamedString("title", "Untitled"), Host = row.GetNamedString("host", "Ahoy"),
                        Url = row.GetNamedString("url", ""), Category = row.GetNamedString("category", ""),
                        Tags = row.ContainsKey("tags") ? row.GetNamedArray("tags").Select(t => t.GetString()).ToList() : new List<string>()
                    };
                }).Where(v => Uri.TryCreate(v.Url, UriKind.Absolute, out var uri) && uri.Scheme == "https").ToList();
                var channels = new List<Channel> { new Channel { Name = "Ahoy Mix", Videos = videos } };
                AddChannel(channels, "Music Videos", videos.Where(v => v.Tags.Contains("music-video")));
                AddChannel(channels, "Skating", videos.Where(v => v.Category == "skating" || v.Tags.Contains("skating")));
                AddChannel(channels, "G-Dub Disc Golf", videos.Where(v => v.Tags.Contains("g-dub-disc-golf")));
                Channels.ItemsSource = channels;
                Channels.SelectedIndex = 0;
                Channels.Focus(FocusState.Programmatic);
                Status.Text = "Choose a video to start its channel. Curated queues, not live broadcasts.";
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
