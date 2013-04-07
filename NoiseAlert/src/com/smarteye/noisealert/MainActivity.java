package com.smarteye.noisealert;

import java.io.IOException;
import java.util.Timer;
import java.util.TimerTask;

import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;
import android.widget.TextView;

import com.google.android.noisealert.SoundMeter;

public class MainActivity extends Activity {
	private SoundMeter meter;
	private Timer timer;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		meter = new SoundMeter();
		setContentView(R.layout.activity_main);
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}
	
	@Override
	public void onResume() {
		super.onResume();
		final TextView text_label = (TextView)findViewById(R.id.textView_sound_level_label);
		final TextView text_sound_level = (TextView)findViewById(R.id.textView_sound_level);
		try {
			meter.start();
		    timer = new Timer();
		    // This timer task will be executed every 1 sec.
		    timer.schedule(new TimerTask() {
		      @Override
		      public void run() {
		    	  runOnUiThread(new Runnable() {
		    		  @Override
		    		  public void run() {
		    			  text_sound_level.setText(Double.toString(meter.getAmplitude()));
		    		  }
		    	  });
		      }
		    }, 0, 1000);
		} catch (IllegalStateException e) {
			text_label.setText("MediaRecorder is in illegal state.");
		} catch (IOException e) {
			text_label.setText("MediaRecorder fails to prepare.");
		}
	}
	
	@Override
	public void onPause() {
		// Suspend the updates when the activity is inactive.
		timer.cancel();
		meter.stop();
	}

}
