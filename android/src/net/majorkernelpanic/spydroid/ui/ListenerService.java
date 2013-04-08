package net.majorkernelpanic.spydroid.ui;

import android.app.Service;
import android.content.Intent;
import android.os.Binder;
import android.os.Handler;
import android.os.IBinder;
import android.media.MediaRecorder;
import android.util.Log;

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
                    mTickCount = 0;
                    mHitCount  = 0;
                } else {
                    Log.d("ListenerService", "Heard noise, polling sooner.");
                    mHandler.postDelayed(mPollTask, POLL_INTERVAL/3);
                    return;
                }
            }

            if ((++mTickCount) > 100) {
                Log.d("ListenerService", "Running again in 3 seconds...");
                mTickCount = 0;
                mHitCount  = 0;
                mHandler.postDelayed(mPollTask, POLL_INTERVAL * 1000);
            } else {
                Log.d("ListenerService", "Running again shortly");
                mHandler.postDelayed(mPollTask, POLL_INTERVAL);
            }
        }
    };




}
