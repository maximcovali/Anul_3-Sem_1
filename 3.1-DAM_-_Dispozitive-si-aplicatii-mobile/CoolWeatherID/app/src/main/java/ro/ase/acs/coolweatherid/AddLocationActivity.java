package ro.ase.acs.coolweatherid;

import android.app.Dialog;
import android.content.Intent;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

public class AddLocationActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_location);

        Intent intent = getIntent();
        if(intent != null) {
            String country = intent.getStringExtra("country");
            EditText countryEditText = findViewById(R.id.countryEditText);
            countryEditText.setText(country);
        }
    }

    public void addLocation(View view) {
        EditText cityEditText = findViewById(R.id.cityEditText);
        EditText countryEditText = findViewById(R.id.countryEditText);
        if(cityEditText.getText().toString().equals("") ||
                countryEditText.getText().toString().equals("")) {
            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setTitle(R.string.error);
            builder.setMessage("Localitatea si tara sunt obligatorii");
            Dialog dialog = builder.create();
            dialog.show();
        }
        else {
            Location location = new Location();
            location.city = cityEditText.getText().toString();
            location.country = countryEditText.getText().toString();
            Intent intent = new Intent();
            intent.putExtra("locatie", location);
            setResult(RESULT_OK, intent);
            finish();
        }
    }
}
