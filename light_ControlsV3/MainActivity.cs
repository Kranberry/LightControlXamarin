using Android.App;
using Android.OS;
using Android.Support.V7.App;
using Android.Runtime;
using Android.Widget;
using System.Net.Sockets;
using System.Text;

namespace light_ControlsV3
{
    [Activity(Label = "@string/app_name", Theme = "@style/AppTheme", MainLauncher = true)]
    public class MainActivity : AppCompatActivity
    {
        TextView tcpTest;
        EditText ipAdress;
        void tcpConnect(string command, int dimm = -50)
        {
            ipAdress = FindViewById<EditText>(Resource.Id.ip);

            string serverIP = ipAdress.Text;                               // Ip adress of the host server
            int serverPort = 8080;

            TcpClient client = new TcpClient(serverIP, serverPort);     // Connect to specific host and port
            NetworkStream stream = client.GetStream();                  // Get the client stream of the tcp connection
            if (dimm == -50)
            {
                int byteCount = Encoding.ASCII.GetByteCount(command);       // Count the amount of bytes inside the message
                byte[] sendData = new byte[byteCount];                      // Create a variable that will send the message with the length of the message
                sendData = Encoding.ASCII.GetBytes(command);                // Get the bytes of the message
                stream.Write(sendData, 0, sendData.Length);                 // Write the data to the stream for the server to pick up
            }
            else
            {
                int byteCount = Encoding.ASCII.GetByteCount(command + ";" + dimm);
                byte[] sendData = new byte[byteCount];
                sendData = Encoding.ASCII.GetBytes(command + ";" + dimm);
                stream.Write(sendData, 0, sendData.Length);
            }
            stream.Close();                                             // Close the stream
            client.Close();                                             // Close the client

        }

        Button btnLeft;
        Button btnRight;
        Button btnBoth;
        SeekBar dimmer;
        

        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            Xamarin.Essentials.Platform.Init(this, savedInstanceState);
            // Set our view from the "main" layout resource
            SetContentView(Resource.Layout.activity_main);

            btnLeft = FindViewById<Button>(Resource.Id.btnLeft);
            btnRight = FindViewById<Button>(Resource.Id.btnRight);
            btnBoth = FindViewById<Button>(Resource.Id.btnBoth);
            dimmer = FindViewById<SeekBar>(Resource.Id.dimmSlide);

            dimmer.ProgressChanged += delegate
            {
                tcpConnect("fin", dimmer.Progress);
            };

            btnRight.Click += delegate
            {
                tcpConnect("nigg");
            };
            btnLeft.Click += delegate
            {
                tcpConnect("Letto");
            };
            btnBoth.Click += delegate
            {
                tcpConnect("BOTH");
            };

            //btn = FindViewById<Button>(Resource.Id.btn);    // Sätter btn som en referens för knappen med id av btn
            // txt = FindViewById<TextView>(Resource.Id.txt);  // Sätter txt som en referens för textvyn med id av txt

            /* txt.Click += delegate                         // En väg att skapa ett klick event för textvyn txt
             {       
                 btn.Text = "Yoo, this is dope bro!";
             };*/

            /*btn.Click += delegate   // En väg att skapa ett klick event för knappen btn
            {
                txt.Text = "Fat fucking nigger bitch boi bag of chips!";
            };*/

        }

    }
}