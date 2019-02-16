package com.example.cristinarichter.myapplication;

import android.graphics.Color;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    // 1. creez obiectele (buton si textview), ca sa pot face referinta la ele
    // astea sunt instance variables
    private Button hiButton;
    private TextView textView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // instantiez butonul si textview-ul
        hiButton = findViewById(R.id.hiButton);
        textView = findViewById(R.id.textView);

        //pot modifica textul butonului cu setText
//        hiButton.setText("hello button"); // hard-coding
        hiButton.setText(R.string.button);
        //pot modifica culoarea textului din buton
        hiButton.setTextColor(Color.BLUE);
        // fac un toast ca sa apara numele butonului (luat dintr-un string)
        Toast.makeText(MainActivity.this, R.string.button, Toast.LENGTH_SHORT).show();
    }
}
