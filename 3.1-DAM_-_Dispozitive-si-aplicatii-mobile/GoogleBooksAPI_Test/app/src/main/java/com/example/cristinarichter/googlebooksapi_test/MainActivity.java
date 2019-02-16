//https://www.youtube.com/watch?v=YEO28_Fv2UI&list=PLeffTIkwmUUCXlwU-rd8ClH22EoMy84Tb


package com.example.cristinarichter.googlebooksapi_test;

import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = MainActivity.class.getSimpleName();
    private EditText mBookInput;
    private TextView mAuthorText, mTitleText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mBookInput = findViewById(R.id.bookInput);
        mAuthorText = findViewById(R.id.titleText);
        mTitleText = findViewById(R.id.authorText);
    }

    public void searchBooks(View view) {
        String queryString = mBookInput.getText().toString();

        // ascund tastatura atunci cand este apasat butonul search
        InputMethodManager inputManager = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
        inputManager.hideSoftInputFromWindow(getCurrentFocus().getWindowToken(),
                InputMethodManager.HIDE_NOT_ALWAYS);

        ///// caut si aduc cartea in TextView/////

        // Verific starea retelei (daca telefonul este conectat la internet)
        // si golesc campul in care se introduce textul de cautat

        ConnectivityManager connMgr = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();

        if (networkInfo != null && networkInfo.isConnected() && queryString.length() != 0){
            new FetchBook(mTitleText, mAuthorText).execute(queryString);
            mAuthorText.setText("");
            mTitleText.setText(getString(R.string.loading)); // pot sa pun si direct "Loading..." in loc de R.string.loading (am creat un string dand Alt+enter (option+enter pe mac))

        } else {
            if (queryString.length() == 0){
                mAuthorText.setText("");
                mTitleText.setText("Please enter a search term");
            } else {
                mAuthorText.setText("");
                mTitleText.setText("Please check your network connection and try again");
            }
        }

//        // fara feedback daca nu am retea //
//        // caut si aduc cartea in TextView
//        Log.i(TAG, "Searched: " + queryString);
//        if (queryString.length() != 0) {
//            new FetchBook(mTitleText, mAuthorText).execute(queryString);
//        }
//        else {
//            Toast.makeText(this, "Please enter a search term", Toast.LENGTH_LONG).show();
//        }
    }
}
