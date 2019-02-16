package ro.ase.acs.coolweatherid;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.GridLayout;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {
    private ArrayList<String> locationList = new ArrayList<>();
    private Spinner spinner;
    private ArrayAdapter<String> adapter;
    private GridLayout gridLayout;
    private ProgressBar progressBar;
    private ImageView weatherImageView;
    private TextView temperatureTextView;
    private TextView descriptionTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Log.d("MainActivity",
                "S-a apelat onCreate");
        Toast.makeText(this, "Aplicatia a pornit",
                Toast.LENGTH_SHORT).show();

        Button addLocationButton = findViewById(R.id.add_location_button);
        addLocationButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intentExplicit =
                        new Intent(MainActivity.this, AddLocationActivity.class);
                intentExplicit.putExtra("country", "Romania");
                startActivityForResult(intentExplicit, 1);
            }
        });
        gridLayout = findViewById(R.id.gridLayout);
        progressBar = findViewById(R.id.progressBar);
        weatherImageView = findViewById(R.id.weatherImageView);
        temperatureTextView = findViewById(R.id.temperatureTextView);
        descriptionTextView = findViewById(R.id.descriptionTextView);

        spinner = findViewById(R.id.spinner);
        adapter = new ArrayAdapter<String>(MainActivity.this,
                R.layout.support_simple_spinner_dropdown_item,
                locationList);
        spinner.setAdapter(adapter);

        spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                WeatherWorker weatherWorker = new WeatherWorker();
                String currentLocation =
                        spinner.getSelectedItem().toString();
                weatherWorker.execute(currentLocation);
            }

            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {

            }
        });
    }

    @Override
    protected void onStop() {
        super.onStop();

        Toast.makeText(this, "S-a apelat onStop",
                Toast.LENGTH_LONG).show();
    }

    public void deschideBrowser(View view) {
        Intent intentImplicit =
                new Intent(Intent.ACTION_VIEW,
                        Uri.parse("http://accuweather.com"));
        startActivity(intentImplicit);
    }

    @Override
    protected void onActivityResult(int requestCode,
                                    int resultCode, Intent data) {
        if(requestCode == 1 && resultCode == RESULT_OK) {
            Location location =
                    (Location)data.getSerializableExtra("locatie");
            Log.i("CoolWeather", location.toString());
            locationList.add(location.toString());
            adapter.notifyDataSetChanged();
        }
    }

    class WeatherWorker
            extends AsyncTask<String, Integer, WeatherCondition> {

        @Override
        protected WeatherCondition doInBackground(String... strings) {
            if(strings != null && strings.length > 0) {
                String location = strings[0];
                String address = String.format("http://api.openweathermap.org/data/2.5/weather?q=%s&appid=7b10426ee90376dc3d6525f847128b35&units=metric&format=json&lang=ro",
                        location);
                try {
                    URL url = new URL(address);
                    HttpURLConnection connection =
                            (HttpURLConnection) url.openConnection();
                    InputStream is = connection.getInputStream();
                    BufferedReader reader =
                            new BufferedReader(new InputStreamReader(is));
                    String line = null;
                    StringBuilder stringBuilder = new StringBuilder();
                    while((line = reader.readLine()) != null) {
                        stringBuilder.append(line);
                    }
                    is.close();
                    String response = stringBuilder.toString();
                    Log.d("Response", response);

                    WeatherCondition condition = new WeatherCondition();
                    JSONObject jsonObject = new JSONObject(response);
                    JSONObject mainObject =
                            jsonObject.getJSONObject("main");
                    double temp = mainObject.getDouble("temp");
                    condition.temperature = (int)Math.round(temp);
                    JSONArray weatherArray =
                            jsonObject.getJSONArray("weather");
                    JSONObject weatherObject =
                            (JSONObject) weatherArray.get(0);
                    condition.description =
                            weatherObject.getString("description");

                    String icon = weatherObject.getString("icon");
                    address =
                        String.format("http://openweathermap.org/img/w/%s.png", icon);
                    URL url2 = new URL(address);
                    HttpURLConnection connection2 = (HttpURLConnection)url2.openConnection();
                    InputStream is2 = connection2.getInputStream();
                    Bitmap bitmap = BitmapFactory.decodeStream(is2);
                    condition.image = bitmap;
                    is2.close();
                    return condition;
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
            return null;
        }

        @Override
        protected void onPreExecute() {
            gridLayout.setVisibility(View.GONE);
            progressBar.setVisibility(View.VISIBLE);
        }

        @Override
        protected void onPostExecute(WeatherCondition weatherCondition) {
            gridLayout.setVisibility(View.VISIBLE);
            progressBar.setVisibility(View.GONE);
            if(weatherCondition != null) {
                weatherImageView.setImageBitmap(weatherCondition.image);
                descriptionTextView.setText(weatherCondition.description);
                temperatureTextView.setText(weatherCondition.temperature + "°C");
            }
        }
    }
}
