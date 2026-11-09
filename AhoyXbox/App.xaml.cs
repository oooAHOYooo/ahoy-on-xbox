using Windows.ApplicationModel.Activation;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
namespace AhoyXbox
{
    sealed partial class App : Application
    {
        public App()
        {
            InitializeComponent();
            // Lock out virtual mouse cursor for 100% controller-driven Xbox TV experience
            this.RequiresPointerMode = ApplicationRequiresPointerMode.WhenRequested;
            // Enable native Xbox UI sound effects (dashboard ticks on D-pad, select blip on A, back pop on B)
            ElementSoundPlayer.State = ElementSoundPlayerState.On;
        }
        protected override void OnLaunched(LaunchActivatedEventArgs e)
        {
            var frame = Window.Current.Content as Frame;
            if (frame == null) { frame = new Frame(); Window.Current.Content = frame; }
            if (frame.Content == null) frame.Navigate(typeof(MainPage));
            Window.Current.Activate();
        }
    }
}
